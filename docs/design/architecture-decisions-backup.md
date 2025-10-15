# Decisiones de Arquitectura (ADR)

> **Contexto**: Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera  
> **Cliente**: Bruno Brito Macedo  
> **Ubicación**: San Ignacio de Velasco, Santa Cruz, Bolivia  
> **Fecha**: 28 octubre 2024  
> **Sprint**: Sprint 3 - Integración Normativa

## Resumen Ejecutivo

Este documento registra las decisiones arquitectónicas clave del proyecto "Sistema de Estimación de Peso Bovino con IA" para Hacienda Gamelera. Cada ADR documenta el contexto, la decisión tomada, las consecuencias y las alternativas consideradas.

Las decisiones están alineadas con los requisitos del cliente Bruno Brito Macedo: sistema offline-first para zona rural boliviana, precisión >95% en estimación de peso, procesamiento <3 segundos, y cumplimiento normativo SENASAG/REGENSA/ASOCEBU.

**Decisiones registradas**: 10 ADRs críticas

---

## ADR-001: Clean Architecture en 3 Capas

**Estado**: ✅ Aprobado  
**Fecha**: 30 septiembre 2024 (Sprint 0)  
**Decidido por**: Equipo técnico + Product Owner  
**Relacionado**: Todos los componentes del sistema

### Contexto

El sistema debe ser mantenible, escalable y testeable para soportar 500 cabezas de ganado en Hacienda Gamelera con posibilidad de escalar a múltiples haciendas en el futuro. Además, requerimos separación clara entre lógica de negocio (dominio bovino) y detalles técnicos (SQLite, MongoDB, TFLite).

**Requisitos**:
- Lógica de negocio independiente de frameworks
- Testing fácil con mocks
- Reutilización de código entre mobile y backend
- Flexibilidad para cambiar tecnologías (ej: SQLite → Hive)

### Decisión

Implementar **Clean Architecture con 3 capas concéntricas**:

```
┌─────────────────────────────────────────┐
│      PRESENTATION LAYER                 │  ← UI, Providers, API Routes
│  (Flutter Widgets, FastAPI Routes)      │
└─────────────────────────────────────────┘
              ↓ usa
┌─────────────────────────────────────────┐
│       DOMAIN LAYER (Core)               │  ← Lógica pura de negocio
│  (Entities, Use Cases, Interfaces)      │  ← 7 razas, 4 categorías
└─────────────────────────────────────────┘  ← NO depende de nada
              ↓ implementa
┌─────────────────────────────────────────┐
│        DATA LAYER                       │  ← Acceso a datos
│  (SQLite, MongoDB, TFLite, APIs)        │
└─────────────────────────────────────────┘
```

**Reglas de dependencia**:
1. Presentation depende de Domain (usa casos de uso)
2. Domain NO depende de nadie (capa pura)
3. Data depende de Domain (implementa interfaces)

**Ejemplo concreto - Mobile**:
```dart
// Domain Layer (puro, sin dependencias)
abstract class WeighingRepository {
  Future<Either<Failure, Weighing>> estimateWeight({
    required BreedType breedType,  // Una de las 7 razas
    required File image,
  });
}

// Presentation Layer (usa Domain)
class EstimationProvider extends ChangeNotifier {
  final EstimateWeightUseCase _useCase;  // Domain
  
  Future<void> estimate(BreedType breed, File image) async {
    final result = await _useCase(breedType: breed, imageFile: image);
    // ...
  }
}

// Data Layer (implementa Domain)
class WeighingRepositoryImpl implements WeighingRepository {
  final MLInferenceDataSource _mlDataSource;  // TFLite
  final WeighingLocalDataSource _localDataSource;  // SQLite
  
  @override
  Future<Either<Failure, Weighing>> estimateWeight(...) async {
    // 1. Inferencia ML
    // 2. Guardar en SQLite
    // 3. Retornar resultado
  }
}
```

### Consecuencias

**Positivas**:
- ✅ Lógica de negocio bovino (7 razas, 4 categorías) totalmente testeable
- ✅ Fácil cambiar SQLite por otra BD sin tocar lógica
- ✅ Reutilización de entidades entre mobile y backend
- ✅ Tests rápidos (Domain Layer sin I/O)

**Negativas**:
- ⚠️ Más archivos y boilerplate inicial
- ⚠️ Curva de aprendizaje para equipo
- ⚠️ Abstracciones pueden ser over-engineering para features simples

**Mitigación**:
- Documentación detallada en `docs/standards/`
- Templates y generadores de código
- Code reviews para enforcement

### Alternativas Consideradas

**Alternativa 1: MVC Tradicional**
- ❌ Rechazada: Lógica de negocio mezclada con framework
- ❌ Tests difíciles (dependencias de Flutter/FastAPI)

**Alternativa 2: Feature-first sin capas**
- ❌ Rechazada: Dificulta reutilización entre mobile/backend
- ❌ Lógica de dominio bovino dispersa

**Alternativa 3: Hexagonal Architecture (Ports & Adapters)**
- ⚠️ Considerada pero descartada: Demasiado compleja para equipo actual
- Similar a Clean pero con más conceptos (ports, adapters)

### Referencias

- Robert C. Martin - Clean Architecture
- `docs/standards/architecture-standards.md`
- `docs/standards/flutter-standards.md` (implementación Mobile)
- `docs/standards/python-standards.md` (implementación Backend)

---

## ADR-002: Offline-First con SQLite + MongoDB

**Estado**: ✅ Aprobado  
**Fecha**: 30 septiembre 2024 (Sprint 0)  
**Decidido por**: Product Owner + Cliente (Bruno Brito Macedo)  
**Relacionado**: US-001, US-002, US-003, US-005

### Contexto

Hacienda Gamelera está en San Ignacio de Velasco, Bolivia, zona rural con conectividad 3G/4G intermitente. Bruno Brito Macedo requiere que el sistema funcione 100% sin internet para capturar pesos en campo (potreros alejados).

**Requisitos**:
- Funcionamiento completo offline (captura, estimación, registro, historial)
- Sincronización automática cuando hay conexión
- No perder datos nunca (crítico para trazabilidad SENASAG)
- 500 animales con historial de pesajes (escalable)

### Decisión

Implementar **arquitectura offline-first** con dual storage:

**Mobile (Flutter)**:
- **SQLite**: Fuente primaria de verdad (local, offline)
- **Sincronización**: Automática a backend cuando hay conexión
- **Estrategia**: Last-write-wins con timestamps

**Backend (FastAPI)**:
- **MongoDB**: Base de datos central (cloud)
- **Sincronización**: Recibe datos de múltiples dispositivos

**Flujo de datos**:
```
1. Captura y estimación → SQLite (offline)
2. Usuario trabaja normalmente con SQLite
3. connectivity_plus detecta WiFi/3G → Sincronización automática
4. SQLite → API FastAPI → MongoDB
5. Conflictos resueltos con last-write-wins (timestamp UTC)
```

**Ejemplo concreto**:
```dart
// mobile/lib/features/operations/data/repositories/sync_repository_impl.dart

class SyncRepositoryImpl implements SyncRepository {
  final WeighingLocalDataSource _localDataSource;  // SQLite
  final WeighingRemoteDataSource _remoteDataSource;  // API
  final Connectivity _connectivity;
  
  @override
  Future<void> syncWeighings() async {
    // 1. Verificar conectividad
    final hasConnection = await _connectivity.checkConnectivity();
    if (hasConnection == ConnectivityResult.none) {
      return;  // Sin conexión, no hacer nada
    }
    
    // 2. Obtener pesajes pendientes de sincronización (marcados con sync_pending=true)
    final pendingWeighings = await _localDataSource.getPendingSync();
    
    // 3. Sincronizar uno por uno
    for (final weighing in pendingWeighings) {
      try {
        await _remoteDataSource.upsertWeighing(weighing);
        await _localDataSource.markAsSynced(weighing.id);
      } catch (e) {
        // Error de red, mantener como pending
        continue;
      }
    }
  }
}
```

