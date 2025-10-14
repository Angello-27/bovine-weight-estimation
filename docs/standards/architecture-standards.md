# Estándares de Arquitectura

## Contexto del Proyecto

**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Ubicación**: San Ignacio de Velasco, Bolivia (15°51′34.2′′S, 60°47′52.4′′W)  
**Escala**: 500 cabezas de ganado bovino, 48.5 hectáreas

## Visión Arquitectónica

### Principios Fundamentales

1. **Offline-First**: Sistema debe funcionar completamente sin conexión a internet
2. **Mobile-First**: Dispositivos móviles (smartphones) son el punto de captura principal
3. **Clean Architecture**: Separación clara de responsabilidades en 3 capas
4. **Domain-Driven Design**: Modelo de dominio refleja exactamente Hacienda Gamelera
5. **SOLID Principles**: Código mantenible, escalable y testeable

### Datos Críticos del Dominio (INVARIANTES)

#### 7 Razas Bovinas (EXACTAS - NO MODIFICAR)
1. Brahman (Bos indicus)
2. Nelore (Bos indicus)
3. Angus (Bos taurus)
4. Cebuinas (Bos indicus)
5. Criollo (Bos taurus)
6. Pardo Suizo (Bos taurus)
7. Jersey (Bos taurus)

#### 4 Categorías de Edad (EXACTAS - NO MODIFICAR)
1. Terneros (<8 meses)
2. Vaquillonas/Torillos (6-18 meses)
3. Vaquillonas/Toretes (19-30 meses)
4. Vacas/Toros (>30 meses)

#### Métricas del Sistema (OBLIGATORIAS)
- **Precisión ML**: ≥95% (R² ≥ 0.95)
- **Error absoluto**: <5 kg
- **Tiempo procesamiento**: <3 segundos
- **Captura continua**: 10-15 FPS durante 3-5 segundos (30-75 fotogramas)

#### Entidades Regulatorias Bolivianas
- **SENASAG**: Trazabilidad ganadera (reportes automáticos PDF/CSV/XML)
- **REGENSA**: Capítulos 3.10 y 7.1, sistema Gran Paitití, GMA (Guía Movimiento Animal)
- **ASOCEBU**: Competencias ganaderas (exportación datos, 3ª Faena Técnica 2024)

---

## Arquitectura del Sistema

### Diagrama C4 - Nivel 1: Contexto

```
┌─────────────────────────────────────────────────────────────────┐
│                     ENTORNO EXTERNO                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Bruno Brito Macedo]                                           │
│  Ganadero - Hacienda Gamelera                                   │
│         │                                                        │
│         │ Captura fotogramas,                                   │
│         │ consulta peso estimado                                │
│         ↓                                                        │
│  ┌──────────────────────────────────────┐                      │
│  │                                       │                      │
│  │  Sistema Estimación Peso Bovino IA   │                      │
│  │                                       │                      │
│  │  - Captura continua (10-15 FPS)      │                      │
│  │  - Estimación IA por raza (>95%)     │                      │
│  │  - Gestión 500 cabezas offline       │                      │
│  │  - Reportes normativos automáticos   │                      │
│  │                                       │                      │
│  └──────────────────────────────────────┘                      │
│         │                                                        │
│         │ Reportes, certificados,                               │
│         │ trazabilidad                                          │
│         ↓                                                        │
│  [SENASAG] [REGENSA/Gran Paitití] [ASOCEBU]                    │
│  Entidades Regulatorias Bolivianas                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Diagrama C4 - Nivel 2: Contenedores

```
┌────────────────────────────────────────────────────────────────────┐
│                   Sistema Estimación Peso Bovino IA                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────┐         ┌──────────────────────────┐ │
│  │                          │         │                           │ │
│  │   Mobile App (Flutter)   │◄────────┤   Backend API (FastAPI)  │ │
│  │                          │  HTTPS  │                           │ │
│  │  - Captura cámara       │  JSON   │  - Business logic        │ │
│  │  - TensorFlow Lite      │         │  - Reportes SENASAG      │ │
│  │  - SQLite (offline)     │         │  - Integración Gran P.   │ │
│  │  - Sincronización       │         │  - Exportación ASOCEBU   │ │
│  │                          │         │                           │ │
│  └─────────────────────────┘         └──────────────────────────┘ │
│           │                                     │                  │
│           │ Lee modelos ML                      │ CRUD             │
│           ↓                                     ↓                  │
│  ┌─────────────────────────┐         ┌──────────────────────────┐ │
│  │                          │         │                           │ │
│  │  ML Models (TFLite)     │         │   Database (MongoDB)      │ │
│  │                          │         │                           │ │
│  │  - brahman-v1.0.0       │         │  - animals                │ │
│  │  - nelore-v1.0.0        │         │  - weighings              │ │
│  │  - angus-v1.0.0         │         │  - senasag_reports        │ │
│  │  - cebuinas-v1.0.0      │         │  - gmas                   │ │
│  │  - criollo-v1.0.0       │         │  - asocebu_data           │ │
│  │  - pardo-suizo-v1.0.0   │         │                           │ │
│  │  - jersey-v1.0.0        │         │                           │ │
│  │  - manifest.json        │         │                           │ │
│  │                          │         │                           │ │
│  └─────────────────────────┘         └──────────────────────────┘ │
│           │                                                        │
│           │ Almacenados en                                        │
│           ↓                                                        │
│  ┌─────────────────────────┐                                     │
│  │                          │                                     │
│  │  Cloud Storage (AWS S3)  │                                     │
│  │                          │                                     │
│  │  - Modelos ML versionados│                                     │
│  │  - Imágenes entrenamiento│                                     │
│  │  - Backups BD            │                                     │
│  │                          │                                     │
│  └─────────────────────────┘                                     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## Clean Architecture - 3 Capas

