# 03. Arquitectura de Componentes

## Mapeo de Áreas Funcionales a Componentes

| Área Funcional | Capa Presentation | Capa Domain | Capa Data | Normativa |
|----------------|-------------------|-------------|-----------|-----------|
| 1. Gestión Datos | CameraScreen, FrameEvaluationWidget, BreedSelectorWidget | CaptureFramesUseCase (10-15 FPS, 3-5s), EvaluateQualityUseCase (criterios: nitidez>0.7, brillo 0.4-0.8, silueta>0.8), SelectBestFrameUseCase (score ponderado) | LocalImageDataSource, ImageQualityService, BreedModelRegistry (7 razas) | - |
| 2. Análisis Reportes | ReportScreen, WeightChartWidget, BreedComparisonWidget | GenerateEvolutionChartUseCase, CompareAnimalsUseCase, ExportSENASAGReportUseCase | WeighingRepository, AnalyticsService, SENASAGExportService | SENASAG |
| 3. Monitoreo | AlertScreen, CalendarWidget, ASOCEBUScheduleWidget | CreateAlertUseCase, ScheduleSessionUseCase, GenerateGMAUseCase | AlertRepository, NotificationService, REGENSAService | REGENSA, ASOCEBU |
| 4. Usuario | SearchScreen, ListManagementScreen, BreedFilterWidget | SearchByCriteriaUseCase (7 razas, 4 categorías edad), ManageListsUseCase | AnimalRepository, PreferencesService | - |
| 5. Operación | SyncIndicatorWidget, GranPaititiSyncWidget | SyncDataUseCase, BackupDataUseCase, SyncGranPaititiUseCase | SyncService, ConflictResolver, GranPaititiConnector | REGENSA |

## Diagrama C4 Nivel 3 - Componentes Internos

### Arquitectura Flutter (App Móvil)

#### Capa de Presentación (Presentation Layer)

- **Responsabilidades**:
  - Interfaz de usuario (UI)
  - Gestión de estado de la UI
  - Navegación entre pantallas
  - Validación de entrada de usuario
  - Manejo de eventos de usuario

- **Componentes principales**:
  - **Screens**: Pantallas principales de la aplicación
    - `HomeScreen`: Dashboard principal
    - `AnimalListScreen`: Lista de animales
    - `AnimalDetailScreen`: Detalles de animal
    - `CameraScreen`: **Captura continua de fotogramas**
    - `FrameEvaluationScreen`: **Evaluación en tiempo real**
    - `BreedSelectorScreen`: **Selector de raza (7 razas)**
    - `ReportScreen`: Visualización de reportes
    - `AlertScreen`: Gestión de alertas
    - `SearchScreen`: Búsqueda avanzada
    - `SettingsScreen`: Configuraciones
  - **Widgets**: Componentes reutilizables (Atomic Design)
    - `AnimalCard`: Tarjeta de animal
    - `WeightChart`: Gráfico de peso
    - `CameraButton`: Botón de cámara
    - `FrameQualityIndicator`: **Indicador de calidad de fotograma**
    - `BreedSelector`: **Selector de raza**
    - `AgeCategoryWidget`: **Widget de categoría de edad**
    - `LoadingIndicator`: Indicador de carga
    - `CustomTextField`: Campo de texto personalizado
    - `SyncIndicatorWidget`: **Indicador de sincronización**
    - `GranPaititiSyncWidget`: **Widget de sincronización Gran Paitití**
  - **Providers**: Gestión de estado
    - `AnimalProvider`: Estado de animales
    - `CameraProvider`: **Estado de captura continua**
    - `FrameEvaluationProvider`: **Estado de evaluación de fotogramas**
    - `BreedProvider`: **Estado de razas bovinas**
    - `AuthProvider`: Estado de autenticación
    - `SyncProvider`: **Estado de sincronización offline**

#### Capa de Dominio (Domain Layer)

- **Responsabilidades**:
  - Lógica de negocio
  - Reglas de validación
  - Casos de uso
  - Entidades del dominio
  - Interfaces de repositorios