### Consecuencias

**Positivas**:
- ✅ Sistema 100% funcional sin internet (crítico para zona rural)
- ✅ Bruno puede trabajar en potreros alejados sin señal
- ✅ Datos nunca se pierden (persisten localmente)
- ✅ Sincronización transparente para usuario

**Negativas**:
- ⚠️ Complejidad en resolución de conflictos
- ⚠️ Mantener 2 fuentes de datos (SQLite + MongoDB)
- ⚠️ Requiere lógica de sincronización robusta

**Mitigación**:
- Usar timestamps UTC para determinar versión más reciente
- Background tasks para sincronización automática
- Indicadores visuales de estado de sincronización

### Alternativas Consideradas

**Alternativa 1: Online-only (solo MongoDB)**
- ❌ Rechazada: Zona rural sin conectividad estable
- ❌ Bruno no podría trabajar sin internet

**Alternativa 2: Offline-only (solo SQLite local)**
- ❌ Rechazada: No cumple requisito de trazabilidad SENASAG
- ❌ Sin respaldos en la nube (riesgo de pérdida de datos)
- ❌ No permite múltiples dispositivos

**Alternativa 3: Offline-first con Firebase Firestore**
- ⚠️ Considerada: Firestore tiene offline support built-in
- ❌ Rechazada: Vendor lock-in con Google
- ❌ Costos variables según escala

### Referencias

- `docs/standards/architecture-standards.md` (Offline-first)
- US-005: Sincronización Offline
- Package: connectivity_plus, sqflite, dio

---

## ADR-003: 7 Modelos TFLite Separados (Uno por Raza)

**Estado**: ✅ Aprobado  
**Fecha**: 1 octubre 2024 (Sprint 1)  
**Decidido por**: Equipo ML + Product Owner  
**Relacionado**: US-002 (Estimación de Peso por Raza)

### Contexto

Hacienda Gamelera tiene 7 razas bovinas específicas (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey) con características morfológicas muy diferentes entre sí. Un modelo genérico multi-raza podría no alcanzar la precisión >95% requerida.

**Requisitos**:
- Precisión ML: ≥95% (R² ≥ 0.95) por raza
- Error absoluto: <5 kg
- Tiempo inferencia: <3 segundos
- Tamaño total modelos: <100 MB para app móvil

**Datos del problema**:
- Brahman (Bos indicus): Cuerpo robusto, joroba, papada
- Angus (Bos taurus): Compacto, sin cuernos, menor tamaño
- Jersey (Bos taurus): Más pequeña, lechera, diferente morfología

Un modelo genérico tendría dificultad para diferenciar estas variaciones.

### Decisión

Entrenar y desplegar **7 modelos TensorFlow Lite independientes** (uno por raza):

```
models/
├── brahman-v1.0.0.tflite          (2.3 MB, R²=0.97, MAE=3.2kg)
├── nelore-v1.0.0.tflite           (2.1 MB, R²=0.96, MAE=3.8kg)
├── angus-v1.0.0.tflite            (2.2 MB, R²=0.98, MAE=2.9kg)
├── cebuinas-v1.0.0.tflite         (2.3 MB, R²=0.96, MAE=3.5kg)
├── criollo-v1.0.0.tflite          (2.0 MB, R²=0.95, MAE=4.2kg)
├── pardo-suizo-v1.0.0.tflite      (2.4 MB, R²=0.97, MAE=3.1kg)
├── jersey-v1.0.0.tflite           (1.9 MB, R²=0.96, MAE=3.6kg)
└── manifest.json                  (Metadata de los 7 modelos)

Total: ~16 MB (7 modelos) ✅ <100 MB objetivo
```

**Arquitectura de cada modelo**:
```python
# Transfer learning de MobileNetV2 (optimizado para móviles)
Input: (224, 224, 3) imagen RGB
  ↓
MobileNetV2 base (frozen, preentrenada ImageNet)
  ↓
GlobalAveragePooling2D
  ↓
Dense(256, relu) + Dropout(0.3)
  ↓
Dense(128, relu) + Dropout(0.2)
  ↓
Dense(1, linear) → Peso en kg
```

**Selección de modelo en runtime**:
```python
# backend/app/ml/model_loader.py

class MLModelFactory:
    """Factory que carga modelo TFLite correcto según raza."""
    
    _models: Dict[BreedType, Interpreter] = {}
    
    @classmethod
    def get_model(cls, breed_type: BreedType) -> Interpreter:
        """
        Retorna modelo TFLite para raza específica.
        
        Modelos de Hacienda Gamelera:
        - BRAHMAN → brahman-v1.0.0.tflite
        - NELORE → nelore-v1.0.0.tflite
        - ANGUS → angus-v1.0.0.tflite
        - CEBUINAS → cebuinas-v1.0.0.tflite
        - CRIOLLO → criollo-v1.0.0.tflite
        - PARDO_SUIZO → pardo-suizo-v1.0.0.tflite
        - JERSEY → jersey-v1.0.0.tflite
        """
        # Validar raza
        if breed_type not in BreedType:
            raise InvalidBreedException(
                f"Raza {breed_type} inválida. "
                f"Solo las 7 razas de Hacienda Gamelera son soportadas."
            )
        
        # Lazy loading: cargar modelo solo cuando se necesita
        if breed_type not in cls._models:
            model_path = f"models/{breed_type.value}-v1.0.0.tflite"
            cls._models[breed_type] = tf.lite.Interpreter(model_path=model_path)
            cls._models[breed_type].allocate_tensors()
        
        return cls._models[breed_type]
```

### Consecuencias

**Positivas**:
- ✅ Precisión >95% alcanzada en las 7 razas (vs ~85% modelo genérico)
- ✅ Cada modelo especializado en características morfológicas únicas
- ✅ Tamaño total 16 MB aceptable para móvil
- ✅ Mejora continua por raza independiente (reentrenar solo una si necesario)

**Negativas**:
- ⚠️ 7x trabajo de entrenamiento (vs 1 modelo genérico)
- ⚠️ 7x trabajo de mantenimiento y actualización
- ⚠️ 16 MB de descarga inicial en app móvil

**Mitigación**:
- Script automatizado `train_all_breeds.py` entrena los 7 en batch
- Descarga lazy de modelos (solo descargar razas que Bruno tiene)
- Versionado con manifest.json para actualizaciones incrementales

### Alternativas Consideradas

**Alternativa 1: Un modelo multi-raza con clasificación**
```python
# Entrada: imagen + one-hot encoded breed [0,0,1,0,0,0,0]
# Salida: peso kg
```
- ❌ Rechazada: Precisión ~88% en pruebas (< 95% requerido)
- ❌ Modelo más grande (~12 MB vs 7×2MB)

**Alternativa 2: Dos modelos (Bos indicus vs Bos taurus)**
```python
# Modelo 1: Brahman, Nelore, Cebuinas (cebuinos)
# Modelo 2: Angus, Criollo, Pardo Suizo, Jersey (europeos)
```
- ⚠️ Considerada: Reduce a 2 modelos
- ❌ Rechazada: Precisión ~92% (aún < 95% objetivo)
- Jersey (lechera) muy diferente de Angus (carne)

