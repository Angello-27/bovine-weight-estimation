# Backend FastAPI - Sistema de Estimación de Peso Bovino

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Stack**: Python 3.11+ | FastAPI | MongoDB (Beanie ODM) | TensorFlow Lite  
**Arquitectura**: Clean Architecture + SOLID Principles

---

## 🏗️ Arquitectura Backend (Clean Architecture)

```
backend/app/
├── core/                      # Core Layer (independiente)
│   ├── config.py              # Configuración (Pydantic Settings)
│   ├── constants/             # Constantes del dominio
│   │   ├── breeds.py          # 7 razas exactas
│   │   ├── age_categories.py  # 4 categorías de edad
│   │   ├── metrics.py         # Métricas del sistema
│   │   └── hacienda.py        # Datos Hacienda Gamelera
│   └── errors/
│       └── exceptions.py      # Excepciones personalizadas
│
├── models/                    # Data Layer (Beanie ODM)
│   ├── alert_model.py         # Alertas y cronograma
│   ├── animal_model.py        # Modelo MongoDB de animales
│   ├── farm_model.py          # Modelo de fincas
│   ├── role_model.py          # Modelo de roles
│   ├── user_model.py          # Modelo de usuarios
│   └── weight_estimation_model.py  # Modelo de pesajes
│
├── schemas/                   # API Layer (Pydantic DTOs)
│   ├── alert_schemas.py       # Request/Response alertas
│   ├── animal_schemas.py      # Request/Response animales
│   ├── auth_schemas.py        # Request/Response autenticación
│   ├── farm_schemas.py        # Request/Response fincas
│   ├── role_schemas.py        # Request/Response roles
│   ├── sync_schemas.py        # DTOs sincronización
│   ├── user_schemas.py        # Request/Response usuarios
│   └── weighing_schemas.py    # Request/Response pesajes
│
├── services/                  # Business Logic Layer
│   ├── alert_service.py        # Lógica de negocio alertas
│   ├── animal_service.py      # Lógica de negocio animales
│   ├── auth_service.py        # Lógica de autenticación
│   ├── farm_service.py        # Lógica de negocio fincas
│   ├── ml_service.py          # Lógica de ML/inferencia
│   ├── role_service.py        # Lógica de negocio roles
│   ├── sync_service.py        # Lógica sincronización
│   ├── user_service.py        # Lógica de negocio usuarios
│   └── weighing_service.py    # Lógica de negocio pesajes
│
├── api/routes/                # Presentation Layer (Routers)
│   ├── alert.py               # Endpoints alertas y cronograma
│   ├── animals.py             # Endpoints CRUD animales
│   ├── auth.py                # Endpoints autenticación
│   ├── farm.py                # Endpoints CRUD fincas
│   ├── ml.py                  # Endpoints ML/predicción
│   ├── role.py                # Endpoints CRUD roles
│   ├── sync.py                # Endpoints sincronización
│   ├── user.py                # Endpoints CRUD usuarios
│   └── weighings.py           # Endpoints pesajes
│
└── main.py                    # Application entry point
```

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

## 📊 Modelos Implementados

| Modelo | Estado | Archivo | Servicio | Rutas |
|--------|--------|---------|----------|-------|
| `AlertModel` | ✅ | `alert_model.py` | ✅ | ✅ |
| `AnimalModel` | ✅ | `animal_model.py` | ✅ | ✅ |
| `WeightEstimationModel` | ✅ | `weight_estimation_model.py` | ✅ | ✅ |
| `UserModel` | ✅ | `user_model.py` | ✅ | ✅ |
| `FarmModel` | ✅ | `farm_model.py` | ✅ | ✅ |
| `RoleModel` | ✅ | `role_model.py` | ✅ | ✅ |

**Total**: 6 modelos completamente implementados con CRUD completo.

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
- **Scripts**: [`scripts/README.md`](scripts/README.md) - Documentación de scripts de utilidad

---

## 🎯 Estado del Proyecto

### ✅ Completado

- ✅ Todos los modelos implementados (Alert, Animal, WeightEstimation, User, Farm, Role)
- ✅ AlertModel con cronograma completo
- ✅ API de consulta de alertas (today, upcoming, scheduled/list)
- ✅ Preparación para TFLite real
- ✅ Scripts de utilidad (seed_data, setup_production, download_model_from_drive)
- ✅ Endpoints REST completos (CRUD para todos los modelos)
- ✅ Integración en main.py

### 📱 Próximos Pasos (Móvil)

- [ ] Integrar endpoints de alertas en el móvil Flutter
- [ ] Mostrar alertas del día en pantalla principal
- [ ] Implementar calendario de alertas próximas

---

**Última actualización**: Diciembre 2024
