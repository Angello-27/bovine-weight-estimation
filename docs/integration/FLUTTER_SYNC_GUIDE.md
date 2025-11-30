# 🔄 Guía de Sincronización Flutter → Backend

**Objetivo**: Documentar el flujo completo de sincronización desde la captura de fotogramas en Flutter hasta el almacenamiento en el backend MongoDB.

**US-005**: Sincronización Offline-First con estrategia Last-Write-Wins

---

## 📋 Resumen del Flujo

```
Flutter App (Offline-First)
├── 1. Captura de fotogramas (cámara)
├── 2. Estimación de peso (TFLite local)
├── 3. Guardado local (SQLite)
│   ├── weight_estimations (estimación)
│   └── sync_queue (cola de sincronización)
├── 4. Sincronización automática/manual
│   ├── Health check → GET /api/v1/sync/health
│   ├── Sync cattle → POST /api/v1/sync/cattle
│   └── Sync estimations → POST /api/v1/sync/weight-estimations
└── 5. Actualización de estados (synced/error/conflict)
```

---

## 🎯 Estrategia Offline-First

### Principios

1. **SQLite es la fuente de verdad local**
   - Todas las estimaciones se guardan primero en SQLite
   - La app funciona 100% offline

2. **Sincronización automática**
   - Se detecta conectividad y sincroniza automáticamente
   - Batch processing (hasta 100 items por request)

3. **Last-Write-Wins**
   - Resolución de conflictos basada en timestamps UTC
   - El dato más reciente prevalece automáticamente

4. **Cola de sincronización**
   - Items pendientes se guardan en `sync_queue`
   - Reintentos automáticos con backoff exponencial

---

## 🔄 Flujo Completo: Captura → Sincronización

### Paso 1: Captura y Estimación (Flutter)

```dart
// lib/presentation/providers/capture_provider.dart

// 1. Capturar fotogramas continuos (10-15 FPS, 3-5 segundos)
final frames = await cameraController.captureContinuousFrames(
  duration: Duration(seconds: 4),
  fps: 12,
);

// 2. Seleccionar mejor fotograma (IA)
final bestFrame = await frameSelector.selectBestFrame(frames);

// 3. Estimar peso con TFLite (offline)
final estimation = await weightEstimationUseCase.execute(
  breedType: BreedType.brahman,
  imageFile: bestFrame.file,
);

// estimation contiene:
// - estimatedWeight: 487.3 kg
// - confidence: 0.97 (≥95%)
// - processingTimeMs: 2543 (<3s)
// - method: 'tflite'
// - modelVersion: '1.0.0'
```

### Paso 2: Guardado Local (SQLite)

```dart
// lib/domain/usecases/save_weight_estimation_usecase.dart

// 1. Guardar estimación en SQLite
await weightEstimationRepository.saveEstimation(estimation);

// 2. Agregar a cola de sincronización automáticamente
final syncItem = SyncQueueItem(
  id: Uuid().v4(),
  entityType: SyncEntityType.weightEstimation,
  entityId: estimation.id,
  operation: SyncOperation.create,
  data: jsonEncode({
    'id': estimation.id,
    'cattle_id': estimation.cattleId,
    'breed': estimation.breed.name,
    'estimated_weight': estimation.estimatedWeight,
    'confidence_score': estimation.confidence,
    'frame_image_path': estimation.frameImagePath,
    'timestamp': estimation.timestamp.toIso8601String(),
    'gps_latitude': estimation.gpsLatitude,
    'gps_longitude': estimation.gpsLongitude,
    'method': estimation.method,
    'model_version': estimation.modelVersion,
    'processing_time_ms': estimation.processingTimeMs,
  }),
  status: SyncStatus.pending,
  createdAt: DateTime.now(),
  retryCount: 0,
);

await syncRepository.enqueueItem(syncItem);
```

### Paso 3: Sincronización Automática

