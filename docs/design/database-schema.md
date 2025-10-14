# Esquema de Base de Datos

> **Contexto**: Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera  
> **Cliente**: Bruno Brito Macedo  
> **Ubicación**: San Ignacio de Velasco, Santa Cruz, Bolivia  
> **Fecha**: 28 octubre 2024  
> **Sprint**: Sprint 3 - Integración Normativa

## Resumen Ejecutivo

Este documento especifica el esquema completo de base de datos del sistema, incluyendo:
- **SQLite** (móvil): Fuente primaria offline con 500+ animales de Hacienda Gamelera
- **MongoDB** (backend): Base de datos central en la nube con sincronización

El diseño soporta las 7 razas bovinas exactas, 4 categorías de edad, cumplimiento normativo SENASAG/REGENSA/ASOCEBU, y sincronización offline-first.

---

## Estrategia Dual: SQLite + MongoDB

### Arquitectura de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                    MOBILE APP (Flutter)                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │             SQLite (Offline-first)                      │ │
│  │  - Fuente primaria de verdad                           │ │
│  │  - 500 animales de Hacienda Gamelera                   │ │
│  │  - Historial completo de pesajes                       │ │
│  │  - Funciona 100% sin conexión                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│                          │ Sincronización                    │
│                          │ (when online)                     │
│                          ↓                                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS/JSON
                           │ Last-write-wins
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND API (FastAPI)                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           MongoDB Atlas (Cloud)                         │ │
│  │  - Base de datos central                               │ │
│  │  - Múltiples dispositivos                              │ │
│  │  - Reportes SENASAG/REGENSA                            │ │
│  │  - Backups automáticos                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## SQLite Schema (Mobile - Offline-first)

### Tablas Principales

#### 1. animals (Animales de Hacienda Gamelera)

```sql
CREATE TABLE animals (
    -- Identificación
    id TEXT PRIMARY KEY,                    -- UUID
    tag_number TEXT NOT NULL UNIQUE,        -- Número de caravana (ej: "HG-001")
    
    -- Datos principales (7 razas, 4 categorías)
    breed_type TEXT NOT NULL CHECK(breed_type IN (
        'brahman', 'nelore', 'angus', 'cebuinas',
        'criollo', 'pardo_suizo', 'jersey'
    )),
    birth_date TEXT NOT NULL,               -- ISO 8601: "2020-03-15T00:00:00Z"
    gender TEXT NOT NULL CHECK(gender IN ('male', 'female')),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN (
        'active', 'inactive', 'sold', 'dead'
    )),
    
    -- Campos opcionales
    color TEXT,                             -- ej: "Rojo", "Negro"
    weight_at_birth_kg REAL CHECK(weight_at_birth_kg >= 15 AND weight_at_birth_kg <= 60),
    mother_id TEXT REFERENCES animals(id),
    father_id TEXT REFERENCES animals(id),
    observations TEXT,
    
    -- Metadatos
    farm_id TEXT NOT NULL,                  -- Hacienda Gamelera ID
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT,
    
    -- Sincronización
    sync_status TEXT NOT NULL DEFAULT 'pending' CHECK(sync_status IN (
        'pending', 'synced', 'conflict'
    )),
    sync_at TEXT,                           -- Última sincronización exitosa
    
    -- Índices inline
    CHECK (length(tag_number) >= 1 AND length(tag_number) <= 50)
);

-- Índices para búsqueda optimizada (US-006)
CREATE INDEX idx_animals_breed_type ON animals(breed_type);
CREATE INDEX idx_animals_status ON animals(status);
CREATE INDEX idx_animals_farm_id ON animals(farm_id);
CREATE INDEX idx_animals_sync_status ON animals(sync_status);

-- Índice compuesto para búsqueda compleja
CREATE INDEX idx_animals_search ON animals(farm_id, breed_type, status);

-- Trigger para calcular updated_at automáticamente
CREATE TRIGGER animals_updated_at 
AFTER UPDATE ON animals
FOR EACH ROW
BEGIN
    UPDATE animals SET updated_at = datetime('now') WHERE id = NEW.id;
END;
```

**Datos de ejemplo (Hacienda Gamelera)**:
```sql
INSERT INTO animals (id, tag_number, breed_type, birth_date, gender, color, farm_id) VALUES
('a1b2c3-brahman-001', 'HG-BRA-001', 'brahman', '2020-03-15T00:00:00Z', 'female', 'Rojo', 'farm-gamelera-001'),
('a1b2c3-nelore-001', 'HG-NEL-001', 'nelore', '2021-05-20T00:00:00Z', 'male', 'Gris', 'farm-gamelera-001'),
('a1b2c3-angus-001', 'HG-ANG-001', 'angus', '2022-01-10T00:00:00Z', 'female', 'Negro', 'farm-gamelera-001');
-- ... hasta 500 animales
```

#### 2. weighings (Pesajes/Estimaciones)