- **Componentes principales**:
  - **Entities**: Entidades del dominio
    - `Animal`: Entidad animal
    - `Weighing`: Entidad pesaje
    - `User`: Entidad usuario
    - `Image`: Entidad imagen
    - `Meta`: Metadatos del sistema
    - `Alert`: Alertas y recordatorios
    - `Farm`: Finca/hacienda
    - `CaptureSession`: **Sesión de captura continua**
    - `FrameQuality`: **Métricas de calidad de fotograma**
    - `Breed`: **Entidad de raza bovina** (7 razas específicas)
    - `AgeCategory`: **Categoría de edad** (4 categorías específicas)
    - `SENASAGReport`: **Reporte para SENASAG**
    - `GMA`: **Guía de Movimiento Animal (REGENSA)**
    - `ASOCEBURecord`: **Registro para competencias ASOCEBU**
  - **Use Cases Área 1 - Gestión de Datos**:
    - `StartContinuousCaptureUseCase`: **Iniciar captura continua**
    - `EvaluateFrameQualityUseCase`: **Evaluar calidad de fotograma**
    - `SelectBestFrameUseCase`: **Seleccionar mejor fotograma**
    - `ProcessByBreedUseCase`: **Procesar según raza específica**
    - `SaveWeighingLocallyUseCase`: **Guardar pesaje localmente**
  - **Use Cases Área 2 - Análisis**:
    - `GenerateWeightEvolutionChartUseCase`: **Gráfico evolución**
    - `CompareAnimalPerformanceUseCase`: **Comparar animales**
    - `SetWeightGoalsUseCase`: **Establecer metas de peso**
    - `ExportReportUseCase`: **Exportar reportes (PDF/CSV)**
  - **Use Cases Área 3 - Monitoreo**:
    - `CreateCustomAlertUseCase`: **Crear alerta personalizada**
    - `ConfigureAlertThresholdsUseCase`: **Configurar umbrales**
    - `ScheduleMassiveCaptureUseCase`: **Programar sesión masiva**
    - `OptimizeRouteUseCase`: **Optimizar ruta de captura**
  - **Use Cases Área 4 - Usuario**:
    - `SearchAnimalsByCriteriaUseCase`: **Búsqueda avanzada**
    - `CreateCustomListUseCase`: **Crear lista personalizada**
    - `CustomizeUIUseCase`: **Personalizar interfaz (tema, tamaño texto, etc)**
  - **Use Cases Área 5 - Operación**:
    - `SyncDataUseCase`: **Sincronizar datos (ya existe)**
    - `ResolveConflictsUseCase`: **Resolver conflictos offline**
    - `BackupDataAutomaticallyUseCase`: **Respaldo automático**
    - `RestoreFromBackupUseCase`: **Restaurar desde respaldo**
  - **Use Cases Integración Normativa**:
    - `GenerateSENASAGReportUseCase`: **Generar reporte para SENASAG**
    - `ExportToGranPaititiUseCase`: **Exportar a Sistema Gran Paitití**
    - `CreateGMAUseCase`: **Crear Guía de Movimiento Animal**
    - `ValidateREGENSAComplianceUseCase`: **Validar cumplimiento REGENSA (caps 3.10, 7.1)**
    - `ExportASOCEBUDataUseCase`: **Exportar datos para ASOCEBU**
  - **Repositories**: Interfaces de repositorios
    - `AnimalRepository`: Repositorio de animales
    - `WeighingRepository`: Repositorio de pesajes
    - `UserRepository`: Repositorio de usuarios
    - `ImageRepository`: Repositorio de imágenes
    - `CaptureSessionRepository`: **Repositorio de sesiones de captura**
    - `BreedRepository`: **Repositorio de razas bovinas**
    - `SENASAGReportRepository`: **Repositorio de reportes SENASAG**

#### Capa de Datos Flutter (Data Layer)

- **Responsabilidades**:
  - Acceso a datos locales
  - Acceso a datos remotos
  - Caché y persistencia
  - Transformación de datos
  - Gestión de sincronización

- **Componentes principales**:
  - **Data Sources**: Fuentes de datos
    - `LocalAnimalDataSource`: SQLite local
    - `RemoteAnimalDataSource`: API REST
    - `LocalImageDataSource`: Almacenamiento local
    - `RemoteImageDataSource`: S3/API
    - `LocalCaptureSessionDataSource`: **Sesiones de captura locales**
    - `LocalBreedDataSource`: **Datos locales de razas**
  - **Models**: Modelos de datos
    - `AnimalModel`: Modelo de animal
    - `WeighingModel`: Modelo de pesaje
    - `UserModel`: Modelo de usuario
    - `ImageModel`: Modelo de imagen
    - `CaptureSessionModel`: **Modelo de sesión de captura**
    - `BreedModel`: **Modelo de raza bovina**
  - **Repositories Implementation**: Implementaciones
    - `AnimalRepositoryImpl`: Implementación de repositorio
    - `WeighingRepositoryImpl`: Implementación de pesajes
    - `UserRepositoryImpl`: Implementación de usuarios
    - `ImageRepositoryImpl`: Implementación de imágenes

#### Servicios Especializados

- **Frame Evaluation Service**: **Evaluación de fotogramas**
  - `FrameQualityEvaluator`: **Evalúa calidad en tiempo real**
  - `SilhouetteDetector`: **Detecta silueta del animal**
  - `FrameSelector`: **Selecciona mejor fotograma**