### Estructura General

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                     │
│  (UI, Widgets, Screens, Controllers, Providers)         │
│                                                          │
│  Responsabilidad: Interacción con usuario               │
│  Depende de: Domain Layer                               │
│  Framework: Flutter (Mobile), FastAPI (Backend)         │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓ Usa casos de uso
┌─────────────────────────────────────────────────────────┐
│                     DOMAIN LAYER                         │
│  (Entities, Use Cases, Repository Interfaces)           │
│                                                          │
│  Responsabilidad: Lógica de negocio pura                │
│  Depende de: Nada (capa más interna)                    │
│  Lenguaje: Dart (Mobile), Python (Backend)              │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓ Implementa interfaces
┌─────────────────────────────────────────────────────────┐
│                      DATA LAYER                          │
│  (Repository Impl, Data Sources, Models, APIs)          │
│                                                          │
│  Responsabilidad: Acceso a datos (BD, API, Cache)       │
│  Depende de: Domain Layer (interfaces)                  │
│  Tecnologías: SQLite, MongoDB, HTTP, TFLite             │
└─────────────────────────────────────────────────────────┘
```

### Reglas de Dependencia

1. **Presentation** → depende de → **Domain** (usa casos de uso)
2. **Domain** → NO depende de nadie (capa pura)
3. **Data** → depende de → **Domain** (implementa interfaces)
4. **NUNCA**: Domain depende de Presentation o Data
5. **NUNCA**: Data depende de Presentation

---

## Estructura de Carpetas

### Mobile (Flutter)

```
mobile/
├── lib/
│   ├── core/                              # Código compartido
│   │   ├── constants/                     # Constantes del dominio
│   │   │   ├── breeds.dart                # 7 razas EXACTAS
│   │   │   ├── age_categories.dart        # 4 categorías EXACTAS
│   │   │   ├── capture_constants.dart     # 10-15 FPS, 3-5s
│   │   │   ├── metrics.dart               # ≥95%, <5kg, <3s
│   │   │   └── hacienda_constants.dart    # GPS, Schaeffer
│   │   │
│   │   ├── errors/                        # Excepciones custom
│   │   │   ├── failures.dart
│   │   │   └── exceptions.dart
│   │   │
│   │   ├── utils/                         # Utilidades
│   │   │   ├── either.dart                # Either<Failure, Success>
│   │   │   ├── validators.dart
│   │   │   └── formatters.dart
│   │   │
│   │   └── ui/                            # Atomic Design
│   │       ├── atoms/                     # Componentes básicos
│   │       ├── molecules/                 # Combinación de atoms
│   │       └── organisms/                 # Componentes complejos
│   │
│   ├── features/                          # Features por área funcional
│   │   │
│   │   ├── data_management/               # Área 1: Captura y estimación
│   │   │   ├── presentation/
│   │   │   │   ├── screens/
│   │   │   │   │   ├── camera_screen.dart
│   │   │   │   │   └── estimation_screen.dart
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── breed_selector_widget.dart
│   │   │   │   │   ├── camera_preview_widget.dart
│   │   │   │   │   └── capture_progress_widget.dart
│   │   │   │   └── providers/
│   │   │   │       ├── camera_provider.dart
│   │   │   │       └── estimation_provider.dart
│   │   │   │
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   │   ├── animal.dart
│   │   │   │   │   ├── capture_session.dart
│   │   │   │   │   └── weighing.dart
│   │   │   │   ├── repositories/
│   │   │   │   │   ├── animal_repository.dart
│   │   │   │   │   └── weighing_repository.dart
│   │   │   │   └── usecases/
│   │   │   │       ├── start_continuous_capture_usecase.dart
│   │   │   │       ├── estimate_weight_usecase.dart
│   │   │   │       └── register_animal_usecase.dart
│   │   │   │
│   │   │   └── data/
│   │   │       ├── models/
│   │   │       │   ├── animal_model.dart
│   │   │       │   ├── capture_session_model.dart
│   │   │       │   └── weighing_model.dart
│   │   │       ├── repositories/
│   │   │       │   ├── animal_repository_impl.dart
│   │   │       │   └── weighing_repository_impl.dart
│   │   │       └── datasources/
│   │   │           ├── animal_local_datasource.dart
│   │   │           ├── animal_remote_datasource.dart
│   │   │           └── ml_inference_datasource.dart
│   │   │
│   │   ├── analytics_reports/             # Área 2: Análisis y reportes
│   │   │   ├── presentation/
│   │   │   ├── domain/
│   │   │   └── data/
│   │   │
│   │   ├── monitoring/                    # Área 3: Monitoreo SENASAG/REGENSA
│   │   │   ├── presentation/
│   │   │   ├── domain/
│   │   │   └── data/
│   │   │
│   │   ├── user_features/                 # Área 4: Búsqueda y filtros
│   │   │   ├── presentation/
│   │   │   ├── domain/
│   │   │   └── data/
│   │   │
│   │   └── operations/                    # Área 5: Sincronización offline
│   │       ├── presentation/
│   │       ├── domain/
│   │       └── data/
│   │
│   └── main.dart                          # Entry point
│
├── test/                                  # Tests unitarios
│   ├── core/
│   └── features/
│
├── integration_test/                      # Tests de integración
│
├── assets/                                # Assets estáticos
│   ├── models/                            # Modelos TFLite
│   │   ├── brahman-v1.0.0.tflite
│   │   ├── nelore-v1.0.0.tflite
│   │   ├── angus-v1.0.0.tflite
│   │   ├── cebuinas-v1.0.0.tflite
│   │   ├── criollo-v1.0.0.tflite
│   │   ├── pardo-suizo-v1.0.0.tflite
│   │   ├── jersey-v1.0.0.tflite
│   │   └── manifest.json
│   ├── images/
│   └── icons/
│
├── pubspec.yaml                           # Dependencies
└── README.md
```

### Backend (Python/FastAPI)

```
backend/
├── app/
│   ├── core/                              # Código compartido
│   │   ├── config.py                      # Configuración (env vars)
│   │   ├── security.py                    # JWT, auth
│   │   ├── exceptions.py                  # Excepciones custom
│   │   │
│   │   └── constants/                     # Constantes del dominio
│   │       ├── __init__.py
│   │       ├── breeds.py                  # 7 razas EXACTAS
│   │       ├── age_categories.py          # 4 categorías EXACTAS
│   │       ├── capture_constants.py       # 10-15 FPS, 3-5s
│   │       ├── metrics.py                 # ≥95%, <5kg, <3s
│   │       ├── hacienda_constants.py      # GPS, Schaeffer
│   │       └── regulatory.py              # SENASAG/REGENSA/ASOCEBU
│   │
│   ├── domain/                            # Domain Layer
│   │   ├── entities/                      # Entidades puras
│   │   │   ├── animal.py
│   │   │   ├── weighing.py
│   │   │   ├── senasag_report.py
│   │   │   ├── gma.py
│   │   │   └── asocebu_data.py
│   │   │
│   │   ├── enums.py                       # BreedType, AgeCategory
│   │   │
│   │   └── value_objects/                 # Value objects
│   │       ├── breed_weight_ranges.py
│   │       └── hacienda_location.py
│   │
│   ├── api/                               # Presentation Layer (FastAPI)
│   │   ├── routes/                        # Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── animals.py                 # CRUD animales
│   │   │   ├── weighings.py               # CRUD pesajes
│   │   │   ├── senasag.py                 # US-007: Reportes SENASAG
│   │   │   ├── regensa.py                 # US-008: GMA
│   │   │   ├── gran_paititi.py            # US-008: API Gran Paitití
│   │   │   └── asocebu.py                 # US-009: Exportación ASOCEBU
│   │   │
│   │   ├── schemas/                       # Pydantic schemas
│   │   │   ├── animal_schemas.py
│   │   │   ├── weighing_schemas.py
│   │   │   ├── senasag_schemas.py
│   │   │   ├── gma_schemas.py
│   │   │   └── asocebu_schemas.py
│   │   │
│   │   └── dependencies.py                # FastAPI dependencies
│   │
│   ├── services/                          # Business Logic Layer
│   │   ├── animal_service.py
│   │   ├── weighing_service.py
│   │   ├── senasag_service.py             # Generación reportes PDF/CSV/XML
│   │   ├── gma_service.py                 # Generación GMA con QR
│   │   ├── gran_paititi_service.py        # Integración API gubernamental
│   │   └── asocebu_service.py             # Certificaciones competencias
│   │
│   ├── repositories/                      # Data Layer (MongoDB)
│   │   ├── animal_repository.py
│   │   ├── weighing_repository.py
│   │   ├── senasag_repository.py
│   │   ├── gma_repository.py
│   │   └── asocebu_repository.py
│   │
│   ├── clients/                           # HTTP clients externos
│   │   └── gran_paititi_client.py         # Cliente API Gran Paitití
│   │
│   ├── database/                          # Database setup
│   │   ├── mongodb.py                     # Conexión MongoDB
│   │   └── seed_data.py                   # Seed 7 razas, Bruno, etc.
│   │
│   ├── ml/                                # Machine Learning
│   │   ├── model_loader.py                # Carga modelos TFLite
│   │   ├── inference.py                   # Inferencia
│   │   └── preprocessing.py               # Preprocesamiento imágenes
│   │
│   └── main.py                            # FastAPI app entry point
│
├── tests/                                 # Tests
│   ├── unit/
│   │   ├── services/
│   │   └── repositories/
│   ├── integration/
│   │   └── api/
│   └── conftest.py
│
├── alembic/                               # Migraciones (si se usa SQL)
│
├── requirements.txt                       # Dependencies
├── requirements-dev.txt                   # Dev dependencies
├── .env.example                           # Environment variables template
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### ML Training (Python/TensorFlow)