```sql
CREATE TABLE weighings (
    -- Identificación
    id TEXT PRIMARY KEY,                    -- UUID
    animal_id TEXT NOT NULL REFERENCES animals(id) ON DELETE CASCADE,
    
    -- Datos de estimación
    estimated_weight_kg REAL NOT NULL CHECK(estimated_weight_kg > 0 AND estimated_weight_kg < 1500),
    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
    
    -- Métricas del sistema (US-002)
    processing_time_ms INTEGER NOT NULL CHECK(processing_time_ms > 0),
    meets_precision_threshold INTEGER NOT NULL DEFAULT 1 CHECK(
        (confidence >= 0.95 AND meets_precision_threshold = 1) OR
        (confidence < 0.95 AND meets_precision_threshold = 0)
    ),
    meets_time_threshold INTEGER NOT NULL DEFAULT 1 CHECK(
        (processing_time_ms < 3000 AND meets_time_threshold = 1) OR
        (processing_time_ms >= 3000 AND meets_time_threshold = 0)
    ),
    
    -- Contexto
    method TEXT NOT NULL CHECK(method IN ('ia', 'manual', 'bascula')),
    breed_model_version TEXT,               -- ej: "v1.0.0" del modelo TFLite
    
    -- Imagen y sesión
    capture_session_id TEXT,                -- Referencia a sesión de captura
    image_path TEXT,                        -- Ruta local del fotograma usado
    
    -- Ubicación GPS
    latitude REAL,                          -- GPS donde se capturó
    longitude REAL,
    
    -- Timestamp
    weighing_date TEXT NOT NULL DEFAULT (datetime('now')),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    -- Sincronización
    sync_status TEXT NOT NULL DEFAULT 'pending',
    sync_at TEXT
);

-- Índices
CREATE INDEX idx_weighings_animal_id ON weighings(animal_id);
CREATE INDEX idx_weighings_date ON weighings(weighing_date DESC);
CREATE INDEX idx_weighings_method ON weighings(method);
CREATE INDEX idx_weighings_sync_status ON weighings(sync_status);

-- Índice compuesto para historial de animal (US-004)
CREATE INDEX idx_weighings_animal_history ON weighings(animal_id, weighing_date DESC);
```

**Datos de ejemplo**:
```sql
INSERT INTO weighings (
    id, animal_id, estimated_weight_kg, confidence, processing_time_ms,
    method, breed_model_version, latitude, longitude, weighing_date
) VALUES (
    'w1b2c3-001',
    'a1b2c3-brahman-001',
    487.3,                          -- Peso estimado
    0.97,                           -- 97% confidence ✅ ≥95%
    2543,                           -- 2.5s procesamiento ✅ <3s
    'ia',
    'v1.0.0',
    -15.859500,                     -- GPS Hacienda Gamelera
    -60.797889,
    '2024-10-28T10:30:00Z'
);
```

#### 3. capture_sessions (Sesiones de Captura Continua)

```sql
CREATE TABLE capture_sessions (
    id TEXT PRIMARY KEY,
    animal_id TEXT NOT NULL REFERENCES animals(id),
    breed_type TEXT NOT NULL,              -- Raza seleccionada antes de capturar
    
    -- Configuración de captura (US-001)
    frames_per_second INTEGER NOT NULL DEFAULT 12 CHECK(frames_per_second BETWEEN 10 AND 15),
    capture_duration_seconds INTEGER NOT NULL DEFAULT 4 CHECK(capture_duration_seconds BETWEEN 3 AND 5),
    total_frames_captured INTEGER NOT NULL,
    
    -- Fotograma seleccionado
    selected_frame_index INTEGER,
    selected_frame_path TEXT,
    selected_frame_score REAL CHECK(selected_frame_score >= 0 AND selected_frame_score <= 1),
    
    -- Métricas de calidad del fotograma seleccionado
    sharpness REAL CHECK(sharpness >= 0 AND sharpness <= 1),
    brightness REAL CHECK(brightness >= 0 AND brightness <= 1),
    contrast REAL CHECK(contrast >= 0 AND contrast <= 1),
    silhouette_visibility REAL CHECK(silhouette_visibility >= 0 AND silhouette_visibility <= 1),
    angle_score REAL CHECK(angle_score >= 0 AND angle_score <= 1),
    
    -- Timestamps
    started_at TEXT NOT NULL,
    completed_at TEXT,
    
    -- Sincronización
    sync_status TEXT DEFAULT 'pending'
);

CREATE INDEX idx_capture_sessions_animal ON capture_sessions(animal_id);
CREATE INDEX idx_capture_sessions_date ON capture_sessions(started_at DESC);
```

#### 4. senasag_reports (Reportes SENASAG - US-007)

