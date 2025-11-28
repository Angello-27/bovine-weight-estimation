# Análisis de Modelos: Documentación vs Implementación

**Fecha**: 2024-12-XX  
**Objetivo**: Comparar modelos definidos en documentación vs modelos implementados en backend

---

## 📊 Resumen Ejecutivo

### Modelos Implementados ✅
- `AnimalModel` - ✅ Completo y alineado
- `WeightEstimationModel` - ✅ Completo y alineado  
- `UserModel` - ✅ Implementado (nuevo)
- `RoleModel` - ✅ Implementado (nuevo, no en doc pero necesario)

### Modelos Faltantes según Documentación ❌
- `FarmModel` - ❌ Mencionado en domain-model.md
- `CaptureSessionModel` - ❌ Mencionado en domain-model.md (opcional)
- `ImageModel` - ❌ Mencionado en domain-model.md (opcional)
- `AlertModel` - ❌ Mencionado en domain-model.md (opcional)

### Modelos Eliminados del Alcance 🚫
- `SENASAGReportModel` - 🚫 Fuera de alcance académico
- `GMAModel` - 🚫 Fuera de alcance académico

---

## 📋 Comparación Detallada

### 1. AnimalModel ✅

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  tag_number: String,
  breed: String, // Una de las 7 razas
  birth_date: Date,
  gender: String,
  status: String
}
```

**Implementación** (`animal_model.py`):
- ✅ `id` (UUID)
- ✅ `ear_tag` (equivalente a tag_number)
- ✅ `breed` (Indexed)
- ✅ `birth_date` (datetime)
- ✅ `gender` (Indexed)
- ✅ `status` (Indexed)
- ✅ Campos adicionales: `name`, `color`, `birth_weight_kg`, `mother_id`, `father_id`, `observations`, `photo_url`
- ✅ Sincronización: `device_id`, `synced_at`
- ✅ Metadata: `farm_id`, `registration_date`, `last_updated`

**Estado**: ✅ **COMPLETO Y ALINEADO** - Incluso tiene campos adicionales útiles

---

### 2. WeightEstimationModel ✅

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  animal_id: ObjectId,
  estimated_weight: Number,
  weighing_date: Date,
  method: String,
  confidence_score: Number
}
```

**Documentación** (`database-schema.md`):
```sql
CREATE TABLE weighings (
    id TEXT PRIMARY KEY,
    animal_id TEXT NOT NULL,
    estimated_weight_kg REAL NOT NULL,
    confidence REAL NOT NULL,
    processing_time_ms INTEGER,
    method TEXT CHECK(method IN ('hybrid', 'tflite', 'manual', 'bascula')),
    breed_model_version TEXT,
    latitude REAL,
    longitude REAL,
    weighing_date TEXT
);
```

**Implementación** (`weight_estimation_model.py`):
- ✅ `id` (UUID)
- ✅ `animal_id` (Indexed)
- ✅ `estimated_weight_kg` (equivalente a estimated_weight)
- ✅ `confidence` (equivalente a confidence_score)
- ✅ `method` (default "tflite")
- ✅ `model_version` (equivalente a breed_model_version)
- ✅ `processing_time_ms`
- ✅ `latitude`, `longitude`
- ✅ `timestamp` (equivalente a weighing_date)
- ✅ Campos adicionales: `breed`, `frame_image_path`
- ✅ Sincronización: `device_id`, `synced_at`

**Estado**: ✅ **COMPLETO Y ALINEADO** - Incluso tiene campos adicionales

---