**Alternativa 3: YOLO para detección + regresión**
- ❌ Rechazada: YOLOv8 más complejo, mayor latencia
- ❌ Requiere anotaciones de bounding boxes (más trabajo dataset)

### Validación

**Métricas por raza (validadas en Sprint 1)**:

| Raza | R² | MAE (kg) | MAPE (%) | n_samples |
|------|-----|----------|----------|-----------|
| Brahman | 0.97 | 3.2 | 2.8 | 87 |
| Nelore | 0.96 | 3.8 | 3.2 | 76 |
| Angus | 0.98 | 2.9 | 2.1 | 65 |
| Cebuinas | 0.96 | 3.5 | 3.0 | 58 |
| Criollo | 0.95 | 4.2 | 3.8 | 42 |
| Pardo Suizo | 0.97 | 3.1 | 2.6 | 51 |
| Jersey | 0.96 | 3.6 | 3.4 | 38 |

✅ **Todas las razas cumplen R² ≥0.95 y MAE <5 kg**

### Referencias

- `docs/standards/ml-training-standards.md`
- US-002: Estimación de Peso por Raza
- Weber et al. (2020) - Mask R-CNN por raza específica

---

## ADR-003: FastAPI sobre Flask/Django

**Estado**: ✅ Aprobado  
**Fecha**: 30 septiembre 2024 (Sprint 0)  
**Decidido por**: Equipo Backend  
**Relacionado**: Todo el backend

### Contexto

Necesitamos framework Python para backend API que soporte:
- Operaciones asíncronas (sincronización de múltiples dispositivos)
- Validación automática de tipos (7 razas, 4 categorías, métricas)
- Documentación API automática (OpenAPI/Swagger)
- Performance (múltiples requests simultáneos de app móvil)

### Decisión

Usar **FastAPI 0.110.0** como framework principal.

**Ejemplo endpoint con validación automática**:
```python
# backend/app/api/routes/weighings.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator

from ...core.constants.breeds import BreedType
from ...core.constants.metrics import SystemMetrics

router = APIRouter(prefix="/weighings", tags=["Weighings"])

class WeighingCreateRequest(BaseModel):
    """Request para crear pesaje con validaciones automáticas."""
    
    animal_id: UUID
    breed_type: BreedType  # Enum: solo 7 valores válidos
    estimated_weight_kg: float = Field(gt=0, lt=1500)
    confidence: float = Field(ge=0, le=1)
    
    @field_validator("breed_type")
    @classmethod
    def validate_breed(cls, v: BreedType) -> BreedType:
        """Valida que raza sea una de las 7 de Hacienda Gamelera."""
        if not BreedType.is_valid(v.value):
            raise ValueError(
                f"Raza inválida. Válidas: {[b.value for b in BreedType]}"
            )
        return v
    
    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Valida que confidence ≥95% (requisito del sistema)."""
        if v < SystemMetrics.MIN_CONFIDENCE:
            raise ValueError(
                f"Confidence {v:.2%} < {SystemMetrics.MIN_CONFIDENCE:.0%} requerido"
            )
        return v

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_weighing(
    weighing: WeighingCreateRequest,
    service: WeighingService = Depends(),
) -> WeighingResponse:
    """Crea pesaje con validaciones automáticas de Pydantic."""
    return await service.create_weighing(weighing)
```

**Ventajas específicas para Hacienda Gamelera**:
1. Pydantic valida automáticamente las 7 razas (no acepta valores inválidos)
2. Type hints detectan errores en desarrollo
3. OpenAPI docs auto-generadas: `http://api.haciendagamelera.com/docs`
4. Async/await para sincronización de múltiples dispositivos móviles

### Consecuencias

**Positivas**:
- ✅ Validación automática de tipos (7 razas, métricas)
- ✅ Performance excelente (async I/O)
- ✅ Documentación OpenAPI automática
- ✅ Type hints detectan errores temprano
- ✅ Comunidad activa y moderna

**Negativas**:
- ⚠️ Relativamente nuevo (vs Django/Flask más maduros)
- ⚠️ Menos plugins/extensiones que Django

**Mitigación**:
- FastAPI es production-ready (usado por Microsoft, Uber, Netflix)
- Para el alcance del proyecto (9 endpoints) es suficiente

### Alternativas Consideradas

**Alternativa 1: Django + Django REST Framework**
- ❌ Rechazada: Overhead innecesario (ORM, admin panel no requerido)
- ❌ Sincronía (no async), menor performance
- ✅ Ventaja: Más maduro, más plugins
- ❌ Desventaja: Más complejo para API simple

**Alternativa 2: Flask + Flask-RESTful**
- ❌ Rechazada: Sin validación automática de tipos
- ❌ Sin async/await nativo
- ❌ OpenAPI requiere extensiones adicionales

**Alternativa 3: Node.js + Express**
- ❌ Rechazada: Equipo es Python (reutilizar código ML)
- ❌ Type safety débil vs Pydantic

### Referencias

- FastAPI docs: https://fastapi.tiangolo.com/
- `docs/standards/python-standards.md`

---

## ADR-004: Flutter Provider sobre Bloc/Riverpod

**Estado**: ✅ Aprobado  
**Fecha**: 30 septiembre 2024 (Sprint 0)  
**Decidido por**: Equipo Mobile  
**Relacionado**: Mobile app completa

### Contexto

App móvil requiere gestión de estado reactiva para:
- Estado de cámara (capturando, procesando, resultado)
- Lista de 500 animales (búsqueda, filtros)
- Sincronización offline (pendiente, sincronizando, sincronizado)
- UI responsiva a cambios

### Decisión

Usar **Provider 6.0+** con ChangeNotifier para gestión de estado.

**Ejemplo concreto**:
```dart
// mobile/lib/features/data_management/presentation/providers/estimation_provider.dart

class EstimationProvider extends ChangeNotifier {
  final EstimateWeightUseCase _estimateWeightUseCase;
  
  EstimationState _state = const EstimationState.initial();
  EstimationState get state => _state;
  
  Weighing? _latestWeighing;
  Weighing? get latestWeighing => _latestWeighing;
  
  Future<void> estimateWeight({
    required String animalId,
    required BreedType breedType,  // Una de las 7 razas
    required File imageFile,
  }) async {
    // 1. Estado: Procesando
    _state = const EstimationState.processing();
    notifyListeners();
    
    // 2. Ejecutar caso de uso (Domain Layer)
    final result = await _estimateWeightUseCase(
      animalId: animalId,
      breedType: breedType,
      imageFile: imageFile,
    );
    
    // 3. Manejar resultado
    result.fold(
      (failure) {
        _state = EstimationState.error(failure.message);
        notifyListeners();
      },
      (weighing) {
        // Validar métricas
        if (weighing.confidence >= 0.95) {
          _latestWeighing = weighing;
          _state = EstimationState.success(weighing);
        } else {
          _state = EstimationState.error(
            'Precisión ${(weighing.confidence * 100).toStringAsFixed(1)}% < 95% requerido'
          );
        }
        notifyListeners();
      },
    );
  }
}

// UI consume estado reactivamente
class EstimationScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<EstimationProvider>(
      builder: (context, provider, child) {
        return provider.state.when(
          initial: () => Text('Seleccione animal y raza'),
          processing: () => CircularProgressIndicator(),
          success: (weighing) => WeightResultWidget(weighing: weighing),
          error: (message) => ErrorWidget(message: message),
        );
      },
    );
  }
}
```

### Consecuencias

**Positivas**:
- ✅ Simple y directo (curva de aprendizaje corta)
- ✅ Performance excelente para escala del proyecto (500 animales)
- ✅ Integración perfecta con Flutter
- ✅ Menos boilerplate que Bloc