```sql
CREATE TABLE senasag_reports (
    id TEXT PRIMARY KEY,
    farm_id TEXT NOT NULL,                  -- Hacienda Gamelera
    
    -- Tipo y período
    report_type TEXT NOT NULL CHECK(report_type IN (
        'inventario_mensual', 'movimientos_trimestrales', 'trazabilidad_animal'
    )),
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    
    -- Formato
    format TEXT NOT NULL CHECK(format IN ('pdf', 'csv', 'xml')),
    
    -- Archivo generado
    file_path TEXT NOT NULL,                -- Ruta local del archivo
    file_size_bytes INTEGER,
    
    -- Metadatos
    total_animals INTEGER NOT NULL,         -- Animales incluidos en reporte
    generated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    -- Envío
    sent_to_email TEXT,
    sent_at TEXT,
    status TEXT NOT NULL DEFAULT 'generated' CHECK(status IN (
        'generated', 'sent', 'confirmed', 'failed'
    )),
    
    -- Sincronización
    sync_status TEXT DEFAULT 'pending'
);

CREATE INDEX idx_senasag_reports_farm ON senasag_reports(farm_id);
CREATE INDEX idx_senasag_reports_date ON senasag_reports(generated_at DESC);
CREATE INDEX idx_senasag_reports_type ON senasag_reports(report_type);
```

#### 5. gmas (Guías de Movimiento Animal - US-008)

```sql
CREATE TABLE gmas (
    id TEXT PRIMARY KEY,
    gma_number TEXT NOT NULL UNIQUE,        -- ej: "GMA-2024-001234"
    
    -- Hacienda origen
    origin_farm_id TEXT NOT NULL,           -- Hacienda Gamelera
    origin_location_lat REAL NOT NULL,      -- -15.859500
    origin_location_lon REAL NOT NULL,      -- -60.797889
    
    -- Destino
    destination_name TEXT NOT NULL,
    destination_location_lat REAL,
    destination_location_lon REAL,
    
    -- Movimiento
    movement_reason TEXT NOT NULL CHECK(movement_reason IN (
        'venta', 'traslado', 'sacrificio', 'exposicion'
    )),
    movement_date TEXT NOT NULL,
    
    -- Animales incluidos (lista de IDs separados por coma)
    animal_ids TEXT NOT NULL,               -- ej: "id1,id2,id3"
    total_animals INTEGER NOT NULL,
    
    -- Cumplimiento REGENSA (capítulos 3.10 y 7.1)
    chapter_3_10_compliant INTEGER NOT NULL DEFAULT 1,
    chapter_7_1_compliant INTEGER NOT NULL DEFAULT 1,
    infrastructure_notes TEXT,              -- Datos de rampas, corrales, etc.
    veterinary_notes TEXT,                  -- Control veterinario
    
    -- Código QR
    qr_code_data TEXT NOT NULL,             -- Datos codificados en QR
    qr_code_image_path TEXT,                -- Imagen PNG del QR
    
    -- Estado
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN (
        'pending', 'approved', 'rejected', 'completed'
    )),
    
    -- Timestamps
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    approved_at TEXT,
    completed_at TEXT,
    
    -- Sincronización
    synced_to_gran_paititi INTEGER DEFAULT 0,
    gran_paititi_sync_at TEXT
);

CREATE INDEX idx_gmas_number ON gmas(gma_number);
CREATE INDEX idx_gmas_origin_farm ON gmas(origin_farm_id);
CREATE INDEX idx_gmas_status ON gmas(status);
CREATE INDEX idx_gmas_date ON gmas(created_at DESC);
```

### Relaciones entre Tablas SQLite

```
animals (1) ──────< weighings (N)
   │                   │
   │                   └─── capture_sessions (1)
   │
   ├──────< senasag_reports (N) [via farm_id]
   │
   └──────< gmas (N) [via animal_ids JSON array]
```

---

## MongoDB Schema (Backend - Cloud)

### Collections

#### 1. animals (Collection)

```javascript
// Ejemplo de documento en MongoDB

{
  "_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",  // UUID
  "tag_number": "HG-BRA-001",                      // Único en Hacienda Gamelera
  
  // Datos principales (7 razas, 4 categorías)
  "breed_type": "brahman",                         // Enum: solo 7 valores
  "birth_date": ISODate("2020-03-15T00:00:00Z"),
  "gender": "female",
  "status": "active",                              // active, inactive, sold, dead
  
  // Campos opcionales
  "color": "Rojo",
  "weight_at_birth_kg": 35.5,
  "mother_id": "uuid-madre",
  "father_id": "uuid-padre",
  "observations": "Primera cría de vaca HG-MAD-001",
  
  // Campos calculados (no almacenados, calculados en query)
  "age_months": 56,                                // Calculado desde birth_date
  "age_category": "vacas_toros",                   // Calculado desde age_months
  
  // Peso actual (desnormalizado para performance)
  "latest_weight_kg": 487.3,
  "latest_weighing_date": ISODate("2024-10-28T10:30:00Z"),
  "latest_confidence": 0.97,
  
  // ASOCEBU (US-009)
  "asocebu_registered": true,
  "asocebu_id": "ASOC-12345",
  "competition_history": [
    {
      "event_name": "3ª Faena Técnica 2024",
      "date": ISODate("2024-09-15"),
      "category": "Mejor lote de carcasas de hembras en confinamiento",
      "award": "Medalla de Bronce",
      "weight_at_event_kg": 485.0
    }
  ],
  
  // Metadatos
  "farm_id": "farm-gamelera-001",
  "created_at": ISODate("2024-01-15T08:00:00Z"),
  "updated_at": ISODate("2024-10-28T10:30:00Z"),
  "created_by_user_id": "user-bruno-001"
}
```

