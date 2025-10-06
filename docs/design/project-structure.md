# Estructura del Proyecto

Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera

## 1. MOBILE (Flutter) 📱

### 1.1 Arquitectura Clean Architecture

La aplicación móvil sigue **Clean Architecture** con separación clara de responsabilidades en 3 capas:

- **Presentation Layer**: UI, Widgets, Providers (gestión de estado)
- **Domain Layer**: Entities, Use Cases, Repository Interfaces (lógica de negocio)
- **Data Layer**: Models, Data Sources, Repository Implementations (acceso a datos)

### 1.2 Organización por Features

Cada feature se organiza según las **5 áreas funcionales** del sistema:

```
lib/
├── features/
│   ├── data_management/           # Área 1: Gestión de Datos
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   │   ├── camera_screen.dart
│   │   │   │   ├── frame_evaluation_screen.dart
│   │   │   │   └── breed_selection_screen.dart
│   │   │   ├── widgets/
│   │   │   │   ├── breed_selector_widget.dart
│   │   │   │   ├── frame_quality_indicator.dart
│   │   │   │   └── capture_progress_widget.dart
│   │   │   └── providers/
│   │   │       ├── camera_provider.dart
│   │   │       └── frame_evaluation_provider.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── capture_session.dart
│   │   │   │   ├── frame_quality.dart
│   │   │   │   └── breed_type.dart
│   │   │   ├── usecases/
│   │   │   │   ├── start_continuous_capture_usecase.dart
│   │   │   │   ├── evaluate_frame_quality_usecase.dart
│   │   │   │   └── select_best_frame_usecase.dart
│   │   │   └── repositories/
│   │   │       └── capture_session_repository.dart
│   │   └── data/
│   │       ├── models/
│   │       │   ├── capture_session_model.dart
│   │       │   └── frame_quality_model.dart
│   │       ├── datasources/
│   │       │   ├── local_capture_session_datasource.dart
│   │       │   └── remote_capture_session_datasource.dart
│   │       └── repositories/
│   │           └── capture_session_repository_impl.dart
│   │
│   ├── analytics_reports/          # Área 2: Análisis y Reportes
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   │   ├── report_screen.dart
│   │   │   │   ├── weight_evolution_screen.dart
│   │   │   │   └── breed_comparison_screen.dart
│   │   │   └── widgets/
│   │   │       ├── weight_chart_widget.dart
│   │   │       └── breed_performance_card.dart
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── generate_weight_evolution_chart_usecase.dart
│   │   │   │   ├── compare_animal_performance_usecase.dart
│   │   │   │   └── export_senasag_report_usecase.dart
│   │   └── data/
│   │       └── repositories/
│   │           └── analytics_repository_impl.dart
│   │
│   ├── monitoring/                 # Área 3: Monitoreo y Planificación
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   │   ├── alert_screen.dart
│   │   │   │   └── calendar_screen.dart
│   │   │   └── widgets/
│   │   │       ├── alert_card_widget.dart
│   │   │       └── asocebu_schedule_widget.dart
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── create_custom_alert_usecase.dart
│   │   │   │   ├── schedule_massive_capture_usecase.dart
│   │   │   │   └── generate_gma_usecase.dart
│   │   └── data/
│   │       └── repositories/
│   │           └── monitoring_repository_impl.dart
│   │
│   ├── user_features/              # Área 4: Funcionalidades Usuario
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   │   ├── search_screen.dart
│   │   │   │   ├── list_management_screen.dart
│   │   │   │   └── settings_screen.dart
│   │   │   └── widgets/
│   │   │       ├── breed_filter_widget.dart
│   │   │       └── age_category_filter_widget.dart
│   │   └── domain/
│   │       ├── usecases/
│   │       │   ├── search_animals_by_criteria_usecase.dart
│   │       │   └── create_custom_list_usecase.dart
│   │       └── repositories/
│   │           └── user_preferences_repository.dart
│   │
│   └── operations/                 # Área 5: Operación y Respaldos
│       ├── presentation/
│       │   └── widgets/
│       │       ├── sync_indicator_widget.dart
│       │       └── gran_paititi_sync_widget.dart
│       ├── domain/
│       │   ├── usecases/
│       │   │   ├── sync_data_usecase.dart
│       │   │   ├── resolve_conflicts_usecase.dart
│       │   │   └── sync_gran_paititi_usecase.dart
│       │   └── repositories/
│       │       └── sync_repository.dart
│       └── data/
│           └── repositories/
│               └── sync_repository_impl.dart
│
├── core/
│   ├── constants/
│   │   ├── breeds.dart              # Constantes de las 7 razas
│   │   ├── age_categories.dart      # Constantes de 4 categorías
│   │   ├── capture_constants.dart   # FPS, duración, umbrales
│   │   ├── metrics.dart             # Métricas del sistema
│   │   └── regulatory.dart          # SENASAG, REGENSA, ASOCEBU
│   ├── errors/
│   │   ├── failures.dart
│   │   └── exceptions.dart
│   ├── network/
│   │   ├── api_client.dart
│   │   └── network_info.dart
│   ├── database/
│   │   ├── local_database.dart
│   │   └── sqlite_helper.dart
│   ├── ml/
│   │   ├── tflite_manager.dart
│   │   └── image_processor.dart
│   └── utils/
│       ├── breed_validator.dart
│       ├── age_category_calculator.dart
│       └── frame_quality_calculator.dart
│
└── main.dart
```