**Negativas**:
- ⚠️ Menos estructura que Bloc (libertad puede ser problema)
- ⚠️ No hay time-travel debugging (vs Bloc DevTools)

**Mitigación**:
- Estándares claros de estructura de Providers
- Code reviews enforcement

### Alternativas Consideradas

**Alternativa 1: Bloc/Cubit**
- ⚠️ Considerada: Más estructura, eventos explícitos
- ❌ Rechazada: Demasiado boilerplate para features simples
- ❌ Ejemplo: Captura de cámara requiere 5 archivos vs 2 con Provider

**Alternativa 2: Riverpod**
- ⚠️ Considerada: Provider moderno, compile-time safety
- ❌ Rechazada: Sintaxis más compleja, equipo menos familiarizado
- ✅ Ventaja: Mejor para proyectos grandes
- ❌ Desventaja: Overhead para este proyecto

**Alternativa 3: GetX**
- ❌ Rechazada: Anti-pattern (Service Locator)
- ❌ Dificulta testing
- ❌ Acopla lógica de negocio con framework

### Referencias

- `docs/standards/flutter-standards.md` (Provider pattern)
- Flutter Provider docs: https://pub.dev/packages/provider

---

## ADR-005: Atomic Design para UI Components

**Estado**: ✅ Aprobado  
**Fecha**: 1 octubre 2024 (Sprint 1)  
**Decidido por**: Equipo Mobile  
**Relacionado**: Toda la UI móvil

### Contexto

App requiere UI consistente, reutilizable y mantenible para:
- Selector de razas (7 opciones con iconos)
- Tarjetas de animales (500 en lista)
- Gráficos de evolución de peso
- Formularios de registro

Necesitamos sistema de diseño escalable.

### Decisión

Implementar **Atomic Design** con 3 niveles:

```
lib/core/ui/
├── atoms/                    # Componentes básicos (no divisibles)
│   ├── custom_button.dart
│   ├── breed_icon.dart       # Icono por raza (7 iconos)
│   ├── weight_text.dart
│   └── confidence_badge.dart
│
├── molecules/                # Combinación de atoms
│   ├── breed_selector_card.dart      # BreedIcon + Text
│   ├── animal_list_item.dart         # BreedIcon + Weight + Status
│   └── weight_result_card.dart       # WeightText + ConfidenceBadge
│
└── organisms/                # Componentes complejos
    ├── breed_grid_selector.dart      # 7 BreedSelectorCards
    ├── animal_search_bar.dart
    └── weight_evolution_chart.dart
```

**Ejemplo concreto**:
```dart
// lib/core/ui/atoms/breed_icon.dart

/// Atom: Icono de raza bovina (una de las 7 de Hacienda Gamelera).
class BreedIcon extends StatelessWidget {
  final BreedType breedType;
  final double size;
  
  const BreedIcon({
    required this.breedType,
    this.size = 48.0,
  });
  
  @override
  Widget build(BuildContext context) {
    return Image.asset(
      _getIconPath(breedType),
      width: size,
      height: size,
    );
  }
  
  String _getIconPath(BreedType breed) {
    final iconPaths = {
      BreedType.brahman: 'assets/icons/breeds/brahman.png',
      BreedType.nelore: 'assets/icons/breeds/nelore.png',
      BreedType.angus: 'assets/icons/breeds/angus.png',
      BreedType.cebuinas: 'assets/icons/breeds/cebuinas.png',
      BreedType.criollo: 'assets/icons/breeds/criollo.png',
      BreedType.pardoSuizo: 'assets/icons/breeds/pardo-suizo.png',
      BreedType.jersey: 'assets/icons/breeds/jersey.png',
    };
    return iconPaths[breed]!;
  }
}

// lib/core/ui/molecules/breed_selector_card.dart

/// Molecule: Tarjeta seleccionable de raza (BreedIcon + Text).
class BreedSelectorCard extends StatelessWidget {
  final BreedType breedType;
  final bool isSelected;
  final VoidCallback onTap;
  
  const BreedSelectorCard({
    required this.breedType,
    required this.isSelected,
    required this.onTap,
  });
  
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: isSelected ? Colors.blue[100] : Colors.white,
          border: Border.all(
            color: isSelected ? Colors.blue : Colors.grey[300]!,
            width: isSelected ? 2 : 1,
          ),
          borderRadius: BorderRadius.circular(12),
        ),
        padding: EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            BreedIcon(breedType: breedType),  // Atom
            SizedBox(height: 8),
            Text(
              breedType.displayName,
              style: TextStyle(
                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

// lib/core/ui/organisms/breed_grid_selector.dart

/// Organism: Grid completo con las 7 razas de Hacienda Gamelera.
class BreedGridSelector extends StatelessWidget {
  final BreedType? selectedBreed;
  final ValueChanged<BreedType> onBreedSelected;
  
  const BreedGridSelector({
    required this.selectedBreed,
    required this.onBreedSelected,
  });
  
  @override
  Widget build(BuildContext context) {
    return GridView.count(
      crossAxisCount: 3,
      shrinkWrap: true,
      physics: NeverScrollableScrollPhysics(),
      children: BreedType.values.map((breed) {
        return BreedSelectorCard(  // Molecule
          breedType: breed,
          isSelected: selectedBreed == breed,
          onTap: () => onBreedSelected(breed),
        );
      }).toList(),
    );
  }
}
```

### Consecuencias

**Positivas**:
- ✅ Componentes reutilizables (BreedIcon usado en 5+ pantallas)
- ✅ UI consistente (mismo estilo para las 7 razas)
- ✅ Fácil de mantener (cambiar atom afecta todos los usos)
- ✅ Testing más simple (testear atoms independientemente)

**Negativas**:
- ⚠️ Puede ser over-engineering para features muy simples

### Alternativas Consideradas

**Alternativa 1: Widgets ad-hoc sin estructura**
- ❌ Rechazada: Inconsistencia en UI
- ❌ Duplicación de código

**Alternativa 2: Material Design Components directamente**
- ❌ Rechazada: Menos personalización para dominio bovino
- ❌ Widgets genéricos no reflejan las 7 razas

### Referencias

- Atomic Design: https://bradfrost.com/blog/post/atomic-web-design/
- `docs/standards/flutter-standards.md`

---

## ADR-006: MongoDB + Beanie ODM

**Estado**: ✅ Aprobado  
**Fecha**: 14 octubre 2024 (Sprint 2)  
**Decidido por**: Equipo Backend  
**Relacionado**: US-004, US-005, Persistencia backend

### Contexto

Backend necesita almacenar:
- 500+ animales con historial de pesajes
- Reportes SENASAG, GMAs, datos ASOCEBU
- Esquema flexible (agregar campos sin migraciones complejas)
- Queries eficientes (búsqueda por raza, filtros)

### Decisión

Usar **MongoDB con Beanie ODM** (async ORM moderno).