```
ml-training/
├── data/                                  # Datasets
│   ├── raw/                               # Imágenes originales
│   │   ├── brahman/
│   │   ├── nelore/
│   │   ├── angus/
│   │   ├── cebuinas/
│   │   ├── criollo/
│   │   ├── pardo-suizo/
│   │   └── jersey/
│   │
│   ├── processed/                         # Imágenes preprocesadas
│   │   └── [misma estructura]
│   │
│   └── annotations.csv                    # Labels con peso real
│
├── notebooks/                             # Jupyter notebooks
│   ├── 01-exploratory-data-analysis.ipynb
│   ├── 02-preprocessing.ipynb
│   ├── 03-model-training.ipynb
│   └── 04-model-evaluation.ipynb
│
├── src/                                   # Código fuente
│   ├── data/
│   │   ├── dataset_builder.py             # Construcción dataset
│   │   ├── augmentation.py                # Data augmentation
│   │   └── validation.py                  # Validación datos
│   │
│   ├── models/
│   │   ├── cnn_architecture.py            # Arquitectura CNN custom
│   │   ├── transfer_learning.py           # MobileNetV2/EfficientNet
│   │   └── model_builder.py
│   │
│   ├── training/
│   │   ├── trainer.py                     # Training loop
│   │   ├── callbacks.py                   # Callbacks custom
│   │   └── hyperparameters.py             # Hiperparámetros
│   │
│   ├── evaluation/
│   │   ├── metrics.py                     # R², MAE, MAPE
│   │   └── visualizations.py              # Gráficos
│   │
│   └── export/
│       ├── tflite_converter.py            # TF → TFLite
│       └── manifest_generator.py          # manifest.json
│
├── experiments/                           # MLflow experiments
│   └── mlruns/
│
├── models/                                # Modelos entrenados
│   ├── brahman/
│   │   ├── v1.0.0/
│   │   │   ├── saved_model/
│   │   │   ├── brahman-v1.0.0.tflite
│   │   │   └── metrics.json
│   │   └── v1.1.0/
│   ├── nelore/
│   └── [resto de razas...]
│
├── requirements.txt
└── README.md
```