**Índices MongoDB**:
```javascript
// Índice único en tag_number
db.animals.createIndex(
    { "tag_number": 1 },
    { unique: true, name: "idx_tag_number_unique" }
);

// Índice compuesto para búsqueda (US-006)
db.animals.createIndex(
    { "farm_id": 1, "breed_type": 1, "status": 1 },
    { name: "idx_search_animals" }
);

// Índice para filtros por raza
db.animals.createIndex(
    { "breed_type": 1 },
    { name: "idx_breed_type" }
);

// Índice para filtros por estado
db.animals.createIndex(
    { "status": 1 },
    { name: "idx_status" }
);

// Índice text search para búsqueda por caravana
db.animals.createIndex(
    { "tag_number": "text", "observations": "text" },
    { name: "idx_text_search" }
);
```

**Validación con Beanie**:
```python
# backend/app/database/models.py

from beanie import Document, Indexed
from pydantic import Field, field_validator
from datetime import datetime
from uuid import UUID

from ..core.constants.breeds import BreedType
from ..core.constants.age_categories import AgeCategory

class AnimalModel(Document):
    """
    Modelo MongoDB para Animal usando Beanie ODM.
    
    Validaciones:
    - breed_type: Solo 7 razas de Hacienda Gamelera
    - tag_number: Único por hacienda
    - birth_date: No futura
    - weight_at_birth_kg: Entre 15-60 kg realista
    """
    
    id: UUID = Field(default_factory=uuid4, alias="_id")
    tag_number: Indexed(str, unique=True)
    
    breed_type: Indexed(BreedType)  # Pydantic valida automáticamente
    birth_date: datetime
    gender: str  # "male" o "female"
    status: Indexed(str) = "active"
    
    # Opcionales
    color: Optional[str] = None
    weight_at_birth_kg: Optional[float] = Field(None, ge=15.0, le=60.0)
    mother_id: Optional[UUID] = None
    father_id: Optional[UUID] = None
    observations: Optional[str] = None
    
    # Peso actual (desnormalizado)
    latest_weight_kg: Optional[float] = None
    latest_weighing_date: Optional[datetime] = None
    latest_confidence: Optional[float] = None
    
    # ASOCEBU
    asocebu_registered: bool = False
    asocebu_id: Optional[str] = None
    
    # Metadatos
    farm_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    class Settings:
        name = "animals"
        indexes = [
            "tag_number",
            "breed_type",
            "status",
            "farm_id",
            [("farm_id", 1), ("breed_type", 1), ("status", 1)],  # Compuesto
        ]
    
    @field_validator("breed_type")
    @classmethod
    def validate_breed(cls, v: BreedType) -> BreedType:
        """Valida que sea una de las 7 razas de Hacienda Gamelera."""
        if not BreedType.is_valid(v.value):
            raise ValueError(f"Raza inválida: {v.value}")
        return v
    
    @property
    def age_months(self) -> int:
        """Calcula edad en meses desde birth_date."""
        now = datetime.now()
        return (now.year - self.birth_date.year) * 12 + (now.month - self.birth_date.month)
    
    @property
    def age_category(self) -> AgeCategory:
        """Categoría de edad calculada (una de las 4)."""
        return AgeCategory.from_birth_date(self.birth_date)
```

#### 2. weighings (Collection)

```javascript
{
  "_id": "w1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "animal_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  
  // Datos de estimación
  "estimated_weight_kg": 487.3,
  "confidence": 0.97,                              // ✅ ≥0.95 requerido
  
  // Métricas del sistema
  "processing_time_ms": 2543,                      // ✅ <3000ms requerido
  "meets_precision_threshold": true,
  "meets_time_threshold": true,
  
  // Contexto
  "method": "ia",                                  // ia, manual, bascula
  "breed_model_version": "v1.0.0",                 // Modelo TFLite usado
  "breed_type": "brahman",                         // Desnormalizado para queries
  
  // Captura
  "capture_session_id": "cs-uuid",
  "image_path": "s3://images/brahman/img_123.jpg",
  "frame_metadata": {
    "sharpness": 0.89,
    "brightness": 0.72,
    "contrast": 0.65,
    "silhouette_visibility": 0.93,
    "angle_score": 0.78,
    "global_score": 0.85                           // Score ponderado
  },
  
  // Ubicación GPS (donde se capturó)
  "location": {
    "type": "Point",
    "coordinates": [-60.797889, -15.859500]        // [lon, lat] GeoJSON
  },
  
  // Timestamps
  "weighing_date": ISODate("2024-10-28T10:30:00Z"),
  "created_at": ISODate("2024-10-28T10:30:05Z"),
  
  // Validación
  "validated_by_user_id": "user-bruno-001",
  "validated_at": ISODate("2024-10-28T10:31:00Z"),
  
  // Sincronización
  "synced_from_device": "mobile-android-bruno-phone",
  "synced_at": ISODate("2024-10-28T11:00:00Z")
}
```