### 3. UserModel ✅ (NUEVO)

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  email: String,
  name: String,              // ⚠️ FALTA en implementación
  farm_name: String,        // ⚠️ FALTA en implementación (debería ser farm_id)
  role: String              // ✅ Tenemos role_id
}
```

**Implementación** (`user_model.py`):
- ✅ `id` (UUID)
- ✅ `username` (único, no en doc pero necesario)
- ✅ `email` (Indexed, único)
- ✅ `hashed_password` (seguridad)
- ✅ `role_id` (UUID, relación con RoleModel)
- ✅ `is_active`, `is_superuser`
- ✅ Metadata: `created_at`, `last_updated`, `last_login`
- ❌ `name` - **FALTA** (mencionado en doc)
- ❌ `farm_id` - **FALTA** (mencionado como farm_name en doc, pero debería ser relación)

**Estado**: ⚠️ **PARCIALMENTE ALINEADO** - Falta `name` y relación con `farm_id`

---

### 4. RoleModel ✅ (NUEVO - No en documentación)

**Documentación**: No mencionado explícitamente, pero necesario para autenticación

**Implementación** (`role_model.py`):
- ✅ `id` (UUID)
- ✅ `name` (Indexed, único)
- ✅ `description`
- ✅ `priority` (default "Invitado")
- ✅ `permissions` (lista de strings)
- ✅ Metadata: `created_at`, `last_updated`

**Estado**: ✅ **NECESARIO Y COMPLETO** - Aunque no está en la doc, es esencial para autenticación

---

### 5. FarmModel ❌ FALTANTE

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  name: String,              // "Hacienda Gamelera"
  location: GeoJSON,         // GPS
  owner_id: ObjectId,        // Referencia al propietario
  total_animals: Number
}
```

**Documentación** (`database-schema.md` - seed data):
```javascript
{
  "_id": str(farm_id),
  "name": "Hacienda Gamelera",
  "owner": "Bruno Brito Macedo",
  "location": {"type": "Point", "coordinates": [-60.797889, -15.859500]},
  "capacity": 500,
}
```

**Estado**: ❌ **NO IMPLEMENTADO** - Mencionado en múltiples lugares de la documentación

**Campos necesarios**:
- `id` (UUID)
- `name` (String)
- `owner_id` (UUID, relación con UserModel)
- `location` (GeoJSON Point)
- `capacity` (Integer)
- `total_animals` (Integer, calculado)
- Metadata: `created_at`, `last_updated`

---

### 6. SENASAGReportModel ❌ FALTANTE

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  farm_id: ObjectId,
  report_type: String,
  period_start/end: Date,
  status: String
}
```

**Documentación** (`database-schema.md`):
```sql
CREATE TABLE senasag_reports (
    id TEXT PRIMARY KEY,
    report_type TEXT CHECK(report_type IN ('inventario_mensual', 'movimientos', 'trazabilidad')),
    period_start TEXT,
    period_end TEXT,
    format TEXT CHECK(format IN ('pdf', 'csv', 'xml')),
    file_path TEXT,
    total_animals INTEGER,
    generated_at TEXT,
    sent_to_email TEXT,
    status TEXT DEFAULT 'generated'
);
```

**Estado**: ❌ **NO IMPLEMENTADO** - Crítico para cumplimiento normativo (US-007)

**Campos necesarios**:
- `id` (UUID)
- `farm_id` (UUID, relación con FarmModel)
- `report_type` (Enum: inventario_mensual, movimientos, trazabilidad)
- `period_start`, `period_end` (datetime)
- `format` (Enum: pdf, csv, xml)
- `file_path` (String, opcional)
- `total_animals` (Integer)
- `sent_to_email` (EmailStr, opcional)
- `status` (Enum: generated, sent, failed)
- Metadata: `generated_at`, `created_at`

---

### 7. GMAModel ❌ FALTANTE

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  gma_number: String,        // "GMA-2024-001234"
  animal_ids: Array,         // Referencias a animales
  origin_farm_id: ObjectId,
  destination: String,
  status: String
}
```

**Documentación** (`database-schema.md`):
```sql
CREATE TABLE gmas (
    id TEXT PRIMARY KEY,
    gma_number TEXT UNIQUE,
    origin_farm_id TEXT,
    origin_lat REAL,
    origin_lon REAL,
    destination_name TEXT,
    movement_reason TEXT CHECK(movement_reason IN ('venta', 'traslado', 'sacrificio')),
    movement_date TEXT,
    animal_ids TEXT,         -- JSON array IDs
    qr_code_data TEXT,
    status TEXT DEFAULT 'pending'
);
```

