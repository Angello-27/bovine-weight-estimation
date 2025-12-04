# 🔌 Guía de Integración API Flutter - Endpoints Completos

**Objetivo**: Documentación completa de todos los endpoints de la API que deben integrarse en la aplicación Flutter Mobile.

**Base URL**: `http://localhost:8000` (desarrollo) | `https://api.haciendagamelera.com` (producción)

**Versión API**: `v1`

**Autenticación**: JWT Bearer Token (excepto `/api/v1/auth/login` y algunos endpoints de sincronización)

---

## 📋 Índice

1. [Autenticación JWT](#autenticación-jwt)
2. [Machine Learning](#machine-learning)
3. [Gestión de Animales](#gestión-de-animales)
4. [Historial de Pesajes](#historial-de-pesajes)
5. [Reportes](#reportes)
6. [Alertas y Cronograma](#alertas-y-cronograma)
7. [Sincronización](#sincronización) (Ver `FLUTTER_SYNC_GUIDE.md`)

---

## 🔐 Autenticación JWT

### POST `/api/v1/auth/login`

**Descripción**: Autentica un usuario y retorna un token JWT.

**Autenticación**: No requerida

**Request Body**:
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response 200**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "admin",
  "email": "admin@hacienda.com",
  "role": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Administrador",
    "priority": "Administrador"
  },
  "role_id": "660e8400-e29b-41d4-a716-446655440001",
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Nota**: El campo `farm_id` puede ser `null`. Si es `null`, el usuario deberá seleccionar una finca antes de poder listar animales.

**Implementación en Flutter**:
```dart
// lib/data/datasources/auth_remote_datasource.dart

Future<LoginResponseModel> login({
  required String username,
  required String password,
}) async {
  final response = await dio.post(
    '/api/v1/auth/login',
    data: {
      'username': username,
      'password': password,
    },
  );
  
  final loginResponse = LoginResponseModel.fromJson(response.data);
  
  // Guardar token en SecureStorage
  await secureStorage.write(
    key: 'access_token',
    value: loginResponse.accessToken,
  );
  
  // Guardar datos del usuario
  await secureStorage.write(
    key: 'user_data',
    value: jsonEncode(loginResponse.toJson()),
  );
  
  return loginResponse;
}
```

**Manejo de Token en Requests**:
```dart
// lib/core/network/dio_client.dart

class DioClient {
  final Dio _dio;
  final SecureStorage _secureStorage;
  
  DioClient(this._dio, this._secureStorage) {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // Agregar token a todas las requests
          final token = await _secureStorage.read(key: 'access_token');
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          handler.next(options);
        },
        onError: (error, handler) async {
          // Manejar token expirado (401)
          if (error.response?.statusCode == 401) {
            // Limpiar token y redirigir a login
            await _secureStorage.delete(key: 'access_token');
            await _secureStorage.delete(key: 'user_data');
            // Navigate to login
          }
          handler.next(error);
        },
      ),
    );
  }
}
```

---

## 🤖 Machine Learning

### POST `/api/v1/ml/predict`

**Descripción**: Predice peso de bovino con IA **SIN guardar** en base de datos. Útil para estimaciones rápidas durante la captura.

**Autenticación**: Opcional

**Content-Type**: `multipart/form-data`

**Request**:
- `image` (File, required): Imagen del bovino (JPEG/PNG)
- `breed` (string, required): Raza (`nelore`, `brahman`, `guzerat`, `senepol`, `girolando`, `gyr_lechero`, `sindi`)
- `animal_id` (UUID, optional): ID del animal si existe
- `device_id` (string, optional): ID del dispositivo móvil

**Response 200**:
```json
{
  "id": "2e0a53d6-86c0-4ae8-b402-ae09233861b7",
  "animal_id": null,
  "breed": "nelore",
  "estimated_weight_kg": 289.25,
  "confidence": 0.92,
  "confidence_level": "high",
  "processing_time_ms": 397,
  "ml_model_version": "1.0.0-deep_learning_tflite",
  "method": "strategy_based",
  "meets_quality_criteria": true,
  "timestamp": "2025-11-30T14:54:25.964158"
}
```

**Implementación en Flutter**:
```dart
// lib/data/datasources/ml_remote_datasource.dart

Future<WeightPredictionResponseModel> predictWeight({
  required File imageFile,
  required String breed,
  String? animalId,
  String? deviceId,
}) async {
  final formData = FormData.fromMap({
    'image': await MultipartFile.fromFile(
      imageFile.path,
      filename: 'cow_image.jpg',
    ),
    'breed': breed,
    if (animalId != null) 'animal_id': animalId,
    if (deviceId != null) 'device_id': deviceId,
  });
  
  final response = await dio.post(
    '/api/v1/ml/predict',
    data: formData,
  );
  
  return WeightPredictionResponseModel.fromJson(response.data);
}
```

**Notas**:
- Este endpoint **NO guarda** la estimación en BD
- Úsalo para estimaciones rápidas durante la captura
- La estimación se guarda luego mediante sincronización offline

---

### GET `/api/v1/ml/models/status`

**Descripción**: Obtiene información de modelos ML cargados en el servidor.

**Autenticación**: No requerida

**Response 200**:
```json
{
  "status": "ok",
  "total_loaded": 1,
  "breeds_loaded": ["generic"],
  "all_breeds": [
    "nelore",
    "brahman",
    "guzerat",
    "senepol",
    "girolando",
    "gyr_lechero",
    "sindi"
  ],
  "missing_breeds": [],
  "strategies": {
    "total_strategies": 2,
    "available_strategies": ["morphometric_yolo_detection"],
    "strategy_details": [
      {
        "strategy_name": "deep_learning_tflite",
        "available": true
      },
      {
        "strategy_name": "morphometric_yolo_detection",
        "available": true
      }
    ]
  },
  "available_strategies": ["deep_learning_tflite", "morphometric_yolo_detection"],
  "note": "Sistema de estrategias activo: ML entrenado + híbrido YOLO como fallback",
  "method": "strategy_based"
}
```

**Implementación en Flutter**:
```dart
// lib/data/datasources/ml_remote_datasource.dart

Future<MLModelsStatusResponseModel> getModelsStatus() async {
  final response = await dio.get('/api/v1/ml/models/status');
  return MLModelsStatusResponseModel.fromJson(response.data);
}
```

**Uso**: Verificar qué modelos están disponibles en el servidor antes de hacer predicciones.

---

## 🐄 Gestión de Animales

### POST `/api/v1/animals`

**Descripción**: Crea un nuevo animal.

**Autenticación**: Requerida

**Request Body**:
```json
{
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
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "photo_path": "/storage/frames/animal_001.jpg"
}
```

**Response 201**:
```json
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
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "photo_path": "/storage/frames/animal_001.jpg",
  "registration_date": "2024-12-20T10:00:00Z",
  "last_updated": "2024-12-20T10:00:00Z"
}
```

**Validaciones**:
- Caravana (`ear_tag`) única por hacienda
- Raza debe ser una de las 7 exactas
- Fecha de nacimiento no puede ser futura
- Género: `male` o `female`

**Implementación en Flutter**:
```dart
// lib/data/datasources/animals_remote_datasource.dart

Future<AnimalResponseModel> createAnimal({
  required AnimalCreateRequestModel request,
}) async {
  final response = await dio.post(
    '/api/v1/animals',
    data: request.toJson(),
  );
  
  return AnimalResponseModel.fromJson(response.data);
}
```

---

### GET `/api/v1/animals`

**Descripción**: Lista animales con filtros y paginación.

**Autenticación**: Requerida

**Query Parameters**:
- `page` (int, default: 1): Número de página
- `page_size` (int, default: 50, max: 100): Tamaño de página
- `farm_id` (UUID, optional): Filtrar por finca
- `breed` (string, optional): Filtrar por raza
- `gender` (string, optional): Filtrar por género
- `status` (string, optional): Filtrar por estado

**Response 200**:
```json
{
  "total": 1,
  "animals": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "ear_tag": "HG-BRA-001",
      "name": "Brahman #1",
      "breed": "brahman",
      ...
    }
  ],
  "page": 1,
  "page_size": 50
}
```

**Implementación en Flutter**:
```dart
// lib/data/datasources/animals_remote_datasource.dart

Future<AnimalsListResponseModel> getAnimals({
  int page = 1,
  int pageSize = 50,
  String? farmId,
  String? breed,
  String? gender,
  String? status,
}) async {
  final queryParams = <String, dynamic>{
    'page': page,
    'page_size': pageSize,
    if (farmId != null) 'farm_id': farmId,
    if (breed != null) 'breed': breed,
    if (gender != null) 'gender': gender,
    if (status != null) 'status': status,
  };
  
  final response = await dio.get(
    '/api/v1/animals',
    queryParameters: queryParams,
  );
  
  return AnimalsListResponseModel.fromJson(response.data);
}
```

---

### GET `/api/v1/animals/{animal_id}`

**Descripción**: Obtiene un animal específico.

**Autenticación**: Requerida

**Implementación en Flutter**:
```dart
Future<AnimalResponseModel> getAnimalById(String animalId) async {
  final response = await dio.get('/api/v1/animals/$animalId');
  return AnimalResponseModel.fromJson(response.data);
}
```

---

### PUT `/api/v1/animals/{animal_id}`

**Descripción**: Actualiza un animal.

**Autenticación**: Requerida

**Request Body**: Mismo formato que POST (campos opcionales)

**Implementación en Flutter**:
```dart
Future<AnimalResponseModel> updateAnimal({
  required String animalId,
  required AnimalUpdateRequestModel request,
}) async {
  final response = await dio.put(
    '/api/v1/animals/$animalId',
    data: request.toJson(),
  );
  
  return AnimalResponseModel.fromJson(response.data);
}
```

---

### DELETE `/api/v1/animals/{animal_id}`

**Descripción**: Elimina un animal.

**Autenticación**: Requerida

**Response 204**: Sin contenido

**Implementación en Flutter**:
```dart
Future<void> deleteAnimal(String animalId) async {
  await dio.delete('/api/v1/animals/$animalId');
}
```

---

### GET `/api/v1/animals/{animal_id}/timeline`

**Descripción**: Obtiene timeline de eventos de un animal (registro, pesajes, etc.).

**Autenticación**: Requerida

**Response 200**:
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "events": [
    {
      "type": "registration",
      "date": "2024-12-20T10:00:00Z",
      "description": "Animal registrado"
    },
    {
      "type": "weight_estimation",
      "date": "2024-12-20T10:25:00Z",
      "description": "Peso estimado: 487.3 kg",
      "weight_kg": 487.3
    }
  ]
}
```

**Implementación en Flutter**:
```dart
Future<AnimalTimelineResponseModel> getAnimalTimeline(String animalId) async {
  final response = await dio.get('/api/v1/animals/$animalId/timeline');
  return AnimalTimelineResponseModel.fromJson(response.data);
}
```

---

### GET `/api/v1/animals/{animal_id}/lineage`

**Descripción**: Obtiene linaje (padre, madre, descendientes) de un animal.

**Autenticación**: Requerida

**Response 200**:
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "father": null,
  "mother": null,
  "offspring": []
}
```

**Implementación en Flutter**:
```dart
Future<AnimalLineageResponseModel> getAnimalLineage(String animalId) async {
  final response = await dio.get('/api/v1/animals/$animalId/lineage');
  return AnimalLineageResponseModel.fromJson(response.data);
}
```

---

## ⚖️ Historial de Pesajes

### GET `/api/v1/weighings/animal/{animal_id}`

**Descripción**: Obtiene historial completo de pesajes de un animal.

**Autenticación**: Requerida

**Query Parameters**:
- `page` (int, default: 1)
- `page_size` (int, default: 50, max: 100)

**Response 200**:
```json
{
  "total": 5,
  "weighings": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "animal_id": "550e8400-e29b-41d4-a716-446655440000",
      "breed": "brahman",
      "estimated_weight_kg": 487.3,
      "confidence": 0.97,
      "ml_model_version": "1.0.0",
      "processing_time_ms": 2543,
      "timestamp": "2024-12-20T10:25:00Z"
    }
  ],
  "page": 1,
  "page_size": 50
}
```

**Implementación en Flutter**:
```dart
// lib/data/datasources/weighings_remote_datasource.dart

Future<WeighingsListResponseModel> getAnimalWeighings({
  required String animalId,
  int page = 1,
  int pageSize = 50,
}) async {
  final response = await dio.get(
    '/api/v1/weighings/animal/$animalId',
    queryParameters: {
      'page': page,
      'page_size': pageSize,
    },
  );
  
  return WeighingsListResponseModel.fromJson(response.data);
}
```

---

### GET `/api/v1/weighings/{weighing_id}`

**Descripción**: Obtiene una estimación específica.

**Autenticación**: Requerida

**Implementación en Flutter**:
```dart
Future<WeighingResponseModel> getWeighingById(String weighingId) async {
  final response = await dio.get('/api/v1/weighings/$weighingId');
  return WeighingResponseModel.fromJson(response.data);
}
```

---

## 📊 Reportes

Todos los reportes requieren **autenticación** y retornan archivos como `StreamingResponse`.

### POST `/api/v1/reports/traceability/{animal_id}`

**Descripción**: Genera reporte de trazabilidad individual (PDF o Excel).

**Autenticación**: Requerida

**Request Body**:
```json
{
  "format": "pdf"  // o "excel"
}
```

**Response 200**: Archivo PDF o Excel descargable

**Headers de respuesta**:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="trazabilidad_{animal_id}.pdf"
```

**Implementación en Flutter**:
```dart
// lib/data/datasources/reports_remote_datasource.dart

Future<String> downloadTraceabilityReport({
  required String animalId,
  required String format, // 'pdf' o 'excel'
}) async {
  final response = await dio.post(
    '/api/v1/reports/traceability/$animalId',
    data: {'format': format},
    options: Options(
      responseType: ResponseType.bytes,
      followRedirects: false,
    ),
  );
  
  // Guardar archivo localmente
  final directory = await getApplicationDocumentsDirectory();
  final file = File('${directory.path}/trazabilidad_$animalId.$format');
  await file.writeAsBytes(response.data);
  
  return file.path;
}
```

---

### POST `/api/v1/reports/inventory`

**Descripción**: Genera reporte de inventario de animales (PDF o Excel).

**Autenticación**: Requerida

**Request Body**:
```json
{
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "format": "excel",
  "status": "active",
  "breed": "brahman",
  "date_from": "2024-01-01T00:00:00Z",
  "date_to": "2024-12-31T23:59:59Z"
}
```

**Implementación en Flutter**:
```dart
Future<String> downloadInventoryReport({
  required String farmId,
  required String format,
  String? status,
  String? breed,
  DateTime? dateFrom,
  DateTime? dateTo,
}) async {
  final response = await dio.post(
    '/api/v1/reports/inventory',
    data: {
      'farm_id': farmId,
      'format': format,
      if (status != null) 'status': status,
      if (breed != null) 'breed': breed,
      if (dateFrom != null) 'date_from': dateFrom.toIso8601String(),
      if (dateTo != null) 'date_to': dateTo.toIso8601String(),
    },
    options: Options(
      responseType: ResponseType.bytes,
    ),
  );
  
  final directory = await getApplicationDocumentsDirectory();
  final file = File('${directory.path}/inventario_${DateTime.now().millisecondsSinceEpoch}.$format');
  await file.writeAsBytes(response.data);
  
  return file.path;
}
```

---

### POST `/api/v1/reports/movements`

**Descripción**: Genera reporte de movimientos (ventas, fallecimientos).

**Autenticación**: Requerida

**Request Body**:
```json
{
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "format": "pdf",
  "movement_type": "sold",  // "sold", "deceased", o null (todos)
  "date_from": "2024-01-01T00:00:00Z",
  "date_to": "2024-12-31T23:59:59Z"
}
```

---

### POST `/api/v1/reports/growth`

**Descripción**: Genera reporte de crecimiento y GDP.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",  // Opcional
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",  // Opcional (si no animal_id)
  "format": "excel"
}
```

---

## 🔔 Alertas y Cronograma

### POST `/api/v1/alerts`

**Descripción**: Crea una nueva alerta o evento programado.

**Autenticación**: Requerida

**Request Body**:
```json
{
  "title": "Pesaje masivo programado",
  "description": "Pesaje mensual de hato",
  "type": "scheduled_weighing",
  "status": "pending",
  "scheduled_date": "2024-12-25T08:00:00Z",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "farm_id": "770e8400-e29b-41d4-a716-446655440000"
}
```

**Response 201**:
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440000",
  "title": "Pesaje masivo programado",
  "description": "Pesaje mensual de hato",
  "type": "scheduled_weighing",
  "status": "pending",
  "scheduled_date": "2024-12-25T08:00:00Z",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-12-20T10:00:00Z"
}
```

**Implementación en Flutter**:
```dart
// lib/data/datasources/alerts_remote_datasource.dart

Future<AlertResponseModel> createAlert({
  required AlertCreateRequestModel request,
}) async {
  final response = await dio.post(
    '/api/v1/alerts',
    data: request.toJson(),
  );
  
  return AlertResponseModel.fromJson(response.data);
}
```

---

### GET `/api/v1/alerts`

**Descripción**: Lista alertas con filtros.

**Autenticación**: Requerida

**Query Parameters**:
- `page` (int, default: 1)
- `page_size` (int, default: 50, max: 100)
- `user_id` (UUID, optional)
- `farm_id` (UUID, optional)
- `type` (string, optional)
- `status` (string, optional)
- `scheduled_from` (datetime, optional)
- `scheduled_to` (datetime, optional)

**Implementación en Flutter**:
```dart
Future<AlertsListResponseModel> getAlerts({
  int page = 1,
  int pageSize = 50,
  String? userId,
  String? farmId,
  String? type,
  String? status,
  DateTime? scheduledFrom,
  DateTime? scheduledTo,
}) async {
  final queryParams = <String, dynamic>{
    'page': page,
    'page_size': pageSize,
    if (userId != null) 'user_id': userId,
    if (farmId != null) 'farm_id': farmId,
    if (type != null) 'type': type,
    if (status != null) 'status': status,
    if (scheduledFrom != null) 'scheduled_from': scheduledFrom.toIso8601String(),
    if (scheduledTo != null) 'scheduled_to': scheduledTo.toIso8601String(),
  };
  
  final response = await dio.get(
    '/api/v1/alerts',
    queryParameters: queryParams,
  );
  
  return AlertsListResponseModel.fromJson(response.data);
}
```

---

### GET `/api/v1/alerts/today`

**Descripción**: Obtiene alertas programadas para el día de hoy.

**Autenticación**: Requerida

**Query Parameters**:
- `user_id` (UUID, optional)
- `farm_id` (UUID, optional)

**Implementación en Flutter**:
```dart
Future<AlertsListResponseModel> getTodayAlerts({
  String? userId,
  String? farmId,
}) async {
  final queryParams = <String, dynamic>{
    if (userId != null) 'user_id': userId,
    if (farmId != null) 'farm_id': farmId,
  };
  
  final response = await dio.get(
    '/api/v1/alerts/today',
    queryParameters: queryParams,
  );
  
  return AlertsListResponseModel.fromJson(response.data);
}
```

---

### GET `/api/v1/alerts/upcoming`

**Descripción**: Obtiene alertas programadas para los próximos N días.

**Autenticación**: Requerida

**Query Parameters**:
- `days_ahead` (int, default: 7, max: 30): Días hacia adelante
- `user_id` (UUID, optional)
- `farm_id` (UUID, optional)

**Implementación en Flutter**:
```dart
Future<AlertsListResponseModel> getUpcomingAlerts({
  int daysAhead = 7,
  String? userId,
  String? farmId,
}) async {
  final queryParams = <String, dynamic>{
    'days_ahead': daysAhead,
    if (userId != null) 'user_id': userId,
    if (farmId != null) 'farm_id': farmId,
  };
  
  final response = await dio.get(
    '/api/v1/alerts/upcoming',
    queryParameters: queryParams,
  );
  
  return AlertsListResponseModel.fromJson(response.data);
}
```

---

## 🔄 Sincronización

Para documentación completa de sincronización, ver: [`FLUTTER_SYNC_GUIDE.md`](./FLUTTER_SYNC_GUIDE.md)

**Endpoints de sincronización**:
- `GET /api/v1/sync/health` - Health check
- `POST /api/v1/sync/cattle` - Sincronizar animales
- `POST /api/v1/sync/weight-estimations` - Sincronizar estimaciones

---

## 📝 Notas Importantes

1. **Autenticación**: Todos los endpoints (excepto login y algunos de sync) requieren el header `Authorization: Bearer {token}`

2. **Manejo de Token Expirado**: Si recibes un 401, debes limpiar el token y redirigir al usuario al login

3. **Paginación**: La mayoría de listados soportan paginación con `page` y `page_size`. El máximo `page_size` es generalmente 100.

4. **Timestamps**: Todos los timestamps están en formato ISO 8601 UTC (ej: `2024-12-20T10:30:00Z`)

5. **UUIDs**: Todos los IDs son UUIDs v4 (ej: `550e8400-e29b-41d4-a716-446655440000`)

6. **Razas válidas**: Solo estas 7 razas están permitidas:
   - `nelore`
   - `brahman`
   - `guzerat`
   - `senepol`
   - `girolando`
   - `gyr_lechero`
   - `sindi`

7. **Estados de animales**: `active`, `sold`, `deceased`, `inactive`

8. **Géneros**: `male`, `female`

---

## ✅ Checklist de Implementación

### Autenticación
- [ ] POST `/api/v1/auth/login`
- [ ] Manejo de token JWT en interceptor
- [ ] Manejo de token expirado (401)
- [ ] Almacenamiento seguro de token (SecureStorage)

### Machine Learning
- [ ] POST `/api/v1/ml/predict`
- [ ] GET `/api/v1/ml/models/status`

### Gestión de Animales
- [ ] POST `/api/v1/animals` (Crear)
- [ ] GET `/api/v1/animals` (Listar con filtros)
- [ ] GET `/api/v1/animals/{animal_id}` (Obtener)
- [ ] PUT `/api/v1/animals/{animal_id}` (Actualizar)
- [ ] DELETE `/api/v1/animals/{animal_id}` (Eliminar)
- [ ] GET `/api/v1/animals/{animal_id}/timeline` (Timeline)
- [ ] GET `/api/v1/animals/{animal_id}/lineage` (Linaje)

### Historial de Pesajes
- [ ] GET `/api/v1/weighings/animal/{animal_id}` (Historial)
- [ ] GET `/api/v1/weighings/{weighing_id}` (Detalle)

### Reportes
- [ ] POST `/api/v1/reports/traceability/{animal_id}` (Trazabilidad)
- [ ] POST `/api/v1/reports/inventory` (Inventario)
- [ ] POST `/api/v1/reports/movements` (Movimientos)
- [ ] POST `/api/v1/reports/growth` (Crecimiento)

### Alertas
- [ ] POST `/api/v1/alerts` (Crear)
- [ ] GET `/api/v1/alerts` (Listar)
- [ ] GET `/api/v1/alerts/today` (Hoy)
- [ ] GET `/api/v1/alerts/upcoming` (Próximas)

### Sincronización
- [ ] Ver `FLUTTER_SYNC_GUIDE.md` para endpoints de sync

---

**Última actualización**: 2024-12-30  
**Versión API**: 1.0.0  
**Backend**: FastAPI (Python 3.11+)