**Índices MongoDB**:
```javascript
// Índice por animal para historial (US-004)
db.weighings.createIndex(
    { "animal_id": 1, "weighing_date": -1 },
    { name: "idx_animal_history" }
);

// Índice geoespacial para pesajes por ubicación
db.weighings.createIndex(
    { "location": "2dsphere" },
    { name: "idx_location" }
);

// Índice para filtrar por método
db.weighings.createIndex(
    { "method": 1, "weighing_date": -1 },
    { name: "idx_method_date" }
);

// Índice compuesto para análisis por raza
db.weighings.createIndex(
    { "breed_type": 1, "weighing_date": -1 },
    { name: "idx_breed_analysis" }
);
```

#### 3. senasag_reports (Collection)

```javascript
{
  "_id": "r1b2c3d4-uuid",
  "farm_id": "farm-gamelera-001",
  
  // Tipo y período
  "report_type": "inventario_mensual",
  "period_start": ISODate("2024-10-01T00:00:00Z"),
  "period_end": ISODate("2024-10-31T23:59:59Z"),
  
  // Formato generado
  "format": "pdf",
  
  // Archivo
  "file_path": "senasag-reports/farm-gamelera-001/2024-10-28_inventario.pdf",
  "file_size_bytes": 892160,                       // ~872 KB
  "s3_bucket": "bovine-reports-production",
  "s3_key": "senasag/2024-10/hacienda-gamelera-inventario.pdf",
  
  // Contenido del reporte
  "summary": {
    "total_animals": 500,
    "by_breed": {
      "brahman": 150,
      "nelore": 120,
      "angus": 80,
      "cebuinas": 70,
      "criollo": 40,
      "pardo_suizo": 30,
      "jersey": 10
    },
    "by_age_category": {
      "terneros": 45,
      "vaquillonas_torillos": 120,
      "vaquillonas_toretes": 135,
      "vacas_toros": 200
    },
    "average_weight_kg": 425.7,
    "total_weighings_period": 243
  },
  
  // Generación
  "generated_at": ISODate("2024-10-28T14:30:00Z"),
  "generated_by_user_id": "user-bruno-001",
  
  // Envío
  "sent_to_emails": ["bruno@haciendagamelera.com", "senasag@gov.bo"],
  "sent_at": ISODate("2024-10-28T14:32:00Z"),
  "status": "sent",
  
  // Validación
  "validated_structure": true,                     // Contra spec SENASAG
  "validation_errors": []
}
```

#### 4. gmas (Collection)

```javascript
{
  "_id": "g1b2c3d4-uuid",
  "gma_number": "GMA-2024-001234",                 // Número único
  
  // Origen (Hacienda Gamelera)
  "origin": {
    "farm_id": "farm-gamelera-001",
    "farm_name": "Hacienda Gamelera",
    "owner_name": "Bruno Brito Macedo",
    "location": {
      "type": "Point",
      "coordinates": [-60.797889, -15.859500]      // [lon, lat]
    },
    "address": "San Ignacio de Velasco, Santa Cruz, Bolivia"
  },
  
  // Destino
  "destination": {
    "name": "Frigorífico BFC S.A.",
    "location": {
      "type": "Point",
      "coordinates": [-60.7899, -15.8595]
    },
    "address": "San Ignacio de Velasco"
  },
  
  // Movimiento
  "movement": {
    "reason": "venta",                             // venta, traslado, sacrificio, exposicion
    "date": ISODate("2024-11-05T08:00:00Z"),
    "transport_details": "Camión GAM-TRUCK-01"
  },
  
  // Animales incluidos
  "animals": [
    {
      "animal_id": "uuid-animal-1",
      "tag_number": "HG-BRA-045",
      "breed_type": "brahman",
      "current_weight_kg": 520.5,
      "age_category": "vacas_toros"
    },
    {
      "animal_id": "uuid-animal-2",
      "tag_number": "HG-NEL-032",
      "breed_type": "nelore",
      "current_weight_kg": 495.2,
      "age_category": "vacas_toros"
    }
    // ... más animales
  ],
  "total_animals": 10,
  
  // Cumplimiento REGENSA (capítulos 3.10 y 7.1)
  "regensa_compliance": {
    "chapter_3_10": {
      "compliant": true,
      "ramp_width_meters": 1.8,                    // ≥1.6m requerido
      "space_per_animal_m2": 2.5,                  // ≥2m² requerido
      "has_disinfection_system": true,
      "has_quarantine_corral": true
    },
    "chapter_7_1": {
      "compliant": true,
      "veterinary_inspection": true,
      "veterinarian_name": "Dr. José Pérez",
      "veterinarian_license": "VET-SC-12345",
      "inspection_date": ISODate("2024-11-04T10:00:00Z")
    }
  },
  
  // Código QR para verificación digital
  "qr_code": {
    "data": "GMA-2024-001234|farm-gamelera-001|2024-11-05|10-animals",
    "image_url": "s3://gmas/qr-codes/GMA-2024-001234.png",
    "format": "QR_CODE_128"
  },
  
  // Estado y tracking
  "status": "approved",                            // pending, approved, rejected, completed
  "status_history": [
    {
      "status": "pending",
      "timestamp": ISODate("2024-11-01T10:00:00Z"),
      "user_id": "user-bruno-001"
    },
    {
      "status": "approved",
      "timestamp": ISODate("2024-11-03T14:30:00Z"),
      "user_id": "admin-senasag-001",
      "notes": "Aprobado por SENASAG"
    }
  ],
  
  // Integración Gran Paitití (US-008)
  "gran_paititi_integration": {
    "synced": true,
    "sync_timestamp": ISODate("2024-11-03T14:35:00Z"),
    "gran_paititi_id": "GP-2024-SC-001234",
    "sync_status": "success",
    "api_response_code": 200
  },
  
  // Timestamps
  "created_at": ISODate("2024-11-01T10:00:00Z"),
  "approved_at": ISODate("2024-11-03T14:30:00Z"),
  "completed_at": null
}
```