---

## Patrones de Diseño Aplicados

### 1. Repository Pattern (Data Layer)

**Problema**: Abstraer acceso a datos (BD, API, cache)  
**Solución**: Interfaces en Domain, implementaciones en Data

```dart
// Domain Layer - Interface
abstract class AnimalRepository {
  Future<Either<Failure, Animal>> getAnimalById(String id);
  Future<Either<Failure, List<Animal>>> getAnimalsByBreed(BreedType breed);
  Future<Either<Failure, void>> saveAnimal(Animal animal);
}

// Data Layer - Implementación
class AnimalRepositoryImpl implements AnimalRepository {
  final AnimalLocalDataSource localDataSource;
  final AnimalRemoteDataSource remoteDataSource;
  
  // Offline-first: primero local, luego sincronizar
  @override
  Future<Either<Failure, Animal>> getAnimalById(String id) async {
    try {
      // 1. Intentar local (SQLite)
      final localAnimal = await localDataSource.getAnimalById(id);
      return Right(localAnimal);
    } catch (e) {
      // 2. Si falla, intentar remoto
      try {
        final remoteAnimal = await remoteDataSource.getAnimalById(id);
        // Guardar en local para próxima vez
        await localDataSource.saveAnimal(remoteAnimal);
        return Right(remoteAnimal);
      } catch (e) {
        return Left(NetworkFailure());
      }
    }
  }
}
```