### 1.3 Convenciones de Naming

| Tipo | Convención | Ejemplo |
|------|------------|---------|
| **Archivos** | snake_case | `capture_session_model.dart` |
| **Clases** | PascalCase | `CaptureSession`, `BreedType` |
| **Variables/Funciones** | camelCase | `startContinuousCapture()` |
| **Constantes** | UPPER_SNAKE_CASE | `FRAMES_PER_SECOND` |
| **Enums** | PascalCase | `BreedType.brahman` |

### 1.4 Dependencias Principales (pubspec.yaml)

```yaml
dependencies:
  # Gestión de Estado
  flutter_riverpod: ^2.4.9          # Provider pattern, gestión reactiva
  riverpod_annotation: ^2.3.3       # Anotaciones para code generation
  
  # Arquitectura y Código
  freezed_annotation: ^2.4.1        # Inmutabilidad, copyWith, toString
  json_annotation: ^4.8.1           # Serialización JSON
  
  # Base de Datos Local
  sqflite: ^2.3.0                   # SQLite para offline-first
  path: ^1.8.3                      # Manejo de rutas de archivos
  
  # Red y Sincronización
  dio: ^5.3.3                       # Cliente HTTP robusto
  connectivity_plus: ^5.0.1         # Monitoreo de conectividad
  
  # Machine Learning
  tflite_flutter: ^0.10.4           # TensorFlow Lite runtime
  image: ^4.1.3                     # Procesamiento de imágenes
  
  # UI y Utilidades
  camera: ^0.10.5+5                 # Acceso a cámara
  permission_handler: ^11.0.1       # Gestión de permisos
  intl: ^0.18.1                     # Internacionalización
  shared_preferences: ^2.2.2        # Preferencias locales

dev_dependencies:
  # Code Generation
  build_runner: ^2.4.7              # Generación de código
  freezed: ^2.4.6                   # Generador de freezed
  json_serializable: ^6.7.1         # Generador de JSON
  
  # Testing
  flutter_test: sdk: flutter
  mockito: ^5.4.2                   # Mocking para tests
  integration_test: sdk: flutter
```

**Justificación de Dependencias**:
- **Riverpod**: Gestión de estado reactiva, mejor que Provider para casos complejos
- **Freezed**: Inmutabilidad y code generation, reduce boilerplate
- **SQLite**: Base de datos local robusta para offline-first
- **TensorFlow Lite**: Inferencia ML local, esencial para el dominio
- **Dio**: Cliente HTTP con interceptors, mejor que http para APIs complejas

## 2. BACKEND (FastAPI - Python) 🐍

### 2.1 Estructura de Carpetas