**Índices MongoDB GMAs**:
```javascript
// Índice único en gma_number
db.gmas.createIndex(
    { "gma_number": 1 },
    { unique: true, name: "idx_gma_number_unique" }
);

// Índice por hacienda origen
db.gmas.createIndex(
    { "origin.farm_id": 1, "created_at": -1 },
    { name: "idx_origin_farm_date" }
);

// Índice geoespacial
db.gmas.createIndex(
    { "origin.location": "2dsphere" },
    { name: "idx_origin_location" }
);

// Índice por estado
db.gmas.createIndex(
    { "status": 1 },
    { name: "idx_status" }
);

// Índice para sincronización Gran Paitití
db.gmas.createIndex(
    { "gran_paititi_integration.synced": 1 },
    { name: "idx_gran_paititi_sync" }
);
```

---

## Seed Data (Datos Iniciales)

### Seed Data SQLite (Mobile)

```sql
-- mobile/assets/database/seed.sql

-- 1. Insertar 7 razas como referencia (opcional, Enums ya validan)
-- Datos de Hacienda Gamelera

INSERT INTO animals (id, tag_number, breed_type, birth_date, gender, color, farm_id) VALUES
-- Brahman (150 animales - 30%)
('uuid-bra-001', 'HG-BRA-001', 'brahman', '2020-03-15T00:00:00Z', 'female', 'Rojo', 'farm-gamelera'),
('uuid-bra-002', 'HG-BRA-002', 'brahman', '2021-05-20T00:00:00Z', 'male', 'Rojo', 'farm-gamelera'),
-- ... hasta HG-BRA-150

-- Nelore (120 animales - 24%)
('uuid-nel-001', 'HG-NEL-001', 'nelore', '2020-07-10T00:00:00Z', 'female', 'Gris', 'farm-gamelera'),
-- ... hasta HG-NEL-120

-- Angus (80 animales - 16%)
('uuid-ang-001', 'HG-ANG-001', 'angus', '2021-02-20T00:00:00Z', 'male', 'Negro', 'farm-gamelera'),
-- ... hasta HG-ANG-080

-- Cebuinas (70 animales - 14%)
-- Criollo (40 animales - 8%)
-- Pardo Suizo (30 animales - 6%)
-- Jersey (10 animales - 2%)
-- TOTAL: 500 animales
;
```

### Seed Data MongoDB (Backend)

```python
# backend/app/database/seed_data.py

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from uuid import uuid4

from ..core.constants.breeds import BreedType
from ..core.constants.hacienda_constants import HaciendaConstants

async def seed_hacienda_gamelera_data(db: AsyncIOMotorClient):
    """
    Seed data para Hacienda Gamelera (Bruno Brito Macedo).
    
    Inserta:
    - Farm (Hacienda Gamelera)
    - User (Bruno Brito Macedo)
    - 500 animales distribuidos en 7 razas
    - Pesajes históricos de ejemplo
    """
    
    # 1. Crear Hacienda Gamelera
    farm_id = uuid4()
    await db.farms.insert_one({
        "_id": str(farm_id),
        "name": HaciendaConstants.HACIENDA_NAME,
        "owner_name": HaciendaConstants.OWNER_NAME,
        "location": {
            "type": "Point",
            "coordinates": [
                HaciendaConstants.LONGITUDE,
                HaciendaConstants.LATITUDE,
            ]
        },
        "city": HaciendaConstants.CITY,
        "department": HaciendaConstants.DEPARTMENT,
        "country": HaciendaConstants.COUNTRY,
        "extension_hectares": HaciendaConstants.EXTENSION_HECTARES,
        "animal_capacity": HaciendaConstants.ANIMAL_CAPACITY,
        "created_at": datetime.now(),
    })
    
    # 2. Crear usuario Bruno Brito Macedo
    user_bruno_id = uuid4()
    await db.users.insert_one({
        "_id": str(user_bruno_id),
        "email": "bruno@haciendagamelera.com",
        "name": "Bruno Brito Macedo",
        "role": "owner",
        "farm_id": str(farm_id),
        "created_at": datetime.now(),
    })
    
    # 3. Crear 500 animales distribuidos en 7 razas
    breed_distribution = {
        BreedType.BRAHMAN: 150,        # 30%
        BreedType.NELORE: 120,         # 24%
        BreedType.ANGUS: 80,           # 16%
        BreedType.CEBUINAS: 70,        # 14%
        BreedType.CRIOLLO: 40,         # 8%
        BreedType.PARDO_SUIZO: 30,     # 6%
        BreedType.JERSEY: 10,          # 2%
    }  # Total: 500
    
    animals = []
    for breed, count in breed_distribution.items():
        for i in range(count):
            animal_id = uuid4()
            
            # Fecha de nacimiento aleatoria (últimos 5 años)
            days_ago = random.randint(30, 1825)  # 1 mes a 5 años
            birth_date = datetime.now() - timedelta(days=days_ago)
            
            animals.append({
                "_id": str(animal_id),
                "tag_number": f"HG-{breed.value.upper()[:3]}-{i+1:03d}",
                "breed_type": breed.value,
                "birth_date": birth_date,
                "gender": random.choice(["male", "female"]),
                "status": "active",
                "farm_id": str(farm_id),
                "created_at": datetime.now(),
                "created_by_user_id": str(user_bruno_id),
            })
    
    await db.animals.insert_many(animals)
    
    print(f"✅ Seed completado:")
    print(f"   - Farm: {HaciendaConstants.HACIENDA_NAME}")
    print(f"   - Owner: {HaciendaConstants.OWNER_NAME}")
    print(f"   - Animals: {len(animals)}/500")
    print(f"   - Breeds: {len(breed_distribution)}/7")
```

