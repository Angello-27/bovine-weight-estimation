# Backend FastAPI - Sistema de Estimación de Peso Bovino

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Stack**: Python 3.11+ | FastAPI | MongoDB (Beanie ODM) | TensorFlow Lite  
**Arquitectura**: Clean Architecture + SOLID Principles

---

## 🏗️ Arquitectura Backend (Clean Architecture)

El proyecto sigue **Clean Architecture** con separación clara de responsabilidades:

```
backend/app/
├── domain/                      # Domain Layer (Lógica de negocio pura)
│   ├── entities/                # Entidades del dominio (sin dependencias)
│   │   ├── animal.py            # Entidad Animal
│   │   ├── user.py              # Entidad User
│   │   └── role.py              # Entidad Role
│   ├── repositories/            # Interfaces de repositorios (ABC)
│   │   ├── animal_repository.py
│   │   ├── user_repository.py
│   │   └── role_repository.py
│   ├── usecases/                # Casos de uso (lógica de negocio)
│   │   ├── animals/             # Use cases de animales
│   │   ├── users/                # Use cases de usuarios
│   │   ├── roles/                # Use cases de roles
│   │   └── auth/                 # Use cases de autenticación
│   └── shared/                  # Código compartido del dominio
│       └── constants/           # Constantes del dominio
│           ├── breeds.py
│           ├── age_categories.py
│           ├── metrics.py
│           └── hacienda.py
│
├── data/                        # Data Layer (Infraestructura)
│   ├── models/                  # Modelos Beanie ODM (persistencia)
│   │   ├── animal_model.py      # AnimalModel (Document)
│   │   ├── user_model.py         # UserModel (Document)
│   │   └── role_model.py         # RoleModel (Document)
│   └── repositories/            # Implementaciones de repositorios
│       ├── animal_repository_impl.py
│       ├── user_repository_impl.py
│       └── role_repository_impl.py
│
├── api/                         # Presentation Layer (FastAPI)
│   ├── routes/                  # Endpoints REST
│   │   ├── animals.py           # CRUD animales
│   │   ├── users.py             # CRUD usuarios
│   │   ├── roles.py             # CRUD roles
│   │   ├── auth.py              # Autenticación
│   │   ├── farm.py              # CRUD fincas
│   │   ├── weighings.py         # Pesajes
│   │   ├── alert.py             # Alertas
│   │   ├── ml.py                # ML/predicción
│   │   └── sync.py              # Sincronización
│   ├── schemas/                 # Pydantic DTOs (Request/Response)
│   │   ├── animal_schemas.py
│   │   ├── user_schemas.py
│   │   ├── role_schemas.py
│   │   └── ...
│   └── dependencies.py          # Dependencias FastAPI (auth, etc.)
│
├── services/                    # ⚠️ DEPRECATED - Ya no se usa
│   └── (Módulos migrados directamente a Use Cases)
│
├── core/                        # Core Layer (Compartido)
│   ├── config.py                # Configuración (Pydantic Settings)
│   ├── database.py              # Configuración MongoDB/Beanie
│   ├── exceptions.py            # Excepciones del dominio
│   ├── lifespan.py              # Lifecycle de FastAPI
│   ├── middleware.py            # Middlewares (CORS, etc.)
│   └── routes.py                # Registro de rutas
│
│
├── ml/                          # Machine Learning
│   ├── model_loader.py           # Carga de modelos TFLite
│   ├── inference.py             # Motor de inferencia
│   ├── preprocessing.py         # Preprocesamiento de imágenes
│   └── strategies/              # Estrategias de estimación
│       ├── deep_learning_strategy.py    # TFLite (primaria)
│       └── morphometric_strategy.py     # YOLO (fallback)
│
└── main.py                      # Application entry point
```

### 📐 Principios de Clean Architecture

1. **Domain Layer** (Independiente):
   - ✅ Sin dependencias externas (no Beanie, no FastAPI)
   - ✅ Solo lógica de negocio pura
   - ✅ Interfaces (ABC) para repositorios
   - ✅ Use Cases con Single Responsibility

2. **Data Layer** (Implementación):
   - ✅ Implementa interfaces de Domain
   - ✅ Usa Beanie para persistencia
   - ✅ Convierte entre Entities y Models

3. **Presentation Layer** (API):
   - ✅ Solo maneja HTTP requests/responses
   - ✅ Convierte entre Schemas y Use Cases
   - ✅ No contiene lógica de negocio

4. **Service Layer** (Orquestadores):
   - ✅ Coordina múltiples use cases
   - ✅ Convierte entre Domain Entities y API Schemas

### 🔄 Flujo de Datos

