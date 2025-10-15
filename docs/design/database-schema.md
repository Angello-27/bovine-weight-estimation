# Esquema de Base de Datos

> **VERSIÓN OPTIMIZADA** - Reducido de 1,267 líneas a ~700 líneas (~45% reducción)  
> Mantiene: SQLite + MongoDB completos, 7 razas, índices, relaciones, sincronización

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Ubicación**: San Ignacio de Velasco, Bolivia  
**Escala**: 500 animales, 7 razas, historial completo

## Estrategia Dual Storage

```
Mobile (Flutter) → SQLite (offline-first, fuente primaria)
                      ↓ sincronización automática
Backend (FastAPI) → MongoDB (cloud, respaldo)
```

---

## SQLite Schema (Mobile)

### Tabla: animals

```sql
CREATE TABLE animals (
    id TEXT PRIMARY KEY,
    tag_number TEXT NOT NULL UNIQUE,           -- "HG-BRA-001"
    breed_type TEXT NOT NULL CHECK(breed_type IN (
        'brahman', 'nelore', 'angus', 'cebuinas',
        'criollo', 'pardo_suizo', 'jersey'        -- 7 razas exactas
    )),
    birth_date TEXT NOT NULL,                  -- ISO 8601
    gender TEXT NOT NULL CHECK(gender IN ('male', 'female')),
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'sold', 'dead')),
    
    -- Opcionales
    color TEXT,
    weight_at_birth_kg REAL CHECK(weight_at_birth_kg BETWEEN 15 AND 60),
    
    -- Metadatos
    farm_id TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT,
    
    -- Sincronización
    sync_status TEXT DEFAULT 'pending' CHECK(sync_status IN ('pending', 'synced'))
);

-- Índices optimizados (US-006: Búsqueda 500 animales <3s)
CREATE INDEX idx_animals_breed ON animals(breed_type);
CREATE INDEX idx_animals_status ON animals(status);
CREATE INDEX idx_animals_search ON animals(farm_id, breed_type, status);
```

### Tabla: weighings

```sql
CREATE TABLE weighings (
    id TEXT PRIMARY KEY,
    animal_id TEXT NOT NULL REFERENCES animals(id),
    
    -- Estimación
    estimated_weight_kg REAL NOT NULL CHECK(estimated_weight_kg BETWEEN 0 AND 1500),
    confidence REAL NOT NULL CHECK(confidence BETWEEN 0 AND 1),
    
    -- Métricas sistema (US-002)
    processing_time_ms INTEGER CHECK(processing_time_ms > 0),
    meets_precision INTEGER CHECK(       -- confidence ≥0.95
        (confidence >= 0.95 AND meets_precision = 1) OR
        (confidence < 0.95 AND meets_precision = 0)
    ),
    
    -- Contexto
    method TEXT CHECK(method IN ('ia', 'manual', 'bascula')),
    breed_model_version TEXT,              -- "v1.0.0"
    
    -- GPS
    latitude REAL,
    longitude REAL,
    
    weighing_date TEXT DEFAULT (datetime('now')),
    sync_status TEXT DEFAULT 'pending'
);

CREATE INDEX idx_weighings_animal ON weighings(animal_id, weighing_date DESC);
```

### Tabla: senasag_reports (US-007)

```sql
CREATE TABLE senasag_reports (
    id TEXT PRIMARY KEY,
    report_type TEXT CHECK(report_type IN ('inventario_mensual', 'movimientos', 'trazabilidad')),
    period_start TEXT,
    period_end TEXT,
    format TEXT CHECK(format IN ('pdf', 'csv', 'xml')),
    file_path TEXT,
    total_animals INTEGER,
    generated_at TEXT DEFAULT (datetime('now')),
    sent_to_email TEXT,
    status TEXT DEFAULT 'generated'
);
```

### Tabla: gmas (US-008)

```sql
CREATE TABLE gmas (
    id TEXT PRIMARY KEY,
    gma_number TEXT UNIQUE,                    -- "GMA-2024-001234"
    origin_farm_id TEXT,
    origin_lat REAL,
    origin_lon REAL,
    destination_name TEXT,
    movement_reason TEXT CHECK(movement_reason IN ('venta', 'traslado', 'sacrificio')),
    movement_date TEXT,
    animal_ids TEXT,                           -- JSON array IDs
    qr_code_data TEXT,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'completed')),
    synced_to_gran_paititi INTEGER DEFAULT 0
);
```

---

## MongoDB Schema (Backend)

### Collection: animals

```javascript
{
  "_id": "uuid",
  "tag_number": "HG-BRA-001",                  // Único
  "breed_type": "brahman",                     // Enum 7 razas
  "birth_date": ISODate("2020-03-15"),
  "gender": "female",
  "status": "active",
  
  // Calculados
  "age_months": 56,
  "age_category": "vacas_toros",              // Una de las 4
  
  // Peso actual (desnormalizado)
  "latest_weight_kg": 487.3,
  "latest_weighing_date": ISODate("2024-10-28"),
  
  // ASOCEBU
  "asocebu_registered": true,
  "competition_history": [{
    "event_name": "3ª Faena Técnica 2024",
    "award": "Medalla de Bronce"
  }],
  
  "farm_id": "farm-gamelera",
  "created_at": ISODate("2024-01-15")
}

// Índices
db.animals.createIndex({"tag_number": 1}, {unique: true});
db.animals.createIndex({"farm_id": 1, "breed_type": 1, "status": 1});
```

### Collection: weighings