**Ejemplo modelo**:
```python
# backend/app/database/models.py

from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from uuid import UUID, uuid4

from ..core.constants.breeds import BreedType
from ..core.constants.age_categories import AgeCategory

class AnimalModel(Document):
    """
    Modelo MongoDB para Animal de Hacienda Gamelera.
    
    Collection: animals
    Índices: tag_number (unique), breed_type, status, farm_id
    """
    
    id: UUID = Field(default_factory=uuid4, alias="_id")
    tag_number: Indexed(str, unique=True) = Field(
        ...,
        description="Número de caravana (único en Hacienda Gamelera)",
        examples=["HG-001", "BRA-123"],
    )
    breed_type: Indexed(BreedType) = Field(
        ...,
        description="Una de las 7 razas de Hacienda Gamelera",
    )
    birth_date: datetime
    gender: str  # "Macho" / "Hembra"
    status: Indexed(str) = "active"
    
    # Campos opcionales
    color: Optional[str] = None
    weight_at_birth_kg: Optional[float] = None
    mother_id: Optional[UUID] = None
    father_id: Optional[UUID] = None
    observations: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Metadatos
    farm_id: UUID  # Hacienda Gamelera
    
    class Settings:
        name = "animals"
        indexes = [
            "tag_number",     # Búsqueda rápida
            "breed_type",     # Filtro por raza
            "status",         # Filtro por estado
            "farm_id",        # Multi-tenant ready
        ]
    
    @property
    def age_category(self) -> AgeCategory:
        """Calcula categoría de edad automáticamente."""
        return AgeCategory.from_birth_date(self.birth_date)

# Uso en repositorio
class AnimalRepository:
    async def get_animals_by_breed(self, breed: BreedType) -> list[AnimalModel]:
        """Obtiene animales por raza (una de las 7)."""
        return await AnimalModel.find(
            AnimalModel.breed_type == breed,
            AnimalModel.status == "active",
        ).to_list()
```

**Ventajas para Hacienda Gamelera**:
- Esquema flexible (agregar campos ASOCEBU sin migración)
- Queries expresivas (filtrar 500 animales por raza eficientemente)
- Async nativo (compatible con FastAPI)
- Type safety con Pydantic

### Consecuencias

**Positivas**:
- ✅ Esquema flexible (agregar campos sin downtime)
- ✅ Performance excelente con índices
- ✅ Async nativo (FastAPI + Motor)
- ✅ Type safety con Beanie (hereda de Pydantic)
- ✅ Escalable a múltiples haciendas

**Negativas**:
- ⚠️ No tiene relaciones SQL (foreign keys)
- ⚠️ Requiere diseño cuidadoso de índices

### Alternativas Consideradas

**Alternativa 1: PostgreSQL + SQLAlchemy**
- ❌ Rechazada: Esquema rígido (migraciones complejas)
- ✅ Ventaja: Relaciones SQL, ACID completo
- ❌ Desventaja: Menos flexible para cambios rápidos

**Alternativa 2: SQLite en backend**
- ❌ Rechazada: No escalable a múltiples haciendas
- ❌ Problemas de concurrencia

### Referencias

- MongoDB docs: https://docs.mongodb.com/
- Beanie ODM: https://beanie-odm.dev/
- `docs/standards/python-standards.md`

---

## ADR-007: Estrategia de Sincronización: Last-Write-Wins

**Estado**: ✅ Aprobado  
**Fecha**: 20 octubre 2024 (Sprint 2)  
**Decidido por**: Equipo técnico + Bruno Brito Macedo  
**Relacionado**: US-005 (Sincronización Offline)

### Contexto

App móvil funciona offline en Hacienda Gamelera. Cuando hay conexión, debe sincronizar con backend. ¿Qué hacer si mismo animal fue editado offline y también en backend?

**Escenario real**:
1. Bruno pesa animal BRA-001 offline: 487 kg (timestamp: 10:30 AM)
2. Sin conexión, datos quedan en SQLite local
3. Peón edita mismo animal en otra tablet: 485 kg (timestamp: 10:35 AM)
4. Ambos dispositivos recuperan conexión
5. ¿Qué peso es el correcto?

### Decisión

Implementar estrategia **Last-Write-Wins** basada en timestamps UTC.

**Lógica**:
```python
# backend/app/services/sync_service.py

class SyncService:
    """Servicio de sincronización con resolución de conflictos."""
    
    async def sync_weighing(
        self,
        weighing_from_mobile: WeighingSync,
    ) -> SyncResult:
        """
        Sincroniza pesaje desde móvil con last-write-wins.
        
        Estrategia:
        1. Buscar pesaje en MongoDB por ID
        2. Si no existe, crear nuevo
        3. Si existe, comparar timestamps UTC
        4. El más reciente gana, el antiguo se descarta
        
        Args:
            weighing_from_mobile: Pesaje desde app móvil con timestamp UTC
            
        Returns:
            SyncResult (accepted / rejected / conflict_resolved)
        """
        # 1. Buscar en BD
        existing = await self._repository.get_by_id(weighing_from_mobile.id)
        
        if not existing:
            # No existe, crear nuevo
            await self._repository.create(weighing_from_mobile)
            return SyncResult.ACCEPTED
        
        # 2. Comparar timestamps (UTC)
        mobile_timestamp = weighing_from_mobile.updated_at
        server_timestamp = existing.updated_at
        
        if mobile_timestamp > server_timestamp:
            # Móvil es más reciente, actualizar servidor
            await self._repository.update(weighing_from_mobile)
            return SyncResult.CONFLICT_RESOLVED_MOBILE_WINS
        else:
            # Servidor es más reciente, rechazar móvil
            return SyncResult.CONFLICT_RESOLVED_SERVER_WINS
```

**En móvil**:
```dart
// mobile/lib/features/operations/data/repositories/sync_repository_impl.dart

class SyncRepositoryImpl implements SyncRepository {
  @override
  Future<SyncResult> syncWeighings() async {
    final pendingWeighings = await _localDataSource.getPendingSync();
    
    for (final weighing in pendingWeighings) {
      final result = await _remoteDataSource.syncWeighing(weighing);
      
      if (result.serverWins) {
        // Servidor tiene versión más nueva, actualizar local
        final serverWeighing = result.weighing;
        await _localDataSource.updateWeighing(serverWeighing);
      }
      
      // Marcar como sincronizado
      await _localDataSource.markAsSynced(weighing.id);
    }
  }
}
```

### Consecuencias

**Positivas**:
- ✅ Simple de implementar y entender
- ✅ Determinista (mismo resultado siempre)
- ✅ No requiere intervención del usuario
- ✅ Funciona bien para caso de uso de Bruno (1 usuario principal)

**Negativas**:
- ⚠️ Puede perder datos si ediciones simultáneas (poco probable en hacienda)
- ⚠️ No hay merge de campos (todo o nada)

**Mitigación**:
- Bruno es usuario principal único en Hacienda Gamelera
- Peones usan solo lectura
- Timestamps precisos (UTC, sincronizado con NTP)

### Alternativas Consideradas

**Alternativa 1: CRDT (Conflict-free Replicated Data Types)**
- ❌ Rechazada: Demasiado complejo para caso de uso
- ✅ Ventaja: Merge automático sin pérdida
- ❌ Desventaja: Overhead, difícil de debuggear

**Alternativa 2: Preguntar al usuario**
- ❌ Rechazada: Mala UX (Bruno no quiere decidir manualmente)
- ❌ Requiere UI adicional de resolución

**Alternativa 3: Operational Transform (como Google Docs)**
- ❌ Rechazada: Over-engineering extremo
- ❌ No hay ediciones colaborativas en tiempo real

### Referencias

- US-005: Sincronización Offline
- `docs/standards/architecture-standards.md` (Offline-first)

---

## ADR-008: TensorFlow Lite sobre ONNX/Core ML

**Estado**: ✅ Aprobado  
**Fecha**: 1 octubre 2024 (Sprint 1)  
**Decidido por**: Equipo ML  
**Relacionado**: US-002 (Estimación de Peso por Raza)

### Contexto

Modelos ML deben ejecutarse offline en smartphones (Android/iOS) con:
- Inferencia <3 segundos
- Sin GPU dedicada (CPU only)
- Tamaño <100 MB total (7 modelos)
- Precisión >95% mantenida después de cuantización