```
API Route → Use Case → Repository Interface
                          ↓
              Repository Implementation → Model (Beanie) → MongoDB
              ↑
        Mappers (DTO ↔ Entity)
        Utils (funciones auxiliares)
```

**Nota**: Los Application Services han sido eliminados. Las rutas ahora inyectan directamente los Use Cases siguiendo el patrón de Clean Architecture.

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuración

Crear archivo `.env` en `backend/`:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=bovine_weight_estimation

# Seguridad
SECRET_KEY=tu_secret_key_super_segura_aqui
ENVIRONMENT=development

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# ML Models
ML_MODELS_PATH=./ml_models
ML_DEFAULT_MODEL=generic-cattle-v1.0.0.tflite
```

### 3. Setup Inicial

```bash
# Verificar dependencias y configuración
python scripts/setup_production.py

# Cargar datos iniciales (roles, usuarios, finca, animales, alertas)
python -m scripts.seed_data
```

### 4. Iniciar Backend

```bash
# Desarrollo
python -m app.main

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. Verificar Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Swagger docs
open http://localhost:8000/api/docs
```

---

## 📊 Módulos Implementados con Clean Architecture

| Módulo | Domain | Data | Use Cases | Routes | Estado |
|--------|--------|------|-----------|--------|--------|
| **Animal** | ✅ | ✅ | ✅ | ✅ | ✅ Completado |
| **User** | ✅ | ✅ | ✅ | ✅ | ✅ Completado |
| **Role** | ✅ | ✅ | ✅ | ✅ | ✅ Completado |
| **Auth** | ✅ | ✅ | ✅ | ✅ | ✅ Completado |
| **WeightEstimation** | ✅ | ✅ | ✅ | ✅ | ✅ Completado |
| **Sync** | ✅ | ✅ | ✅ | ✅ | ✅ Completado |
| **Alert** | ✅ | ✅ | ✅ | ✅ | ✅ Completado |
| **Farm** | ✅ | ✅ | ✅ | ✅ | ✅ Completado |

**Total**: 8 módulos completamente migrados a Clean Architecture
**Patrón**: Routes → Use Cases → Repositories → Models (sin Application Services)

---

## 🔔 Sistema de Alertas con Cronograma

### Endpoints de Consulta (para Móvil)

El móvil puede consultar alertas programadas:

- **`GET /api/v1/alerts/today`** - Alertas del día actual
  ```bash
  GET /api/v1/alerts/today?user_id={userId}&farm_id={farmId}
  ```

- **`GET /api/v1/alerts/upcoming?days_ahead=7`** - Alertas próximas (próximos N días)
  ```bash
  GET /api/v1/alerts/upcoming?days_ahead=7&user_id={userId}
  ```

- **`GET /api/v1/alerts/scheduled/list`** - Alertas en rango de fechas
  ```bash
  GET /api/v1/alerts/scheduled/list?from_date=2024-12-20&to_date=2024-12-27
  ```

### Funcionalidades

- ✅ Cronograma y programación de eventos
- ✅ Recurrencia (diario, semanal, mensual, trimestral, anual)
- ✅ Recordatorios (X días antes del evento)
- ✅ Filtros por raza, edad, género, cantidad (en `filter_criteria`)
- ✅ Estados: pending, sent, read, completed, cancelled
- ✅ Ubicación GPS para eventos

---

## 🔄 Sincronización Offline-First (US-005)

### Endpoints de Sincronización

El backend proporciona endpoints para sincronización bidireccional con la app móvil:

- **`POST /api/v1/sync/cattle`** - Sincronizar batch de animales (máximo 100 items)
  ```bash
  POST /api/v1/sync/cattle
  {
    "items": [...],
    "device_id": "android-device-123",
    "sync_timestamp": "2024-12-20T10:30:00Z"
  }
  ```

- **`POST /api/v1/sync/weight-estimations`** - Sincronizar batch de estimaciones (máximo 100 items)
  ```bash
  POST /api/v1/sync/weight-estimations
  {
    "items": [...],
    "device_id": "android-device-123",
    "sync_timestamp": "2024-12-20T10:30:00Z"
  }
  ```

- **`GET /api/v1/sync/health`** - Health check del servicio de sincronización
  ```bash
  GET /api/v1/sync/health
  ```

### Estrategia Last-Write-Wins

- Compara timestamps UTC de mobile vs backend
- El dato más reciente prevalece automáticamente
- Retorna conflictos para que mobile actualice su copia local si es necesario

### Guía de Integración Flutter

Ver documentación completa: [`../docs/integration/FLUTTER_SYNC_GUIDE.md`](../docs/integration/FLUTTER_SYNC_GUIDE.md)

**Resumen**:
- Flutter guarda estimaciones primero en SQLite (offline-first)
- Agrega items a cola de sincronización automáticamente
- Sincroniza en batches de hasta 100 items cuando hay conectividad
- Resuelve conflictos automáticamente con last-write-wins

---

## 🤖 Machine Learning - TFLite

### Estado Actual

- ✅ `model_loader.py` preparado para TFLite real
- ✅ `deep_learning_strategy.py` usa TFLite real
- ✅ `preprocessing.py` compatible con TFLite
- ✅ `requirements.txt` incluye `tensorflow-lite-runtime==2.16.0`

### Integrar Modelo desde Colab/Drive

Ver guía completa: [`INTEGRATION_GUIDE.md`](INTEGRATION_GUIDE.md)

**Resumen rápido**:
```bash
# Opción A: Script automático
python scripts/download_model_from_drive.py --file-id FILE_ID