---

## Queries Comunes

### SQLite (Mobile)

```dart
// Buscar animales por raza (US-006)
Future<List<AnimalModel>> getAnimalsByBreed(BreedType breed) async {
  final db = await database;
  final List<Map<String, dynamic>> maps = await db.query(
    'animals',
    where: 'breed_type = ? AND status = ?',
    whereArgs: [breed.name, 'active'],
    orderBy: 'tag_number ASC',
  );
  return List.generate(maps.length, (i) => AnimalModel.fromMap(maps[i]));
}

// Historial de pesajes de animal (US-004)
Future<List<WeighingModel>> getWeighingHistory(String animalId) async {
  final db = await database;
  final List<Map<String, dynamic>> maps = await db.query(
    'weighings',
    where: 'animal_id = ?',
    whereArgs: [animalId],
    orderBy: 'weighing_date DESC',
    limit: 100,  // Últimos 100 pesajes
  );
  return List.generate(maps.length, (i) => WeighingModel.fromMap(maps[i]));
}

// Pesajes pendientes de sincronización (US-005)
Future<List<WeighingModel>> getPendingSync() async {
  final db = await database;
  final maps = await db.query(
    'weighings',
    where: 'sync_status = ?',
    whereArgs: ['pending'],
    orderBy: 'created_at ASC',
  );
  return List.generate(maps.length, (i) => WeighingModel.fromMap(maps[i]));
}
```

### MongoDB (Backend)

```python
# Buscar animales de Hacienda Gamelera por raza
async def get_animals_by_breed(
    farm_id: UUID,
    breed_type: BreedType,
) -> list[AnimalModel]:
    """Retorna animales activos de raza específica."""
    return await AnimalModel.find(
        AnimalModel.farm_id == farm_id,
        AnimalModel.breed_type == breed_type,
        AnimalModel.status == "active",
    ).to_list()

# Generar reporte SENASAG con aggregation (US-007)
async def get_inventory_summary(
    farm_id: UUID,
    period_start: datetime,
    period_end: datetime,
) -> dict:
    """
    Genera resumen de inventario por raza para reporte SENASAG.
    
    Returns:
        {
          "total_animals": 500,
          "by_breed": {"brahman": 150, "nelore": 120, ...},
          "by_age_category": {"terneros": 45, ...},
        }
    """
    pipeline = [
        # Filtrar por hacienda y período
        {
            "$match": {
                "farm_id": str(farm_id),
                "created_at": {"$gte": period_start, "$lte": period_end},
                "status": "active",
            }
        },
        # Agrupar por raza
        {
            "$group": {
                "_id": "$breed_type",
                "count": {"$sum": 1},
                "avg_weight": {"$avg": "$latest_weight_kg"},
            }
        },
    ]
    
    result = await db.animals.aggregate(pipeline).to_list()
    
    # Formatear resultado
    by_breed = {item["_id"]: item["count"] for item in result}
    total_animals = sum(by_breed.values())
    
    return {
        "total_animals": total_animals,
        "by_breed": by_breed,
    }
```

---

## Migración y Versionado

### SQLite Migrations

```dart
// mobile/lib/core/database/migrations.dart

class DatabaseMigrations {
  /// Versión actual del esquema
  static const int currentVersion = 1;
  
  /// Ejecuta migraciones desde version anterior a actual
  static Future<void> migrate(Database db, int oldVersion, int newVersion) async {
    for (int version = oldVersion + 1; version <= newVersion; version++) {
      await _runMigration(db, version);
    }
  }
  
  static Future<void> _runMigration(Database db, int version) async {
    switch (version) {
      case 1:
        await _migrationV1(db);  // Esquema inicial
        break;
      case 2:
        await _migrationV2(db);  // Agregar campos ASOCEBU
        break;
      // Futuras migraciones...
    }
  }
  
  static Future<void> _migrationV1(Database db) async {
    // Crear tablas iniciales
    await db.execute('''
      CREATE TABLE animals (...)
    ''');
    
    await db.execute('''
      CREATE TABLE weighings (...)
    ''');
    
    // ... resto de tablas
  }
}
```