### 2. Use Case Pattern (Domain Layer)

**Problema**: Encapsular lógica de negocio compleja  
**Solución**: Un caso de uso = una acción del usuario

```dart
// Domain Layer
class EstimateWeightUseCase {
  final WeighingRepository weighingRepository;
  final MLInferenceDataSource mlDataSource;
  
  Future<Either<Failure, Weighing>> call({
    required String animalId,
    required BreedType breedType,
    required File imageFile,
  }) async {
    // 1. Validar raza es una de las 7
    if (!BreedType.values.contains(breedType)) {
      return Left(InvalidBreedFailure());
    }
    
    // 2. Preprocesar imagen
    final preprocessedImage = await _preprocessImage(imageFile);
    
    // 3. Ejecutar inferencia con modelo específico de raza
    final estimationResult = await mlDataSource.estimateWeight(
      image: preprocessedImage,
      breedType: breedType,
    );
    
    // 4. Validar métricas del sistema
    if (estimationResult.confidence < SystemMetrics.minPrecision) {
      return Left(PrecisionBelowThresholdFailure(estimationResult.confidence));
    }
    
    // 5. Validar rango de peso según raza y edad
    if (!BreedWeightRanges.isValidWeight(
      weight: estimationResult.weightKg,
      breedType: breedType,
      ageCategory: animal.ageCategory,
    )) {
      return Left(WeightOutOfRangeFailure());
    }
    
    // 6. Crear entidad Weighing
    final weighing = Weighing(
      id: generateUuid(),
      animalId: animalId,
      estimatedWeight: estimationResult.weightKg,
      confidence: estimationResult.confidence,
      method: WeighingMethod.ia,
      timestamp: DateTime.now(),
    );
    
    // 7. Guardar en repositorio (offline-first)
    await weighingRepository.saveWeighing(weighing);
    
    return Right(weighing);
  }
}
```

### 3. Provider Pattern (Presentation Layer - Flutter)

**Problema**: Gestión de estado reactiva  
**Solución**: Provider + ChangeNotifier

```dart
// Presentation Layer
class CameraProvider extends ChangeNotifier {
  final StartContinuousCaptureUseCase startCaptureUseCase;
  final EstimateWeightUseCase estimateWeightUseCase;
  
  CameraState _state = CameraState.initial();
  CameraState get state => _state;
  
  // Captura continua: 10-15 FPS durante 3-5 segundos
  Future<void> startContinuousCapture({
    required String animalId,
    required BreedType breedType,
  }) async {
    _state = CameraState.capturing();
    notifyListeners();
    
    final result = await startCaptureUseCase(
      animalId: animalId,
      breedType: breedType,
    );
    
    result.fold(
      (failure) {
        _state = CameraState.error(failure.message);
        notifyListeners();
      },
      (captureSession) {
        _state = CameraState.captured(captureSession);
        notifyListeners();
        
        // Automáticamente estimar peso con mejor fotograma
        _estimateWeight(captureSession.bestFrame);
      },
    );
  }
}
```

### 4. Factory Pattern (ML Models)

**Problema**: Cargar modelo TFLite correcto según raza  
**Solución**: Factory que selecciona modelo

```python
# ML Layer - Backend
class MLModelFactory:
    """Factory para cargar modelo TFLite específico por raza."""
    
    _models: Dict[BreedType, Interpreter] = {}
    
    @classmethod
    def get_model(cls, breed_type: BreedType) -> Interpreter:
        """
        Retorna modelo TFLite cargado para la raza especificada.
        
        Modelos disponibles (7 razas exactas de Hacienda Gamelera):
        - brahman-v1.0.0.tflite
        - nelore-v1.0.0.tflite
        - angus-v1.0.0.tflite
        - cebuinas-v1.0.0.tflite
        - criollo-v1.0.0.tflite
        - pardo-suizo-v1.0.0.tflite
        - jersey-v1.0.0.tflite
        """
        # Validar raza
        if not BreedType.is_valid(breed_type.value):
            raise InvalidBreedException(breed_type)
        
        # Cargar modelo si no está en caché
        if breed_type not in cls._models:
            model_path = f"models/{breed_type.value}-v1.0.0.tflite"
            cls._models[breed_type] = tf.lite.Interpreter(model_path=model_path)
            cls._models[breed_type].allocate_tensors()
        
        return cls._models[breed_type]
```