```
app/
├── api/
│   ├── routes/
│   │   ├── data_management/         # Área 1: Gestión de Datos
│   │   │   ├── capture_sessions.py
│   │   │   ├── frame_quality.py
│   │   │   └── breed_processing.py
│   │   ├── analytics/               # Área 2: Análisis y Reportes
│   │   │   ├── weight_evolution.py
│   │   │   ├── breed_comparison.py
│   │   │   └── senasag_reports.py
│   │   ├── monitoring/              # Área 3: Monitoreo y Planificación
│   │   │   ├── alerts.py
│   │   │   ├── calendar.py
│   │   │   └── gma_management.py
│   │   ├── user_features/           # Área 4: Funcionalidades Usuario
│   │   │   ├── search.py
│   │   │   ├── lists.py
│   │   │   └── preferences.py
│   │   └── operations/              # Área 5: Operación y Respaldos
│   │       ├── sync.py
│   │       ├── backup.py
│   │       └── gran_paititi.py
│   └── deps.py                      # Dependencias inyectadas
│
├── core/
│   ├── config.py                    # Configuración de la aplicación
│   ├── security.py                  # Autenticación y autorización
│   ├── database.py                  # Conexión a MongoDB
│   ├── exceptions.py                # Excepciones personalizadas
│   └── constants/
│       ├── breeds.py                # Constantes de las 7 razas
│       ├── age_categories.py        # Constantes de 4 categorías
│       ├── capture_constants.py     # FPS, duración, umbrales
│       └── metrics.py               # Métricas del sistema
│
├── models/                          # Modelos MongoDB (Pydantic)
│   ├── animal.py
│   ├── weighing.py
│   ├── breed.py
│   ├── age_category.py
│   ├── capture_session.py
│   ├── frame_quality.py
│   ├── senasag_report.py
│   ├── gma.py
│   └── regensa_compliance.py
│
├── schemas/                         # Esquemas de request/response
│   ├── animal_schemas.py
│   ├── weighing_schemas.py
│   ├── capture_schemas.py
│   ├── report_schemas.py
│   └── gma_schemas.py
│
├── services/                        # Lógica de negocio
│   ├── data_management/
│   │   ├── capture_service.py
│   │   ├── frame_evaluation_service.py
│   │   └── breed_processing_service.py
│   ├── analytics/
│   │   ├── weight_evolution_service.py
│   │   ├── breed_comparison_service.py
│   │   └── senasag_report_service.py
│   ├── monitoring/
│   │   ├── alert_service.py
│   │   ├── gma_service.py
│   │   └── regensa_compliance_service.py
│   ├── operations/
│   │   ├── sync_service.py
│   │   ├── backup_service.py
│   │   └── gran_paititi_service.py
│   └── external/
│       ├── s3_service.py
│       ├── senasag_client.py
│       └── gran_paititi_client.py
│
├── repositories/                    # Acceso a datos
│   ├── animal_repository.py
│   ├── weighing_repository.py
│   ├── capture_session_repository.py
│   ├── breed_repository.py
│   └── report_repository.py
│
└── main.py                          # Punto de entrada
```

### 2.2 Separación de Responsabilidades

| Capa | Responsabilidad | Ejemplo |
|------|----------------|---------|
| **Routes** | Endpoints HTTP, validación de entrada | `POST /capture-sessions/start` |
| **Services** | Lógica de negocio, orquestación | `CaptureService.start_continuous_capture()` |
| **Models** | Estructura de datos MongoDB | `CaptureSession`, `Breed` |
| **Schemas** | Validación Pydantic, serialización | `StartCaptureRequest`, `CaptureSessionResponse` |
| **Repositories** | Acceso a datos, queries | `CaptureSessionRepository.get_by_id()` |

### 2.3 Dependencias Principales (requirements.txt)

```txt
# Framework Web
fastapi==0.104.1                    # Framework web moderno y rápido
uvicorn[standard]==0.24.0           # Servidor ASGI de alto rendimiento

# Base de Datos
motor==3.3.2                        # Driver asíncrono para MongoDB
pymongo==4.6.0                      # Cliente MongoDB oficial
beanie==1.23.6                      # ODM para MongoDB con Pydantic

# Validación y Serialización
pydantic==2.5.0                     # Validación de datos y serialización
pydantic-settings==2.1.0            # Configuración basada en Pydantic

# Autenticación y Seguridad
python-jose[cryptography]==3.3.0    # JWT tokens
passlib[bcrypt]==1.7.4              # Hashing de contraseñas
python-multipart==0.0.6             # Parsing de form-data

# Cloud y Almacenamiento
boto3==1.34.0                       # Cliente AWS (S3, etc.)
botocore==1.34.0                    # Core de boto3

# Procesamiento de Imágenes
opencv-python==4.8.1.78             # Procesamiento de imágenes
Pillow==10.1.0                      # Manipulación de imágenes
numpy==1.25.2                       # Operaciones numéricas

# Machine Learning
tensorflow==2.15.0                  # TensorFlow para entrenamiento
scikit-learn==1.3.2                 # Algoritmos ML adicionales

# Utilidades
python-dotenv==1.0.0                # Variables de entorno
httpx==0.25.2                       # Cliente HTTP asíncrono
pytest==7.4.3                       # Framework de testing
pytest-asyncio==0.21.1              # Testing asíncrono
```