```dart
// lib/data/repositories/sync_repository_impl.dart

// 1. Verificar conectividad
final isConnected = await syncRepository.checkConnectivity();
// → GET /api/v1/sync/health

if (!isConnected) {
  // Offline: Los items quedan en cola para sincronizar después
  return;
}

// 2. Obtener items pendientes
final pendingItems = await syncQueueLocal.getPendingItems();

// 3. Agrupar por tipo
final weightEstimationItems = pendingItems
    .where((item) => item.entityType == SyncEntityType.weightEstimation)
    .toList();

// 4. Crear batch (máximo 100 items)
final batches = _createBatches(weightEstimationItems, maxSize: 100);

// 5. Sincronizar cada batch
for (final batch in batches) {
  final request = WeightEstimationSyncBatchRequestModel(
    items: batch.map((item) => _toWeightEstimationItem(item)).toList(),
    deviceId: deviceId,
    syncTimestamp: DateTime.now().toUtc(),
  );

  // POST /api/v1/sync/weight-estimations
  final response = await syncRemote.syncWeightEstimationsBatch(request);
  
  // 6. Procesar respuesta
  await _processSyncResponse(response, batch);
}
```

### Paso 4: Procesamiento de Respuesta

```dart
// lib/data/repositories/sync_repository_impl.dart

Future<void> _processSyncResponse(
  SyncBatchResponseModel response,
  List<SyncQueueItem> items,
) async {
  for (final resultItem in response.results) {
    final queueItem = items.firstWhere(
      (item) => item.entityId == resultItem.id,
    );

    final status = SyncStatus.fromString(resultItem.status);

    if (status == SyncStatus.synced) {
      // ✅ Sincronizado exitosamente
      // 1. Remover de cola
      await syncQueueLocal.removeItem(queueItem.id);
      
      // 2. Marcar estimación como sincronizada en SQLite
      await weightEstimationLocal.markAsSynced(queueItem.entityId);
      
    } else if (status == SyncStatus.error) {
      // ❌ Error: Incrementar reintentos
      await syncQueueLocal.incrementRetryCount(queueItem.id);
      await syncQueueLocal.updateItemStatus(
        queueItem.id,
        SyncStatus.error,
        errorMessage: resultItem.message,
      );
      
    } else if (status == SyncStatus.conflict) {
      // ⚠️ Conflicto: Backend tiene versión más reciente
      // Aplicar last-write-wins (actualizar local con datos del backend)
      if (resultItem.conflictData != null) {
        await _updateLocalWithBackendData(
          queueItem.entityId,
          resultItem.conflictData!,
        );
      }
      
      // Remover de cola (ya está sincronizado)
      await syncQueueLocal.removeItem(queueItem.id);
    }
  }
}
```

---

## 📡 Endpoints del Backend

### 1. Health Check

**Endpoint**: `GET /api/v1/sync/health`

**Uso en Flutter**:
```dart
// lib/data/datasources/sync_remote_datasource.dart

Future<HealthCheckResponseModel> healthCheck() async {
  final response = await dio.get(
    '/api/v1/sync/health',
    options: Options(
      sendTimeout: Duration(seconds: 3),  // Timeout corto
      receiveTimeout: Duration(seconds: 3),
    ),
  );
  
  return HealthCheckResponseModel.fromJson(response.data);
}
```

**Respuesta**:
```json
{
  "status": "online",
  "database": "connected",
  "timestamp": "2024-12-20T10:30:00Z",
  "version": "1.0.0"
}
```

### 2. Sincronizar Ganado (Cattle)

**Endpoint**: `POST /api/v1/sync/cattle`

