# Backend FastAPI - Sistema de Estimación de Peso Bovino

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Stack**: Python 3.11+ | FastAPI | MongoDB (Beanie ODM) | TensorFlow  
**Arquitectura**: Clean Architecture + SOLID Principles

---

## 🏗️ Arquitectura Backend

### Clean Architecture en Capas

```
backend/app/
├── core/               # Core Layer (independiente)
│   ├── config.py       # Configuración centralizada (Pydantic Settings)
│   ├── constants/      # Constantes del dominio (7 razas, 4 categorías, métricas)
│   └── errors/         # Excepciones personalizadas
│
├── models/             # Data Layer (MongoDB con Beanie ODM)
│   ├── animal_model.py
│   └── weight_estimation_model.py
│
├── schemas/            # API Layer (Pydantic DTOs)
│   ├── animal_schemas.py
│   ├── weighing_schemas.py
│   └── sync_schemas.py
│
├── services/           # Business Logic Layer
│   ├── animal_service.py
│   ├── weighing_service.py
│   └── sync_service.py
│
├── api/routes/         # Presentation Layer (FastAPI Routers)
│   ├── animals.py      # CRUD de animales
│   ├── weighings.py    # Estimaciones de peso
│   └── sync.py         # Sincronización offline
│
└── main.py             # Application entry point
```

---

## 🚀 Inicio Rápido

### 1. Instalación de Dependencias

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuración

Copiar `.env.example` a `.env` y configurar:

```bash
# MongoDB local (desarrollo)
MONGODB_URL="mongodb://localhost:27017"

# O MongoDB Atlas (producción)
MONGODB_URL="mongodb+srv://user:pass@cluster.mongodb.net/"
```

### 3. Ejecutar Servidor

```bash
# Desarrollo (con auto-reload)
python -m app.main

# O con uvicorn directamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Verificar

Abrir navegador en:
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

---

## 📚 Endpoints Disponibles

### Animals (US-003)

- `POST /api/v1/animals` - Crear animal
- `GET /api/v1/animals/{animal_id}` - Obtener animal
- `GET /api/v1/animals?farm_id=...` - Listar animales
- `PUT /api/v1/animals/{animal_id}` - Actualizar animal
- `DELETE /api/v1/animals/{animal_id}` - Eliminar animal (soft delete)

### Weighings (US-002, US-004)

- `POST /api/v1/weighings` - Crear estimación de peso
- `GET /api/v1/weighings/{weighing_id}` - Obtener estimación
- `GET /api/v1/weighings/animal/{animal_id}` - Historial por animal
- `GET /api/v1/weighings` - Listar todas las estimaciones

### Sync (US-005)

- `POST /api/v1/sync/cattle` - Sincronizar batch de animales
- `POST /api/v1/sync/weight-estimations` - Sincronizar batch de pesajes
- `GET /api/v1/sync/health` - Health check de sincronización

---

## 🗄️ Modelos MongoDB (Beanie)

### AnimalModel

```python
{
  "_id": UUID,
  "ear_tag": "HG-BRA-001",        # UNIQUE
  "breed": "brahman",              # Enum (7 razas)
  "birth_date": datetime,
  "gender": "male|female",
  "status": "active",
  "farm_id": UUID,
  ...
}
```

### WeightEstimationModel

```python
{
  "_id": UUID,
  "animal_id": UUID,
  "breed": "brahman",
  "estimated_weight_kg": 487.5,
  "confidence": 0.95,
  "method": "tflite",
  "processing_time_ms": 2100,
  "timestamp": datetime,
  ...
}
```

---

## 🎯 Constantes del Dominio

### 7 Razas Bovinas (NO MODIFICAR)

1. Brahman (Bos indicus)
2. Nelore (Bos indicus)
3. Angus (Bos taurus)
4. Cebuinas (Bos indicus)
5. Criollo (Bos taurus)
6. Pardo Suizo (Bos taurus)
7. Jersey (Bos taurus)

### 4 Categorías de Edad (NO MODIFICAR)

1. Terneros (<8 meses)
2. Vaquillonas/Torillos (6-18 meses)
3. Vaquillonas/Toretes (19-30 meses)
4. Vacas/Toros (>30 meses)

### Métricas del Sistema

- Precisión ML: ≥95% (R² ≥ 0.95)
- Error absoluto: <5 kg
- Tiempo procesamiento: <3 segundos
- Confidence mínimo: ≥80%

---

## 🔧 Desarrollo

### Linting y Formateo

```bash
# Format con Black
black app/

# Ordenar imports
isort app/

# Linting
flake8 app/
ruff check app/

# Type checking
mypy app/
```

### Testing

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Solo unit tests
pytest tests/unit/
```

---

## 📦 Deployment

### MongoDB Atlas (Producción)

1. Crear cuenta en https://www.mongodb.com/cloud/atlas
2. Crear cluster gratuito (M0)
3. Crear usuario y obtener connection string
4. Actualizar `MONGODB_URL` en `.env`

### Deploy en Railway/Render

```bash
# Railway
railway login
railway init
railway up

# O Render (conectar GitHub)
# Configurar en dashboard: https://render.com
```

---

## 🎯 Próximos Pasos

### Fase 1: Backend Core ✅ COMPLETADO
- [x] Configuración FastAPI + Beanie
- [x] Models MongoDB (Animals, WeightEstimations)
- [x] Services (Business Logic)
- [x] API Routes (CRUD completo)
- [x] Sincronización offline

### Fase 2: ML Integration (SIGUIENTE)
- [ ] Pipeline TensorFlow básico
- [ ] Modelo genérico MVP
- [ ] Endpoint `/weighings/predict` con inferencia
- [ ] Exportar a TFLite

### Fase 3: MongoDB Cloud
- [ ] Registrar MongoDB Atlas
- [ ] Configurar cluster
- [ ] Migrar datos de desarrollo

---

**Última actualización**: 20 Oct 2024  
**Versión**: 1.0.0  
**Equipo**: Agrocom - UAGRM

