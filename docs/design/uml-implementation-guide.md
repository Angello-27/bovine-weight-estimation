# Guía de Implementación del Modelo UML

**Basado en**: Diagrama de Clases del Dominio  
**Alcance**: Backend, Frontend y Mobile  
**Fecha**: 2024-12-XX

---

## 📊 Modelos del Diagrama UML

### Modelos Core (Implementados ✅)
1. **Animal** - ✅ Implementado
2. **Weighing** - ✅ Implementado (WeightEstimation)
3. **User** - ✅ Implementado
4. **Breed** - ✅ Implementado (Enum BreedType)
5. **CaptureSession** - ✅ Implementado (solo mobile)
6. **Image** - ✅ Implementado (Frame en mobile)

### Modelos Faltantes ❌
7. **Farm** - ❌ Falta implementar
8. **Alert** - ❌ Falta implementar

### Modelos Eliminados 🚫
9. **GMA** - 🚫 Fuera de alcance
10. **SENASAGReport** - 🚫 Fuera de alcance

---

## 🔗 Relaciones del Diagrama UML

### Relaciones Implementadas ✅
1. **Animal (1) → Weighing (1..*)** - ✅ Implementado
2. **Weighing (1) → Image (1)** - ✅ Implementado (frame_image_path)
3. **Image (1) → CaptureSession (1)** - ✅ Implementado (solo mobile)
4. **Animal (1) → CaptureSession (1..*)** - ✅ Implementado (solo mobile)
5. **Animal (1) → Breed (1)** - ✅ Implementado (breed enum)

### Relaciones Faltantes ❌
6. **Animal (1) → Farm (1)** - ❌ Falta (AnimalModel tiene farm_id pero no hay modelo Farm)
7. **User (1) → Farm (1..*)** - ❌ Falta (no hay modelo Farm)
8. **User (1) → Alert (1..*)** - ❌ Falta (no hay modelo Alert)
9. **Farm (1) → Animal (1..*)** - ❌ Falta (no hay modelo Farm)

---

## 📱 Implementación por Capa

### 1. Backend (FastAPI + MongoDB)

#### Modelos Existentes ✅

**AnimalModel** (`backend/app/models/animal_model.py`)
```python
class AnimalModel(Document):
    id: UUID
    ear_tag: Indexed(str, unique=True)  # tag_number
    breed: Indexed(str)                  # BreedType enum
    birth_date: datetime
    gender: Indexed(str)
    status: Indexed(str)
    farm_id: UUID                        # ⚠️ Relación sin modelo Farm
    # ... campos adicionales
```

**WeightEstimationModel** (`backend/app/models/weight_estimation_model.py`)
```python
class WeightEstimationModel(Document):
    id: UUID
    animal_id: Indexed(str)              # Relación con Animal
    estimated_weight_kg: float
    confidence: float
    method: str
    frame_image_path: str                # Relación con Image
    # ... campos adicionales
```

**UserModel** (`backend/app/models/user_model.py`)
```python
class UserModel(Document):
    id: UUID
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    role_id: UUID                       # Relación con RoleModel
    # ⚠️ Falta farm_id para relación User → Farm
```

#### Modelos a Crear ❌

**FarmModel** (`backend/app/models/farm_model.py`)
```python
from beanie import Document, Indexed
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime

class FarmModel(Document):
    """Modelo de finca/hacienda."""
    
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: Indexed(str) = Field(..., description="Nombre de la finca")
    owner_id: UUID = Field(..., description="ID del propietario (User)")
    location: dict = Field(..., description="GeoJSON Point: {type: 'Point', coordinates: [lon, lat]}")
    capacity: int = Field(..., description="Capacidad máxima de animales")
    total_animals: int = Field(default=0, description="Total actual de animales")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "farms"
        indexes = ["name", "owner_id"]
```

**AlertModel** (`backend/app/models/alert_model.py`)
```python
from beanie import Document, Indexed
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class AlertType(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    STAGNATION = "stagnation"
    REMINDER = "reminder"
    SYSTEM = "system"

class AlertStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    READ = "read"

class AlertModel(Document):
    """Modelo de alertas y notificaciones."""
    
    id: UUID = Field(default_factory=uuid4, alias="_id")
    user_id: Indexed(UUID) = Field(..., description="ID del usuario")
    type: AlertType = Field(..., description="Tipo de alerta")
    title: str = Field(..., description="Título de la alerta")
    message: str = Field(..., description="Mensaje de la alerta")
    status: AlertStatus = Field(default=AlertStatus.PENDING)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: datetime | None = None
    
    class Settings:
        name = "alerts"
        indexes = ["user_id", "status", "type"]
```

#### Actualizaciones Necesarias