**Request Body**:
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "ear_tag": "HG-BRA-001",
      "name": "Brahman #1",
      "breed": "brahman",
      "birth_date": "2022-03-15T00:00:00Z",
      "gender": "male",
      "color": "Rojo",
      "birth_weight": 35.5,
      "mother_id": null,
      "father_id": null,
      "observations": "Animal de prueba",
      "status": "active",
      "registration_date": "2024-12-20T10:00:00Z",
      "last_updated": "2024-12-20T10:30:00Z",
      "photo_path": "/storage/frames/animal_001.jpg",
      "operation": "create"
    }
  ],
  "device_id": "android-device-123",
  "sync_timestamp": "2024-12-20T10:30:00Z"
}
```

**Uso en Flutter**:
```dart
final request = CattleSyncBatchRequestModel(
  items: cattleItems.map((item) => CattleSyncItemModel(
    id: item.id,
    earTag: item.earTag,
    name: item.name,
    breed: item.breed.name,
    birthDate: item.birthDate,
    gender: item.gender.name,
    color: item.color,
    birthWeight: item.birthWeight,
    motherId: item.motherId,
    fatherId: item.fatherId,
    observations: item.observations,
    status: item.status.name,
    registrationDate: item.registrationDate,
    lastUpdated: item.lastUpdated,
    photoPath: item.photoPath,
    operation: 'create',
  )).toList(),
  deviceId: deviceId,
  syncTimestamp: DateTime.now().toUtc(),
);

final response = await syncRemote.syncCattleBatch(request);
```

**Response**:
```json
{
  "success": true,
  "total_items": 1,
  "synced_count": 1,
  "failed_count": 0,
  "conflict_count": 0,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "synced",
      "message": "Animal creado exitosamente",
      "conflict_data": null,
      "synced_at": "2024-12-20T10:30:05Z"
    }
  ],
  "sync_timestamp": "2024-12-20T10:30:00Z",
  "message": "✓ 1 de 1 items sincronizados exitosamente"
}
```

### 3. Sincronizar Estimaciones de Peso

**Endpoint**: `POST /api/v1/sync/weight-estimations`

**Request Body**:
```json
{
  "items": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "cattle_id": "550e8400-e29b-41d4-a716-446655440000",
      "breed": "brahman",
      "estimated_weight": 487.3,
      "confidence_score": 0.97,
      "frame_image_path": "/storage/frames/estimation_001.jpg",
      "timestamp": "2024-12-20T10:25:00Z",
      "gps_latitude": -15.859500,
      "gps_longitude": -60.797889,
      "method": "tflite",
      "model_version": "1.0.0",
      "processing_time_ms": 2543,
      "operation": "create"
    }
  ],
  "device_id": "android-device-123",
  "sync_timestamp": "2024-12-20T10:30:00Z"
}
```

**Uso en Flutter**:
```dart
final request = WeightEstimationSyncBatchRequestModel(
  items: estimationItems.map((item) => WeightEstimationSyncItemModel(
    id: item.id,
    cattleId: item.cattleId,
    breed: item.breed.name,
    estimatedWeight: item.estimatedWeight,
    confidenceScore: item.confidence,
    frameImagePath: item.frameImagePath,
    timestamp: item.timestamp,
    gpsLatitude: item.gpsLatitude,
    gpsLongitude: item.gpsLongitude,
    method: item.method,
    modelVersion: item.modelVersion,
    processingTimeMs: item.processingTimeMs,
    operation: 'create',
  )).toList(),
  deviceId: deviceId,
  syncTimestamp: DateTime.now().toUtc(),
);

final response = await syncRemote.syncWeightEstimationsBatch(request);
```

**Response**:
```json
{
  "success": true,
  "total_items": 1,
  "synced_count": 1,
  "failed_count": 0,
  "conflict_count": 0,
  "results": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "status": "synced",
      "message": "Estimación creada exitosamente",
      "conflict_data": null,
      "synced_at": "2024-12-20T10:30:05Z"
    }
  ],
  "sync_timestamp": "2024-12-20T10:30:00Z",
  "message": "✓ 1 de 1 items sincronizados exitosamente"
}
```

---

## 🔧 Configuración en Flutter

### 1. Base URL del Backend

```dart
// lib/core/config/app_config.dart

class AppConfig {
  // URL del backend (configurable por ambiente)
  static const String baseUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'http://192.168.0.12:8000',  // Default: emulador Android
  );
  
  // Para producción:
  // flutter run --dart-define=BACKEND_URL=https://api.agrocom.com
}
```

### 2. Device ID

```dart
// lib/core/config/device_id.dart

import 'package:device_info_plus/device_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