### 5. Strategy Pattern (Reportes Normativos)

**Problema**: Diferentes formatos de exportación (PDF, CSV, XML)  
**Solución**: Strategy por formato

```python
# Services Layer - Backend
class ReportExportStrategy(ABC):
    @abstractmethod
    def export(self, report_data: SENASAGReportData) -> bytes:
        pass

class PDFExportStrategy(ReportExportStrategy):
    def export(self, report_data: SENASAGReportData) -> bytes:
        # Generar PDF con logo SENASAG
        pdf = FPDF()
        pdf.add_page()
        pdf.image('assets/senasag-logo.png', x=10, y=8, w=33)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Reporte de Trazabilidad - Hacienda Gamelera', ln=True)
        # ... resto de PDF
        return pdf.output(dest='S').encode('latin1')

class CSVExportStrategy(ReportExportStrategy):
    def export(self, report_data: SENASAGReportData) -> bytes:
        # Generar CSV estructura estándar SENASAG
        csv_data = StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['animal_id', 'caravana', 'raza', 'edad', 'peso_actual', ...])
        for animal in report_data.animals:
            writer.writerow([animal.id, animal.tag_number, animal.breed_type.value, ...])
        return csv_data.getvalue().encode('utf-8')

class SENASAGReportService:
    def generate_report(
        self, 
        report_data: SENASAGReportData, 
        format: ReportFormat
    ) -> bytes:
        # Seleccionar estrategia según formato
        strategy = {
            ReportFormat.PDF: PDFExportStrategy(),
            ReportFormat.CSV: CSVExportStrategy(),
            ReportFormat.XML: XMLExportStrategy(),
        }[format]
        
        return strategy.export(report_data)
```

---

## Requisitos No Funcionales

### Performance

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Tiempo estimación peso** | <3 segundos | Desde fotograma hasta resultado |
| **Tiempo captura continua** | 3-5 segundos | 30-75 fotogramas a 10-15 FPS |
| **Tiempo búsqueda** | <3 segundos | 500 animales con filtros |
| **Tiempo sincronización** | <30 segundos | 50 registros con conexión 3G |
| **Tamaño app móvil** | <100 MB | Con 7 modelos TFLite |
| **Consumo RAM app** | <200 MB | Durante inferencia ML |
| **Uso batería** | <5%/hora | Uso normal sin captura |

### Disponibilidad

- **Offline-first**: 100% funcional sin internet
- **Uptime backend**: >99.5%
- **Sincronización**: Automática al recuperar conexión
- **Recuperación ante fallos**: <5 minutos

### Escalabilidad

- **Animales soportados**: 500+ (Hacienda Gamelera)
- **Usuarios concurrentes**: 10+ (personal de hacienda)
- **Pesajes/día**: 100+ registros
- **Crecimiento futuro**: Preparado para 5,000+ animales (múltiples haciendas)

### Seguridad

- **Autenticación**: JWT con refresh tokens
- **Autorización**: RBAC (Admin, Ganadero, Operador)
- **Encriptación en tránsito**: HTTPS/TLS 1.3
- **Encriptación en reposo**: AES-256 (datos sensibles)
- **Backup automático**: Diario incremental

### Usabilidad

- **Interfaz**: Simple para personal rural sin entrenamiento
- **Idioma**: Español (Bolivia)
- **Accesibilidad**: Botones grandes, alto contraste
- **Feedback visual**: Claro en cada acción
- **Manejo de errores**: Mensajes en español comprensibles

---

## Cumplimiento Normativo Boliviano

### SENASAG (Trazabilidad Ganadera)

**Reportes obligatorios**:
- Inventario mensual/trimestral
- Altas (nacimientos/compras)
- Bajas (ventas/muertes)
- Movimientos entre potreros
- Pesajes con fecha, hora, método

**Formatos**:
- PDF profesional con logo SENASAG
- CSV estructura estándar
- XML compatible con sistemas SENASAG

### REGENSA (Capítulos 3.10 y 7.1)

**Capítulo 3.10 - Centros de concentración animal**:
- Registro de infraestructura (rampas, corrales)
- Superficie mínima: ≥2m² por animal
- Sistemas de desinfección

**Capítulo 7.1 - Requisitos sanitarios**:
- GMA (Guía de Movimiento Animal) digital
- Registro pesajes con GPS y timestamp UTC
- Control veterinario

**Gran Paitití**:
- API REST integración
- Sincronización bidireccional
- Código QR en GMA para verificación

### ASOCEBU (Competencias Ganaderas)