**Justificación de Dependencias**:
- **FastAPI**: Framework moderno con validación automática y documentación
- **Motor/Beanie**: MongoDB asíncrono con ODM type-safe
- **Boto3**: Integración nativa con AWS S3 para modelos ML
- **OpenCV**: Procesamiento de imágenes para evaluación de calidad
- **TensorFlow**: Entrenamiento y conversión de modelos a TFLite

## 3. ML-TRAINING (Entrenamiento de Modelos) 🧠

### 3.1 Estructura de Carpetas

```
ml-training/
├── data/
│   ├── raw/                         # Datos originales
│   │   ├── brahman/
│   │   │   ├── terneros/
│   │   │   ├── vaquillonas_torillos/
│   │   │   ├── vaquillonas_toretes/
│   │   │   └── vacas_toros/
│   │   ├── nelore/
│   │   ├── angus/
│   │   ├── cebuinas/
│   │   ├── criollo/
│   │   ├── pardo_suizo/
│   │   └── jersey/
│   ├── processed/                   # Datos procesados
│   │   ├── train/
│   │   ├── validation/
│   │   └── test/
│   └── metadata/
│       ├── annotations.csv          # Anotaciones de peso real
│       ├── breed_mapping.json       # Mapeo de razas
│       └── age_categories.json      # Categorías de edad
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Exploración de datos
│   ├── 02_data_preprocessing.ipynb  # Limpieza y normalización
│   ├── 03_model_training.ipynb      # Entrenamiento por raza
│   ├── 04_model_evaluation.ipynb    # Evaluación de métricas
│   └── 05_model_export.ipynb        # Conversión a TFLite
│
├── scripts/
│   ├── data_preparation/
│   │   ├── download_dataset.py      # Descarga de datos
│   │   ├── clean_annotations.py     # Limpieza de anotaciones
│   │   └── split_dataset.py         # División train/val/test
│   ├── training/
│   │   ├── train_by_breed.py        # Entrenamiento por raza
│   │   ├── hyperparameter_tuning.py # Optimización de hiperparámetros
│   │   └── cross_validation.py      # Validación cruzada
│   ├── evaluation/
│   │   ├── evaluate_metrics.py      # Cálculo de métricas
│   │   ├── generate_reports.py      # Reportes de evaluación
│   │   └── compare_models.py        # Comparación de modelos
│   └── export/
│       ├── export_to_tflite.py      # Conversión a TFLite
│       ├── optimize_model.py        # Optimización para móvil
│       └── generate_manifest.py     # Generación de manifest.json
│
├── models/
│   ├── checkpoints/                 # Checkpoints durante entrenamiento
│   │   ├── brahman/
│   │   ├── nelore/
│   │   ├── angus/
│   │   ├── cebuinas/
│   │   ├── criollo/
│   │   ├── pardo_suizo/
│   │   └── jersey/
│   ├── exports/                     # Modelos exportados
│   │   ├── brahman-v1.0.0.tflite
│   │   ├── nelore-v1.0.0.tflite
│   │   ├── angus-v1.0.0.tflite
│   │   ├── cebuinas-v1.0.0.tflite
│   │   ├── criollo-v1.0.0.tflite
│   │   ├── pardo_suizo-v1.0.0.tflite
│   │   └── jersey-v1.0.0.tflite
│   └── manifest.json                # Versiones y metadatos
│
├── mlruns/                          # MLflow tracking
│   ├── 0/
│   ├── meta.yaml
│   └── mlflow.db
│
├── config/
│   ├── params.yaml                  # Parámetros de entrenamiento
│   ├── model_config.yaml            # Configuración de modelos
│   └── data_config.yaml             # Configuración de datos
│
└── requirements.txt                 # Dependencias ML
```

