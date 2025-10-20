# Backend FastAPI - Sistema de Estimación de Peso Bovino

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Stack**: Python 3.11+ | FastAPI | MongoDB (Beanie ODM) | TensorFlow  
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
│   ├── animal_model.py        # Modelo MongoDB de animales
│   └── weight_estimation_model.py  # Modelo de pesajes
│
├── schemas/                   # API Layer (Pydantic DTOs)
│   ├── animal_schemas.py      # Request/Response animales
│   ├── weighing_schemas.py    # Request/Response pesajes
│   └── sync_schemas.py        # DTOs sincronización
│
├── services/                  # Business Logic Layer
│   ├── animal_service.py      # Lógica de negocio animales
│   ├── weighing_service.py    # Lógica de negocio pesajes
│   └── sync_service.py        # Lógica sincronización
│
├── api/routes/                # Presentation Layer (Routers)
│   ├── animals.py             # 5 endpoints CRUD animales
│   ├── weighings.py           # 4 endpoints pesajes
│   └── sync.py                # 3 endpoints sincronización
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

### 2. Configuración MongoDB

**Opción A - MongoDB Local (Desarrollo):**
```bash
# macOS
brew install mongodb-community@7.0
brew services start mongodb-community

# Ubuntu
sudo apt install mongodb-org
sudo systemctl start mongod
```

**Opción B - MongoDB Atlas (Cloud Gratuito):**
1. Ir a https://www.mongodb.com/cloud/atlas
2. Crear cuenta y cluster M0 (gratis)
3. Obtener connection string
4. Actualizar en `.env`

### 3. Configurar Variables

```bash
cp .env.example .env
# Editar .env con tu MONGODB_URL
```

### 4. Ejecutar Servidor

```bash
# Con auto-reload
python -m app.main

# O con uvicorn
uvicorn app.main:app --reload
```

### 5. Verificar

- **API Docs**: http://localhost:8000/api/docs
- **Health**: http://localhost:8000/health

---

## 📚 API Endpoints

### 🐄 Animals (US-003)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/animals` | Crear animal |
| GET | `/api/v1/animals/{id}` | Obtener por ID |
| GET | `/api/v1/animals?farm_id=...` | Listar (paginado) |
| PUT | `/api/v1/animals/{id}` | Actualizar |
| DELETE | `/api/v1/animals/{id}` | Eliminar (soft) |

### ⚖️ Weighings (US-002, US-004)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/weighings` | Crear estimación |
| GET | `/api/v1/weighings/{id}` | Obtener por ID |
| GET | `/api/v1/weighings/animal/{id}` | Historial |
| GET | `/api/v1/weighings` | Listar todas |

### 🔄 Sync (US-005)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/sync/cattle` | Batch animales |
| POST | `/api/v1/sync/weight-estimations` | Batch pesajes |
| GET | `/api/v1/sync/health` | Health check |

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

### 4 Categorías de Edad

1. Terneros (<8 meses)
2. Vaquillonas/Torillos (6-18 meses)
3. Vaquillonas/Toretes (19-30 meses)
4. Vacas/Toros (>30 meses)

### Métricas del Sistema

- **Precisión ML**: ≥95% (R² ≥ 0.95)
- **Error absoluto**: <5 kg
- **Tiempo procesamiento**: <3 segundos
- **Confidence mínimo**: ≥80%

---

## 🧪 Testing

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Solo unit tests
pytest tests/unit/ -v
```

---

## 🔧 Desarrollo

### Linting y Formateo (equivalente a `flutter analyze`)

```bash
# ✅ Análisis de código (como flutter analyze)
python3 -m ruff check app/

# 🔧 Corregir automáticamente
python3 -m ruff check app/ --fix

# 🎨 Formatear código (Black-compatible)
python3 -m ruff format app/

# 🚀 Todo en uno (check + fix + format)
python3 -m ruff check app/ --fix && python3 -m ruff format app/
```

**Configuración del IDE**:
- ✅ `.vscode/settings.json` incluido
- ✅ Python interpreter: `venv/bin/python`
- ✅ Ruff linter habilitado
- ✅ Format on save activado
- ✅ Auto fix imports on save

**Reinicia Cursor/VSCode** después de crear el venv para que detecte las dependencias.

---

**Hacienda Gamelera** - Bruno Brito Macedo  
**Versión**: 1.0.0  
**Última actualización**: 20 Oct 2024