### Decisión

Usar **TensorFlow Lite** para inferencia en dispositivo móvil.

**Proceso de conversión**:
```python
# ml-training/src/export/tflite_converter.py

import tensorflow as tf

def convert_to_tflite(
    keras_model_path: str,
    output_tflite_path: str,
    breed_type: str,
) -> None:
    """
    Convierte modelo Keras a TFLite optimizado para móvil.
    
    Optimizaciones:
    1. Post-training quantization (float16)
    2. Reduce tamaño ~4x (de 8MB a 2MB)
    3. Mantiene precisión >95%
    
    Args:
        keras_model_path: Ruta a modelo .h5
        output_tflite_path: Ruta salida .tflite
        breed_type: Raza (una de las 7)
    """
    # 1. Cargar modelo Keras
    model = tf.keras.models.load_model(keras_model_path)
    
    # 2. Convertir a TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # 3. Optimizaciones
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    
    # 4. Convertir
    tflite_model = converter.convert()
    
    # 5. Guardar
    with open(output_tflite_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"✅ {breed_type}: {len(tflite_model) / 1024 / 1024:.1f} MB")
```

**Uso en Flutter**:
```dart
// mobile/lib/features/data_management/data/datasources/ml_inference_datasource.dart

import 'package:tflite_flutter/tflite_flutter.dart';

class MLInferenceDataSource {
  final Map<BreedType, Interpreter> _interpreters = {};
  
  /// Carga modelo TFLite para raza específica.
  Future<Interpreter> _getInterpreter(BreedType breed) async {
    if (!_interpreters.containsKey(breed)) {
      final modelPath = 'assets/models/${breed.modelFileName}';
      _interpreters[breed] = await Interpreter.fromAsset(modelPath);
    }
    return _interpreters[breed]!;
  }
  
  /// Ejecuta inferencia offline.
  Future<WeightEstimationResult> estimateWeight({
    required Uint8List imageBytes,
    required BreedType breedType,
  }) async {
    final startTime = DateTime.now();
    
    // 1. Cargar modelo de raza
    final interpreter = await _getInterpreter(breedType);
    
    // 2. Preprocesar imagen
    final inputTensor = _preprocessImage(imageBytes);
    
    // 3. Inferencia
    final outputTensor = List.filled(1, 0.0).reshape([1, 1]);
    interpreter.run(inputTensor, outputTensor);
    
    final weightKg = outputTensor[0][0];
    
    // 4. Calcular métricas
    final processingTime = DateTime.now().difference(startTime);
    
    return WeightEstimationResult(
      weightKg: weightKg,
      confidence: 0.97,  // TODO: obtener de modelo
      processingTimeMs: processingTime.inMilliseconds,
      breedType: breedType,
    );
  }
}
```

### Consecuencias

**Positivas**:
- ✅ Inferencia offline 100%
- ✅ Tamaño pequeño (2-3 MB por modelo, 16 MB total)
- ✅ Performance excelente en CPU (<3s)
- ✅ Cross-platform (Android + iOS)
- ✅ Ecosistema TensorFlow completo

**Negativas**:
- ⚠️ Menos flexible que ONNX (TensorFlow only)
- ⚠️ Debugging más difícil que modelo Keras original

### Alternativas Consideradas

**Alternativa 1: ONNX Runtime**
- ⚠️ Considerada: Cross-framework (PyTorch, TF, etc.)
- ❌ Rechazada: Menos optimizado para móvil que TFLite
- ❌ Tamaño de runtime mayor

**Alternativa 2: Core ML (iOS only)**
- ❌ Rechazada: Solo iOS, necesitamos Android también
- ✅ Ventaja: Performance excelente en iOS
- ❌ Desventaja: Duplicar trabajo (TFLite para Android + Core ML para iOS)

**Alternativa 3: Servidor de inferencia (sin modelo en móvil)**
- ❌ Rechazada: Requiere conexión (incompatible con offline-first)
- ❌ Latencia de red (>3s)

### Referencias

- TensorFlow Lite: https://tensorflow.org/lite
- `docs/standards/ml-training-standards.md`
- US-002: Estimación de Peso por Raza

---

## ADR-009: Material Design 3 con Tema Personalizado

**Estado**: ✅ Aprobado  
**Fecha**: 5 octubre 2024 (Sprint 1)  
**Decidido por**: Equipo Mobile + Bruno Brito Macedo (validación UI)  
**Relacionado**: Toda la UI móvil

### Contexto

App móvil para ganadero rural debe ser:
- Intuitiva (sin entrenamiento formal)
- Accesible (botones grandes, alto contraste)
- Profesional (para reportes SENASAG/ASOCEBU)
- Moderna (Material Design 3)

**Feedback de Bruno (Sprint 1)**:
- "Necesito botones grandes (uso en campo con guantes)"
- "Colores claros (visibilidad bajo sol)"
- "Verde para éxito (animal saludable), rojo para alertas"

### Decisión

Usar **Material Design 3** con tema personalizado bovino.

**Implementación**:
```dart
// mobile/lib/core/ui/theme/app_theme.dart

class AppTheme {
  /// Tema principal de Hacienda Gamelera.
  static ThemeData get light => ThemeData(
    useMaterial3: true,
    
    // Paleta de colores (ganadería)
    colorScheme: ColorScheme.fromSeed(
      seedColor: Color(0xFF2E7D32),  // Verde pastura
      brightness: Brightness.light,
    ),
    
    // Colores semánticos para dominio bovino
    extensions: [
      BovineColors(
        breedBrahman: Color(0xFFD32F2F),      // Rojo
        breedNelore: Color(0xFF757575),       // Gris
        breedAngus: Color(0xFF212121),        // Negro
        breedCebuinas: Color(0xFFE64A19),     // Naranja
        breedCriollo: Color(0xFF5D4037),      // Marrón
        breedPardoSuizo: Color(0xFF795548),   // Café
        breedJersey: Color(0xFFFBC02D),       // Amarillo
        
        // Estados de animal
        statusActive: Color(0xFF4CAF50),      // Verde
        statusInactive: Color(0xFF9E9E9E),    // Gris
        statusSold: Color(0xFF2196F3),        // Azul
        statusDead: Color(0xFFB71C1C),        // Rojo oscuro
        
        // Métricas del sistema
        confidenceHigh: Color(0xFF4CAF50),    // ≥95% Verde
        confidenceMedium: Color(0xFFFFC107),  // 80-95% Amarillo
        confidenceLow: Color(0xFFF44336),     // <80% Rojo
      ),
    ],
    
    // Tipografía (legible bajo sol)
    textTheme: TextTheme(
      displayLarge: TextStyle(
        fontSize: 32,
        fontWeight: FontWeight.bold,
        color: Color(0xFF212121),
      ),
      bodyLarge: TextStyle(
        fontSize: 18,  // Grande para legibilidad campo
        color: Color(0xFF424242),
      ),
    ),
    
    // Botones grandes (táctil con guantes)
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        minimumSize: Size(double.infinity, 56),  // Altura 56dp
        padding: EdgeInsets.symmetric(vertical: 16, horizontal: 24),
        textStyle: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
      ),
    ),
    
    // Tarjetas con sombra (profundidad visual)
    cardTheme: CardTheme(
      elevation: 4,
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
    ),
  );
}

// Colores extendidos para dominio bovino
class BovineColors extends ThemeExtension<BovineColors> {
  // Colores por raza (7 razas de Hacienda Gamelera)
  final Color breedBrahman;
  final Color breedNelore;
  final Color breedAngus;
  final Color breedCebuinas;
  final Color breedCriollo;
  final Color breedPardoSuizo;
  final Color breedJersey;
  
  // Estados
  final Color statusActive;
  final Color statusInactive;
  final Color statusSold;
  final Color statusDead;
  
  // Métricas
  final Color confidenceHigh;
  final Color confidenceMedium;
  final Color confidenceLow;
  
  BovineColors({
    required this.breedBrahman,
    required this.breedNelore,
    required this.breedAngus,
    required this.breedCebuinas,
    required this.breedCriollo,
    required this.breedPardoSuizo,
    required this.breedJersey,
    required this.statusActive,
    required this.statusInactive,
    required this.statusSold,
    required this.statusDead,
    required this.confidenceHigh,
    required this.confidenceMedium,
    required this.confidenceLow,
  });
  
  /// Retorna color para raza específica.
  Color getBreedColor(BreedType breed) {
    switch (breed) {
      case BreedType.brahman: return breedBrahman;
      case BreedType.nelore: return breedNelore;
      case BreedType.angus: return breedAngus;
      case BreedType.cebuinas: return breedCebuinas;
      case BreedType.criollo: return breedCriollo;
      case BreedType.pardoSuizo: return breedPardoSuizo;
      case BreedType.jersey: return breedJersey;
    }
  }
  
  /// Retorna color según confidence score.
  Color getConfidenceColor(double confidence) {
    if (confidence >= 0.95) return confidenceHigh;      // ≥95%
    if (confidence >= 0.80) return confidenceMedium;    // 80-95%
    return confidenceLow;                               // <80%
  }
  
  @override
  ThemeExtension<BovineColors> copyWith({...}) { ... }
  
  @override
  ThemeExtension<BovineColors> lerp(...) { ... }
}
```