### 3.2 Versionado de Modelos

**Estrategia de Naming**:
- Formato: `{raza}-v{major}.{minor}.{patch}.tflite`
- Ejemplo: `brahman-v1.2.0.tflite`

**Manifest.json**:
```json
{
  "version": "1.2.0",
  "models": {
    "brahman": {
      "url": "s3://bovine-ml-models/brahman-v1.2.0.tflite",
      "md5": "abc123...",
      "size_mb": 4.5,
      "min_app_version": "1.0.0",
      "metrics": {
        "r2_score": 0.97,
        "mae_kg": 3.2,
        "precision": 0.96
      }
    }
  }
}
```

### 3.3 MLflow Tracking

**Configuración**:
- **Tracking URI**: Local (`mlruns/`) + S3 para producción
- **Experimentos**: Uno por raza bovina
- **Métricas clave**: R², MAE, Precisión, Tiempo de inferencia
- **Parámetros**: Learning rate, batch size, epochs, arquitectura

**Métricas de Validación**:
- **R² ≥ 0.95**: Coeficiente de determinación
- **MAE < 5 kg**: Error absoluto promedio
- **Precisión ≥ 95%**: Porcentaje de predicciones correctas
- **Tiempo < 3s**: Inferencia en dispositivo móvil

### 3.4 Dependencias ML (requirements.txt)

```txt
# Machine Learning Core
tensorflow==2.15.0                  # Framework principal
tensorflow-lite==2.15.0             # Conversión a TFLite
scikit-learn==1.3.2                 # Métricas y utilidades

# Procesamiento de Datos
pandas==2.1.4                       # Manipulación de datos
numpy==1.25.2                       # Operaciones numéricas
opencv-python==4.8.1.78             # Procesamiento de imágenes
Pillow==10.1.0                      # Manipulación de imágenes

# Tracking y Experimentación
mlflow==2.8.1                       # Tracking de experimentos
wandb==0.16.0                       # Alternativa para tracking

# Visualización
matplotlib==3.8.2                   # Gráficos básicos
seaborn==0.13.0                     # Gráficos estadísticos
plotly==5.17.0                      # Gráficos interactivos

# Utilidades
tqdm==4.66.1                        # Barras de progreso
pyyaml==6.0.1                       # Configuración YAML
boto3==1.34.0                       # AWS S3 para modelos
```

**Justificación de Dependencias**:
- **TensorFlow**: Framework estándar para deep learning
- **MLflow**: Tracking de experimentos y versionado de modelos
- **OpenCV**: Procesamiento de imágenes para preprocesamiento
- **Boto3**: Subida automática de modelos a S3
- **Scikit-learn**: Métricas adicionales y validación cruzada

## 4. Configuración Global del Proyecto

### 4.1 Archivos de Configuración Raíz

```
bovine-weight-estimation/
├── .gitignore                       # Archivos ignorados por Git
├── .env.example                     # Template de variables de entorno
├── docker-compose.yml               # Orquestación de servicios
├── README.md                        # Documentación principal
├── LICENSE                          # Licencia MIT
├── pyproject.toml                   # Configuración Python
├── pubspec.yaml                     # Dependencias Flutter
└── Makefile                         # Comandos automatizados
```

### 4.2 Variables de Entorno (.env)

```bash
# Base de Datos
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=bovine_weight_estimation

# AWS S3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=bovine-ml-models
S3_REGION=us-east-1

# MLflow
MLFLOW_TRACKING_URI=file:./mlruns
MLFLOW_S3_ENDPOINT_URL=https://s3.amazonaws.com

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Seguridad
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4.3 Docker Compose

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: bovine_weight_estimation

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
    volumes:
      - ./backend:/app

  mlflow:
    image: python:3.11
    ports:
      - "5000:5000"
    volumes:
      - ./ml-training:/app
    working_dir: /app
    command: mlflow server --host 0.0.0.0 --port 5000

volumes:
  mongodb_data:
```

Esta estructura modular permite:
- **Desarrollo independiente** de cada componente
- **Testing aislado** por feature y tecnología
- **Despliegue escalable** con Docker
- **Mantenimiento simplificado** con responsabilidades claras
- **Integración normativa** específica para Bolivia (SENASAG, REGENSA, ASOCEBU)