**Exportación datos**:
- Historial de crecimiento (6 meses mínimo)
- GDP (Ganancia Diaria Promedio)
- Certificación de peso con proyecciones
- Datos 3ª Faena Técnica 2024 (medalla bronce)

---

## Versionado y Releases

### Versionado Semántico (SemVer)

Formato: `MAJOR.MINOR.PATCH` (ej: `v1.2.3`)

- **MAJOR**: Cambios incompatibles en API/arquitectura
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Correcciones de bugs

**Ejemplos**:
- `v1.0.0`: Release inicial (Sprint 1 + 2 + 3)
- `v1.1.0`: Agregar nueva raza bovina
- `v1.1.1`: Corregir bug en cálculo GDP

### Modelos ML Versionados

Formato: `{raza}-v{version}.tflite` (ej: `brahman-v1.0.0.tflite`)

- **v1.0.0**: Modelo inicial entrenado
- **v1.1.0**: Reentrenamiento con más datos
- **v2.0.0**: Cambio de arquitectura CNN

---

## Monitoreo y Observabilidad

### Logs

**Niveles**:
- **ERROR**: Errores críticos (precisión <95%, crashes)
- **WARN**: Advertencias (batería baja, sin conexión)
- **INFO**: Eventos importantes (pesaje exitoso, sincronización)
- **DEBUG**: Debugging (parámetros ML, queries BD)

**Formato estructurado (JSON)**:
```json
{
  "timestamp": "2024-10-28T10:30:45.123Z",
  "level": "INFO",
  "service": "mobile-app",
  "message": "Peso estimado exitosamente",
  "context": {
    "animal_id": "uuid-123",
    "breed_type": "brahman",
    "estimated_weight_kg": 487.3,
    "confidence": 0.97,
    "processing_time_ms": 2543
  }
}
```

### Métricas

**Mobile**:
- Tiempo de respuesta por operación
- Tasa de éxito de estimaciones (confidence >95%)
- Uso de memoria/batería
- Crashes y errores

**Backend**:
- Latencia de APIs (p50, p95, p99)
- Throughput (requests/segundo)
- Tasa de error 4xx/5xx
- Conexiones BD activas

**ML**:
- Precisión por raza (R² por modelo)
- Error absoluto promedio (MAE por raza)
- Tiempo de inferencia (ms)
- Uso GPU/CPU

### Alertas

**Críticas** (notificación inmediata):
- Precisión ML <90% (threshold alert)
- Backend down >5 minutos
- Base de datos inaccesible

**Importantes** (notificación en 15 minutos):
- Precisión ML 90-95%
- Latencia API >5 segundos
- Disco >80% lleno

**Informativas** (revisión diaria):
- Sincronizaciones fallidas >5 en 1 hora
- Batería baja en dispositivos

---

## Documentación del Código

### Comentarios

**Regla general**: Código autodocumentado > Comentarios

**Cuándo comentar**:
1. **Lógica compleja**: Algoritmos no obvios
2. **Decisiones de negocio**: Por qué se hizo así (referencia a Hacienda Gamelera)
3. **Hacks temporales**: TODO/FIXME con contexto
4. **Constantes del dominio**: Las 7 razas, 4 categorías, métricas

**Ejemplo comentarios buenos**:
```dart
// Constantes de Hacienda Gamelera - San Ignacio de Velasco, Bolivia
class HaciendaConstants {
  // GPS de Hacienda Gamelera (Bruno Brito Macedo)
  static const double latitude = -15.859500;   // 15°51′34.2′′S
  static const double longitude = -60.797889;  // 60°47′52.4′′W
  
  // Fórmula Schaeffer para comparación con método tradicional
  // Peso (kg) = (PT² × LC) / 10838
  // PT: Perímetro Torácico (cm), LC: Longitud Cuerpo (cm)
  // Error actual: 5-20 kg por animal
  static double schaefferFormula({
    required double perimeterThoracicCm,
    required double bodyLengthCm,
  }) {
    return (perimeterThoracicCm * perimeterThoracicCm * bodyLengthCm) / 10838;
  }
}
```

**Ejemplo comentarios malos**:
```dart
// ❌ Evitar comentarios obvios
// Incrementar contador
counter++;  // Malo: obvio del código

// ❌ Evitar comentarios desactualizados
// Retorna lista de 5 razas  ← ¡SON 7 RAZAS!
List<BreedType> getBreeds() { ... }

// ❌ Evitar comentarios que deberían ser código
// Si el animal es brahman o nelore, aplicar factor de corrección
if (breed == BreedType.brahman || breed == BreedType.nelore) {
  // Mejor: método isBosTaurus() / isBosIndicus()
}
```

### Docstrings