**1. Actualizar AnimalModel** - Ya tiene `farm_id`, solo falta validar que exista FarmModel

**2. Actualizar UserModel** - Agregar `farm_id` opcional:
```python
# En user_model.py
farm_id: UUID | None = Field(None, description="ID de la finca principal del usuario")
```

**3. Crear Schemas** (`backend/app/schemas/`)
- `farm_schemas.py` - FarmCreateRequest, FarmUpdateRequest, FarmResponse
- `alert_schemas.py` - AlertCreateRequest, AlertResponse, AlertsListResponse

**4. Crear Servicios** (`backend/app/services/`)
- `farm_service.py` - CRUD de fincas
- `alert_service.py` - CRUD de alertas

**5. Crear Rutas** (`backend/app/api/routes/`)
- `farm.py` - Endpoints REST para fincas
- `alert.py` - Endpoints REST para alertas

---

### 2. Frontend (React)

#### Estructura de Componentes

```
frontend/src/
├── components/
│   ├── organisms/
│   │   ├── FarmList/          # ❌ Crear
│   │   ├── FarmForm/          # ❌ Crear
│   │   ├── AlertList/         # ❌ Crear
│   │   └── AlertCard/         # ❌ Crear
│   └── molecules/
│       └── FarmSelector/      # ❌ Crear
├── services/
│   ├── farm/
│   │   ├── getAllFarms.js     # ❌ Crear
│   │   ├── createFarm.js      # ❌ Crear
│   │   └── updateFarm.js      # ❌ Crear
│   └── alert/
│       ├── getAllAlerts.js    # ❌ Crear
│       ├── markAsRead.js      # ❌ Crear
│       └── deleteAlert.js     # ❌ Crear
├── views/
│   ├── FarmView.js            # ❌ Crear
│   └── AlertsView.js          # ❌ Crear
└── containers/
    ├── farm/                  # ❌ Crear
    └── alert/                 # ❌ Crear
```

#### Ejemplo de Servicio

**`frontend/src/services/farm/getAllFarms.js`**
```javascript
import apiClient from '../../api/axiosClient';

const getAllFarms = async () => {
    try {
        const response = await apiClient.get('/farm');
        return response.data;
    } catch (error) {
        throw new Error('Error al obtener fincas');
    }
};

export { getAllFarms };
```

#### Ejemplo de Componente

**`frontend/src/components/organisms/FarmList/index.js`**
```javascript
import React from 'react';
import { getAllFarms } from '../../../services/farm/getAllFarms';

function FarmList() {
    const [farms, setFarms] = React.useState([]);
    
    React.useEffect(() => {
        getAllFarms().then(setFarms);
    }, []);
    
    return (
        <div>
            {farms.map(farm => (
                <div key={farm.id}>
                    <h3>{farm.name}</h3>
                    <p>Capacidad: {farm.capacity}</p>
                    <p>Animales: {farm.total_animals}</p>
                </div>
            ))}
        </div>
    );
}

export default FarmList;
```

---

### 3. Mobile (Flutter)

#### Estructura de Archivos

```
mobile/lib/
├── domain/
│   ├── entities/
│   │   ├── farm.dart          # ❌ Crear
│   │   └── alert.dart         # ❌ Crear
│   └── repositories/
│       ├── farm_repository.dart    # ❌ Crear
│       └── alert_repository.dart   # ❌ Crear
├── data/
│   ├── models/
│   │   ├── farm_model.dart         # ❌ Crear
│   │   └── alert_model.dart        # ❌ Crear
│   ├── datasources/
│   │   ├── farm_local_datasource.dart    # ❌ Crear
│   │   ├── farm_remote_datasource.dart   # ❌ Crear
│   │   ├── alert_local_datasource.dart   # ❌ Crear
│   │   └── alert_remote_datasource.dart  # ❌ Crear
│   └── repositories/
│       ├── farm_repository_impl.dart     # ❌ Crear
│       └── alert_repository_impl.dart    # ❌ Crear
└── presentation/
    ├── pages/
    │   ├── farm_list_page.dart      # ❌ Crear
    │   ├── farm_detail_page.dart     # ❌ Crear
    │   └── alerts_page.dart          # ❌ Crear
    └── widgets/
        ├── farm_card.dart            # ❌ Crear
        └── alert_tile.dart           # ❌ Crear
```

#### Ejemplo de Entidad

**`mobile/lib/domain/entities/farm.dart`**
```dart
/// Entity: Farm
/// 
/// Entidad de dominio para finca/hacienda.
/// Single Responsibility: Representar concepto de finca.
library;

class Farm {
  final String id;
  final String name;
  final String ownerId;
  final double latitude;
  final double longitude;
  final int capacity;
  final int totalAnimals;
  final DateTime createdAt;
  final DateTime lastUpdated;

  const Farm({
    required this.id,
    required this.name,
    required this.ownerId,
    required this.latitude,
    required this.longitude,
    required this.capacity,
    required this.totalAnimals,
    required this.createdAt,
    required this.lastUpdated,
  });
}
```