class DeviceIdManager {
  static const String _key = 'device_id';
  
  static Future<String> getDeviceId() async {
    final prefs = await SharedPreferences.getInstance();
    String? deviceId = prefs.getString(_key);
    
    if (deviceId == null) {
      // Generar nuevo device ID
      final deviceInfo = DeviceInfoPlugin();
      final androidInfo = await deviceInfo.androidInfo;
      deviceId = '${androidInfo.id}-${DateTime.now().millisecondsSinceEpoch}';
      
      await prefs.setString(_key, deviceId);
    }
    
    return deviceId;
  }
}
```

### 3. Inicialización de Sincronización

```dart
// lib/main.dart

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Inicializar dependencias
  await DependencyInjection.setup();
  
  // Iniciar listener de sincronización automática
  final syncRepository = DependencyInjection.get<SyncRepository>();
  await syncRepository.startAutoSyncListener();
  
  runApp(MyApp());
}
```

---

## 🔄 Sincronización Automática

### Listener de Conectividad

```dart
// lib/data/repositories/sync_repository_impl.dart

@override
Future<Either<Failure, void>> startAutoSyncListener() async {
  _autoSyncTimer?.cancel();
  
  // Verificar cada 60 segundos si hay items pendientes
  _autoSyncTimer = Timer.periodic(
    const Duration(seconds: 60),
    (_) => _autoSyncCheck(),
  );
  
  return const Right(null);
}

Future<void> _autoSyncCheck() async {
  // 1. Verificar si hay items pendientes
  final pendingCountResult = await getPendingCount();
  final pendingCount = pendingCountResult.fold((_) => 0, (count) => count);
  
  if (pendingCount > 0) {
    // 2. Verificar conectividad
    final connectivityResult = await checkConnectivity();
    final isConnected = connectivityResult.fold((_) => false, (connected) => connected);
    
    if (isConnected) {
      // 3. Sincronizar automáticamente
      await syncPendingItems();
    }
  }
}
```

### Sincronización Manual

```dart
// lib/presentation/providers/sync_provider.dart

class SyncProvider extends ChangeNotifier {
  final SyncPendingItemsUseCase syncUseCase;
  
  SyncStatus _status = SyncStatus.idle;
  SyncResult? _lastResult;
  
  Future<void> syncNow() async {
    _status = SyncStatus.syncing;
    notifyListeners();
    
    final result = await syncUseCase(NoParams());
    
    result.fold(
      (failure) {
        _status = SyncStatus.error;
        _lastResult = null;
      },
      (syncResult) {
        _status = syncResult.success ? SyncStatus.success : SyncStatus.partial;
        _lastResult = syncResult;
      },
    );
    
    notifyListeners();
  }
}
```

---

## 📊 Estados de Sincronización

### Estados en SQLite

```sql
-- Tabla: weight_estimations
CREATE TABLE weight_estimations (
  id TEXT PRIMARY KEY,
  -- ... otros campos ...
  synced INTEGER NOT NULL DEFAULT 0,           -- 0 = no sincronizado, 1 = sincronizado
  sync_status TEXT NOT NULL DEFAULT 'pending',  -- pending, synced, error, conflict
  last_sync_at INTEGER                          -- Timestamp de última sincronización
);

-- Tabla: sync_queue
CREATE TABLE sync_queue (
  id TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,                    -- 'cattle' o 'weight_estimation'
  entity_id TEXT NOT NULL,
  operation TEXT NOT NULL,                     -- 'create', 'update', 'delete'
  data TEXT NOT NULL,                           -- JSON del item
  status TEXT NOT NULL DEFAULT 'pending',       -- pending, syncing, synced, error, conflict
  retry_count INTEGER NOT NULL DEFAULT 0,
  last_retry_at INTEGER,
  error_message TEXT,
  created_at INTEGER NOT NULL
);
```

### Estados en Flutter

```dart
// lib/domain/entities/sync_status.dart