**Python (Google Style)**:
```python
def estimate_weight(
    image: np.ndarray,
    breed_type: BreedType,
    age_category: AgeCategory,
) -> WeightEstimationResult:
    """
    Estima el peso de un bovino mediante modelo de IA específico por raza.
    
    Este método implementa la inferencia del modelo TensorFlow Lite entrenado
    para la raza específica, garantizando precisión >95% según los requisitos
    de Hacienda Gamelera (Bruno Brito Macedo).
    
    Args:
        image: Imagen preprocesada del bovino (224x224x3, normalizada 0-1)
        breed_type: Una de las 7 razas exactas de Hacienda Gamelera
            (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)
        age_category: Categoría de edad para validar rango de peso
            (Terneros, Vaquillonas/Torillos, Vaquillonas/Toretes, Vacas/Toros)
    
    Returns:
        WeightEstimationResult con:
            - weight_kg: Peso estimado en kilogramos
            - confidence: Nivel de confianza (0.0-1.0), debe ser ≥0.95
            - processing_time_ms: Tiempo de procesamiento, debe ser <3000ms
            - breed_model_version: Versión del modelo usado (ej: v1.0.0)
    
    Raises:
        InvalidBreedException: Si breed_type no es una de las 7 razas exactas
        PrecisionBelowThresholdException: Si confidence <0.95
        WeightOutOfRangeException: Si peso no está en rango válido para raza/edad
        ProcessingTimeTooSlowException: Si procesamiento >3000ms
    
    Example:
        >>> image = preprocess_image(raw_image)
        >>> result = estimate_weight(
        ...     image=image,
        ...     breed_type=BreedType.BRAHMAN,
        ...     age_category=AgeCategory.VACAS_TOROS
        ... )
        >>> print(f"Peso: {result.weight_kg} kg (confianza: {result.confidence:.2%})")
        Peso: 487.3 kg (confianza: 97.00%)
    
    Note:
        - Tiempo objetivo: <3 segundos (US-002)
        - Precisión objetivo: ≥95% (R² ≥0.95)
        - Error absoluto objetivo: <5 kg
        - Modelos ubicados en: models/{breed}-v{version}.tflite
    """
    # Implementación...
```

**Dart (DartDoc)**:
```dart
/// Estima el peso de un bovino mediante modelo de IA específico por raza.
///
/// Este método implementa la inferencia del modelo TensorFlow Lite entrenado
/// para la raza específica, garantizando precisión >95% según los requisitos
/// de Hacienda Gamelera (Bruno Brito Macedo).
///
/// **Parámetros**:
/// - [imageFile]: Archivo de imagen del bovino capturada con cámara
/// - [breedType]: Una de las 7 razas exactas de Hacienda Gamelera
/// - [ageCategory]: Categoría de edad para validar rango de peso
///
/// **Retorna**: [Either<Failure, WeightEstimationResult>]
/// - [Left(Failure)]: Si hay error (raza inválida, precisión baja, etc.)
/// - [Right(Result)]: Si estimación exitosa con confidence ≥95%
///
/// **Lanza**:
/// - [InvalidBreedException]: Si [breedType] no es una de las 7 razas exactas
/// - [PrecisionBelowThresholdException]: Si confidence <0.95
/// - [WeightOutOfRangeException]: Si peso no está en rango válido para raza/edad
///
/// **Ejemplo**:
/// ```dart
/// final result = await estimateWeight(
///   imageFile: capturedImage,
///   breedType: BreedType.brahman,
///   ageCategory: AgeCategory.vacasToros,
/// );
/// 
/// result.fold(
///   (failure) => print('Error: ${failure.message}'),
///   (estimation) => print('Peso: ${estimation.weightKg} kg'),
/// );
/// ```
///
/// **US relacionada**: US-002 (Estimación de Peso por Raza)
/// 
/// **Métricas objetivo**:
/// - Tiempo: <3 segundos
/// - Precisión: ≥95% (R² ≥0.95)
/// - Error: <5 kg
Future<Either<Failure, WeightEstimationResult>> estimateWeight({
  required File imageFile,
  required BreedType breedType,
  required AgeCategory ageCategory,
}) async {
  // Implementación...
}
```

---

## Referencias

- **Product Backlog**: `docs/product/product-backlog.md`
- **Sprint Goals**: `docs/sprints/sprint-{1,2,3}-goal.md`
- **Definition of Done**: `docs/product/definition-of-done.md`
- **Modelo de Dominio**: `docs/vision/04-domain-model.md`
- **Áreas Funcionales**: `docs/vision/03-areas-funcionales.md`

---

**Documento de Estándares de Arquitectura v1.0**  
**Fecha**: 28 octubre 2024  
**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Product Owner**: Miguel Angel Escobar Lazcano  
**Scrum Master**: Rodrigo Escobar Morón