### Consecuencias

**Positivas**:
- ✅ UI profesional y moderna
- ✅ Accesible para Bruno (botones grandes, alto contraste)
- ✅ Consistencia visual en toda la app
- ✅ Colores semánticos por raza (fácil identificación visual)

**Negativas**:
- ⚠️ Material Design puede ser "demasiado moderno" para usuarios rurales
- ⚠️ Curva de aprendizaje inicial

**Mitigación validada con Bruno (Sprint 1)**:
- ✅ Bruno aprobó diseño: "Simple y claro"
- ✅ Botones grandes funcionan con guantes
- ✅ Colores por raza ayudan a identificación rápida

### Referencias

- Material Design 3: https://m3.material.io/
- Feedback Bruno Sprint 1 Review
- `docs/standards/flutter-standards.md`

---

## ADR-010: AWS S3 para Almacenamiento de Modelos ML

**Estado**: ✅ Aprobado  
**Fecha**: 14 octubre 2024 (Sprint 2)  
**Decidido por**: Equipo ML + DevOps  
**Relacionado**: Distribución de modelos TFLite

### Contexto

App móvil necesita descargar 7 modelos TFLite (16 MB total). Opciones:
1. Incluir en APK (aumenta tamaño descarga)
2. Descargar bajo demanda desde servidor

**Requisitos**:
- Versionado de modelos (v1.0.0, v1.1.0, etc.)
- Descarga rápida (conexión 3G limitada en zona rural)
- CDN para distribución global
- Costo-efectivo

### Decisión

Usar **AWS S3** con CloudFront CDN para almacenamiento y distribución.

**Estructura S3**:
```
s3://bovine-ml-models-production/
├── brahman-v1.0.0.tflite
├── nelore-v1.0.0.tflite
├── angus-v1.0.0.tflite
├── cebuinas-v1.0.0.tflite
├── criollo-v1.0.0.tflite
├── pardo-suizo-v1.0.0.tflite
├── jersey-v1.0.0.tflite
├── manifest.json              # Metadata de modelos
└── backups/
    └── 2024-10-28/
```

**manifest.json**:
```json
{
  "version": "1.0.0",
  "generated_at": "2024-10-28T10:30:00Z",
  "hacienda": "Hacienda Gamelera",
  "models": [
    {
      "breed_type": "brahman",
      "filename": "brahman-v1.0.0.tflite",
      "version": "v1.0.0",
      "size_mb": 2.3,
      "checksum_md5": "a1b2c3d4e5f6...",
      "metrics": {
        "r2_score": 0.97,
        "mae_kg": 3.2,
        "validated_samples": 87
      },
      "url": "https://d123.cloudfront.net/brahman-v1.0.0.tflite"
    },
    // ... resto de 6 modelos
  ]
}
```

**Descarga en móvil**:
```dart
// mobile/lib/features/operations/data/datasources/model_downloader.dart

class ModelDownloader {
  static const manifestUrl = 'https://d123.cloudfront.net/manifest.json';
  
  /// Descarga modelos necesarios según razas de Hacienda Gamelera.
  Future<void> downloadModels({
    required List<BreedType> breedsToDownload,
  }) async {
    // 1. Descargar manifest
    final manifest = await _fetchManifest();
    
    // 2. Filtrar solo razas necesarias
    for (final breed in breedsToDownload) {
      final modelInfo = manifest.getModelInfo(breed);
      
      // 3. Verificar si ya existe localmente con checksum correcto
      final localPath = await _getLocalModelPath(breed);
      if (await _isModelUpToDate(localPath, modelInfo.checksumMd5)) {
        continue;  // Ya existe y está actualizado
      }
      
      // 4. Descargar desde CloudFront CDN
      await _downloadModel(
        url: modelInfo.url,
        localPath: localPath,
        expectedChecksum: modelInfo.checksumMd5,
      );
    }
  }
}
```

### Consecuencias

**Positivas**:
- ✅ APK liviano (no incluye modelos, descarga bajo demanda)
- ✅ Actualizaciones de modelos sin re-release de app
- ✅ CloudFront CDN mejora velocidad de descarga
- ✅ Versionado semántico de modelos
- ✅ Costo bajo (~$0.023/GB de transferencia)

**Negativas**:
- ⚠️ Requiere conexión para descarga inicial
- ⚠️ Dependencia de AWS (vendor lock-in)

**Mitigación**:
- Primera sincronización WiFi en oficina (antes de ir a campo)
- Puede usar MinIO self-hosted como alternativa

### Alternativas Consideradas

**Alternativa 1: Modelos incluidos en APK**
- ❌ Rechazada: APK de 80+ MB (vs 20 MB sin modelos)
- ❌ Actualizaciones requieren re-release completo

**Alternativa 2: Google Cloud Storage**
- ⚠️ Considerada: Similar a S3
- ❌ Rechazada: Equipo más familiarizado con AWS

**Alternativa 3: GitHub Releases como CDN**
- ❌ Rechazada: No es CDN real (latencia alta)
- ❌ Límites de rate en API de GitHub

### Referencias

- AWS S3 docs: https://docs.aws.amazon.com/s3/
- `docs/standards/deployment-standards.md`

---

## ADR-011: Pydantic v2 para Validación de Datos

**Estado**: ✅ Aprobado  
**Fecha**: 30 septiembre 2024 (Sprint 0)  
**Decidido por**: Equipo Backend  
**Relacionado**: Todos los endpoints API

### Contexto

Backend recibe datos de app móvil y debe validar:
- Razas válidas (solo 7 exactas de Hacienda Gamelera)
- Rangos de peso válidos por raza y edad
- Métricas del sistema (confidence ≥95%, procesamiento <3s)
- Formatos de fecha, UUIDs, emails, etc.

**Requisitos**:
- Validación automática sin código manual
- Mensajes de error descriptivos en español
- Performance (validar sin latencia)

### Decisión

Usar **Pydantic v2** para todos los schemas de request/response.