---

## Estrategia de Sincronización

### Resolución de Conflictos (Last-Write-Wins)

```dart
// mobile/lib/features/operations/data/repositories/sync_repository_impl.dart

class SyncRepositoryImpl implements SyncRepository {
  @override
  Future<SyncResult> syncAnimal(AnimalModel localAnimal) async {
    try {
      // 1. Enviar a backend con timestamp local
      final response = await _api.syncAnimal({
        ...localAnimal.toJson(),
        'client_timestamp': localAnimal.updatedAt.toIso8601String(),
      });
      
      // 2. Backend compara timestamps (last-write-wins)
      if (response.conflict) {
        if (response.serverWins) {
          // Servidor tiene versión más nueva, actualizar local
          await _localDb.updateAnimal(response.serverAnimal);
          return SyncResult.conflictResolvedServerWins;
        } else {
          // Local más nuevo, servidor ya actualizado
          return SyncResult.conflictResolvedMobileWins;
        }
      }
      
      // 3. No hubo conflicto, marcar como sincronizado
      await _localDb.markAsSynced(localAnimal.id);
      return SyncResult.success;
      
    } catch (e) {
      // Error de red, mantener como pending
      return SyncResult.failed;
    }
  }
}
```

**Backend (resolución de conflictos)**:
```python
# backend/app/services/sync_service.py

async def sync_animal(
    self,
    animal_from_mobile: dict,
    client_timestamp: datetime,
) -> SyncResponse:
    """
    Sincroniza animal con last-write-wins.
    
    Args:
        animal_from_mobile: Datos del móvil
        client_timestamp: Timestamp de última modificación en móvil
        
    Returns:
        SyncResponse indicando si hubo conflicto y quién ganó
    """
    animal_id = animal_from_mobile["id"]
    
    # 1. Buscar en MongoDB
    existing = await AnimalModel.find_one(AnimalModel.id == animal_id)
    
    if not existing:
        # No existe, crear nuevo
        new_animal = AnimalModel(**animal_from_mobile)
        await new_animal.insert()
        return SyncResponse(conflict=False, accepted=True)
    
    # 2. Comparar timestamps (UTC)
    server_timestamp = existing.updated_at or existing.created_at
    
    if client_timestamp > server_timestamp:
        # Móvil más reciente, actualizar servidor
        existing.update(animal_from_mobile)
        await existing.save()
        return SyncResponse(
            conflict=True,
            mobile_wins=True,
            server_wins=False,
        )
    else:
        # Servidor más reciente, enviar de vuelta a móvil
        return SyncResponse(
            conflict=True,
            mobile_wins=False,
            server_wins=True,
            server_animal=existing.dict(),
        )
```

---

## Performance y Optimización

### Índices Críticos para 500 Animales

**Regla general**: Índice en toda columna usada en WHERE, ORDER BY, GROUP BY

```sql
-- SQLite: Verificar que índices existen
SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='animals';

-- Debe retornar:
-- idx_animals_breed_type
-- idx_animals_status
-- idx_animals_search (compuesto)
```

```javascript
// MongoDB: Verificar índices
db.animals.getIndexes()

// Debe incluir:
// { tag_number: 1 } unique
// { farm_id: 1, breed_type: 1, status: 1 } compound
```

### Query Performance Targets

| Query | Target | Medición |
|-------|--------|----------|
| Búsqueda por caravana | <500ms | 500 animales |
| Filtro por raza | <1s | 500 animales |
| Historial animal (12 meses) | <2s | 50 pesajes |
| Generación reporte SENASAG | <5min | 500 animales |

---

## Backup y Recovery

### Backup SQLite (Mobile)

```dart
// Backup automático diario (background task)
Future<void> backupDatabase() async {
  final dbPath = await getDatabasePath();
  final backupPath = '${await getApplicationDocumentsDirectory()}/backups/bovine_${DateTime.now().millisecondsSinceEpoch}.db';
  
  await File(dbPath).copy(backupPath);
  
  // Subir a S3 cuando hay conexión
  await uploadToS3(backupPath);
}
```

### Backup MongoDB (Backend)

```bash
# Backup diario automático (cron)
0 2 * * * mongodump --uri="mongodb+srv://..." --out=/backups/$(date +\%Y\%m\%d) --gzip
```

---

## Referencias

- `docs/standards/architecture-standards.md` (Offline-first)
- `docs/design/architecture-decisions.md` (ADR-002, ADR-006, ADR-007)
- US-005: Sincronización Offline
- US-006: Búsqueda y Filtros
- US-007: Reportes SENASAG

---

**Documento de Database Schema v1.0**  
**Fecha**: 28 octubre 2024  
**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Capacidad**: 500 animales, 7 razas, historial completo