- **Breed-Specific Processing Service**: **Procesamiento por raza**
  - `BreedModelSelector`: **Selecciona modelo según raza**
  - `BreedParametersProvider`: **Provee parámetros por raza**
- **Breed Management Service**: **Gestión de razas bovinas**
  - `BreedRegistry`: **Registro de 7 razas soportadas**
  - `BreedModelMapper`: **Mapeo raza → modelo ML**
  - `BreedConfigProvider`: **Configuraciones por raza**
    - Rangos de peso por categoría de edad
    - Tasas de crecimiento promedio
    - Características físicas distintivas
- **Age Category Service**: **Gestión de categorías de edad**
  - `AgeCategoryCalculator`: **Calcula categoría según fecha nacimiento**
  - `AgeRangeValidator`: **Valida peso según edad y raza**
  - Categorías: Terneros (<8m), Vaquillonas/Torillos (6-18m), Vaquillonas/Toretes (19-30m), Vacas/Toros (>30m)
- **Regulatory Compliance Service**: **Cumplimiento normativo**
  - `SENASAGReportGenerator`: **Genera reportes SENASAG**
  - `REGENSAValidator`: **Valida cumplimiento capítulos 3.10 y 7.1**
  - `GMAGenerator`: **Genera Guía de Movimiento Animal**
  - `GranPaititiConnector`: **Conecta con sistema Gran Paitití**
  - `ASOCEBUExporter`: **Exporta datos para competencias**
- **Offline Sync Service**: **Sincronización offline**
  - `ConflictResolver`: **Resuelve conflictos (last-write-wins)**
  - `SyncQueue`: **Cola de operaciones pendientes**
  - `NetworkMonitor`: **Monitorea conectividad**
- **ML Service**: Servicio de machine learning
  - `TFLiteService`: Ejecución de modelos TFLite
  - `ImageProcessingService`: Procesamiento de imágenes
  - `ModelManager`: Gestión de modelos
- **Storage Service**: Servicio de almacenamiento
  - `LocalStorageService`: Almacenamiento local
  - `CloudStorageService`: Almacenamiento en la nube
  - `CacheService`: Gestión de caché

### Arquitectura Backend (FastAPI)

#### Capa de API (API Layer)

- **Responsabilidades**:
  - Endpoints REST
  - Validación de requests
  - Serialización de responses
  - Manejo de errores HTTP
  - Documentación automática

- **Componentes principales**:
  - **Routes**: Rutas de la API
    - `animal_routes.py`: Endpoints de animales
    - `weighing_routes.py`: Endpoints de pesajes
    - `user_routes.py`: Endpoints de usuarios
    - `image_routes.py`: Endpoints de imágenes
    - `report_routes.py`: Endpoints de reportes
    - `capture_session_routes.py`: **Endpoints de sesiones de captura**
    - `sync_routes.py`: **Endpoints de sincronización**
    - `breed_routes.py`: **Endpoints de razas bovinas**
    - `senasag_routes.py`: **Endpoints de reportes SENASAG**
    - `gma_routes.py`: **Endpoints de GMA**
  - **Schemas**: Esquemas de validación
    - `animal_schemas.py`: Esquemas de animal
    - `weighing_schemas.py`: Esquemas de pesaje
    - `user_schemas.py`: Esquemas de usuario
    - `image_schemas.py`: Esquemas de imagen
    - `capture_session_schemas.py`: **Esquemas de sesión de captura**
    - `breed_schemas.py`: **Esquemas de raza bovina**
  - **Dependencies**: Dependencias
    - `auth_deps.py`: Dependencias de autenticación
    - `db_deps.py`: Dependencias de base de datos
    - `validation_deps.py`: Dependencias de validación

#### Capa de Servicios (Service Layer)

- **Responsabilidades**:
  - Lógica de negocio
  - Orquestación de operaciones
  - Validaciones complejas
  - Integración con servicios externos
  - Gestión de transacciones

- **Componentes principales**:
  - **Business Services**: Servicios de negocio
    - `AnimalService`: Lógica de animales
    - `WeighingService`: Lógica de pesajes
    - `UserService`: Lógica de usuarios
    - `ReportService`: Lógica de reportes
    - `CaptureSessionService`: **Lógica de sesiones de captura**
    - `BreedService`: **Lógica de razas bovinas**
  - **Integration Services**: Servicios de integración
    - `MLService`: Integración con ML
    - `StorageService`: Integración con S3
    - `NotificationService`: Servicio de notificaciones
    - `ExportService`: Servicio de exportación
    - `SyncService`: **Servicio de sincronización**
    - `SENASAGService`: **Servicio de integración SENASAG**
    - `REGENSAService`: **Servicio de integración REGENSA**
  - **Utility Services**: Servicios utilitarios
    - `ImageProcessingService`: Procesamiento de imágenes
    - `ValidationService`: Validaciones complejas
    - `CacheService`: Gestión de caché
    - `LoggingService`: Servicio de logging