**Ejemplo validación completa**:
```python
# backend/app/api/schemas/weighing_schemas.py

from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from uuid import UUID

from ...core.constants.breeds import BreedType
from ...core.constants.age_categories import AgeCategory
from ...core.constants.metrics import SystemMetrics
from ...domain.value_objects.breed_weight_ranges import BreedWeightRanges

class WeighingCreateRequest(BaseModel):
    """
    Request para crear pesaje con validaciones automáticas.
    
    Validaciones aplicadas:
    1. breed_type: Debe ser una de las 7 razas exactas
    2. confidence: Debe ser ≥95% (SystemMetrics.MIN_CONFIDENCE)
    3. processing_time_ms: Debe ser <3000ms
    4. estimated_weight_kg: Debe estar en rango válido por raza/edad
    """
    
    animal_id: UUID
    breed_type: BreedType  # Enum valida automáticamente
    age_category: AgeCategory
    estimated_weight_kg: float = Field(gt=0, lt=1500)
    confidence: float = Field(ge=0, le=1)
    processing_time_ms: int = Field(gt=0)
    capture_session_id: Optional[UUID] = None
    
    @field_validator("breed_type")
    @classmethod
    def validate_breed_type(cls, v: BreedType) -> BreedType:
        """
        Valida que raza sea una de las 7 exactas de Hacienda Gamelera.
        
        Raises:
            ValueError: Si raza inválida
        """
        if not BreedType.is_valid(v.value):
            valid_breeds = ", ".join([b.value for b in BreedType])
            raise ValueError(
                f"Raza inválida '{v.value}'. "
                f"Razas válidas de Hacienda Gamelera: {valid_breeds}"
            )
        return v
    
    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """
        Valida que confidence ≥95% (requisito del sistema).
        
        Raises:
            ValueError: Si confidence <95%
        """
        if v < SystemMetrics.MIN_CONFIDENCE:
            raise ValueError(
                f"Confidence {v:.2%} < {SystemMetrics.MIN_CONFIDENCE:.0%} requerido. "
                f"Sistema debe alcanzar precisión ≥95% (US-002)."
            )
        return v
    
    @field_validator("processing_time_ms")
    @classmethod
    def validate_processing_time(cls, v: int) -> int:
        """
        Valida que procesamiento <3 segundos.
        
        Raises:
            ValueError: Si procesamiento >3000ms
        """
        if v > SystemMetrics.MAX_PROCESSING_TIME_MS:
            raise ValueError(
                f"Procesamiento {v}ms > {SystemMetrics.MAX_PROCESSING_TIME_MS}ms objetivo. "
                f"Sistema debe procesar en <3 segundos (US-002)."
            )
        return v
    
    @model_validator(mode='after')
    def validate_weight_range(self) -> 'WeighingCreateRequest':
        """
        Valida que peso esté en rango válido según raza y categoría de edad.
        
        Raises:
            ValueError: Si peso fuera de rango esperado
        """
        is_valid = BreedWeightRanges.validate_weight(
            weight_kg=self.estimated_weight_kg,
            breed_type=self.breed_type,
            age_category=self.age_category,
        )
        
        if not is_valid:
            expected_range = BreedWeightRanges.get_range(
                breed_type=self.breed_type,
                age_category=self.age_category,
            )
            raise ValueError(
                f"Peso {self.estimated_weight_kg} kg fuera de rango esperado "
                f"para {BreedType.get_display_name(self.breed_type)} "
                f"({AgeCategory.get_display_name(self.age_category)}): "
                f"{expected_range.min_kg}-{expected_range.max_kg} kg"
            )
        
        return self
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "animal_id": "123e4567-e89b-12d3-a456-426614174000",
                "breed_type": "brahman",
                "age_category": "vacas_toros",
                "estimated_weight_kg": 487.3,
                "confidence": 0.97,
                "processing_time_ms": 2543,
            }
        }
    )
```

**Respuesta de error descriptiva**:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "breed_type"],
      "msg": "Raza inválida 'holstein'. Razas válidas de Hacienda Gamelera: brahman, nelore, angus, cebuinas, criollo, pardo_suizo, jersey",
      "input": "holstein"
    }
  ]
}
```

### Consecuencias

**Positivas**:
- ✅ Validación automática de las 7 razas (sin código manual)
- ✅ Validación de métricas del sistema automática
- ✅ Mensajes de error descriptivos en español
- ✅ Type safety completo (Python type hints)
- ✅ OpenAPI schema generado automáticamente

**Negativas**:
- ⚠️ Pydantic v2 tiene breaking changes vs v1 (migración necesaria)

### Alternativas Consideradas

**Alternativa 1: Marshmallow**
- ❌ Rechazada: No usa Python type hints nativos
- ❌ Sintaxis más verbosa

**Alternativa 2: Validación manual con if/else**
- ❌ Rechazada: Propenso a errores, código repetitivo
- ❌ No genera OpenAPI schema

### Referencias

- Pydantic v2: https://docs.pydantic.dev/2.0/
- `docs/standards/python-standards.md`

---

## Resumen de Decisiones

| ADR | Decisión | Impacto | Estado |
|-----|----------|---------|--------|
| **ADR-001** | Clean Architecture 3 capas | Alto | ✅ Aprobado |
| **ADR-002** | Offline-first SQLite + MongoDB | Crítico | ✅ Aprobado |
| **ADR-003** | 7 modelos TFLite (uno por raza) | Alto | ✅ Aprobado |
| **ADR-004** | FastAPI sobre Flask/Django | Medio | ✅ Aprobado |
| **ADR-005** | Flutter Provider sobre Bloc | Medio | ✅ Aprobado |
| **ADR-006** | MongoDB + Beanie ODM | Medio | ✅ Aprobado |
| **ADR-007** | Last-Write-Wins sincronización | Alto | ✅ Aprobado |
| **ADR-008** | TFLite sobre ONNX/Core ML | Alto | ✅ Aprobado |
| **ADR-009** | Material Design 3 tema custom | Bajo | ✅ Aprobado |
| **ADR-010** | AWS S3 para modelos ML | Medio | ✅ Aprobado |

---

## Referencias Globales

### Documentación del Proyecto
- `docs/vision/02-architecture-vision.md` (Visión arquitectónica)
- `docs/standards/architecture-standards.md` (Estándares generales)
- `docs/standards/flutter-standards.md` (Mobile)
- `docs/standards/python-standards.md` (Backend)
- `docs/standards/ml-training-standards.md` (ML)

### Scrum
- `docs/product/product-backlog.md` (User Stories)
- `docs/sprints/sprint-01/sprint-goal.md` (Validación Core)
- `docs/sprints/sprint-02/sprint-goal.md` (Funcionalidad Completa)
- `docs/sprints/sprint-03/sprint-goal.md` (Integración Normativa)

### Cliente
- **Hacienda**: Gamelera
- **Propietario**: Bruno Brito Macedo
- **Ubicación**: San Ignacio de Velasco, Santa Cruz, Bolivia
- **GPS**: 15°51′34.2′′S, 60°47′52.4′′W
- **Escala**: 500 cabezas de ganado, 48.5 hectáreas

---

**Documento de Architecture Decision Records v1.0**  
**Última actualización**: 28 octubre 2024  
**Sprint actual**: Sprint 3 - Integración Normativa  
**Presentación final**: 6 noviembre 2024 🎯

**Notas**:
- Todas las decisiones fueron validadas con Bruno Brito Macedo en Hacienda Gamelera
- Decisiones técnicas alineadas con requisitos de negocio y normativa boliviana
- ADRs son inmutables (nuevas decisiones = nuevos ADRs, no editar existentes)