#### Ejemplo de Modelo

**`mobile/lib/data/models/farm_model.dart`**
```dart
/// Model: FarmModel
/// 
/// Modelo de datos para Farm con serialización JSON y SQLite.
library;

import '../../domain/entities/farm.dart';

class FarmModel extends Farm {
  const FarmModel({
    required super.id,
    required super.name,
    required super.ownerId,
    required super.latitude,
    required super.longitude,
    required super.capacity,
    required super.totalAnimals,
    required super.createdAt,
    required super.lastUpdated,
  });

  factory FarmModel.fromJson(Map<String, dynamic> json) {
    final location = json['location'] as Map<String, dynamic>;
    final coordinates = location['coordinates'] as List;
    
    return FarmModel(
      id: json['id'] as String,
      name: json['name'] as String,
      ownerId: json['owner_id'] as String,
      latitude: coordinates[1] as double,
      longitude: coordinates[0] as double,
      capacity: json['capacity'] as int,
      totalAnimals: json['total_animals'] as int,
      createdAt: DateTime.parse(json['created_at'] as String),
      lastUpdated: DateTime.parse(json['last_updated'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'owner_id': ownerId,
      'location': {
        'type': 'Point',
        'coordinates': [longitude, latitude],
      },
      'capacity': capacity,
      'total_animals': totalAnimals,
      'created_at': createdAt.toIso8601String(),
      'last_updated': lastUpdated.toIso8601String(),
    };
  }
}
```

#### SQLite Schema

**`mobile/lib/data/datasources/farm_local_datasource.dart`**
```dart
// Tabla farms
CREATE TABLE farms (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    capacity INTEGER NOT NULL,
    total_animals INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_farms_owner ON farms(owner_id);
```

---

## 📋 Checklist de Implementación

### Backend
- [ ] Crear `FarmModel` con Beanie
- [ ] Crear `AlertModel` con Beanie
- [ ] Actualizar `UserModel` para agregar `farm_id`
- [ ] Crear schemas: `farm_schemas.py`, `alert_schemas.py`
- [ ] Crear servicios: `farm_service.py`, `alert_service.py`
- [ ] Crear rutas: `farm.py`, `alert.py`
- [ ] Actualizar `main.py` para incluir nuevos modelos y rutas
- [ ] Agregar índices MongoDB para queries eficientes

### Frontend
- [ ] Crear servicios: `farm/`, `alert/`
- [ ] Crear componentes: `FarmList`, `FarmForm`, `AlertList`, `AlertCard`
- [ ] Crear vistas: `FarmView`, `AlertsView`
- [ ] Crear containers: `farm/`, `alert/`
- [ ] Integrar con API backend
- [ ] Agregar rutas en router

### Mobile
- [ ] Crear entidades: `farm.dart`, `alert.dart`
- [ ] Crear modelos: `farm_model.dart`, `alert_model.dart`
- [ ] Crear datasources: `farm_*`, `alert_*`
- [ ] Crear repositories: `farm_repository_impl.dart`, `alert_repository_impl.dart`
- [ ] Crear páginas: `farm_list_page.dart`, `alerts_page.dart`
- [ ] Crear widgets: `farm_card.dart`, `alert_tile.dart`
- [ ] Agregar tablas SQLite
- [ ] Implementar sincronización offline-first

---

## 🔄 Flujos de Datos

### Crear Finca
```
Frontend/Mobile → POST /farm → Backend (FarmService) → MongoDB (FarmModel)
```

### Crear Alerta
```
Backend (sistema) → AlertService → MongoDB (AlertModel)
Mobile → Sincronización → SQLite (alerts table)
```

### Relación Animal → Farm
```
AnimalModel.farm_id → FarmModel.id (validación en servicio)
```

### Relación User → Farm
```
UserModel.farm_id → FarmModel.id (opcional, puede tener múltiples)
```

---

## 📝 Notas Importantes

1. **Farm es crítico**: Necesario para relacionar animales con fincas y usuarios con fincas
2. **Alert es opcional**: Puede implementarse después si no es crítico para MVP
3. **Breed ya existe**: Como enum `BreedType`, no necesita modelo separado
4. **Image/Frame**: Ya implementado en mobile como `FrameModel`, en backend como `frame_image_path`
5. **CaptureSession**: Solo necesario en mobile para tracking de captura, no en backend

---

**Última actualización**: 2024-12-XX  
**Próximo paso**: Implementar `FarmModel` en backend como prioridad