#### Capa de Datos Backend (Data Layer)

- **Responsabilidades**:
  - Acceso a base de datos
  - Mapeo objeto-relacional
  - Gestión de transacciones
  - Optimización de consultas
  - Migraciones de esquema

- **Componentes principales**:
  - **Models**: Modelos de datos
    - `AnimalModel`: Modelo de animal (MongoDB)
    - `WeighingModel`: Modelo de pesaje
    - `UserModel`: Modelo de usuario
    - `ImageModel`: Modelo de imagen
    - `CaptureSessionModel`: **Modelo de sesión de captura**
    - `BreedModel`: **Modelo de raza bovina**
  - **Repositories**: Repositorios de datos
    - `AnimalRepository`: Repositorio de animales
    - `WeighingRepository`: Repositorio de pesajes
    - `UserRepository`: Repositorio de usuarios
    - `ImageRepository`: Repositorio de imágenes
  - **Database**: Configuración de base de datos
    - `mongodb.py`: Configuración MongoDB
    - `connection.py`: Gestión de conexiones
    - `migrations.py`: Migraciones de esquema

#### Servicios de Infraestructura

- **Authentication Service**: Servicio de autenticación
  - `JWTService`: Gestión de tokens JWT
  - `PasswordService`: Gestión de contraseñas
  - `SessionService`: Gestión de sesiones
- **ML Infrastructure**: Infraestructura de ML
  - `ModelService`: Gestión de modelos
  - `InferenceService`: Servicio de inferencia
  - `TrainingService`: Servicio de entrenamiento
- **ML Infrastructure Services**:
  - **Model Management**:
    - `ModelVersionService`: **Gestión de versiones de modelos**
    - `ModelRegistryService`: **Registro de modelos disponibles**
    - `BreedModelService`: **Modelos específicos por raza**
  - **Model Deployment**:
    - `ModelDeploymentService`: **Despliegue de modelos a S3**
    - `ModelValidationService`: **Validación de modelos**
    - `ManifestGeneratorService`: **Genera manifest.json con versiones**
  - **Training Pipeline** (futuro):
    - `DataCollectionService`: **Recolección de datos de entrenamiento**
    - `ModelTrainingService`: **Entrenamiento de modelos**
    - `ModelEvaluationService`: **Evaluación de precisión**
- **Storage Infrastructure**: Infraestructura de almacenamiento
  - `S3Service`: Integración con S3
  - `FileService`: Gestión de archivos
  - `BackupService`: Servicio de respaldo

### Patrones de Diseño Aplicados

#### Clean Architecture

- **Separación de responsabilidades**: Cada capa tiene responsabilidades específicas
- **Inversión de dependencias**: Las capas internas no dependen de las externas
- **Independencia de frameworks**: La lógica de negocio es independiente del framework
- **Testabilidad**: Cada componente es fácilmente testeable

#### SOLID Principles

- **Single Responsibility**: Cada clase tiene una sola razón para cambiar
- **Open/Closed**: Abierto para extensión, cerrado para modificación
- **Liskov Substitution**: Los objetos derivados deben ser sustituibles por sus bases
- **Interface Segregation**: Interfaces específicas en lugar de generales
- **Dependency Inversion**: Depender de abstracciones, no de concreciones

#### Atomic Design

- **Atoms**: Componentes básicos (botones, inputs, textos)
- **Molecules**: Combinaciones de átomos (formularios, tarjetas)
- **Organisms**: Secciones complejas (headers, sidebars)
- **Templates**: Layouts de página
- **Pages**: Instancias específicas de templates

### Flujos de Comunicación

#### Flutter Internal Flow

```text
UI (Screens/Widgets) → Providers → Use Cases → Repositories → Data Sources
```

#### Backend Internal Flow

```text
Routes → Services → Repositories → Database
```

#### Cross-Container Communication

```text
Flutter (HTTP Client) → Backend (FastAPI) → MongoDB
Flutter (TFLite) → Local Processing → Results
Flutter (S3 Client) → AWS S3 → File Storage
```

### Consideraciones de Rendimiento

#### Flutter

- **Lazy Loading**: Carga diferida de componentes
- **State Management**: Gestión eficiente de estado
- **Image Optimization**: Optimización de imágenes
- **Memory Management**: Gestión de memoria
- **Frame Processing**: **Procesamiento eficiente de fotogramas**

#### Backend

- **Async Processing**: Procesamiento asíncrono
- **Connection Pooling**: Pool de conexiones
- **Caching**: Estrategias de caché
- **Database Optimization**: Optimización de consultas
- **ML Model Serving**: **Servicio eficiente de modelos ML**