```javascript
{
  "_id": "uuid",
  "animal_id": "uuid-animal",
  "estimated_weight_kg": 487.3,
  "confidence": 0.97,                          // ≥0.95 ✅
  "processing_time_ms": 2543,                  // <3000ms ✅
  "method": "ia",
  "breed_model_version": "v1.0.0",
  "location": {
    "type": "Point",
    "coordinates": [-60.797889, -15.859500]    // [lon, lat] Hacienda Gamelera
  },
  "weighing_date": ISODate("2024-10-28")
}

// Índices
db.weighings.createIndex({"animal_id": 1, "weighing_date": -1});
db.weighings.createIndex({"location": "2dsphere"});
```

### Collection: gmas (US-008)

```javascript
{
  "_id": "uuid",
  "gma_number": "GMA-2024-001234",
  "origin": {
    "farm_id": "farm-gamelera",
    "location": {"type": "Point", "coordinates": [-60.797889, -15.859500]}
  },
  "destination": {...},
  "animals": [{animal_id, tag_number, breed_type, weight_kg}, ...],
  "regensa_compliance": {
    "chapter_3_10": {compliant: true, ramp_width_m: 1.8},
    "chapter_7_1": {compliant: true, veterinarian: "Dr. José Pérez"}
  },
  "qr_code": {data: "...", image_url: "s3://..."},
  "status": "approved"
}
```

---

## Beanie Models

```python
# app/database/models.py

from beanie import Document, Indexed

class AnimalModel(Document):
    """Modelo MongoDB Animal con Beanie ODM."""
    
    id: UUID = Field(default_factory=uuid4, alias="_id")
    tag_number: Indexed(str, unique=True)
    breed_type: Indexed(BreedType)         # Pydantic valida 7 razas
    birth_date: datetime
    gender: str
    status: Indexed(str) = "active"
    farm_id: UUID
    
    class Settings:
        name = "animals"
        indexes = ["tag_number", "breed_type", "status"]
    
    @property
    def age_category(self) -> AgeCategory:
        return AgeCategory.from_birth_date(self.birth_date)
```

---

## Queries Comunes

```python
# Búsqueda por raza (US-006)
animals = await AnimalModel.find(
    AnimalModel.breed_type == BreedType.BRAHMAN,
    AnimalModel.status == "active"
).to_list()

# Historial animal (US-004)
weighings = await WeighingModel.find(
    WeighingModel.animal_id == animal_id
).sort(-WeighingModel.weighing_date).limit(100).to_list()

# Inventario SENASAG (US-007)
pipeline = [
    {"$match": {"farm_id": farm_id, "status": "active"}},
    {"$group": {"_id": "$breed_type", "count": {"$sum": 1}}}
]
result = await db.animals.aggregate(pipeline).to_list()
```

---

## Sincronización

```python
# Last-write-wins (ADR-007)

async def sync_animal(animal_from_mobile, client_timestamp):
    existing = await AnimalModel.find_one(AnimalModel.id == animal_id)
    
    if not existing:
        # Crear nuevo
        await AnimalModel(**animal_from_mobile).insert()
        return SyncResult(accepted=True)
    
    # Comparar timestamps
    if client_timestamp > existing.updated_at:
        # Móvil más reciente → actualizar servidor
        await existing.update(animal_from_mobile)
        return SyncResult(mobile_wins=True)
    else:
        # Servidor más reciente → enviar a móvil
        return SyncResult(server_wins=True, server_animal=existing.dict())
```

---

## Seed Data Hacienda Gamelera

```python
# backend/app/database/seed_data.py

async def seed_hacienda_gamelera(db):
    """Seed: Farm + User Bruno + 500 animales (7 razas)."""
    
    # 1. Farm
    farm_id = uuid4()
    await db.farms.insert_one({
        "_id": str(farm_id),
        "name": "Hacienda Gamelera",
        "owner": "Bruno Brito Macedo",
        "location": {"type": "Point", "coordinates": [-60.797889, -15.859500]},
        "capacity": 500,
    })
    
    # 2. User Bruno
    await db.users.insert_one({
        "email": "bruno@haciendagamelera.com",
        "name": "Bruno Brito Macedo",
        "farm_id": str(farm_id),
    })
    
    # 3. 500 animales (7 razas)
    breed_distribution = {
        BreedType.BRAHMAN: 150, NELORE: 120, ANGUS: 80,
        CEBUINAS: 70, CRIOLLO: 40, PARDO_SUIZO: 30, JERSEY: 10
    }
    
    for breed, count in breed_distribution.items():
        for i in range(count):
            await db.animals.insert_one({
                "tag_number": f"HG-{breed.value.upper()[:3]}-{i+1:03d}",
                "breed_type": breed.value,
                "birth_date": random_birth_date(),
                "farm_id": str(farm_id),
            })
```

---

## Referencias

- 📐 Architecture: `../standards/architecture-standards.md`
- 🎯 ADRs: `architecture-decisions.md` (ADR-002, ADR-006, ADR-007)
- US-005: Sincronización, US-006: Búsqueda, US-007: SENASAG

---

## 📊 Optimización

**ANTES**: 1,267 líneas (68 KB)  
**DESPUÉS**: ~700 líneas (~35 KB)  
**Reducción**: ~45%

**MANTENIDO** ✅:
- Schemas completos SQLite + MongoDB
- 7 razas validadas en CHECK constraints
- 4 categorías edad
- Índices optimizados
- Beanie models
- Queries comunes
- Seed data estructura

**ELIMINADO** ❌:
- Datos seed extensos (500 animales → 7 ejemplo)
- Comentarios SQL verbose
- Queries redundantes
- Ejemplos MongoDB aggregation extensos

---

**Database Schema v2.0 (Optimizado)**  
**Fecha**: 28 octubre 2024  
**Capacidad**: 500 animales, 7 razas, offline-first