**Documentación** (`database-schema.md` - MongoDB):
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

**Estado**: ❌ **NO IMPLEMENTADO** - Crítico para cumplimiento REGENSA (US-008)

**Campos necesarios**:
- `id` (UUID)
- `gma_number` (String, único)
- `origin_farm_id` (UUID)
- `origin_location` (GeoJSON Point)
- `destination_name` (String)
- `destination_location` (GeoJSON Point, opcional)
- `movement_reason` (Enum: venta, traslado, sacrificio)
- `movement_date` (datetime)
- `animal_ids` (List[UUID])
- `regensa_compliance` (Dict con chapter_3_10 y chapter_7_1)
- `qr_code_data` (String)
- `qr_code_image_url` (String, opcional)
- `status` (Enum: pending, approved, completed)
- `synced_to_gran_paititi` (Boolean)
- Metadata: `created_at`, `last_updated`

---

### 8. CaptureSessionModel ❌ FALTANTE

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  animal_id: ObjectId,
  start_time/end_time: Date,
  total_frames: Number,
  selected_frame_id: ObjectId
}
```

**Estado**: ❌ **NO IMPLEMENTADO** - Mencionado en domain-model pero puede ser opcional

**Nota**: Este modelo puede ser opcional si la captura se hace directamente sin sesión intermedia.

---

### 9. ImageModel ❌ FALTANTE

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  filename: String,
  capture_date: Date,
  capture_session_id: ObjectId,
  was_selected: Boolean
}
```

**Estado**: ❌ **NO IMPLEMENTADO** - Mencionado en domain-model pero puede ser opcional

**Nota**: Actualmente `WeightEstimationModel` tiene `frame_image_path` (String), lo cual puede ser suficiente si no necesitamos metadatos adicionales de imágenes.

---

### 10. AlertModel ❌ FALTANTE

**Documentación** (`04-domain-model.md`):
```javascript
{
  id: ObjectId,
  user_id: ObjectId,
  type: String,
  title/message: String,
  status: String
}
```

**Estado**: ❌ **NO IMPLEMENTADO** - Opcional, puede implementarse más adelante

---

## 🎯 Priorización de Modelos Faltantes

### 🔴 CRÍTICOS
1. **FarmModel** - Necesario para relacionar animales con hacienda

### 🟡 IMPORTANTES (Funcionalidad Core)
4. **Actualizar UserModel** - Agregar `name` y `farm_id`

### 🟢 OPCIONALES (Pueden implementarse después)
5. **CaptureSessionModel** - Solo si se necesita tracking de sesiones
6. **ImageModel** - Solo si se necesita metadata extensa de imágenes
7. **AlertModel** - Funcionalidad de alertas puede esperar

---

## 📝 Recomendaciones

### Inmediatas
1. ✅ **Crear FarmModel** - Base para relaciones
2. ✅ **Actualizar UserModel** - Agregar `name` y `farm_id`

### Futuras
5. ⏳ **Evaluar necesidad de CaptureSessionModel** - Solo si se requiere tracking detallado
6. ⏳ **Evaluar necesidad de ImageModel** - Solo si se requiere metadata extensa
7. ⏳ **Implementar AlertModel** - Cuando se requiera sistema de alertas

---

## 🔗 Relaciones Necesarias

### Actuales
- ✅ User → Role (1:N) - `UserModel.role_id`
- ✅ Animal → WeightEstimation (1:N) - `WeightEstimationModel.animal_id`

### Faltantes
- ❌ User → Farm (N:1) - `UserModel.farm_id` (FALTA)
- ❌ Farm → Animal (1:N) - `AnimalModel.farm_id` (existe pero no hay modelo Farm)

---

**Última actualización**: 2024-12-XX  
**Próximos pasos**: Implementar modelos críticos (Farm)