enum SyncStatus {
  idle,      // No hay sincronización en curso
  syncing,   // Sincronización en progreso
  success,   // Sincronización exitosa
  partial,   // Sincronización parcial (algunos items fallaron)
  error,     // Error durante sincronización
  conflict,  // Conflicto detectado (backend más reciente)
}
```

---

## 🐛 Manejo de Errores

### Errores de Red

```dart
// lib/data/datasources/sync_remote_datasource.dart

Exception _handleDioError(DioException e) {
  switch (e.type) {
    case DioExceptionType.connectionTimeout:
    case DioExceptionType.sendTimeout:
    case DioExceptionType.receiveTimeout:
      return TimeoutException(
        message: 'La conexión tardó demasiado. Verifica tu conectividad.',
      );
      
    case DioExceptionType.connectionError:
      return NetworkException(
        message: 'Sin conexión a internet. La sincronización se ejecutará automáticamente cuando se detecte conexión.',
      );
      
    case DioExceptionType.badResponse:
      final statusCode = e.response?.statusCode ?? 0;
      if (statusCode >= 500) {
        return ServerException(message: 'Error del servidor');
      } else if (statusCode == 400) {
        return ValidationException(message: 'Datos inválidos');
      }
      break;
      
    default:
      return NetworkException(message: 'Error de red desconocido');
  }
}
```

### Reintentos Automáticos

```dart
// lib/data/datasources/sync_queue_local_datasource.dart

Future<List<SyncQueueItem>> getItemsReadyForRetry() async {
  final db = await database;
  
  // Items con error que están listos para reintento (backoff exponencial)
  final now = DateTime.now().millisecondsSinceEpoch;
  
  final maps = await db.query(
    'sync_queue',
    where: '''
      status = ? AND
      retry_count < ? AND
      (last_retry_at IS NULL OR last_retry_at < ?)
    ''',
    whereArgs: [
      SyncStatus.error.name,
      10,  // Máximo 10 reintentos
      now - _calculateBackoffDelay(retryCount),  // Backoff exponencial
    ],
  );
  
  return maps.map((map) => SyncQueueItem.fromSQLite(map)).toList();
}

int _calculateBackoffDelay(int retryCount) {
  // Backoff exponencial: 1s, 2s, 4s, 8s, 16s, 32s, 60s (max)
  final delay = pow(2, retryCount).toInt() * 1000;  // En milisegundos
  return delay > 60000 ? 60000 : delay;  // Máximo 60 segundos
}
```

---

## ✅ Checklist de Implementación

### Backend (Ya implementado ✅)
- [x] Endpoint `POST /api/v1/sync/cattle`
- [x] Endpoint `POST /api/v1/sync/weight-estimations`
- [x] Endpoint `GET /api/v1/sync/health`
- [x] Estrategia Last-Write-Wins
- [x] Validación de batches (máximo 100 items)

### Flutter (Ya implementado ✅)
- [x] SQLite con columnas de sincronización
- [x] SyncQueueLocalDataSource
- [x] SyncRemoteDataSource
- [x] SyncRepository con lógica de batch
- [x] SyncPendingItemsUseCase
- [x] Listener de sincronización automática

### Pendiente (Opcional)
- [ ] Subida de imágenes al backend (actualmente solo se envía `frame_image_path`)
- [ ] Compresión de payloads grandes (>1KB)
- [ ] Métricas de sincronización en UI
- [ ] Notificaciones push cuando hay conflictos

---

## 📝 Notas Importantes

1. **Offline-First**: La app funciona 100% offline. La sincronización es opcional.

2. **Batch Processing**: Siempre enviar batches de hasta 100 items para optimizar red.

3. **Last-Write-Wins**: Los conflictos se resuelven automáticamente. El usuario no necesita intervenir.

4. **Device ID**: Cada dispositivo tiene un ID único que se envía en cada request.

5. **Timestamps UTC**: Todos los timestamps deben estar en UTC para comparación correcta.

6. **Reintentos**: Los items con error se reintentan automáticamente con backoff exponencial.

---

**Última actualización**: 2024-12-20  
**Versión**: 1.0.0  
**US**: US-005 (Sincronización Offline)