# Opción B: Manual
# Descargar desde Google Drive y copiar a:
cp ~/Downloads/generic-cattle-v1.0.0.tflite backend/ml_models/
```

---

## 📋 Scripts de Utilidad

Ver documentación completa: [`scripts/README.md`](scripts/README.md)

### Scripts Disponibles

1. **`setup_production.py`** - Setup para producción/cloud
   - Verifica dependencias
   - Crea directorios necesarios
   - Valida configuración

2. **`seed_data.py`** - Datos iniciales para testing
   - Crea roles, usuarios, finca
   - Genera 200 animales con trazabilidad completa
   - Genera estimaciones de peso y alertas de ejemplo

3. **`download_model_from_drive.py`** - Descargar modelo TFLite
   - Descarga desde Google Drive usando `gdown`

---

## 🔧 Configuración para Cloud

### Variables de Entorno (.env)

```env
# MongoDB (Cloud)
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DB_NAME=bovine_weight_estimation

# Seguridad
SECRET_KEY=tu_secret_key_super_segura_aqui
ENVIRONMENT=production

# CORS (restringir en producción)
CORS_ORIGINS=["https://tu-dominio.com"]

# ML Models
ML_MODELS_PATH=./ml_models
ML_DEFAULT_MODEL=generic-cattle-v1.0.0.tflite
```

### Deployment Checklist

- [ ] Configurar MongoDB Atlas
- [ ] Configurar variables de entorno
- [ ] Descargar modelo TFLite
- [ ] Ejecutar `setup_production.py`
- [ ] Probar endpoints con Swagger
- [ ] Configurar CORS para frontend
- [ ] Configurar SSL/TLS
- [ ] Configurar logging
- [ ] Configurar monitoreo

---

## 📚 Documentación Adicional

- **Integración TFLite**: [`INTEGRATION_GUIDE.md`](INTEGRATION_GUIDE.md) - Guía completa para integrar modelo desde Colab
- **Flujo Clean Architecture**: [`FLUJO_CLEAN_ARCHITECTURE.md`](FLUJO_CLEAN_ARCHITECTURE.md) - Flujo de datos y responsabilidades por capa
- **Scripts**: [`scripts/README.md`](scripts/README.md) - Documentación de scripts de utilidad

---

## 🎯 Estado del Proyecto

### ✅ Completado

- ✅ Migración completa a Clean Architecture (8 módulos: Animal, User, Role, Auth, WeightEstimation, Sync, Alert, Farm)
- ✅ Eliminación de Application Services legacy (MLService, WeighingService)
- ✅ Implementación de Use Cases para WeightEstimations
- ✅ Mapper para WeightEstimation (DTO ↔ Entity)
- ✅ Utils ML inference en core/utils/
- ✅ Endpoint `/api/v1/ml/estimate` para estimación desde web
- ✅ Todos los modelos implementados (Alert, Animal, WeightEstimation, User, Farm, Role)
- ✅ AlertModel con cronograma completo
- ✅ API de consulta de alertas (today, upcoming, scheduled/list)
- ✅ Scripts de utilidad (seed_data, setup_production, download_model_from_drive)
- ✅ Endpoints REST completos (CRUD para todos los modelos)
- ✅ Integración en main.py
- ✅ Preparado para integración de modelo TFLite real

### ⏳ En Progreso

- ⏳ Integración de modelo TFLite real desde Google Drive

### 📱 Próximos Pasos (Móvil)

- [ ] Integrar endpoints de alertas en el móvil Flutter
- [ ] Mostrar alertas del día en pantalla principal
- [ ] Implementar calendario de alertas próximas

---

**Última actualización**: Diciembre 2024
