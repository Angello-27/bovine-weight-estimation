# 04. Modelo de Dominio Conceptual

## Contexto del Proyecto

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Ubicación**: San Ignacio de Velasco, Bolivia  
**Escala**: 500 cabezas de ganado bovino  
**Razas**: 7 razas específicas (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)

## Modelo de Dominio Conceptual

### Entidades Core (Confirmadas)

#### 1. Animal

**Descripción**: Bovino individual en el sistema

**Atributos críticos**:

- `id`: Identificador único
- `tag_number`: Número de caravana/arete
- `breed`: Raza bovina (una de las 7)
- `birth_date`: Fecha de nacimiento
- `gender`: Sexo (Macho/Hembra)
- `status`: Estado (Activo/Inactivo/Vendido/Muerto)

**NOTA**: Otros campos (color, peso_objetivo, etc.) emergerán según necesidad real

#### 2. Weighing

**Descripción**: Registro de estimación de peso

**Atributos críticos**:

- `id`: Identificador único
- `animal_id`: Referencia al animal
- `estimated_weight`: Peso estimado en kg
- `weighing_date`: Fecha del pesaje
- `method`: Método (IA/Manual/Báscula)
- `confidence_score`: Nivel de confianza (0-1)

**NOTA**: Campos técnicos (ML metadata, procesamiento) se definirán en implementación

#### 3. User

**Descripción**: Ganadero usuario del sistema

**Atributos críticos**:

- `id`: Identificador único
- `email`: Correo electrónico
- `name`: Nombre completo
- `farm_name`: Nombre de la finca
- `role`: Rol (Admin/Usuario)

**NOTA**: Preferencias de UI/UX emergerán según feedback de Bruno

### Entidades Normativas (Requeridas por ley)

#### 4. SENASAGReport

**Descripción**: Reportes obligatorios para SENASAG

**Atributos críticos**:

- `id`: Identificador único
- `farm_id`: Referencia a la finca
- `report_type`: Tipo de reporte
- `period_start/end`: Período del reporte
- `status`: Estado (Pendiente/Generado/Enviado)

**NOTA**: Formato específico se definirá según normativa SENASAG

#### 5. GMA (Guía de Movimiento Animal)

**Descripción**: Guía para REGENSA

**Atributos críticos**:

- `id`: Identificador único
- `gma_number`: Número único de GMA
- `animal_ids`: Referencias a animales
- `origin_farm_id`: Finca de origen
- `destination`: Destino del movimiento
- `status`: Estado (Pendiente/Aprobada/Completada)

**NOTA**: Integración con Gran Paitití se implementará cuando sea necesario

#### 6. Farm

**Descripción**: Registro de finca/hacienda

**Atributos críticos**:

- `id`: Identificador único
- `name`: Nombre (ej: "Hacienda Gamelera")
- `location`: Ubicación GPS
- `owner_id`: Referencia al propietario
- `total_animals`: Total de animales

**NOTA**: Campos de cumplimiento normativo se agregarán según validación

### Entidades Técnicas (Emergentes)

#### 7. CaptureSession

**Descripción**: Sesión de captura continua de fotogramas

**Atributos críticos**:

- `id`: Identificador único
- `animal_id`: Referencia al animal
- `start_time/end_time`: Duración de captura
- `total_frames`: Total de fotogramas capturados
- `selected_frame_id`: Fotograma seleccionado

**NOTA**: Métricas de calidad y procesamiento se definirán según algoritmo ML

#### 8. Image

**Descripción**: Fotograma capturado

**Atributos críticos**:

- `id`: Identificador único
- `filename`: Nombre del archivo
- `capture_date`: Fecha de captura
- `capture_session_id`: Sesión a la que pertenece
- `was_selected`: Si fue el fotograma seleccionado

**NOTA**: Métricas de calidad (nitidez, brillo, etc.) se implementarán según necesidad

### Entidades de Soporte (Opcionales)

#### 9. Breed

**Descripción**: Información de razas bovinas

**Atributos críticos**:

- `id`: Identificador único
- `name`: Nombre de la raza (una de las 7)
- `scientific_name`: Nombre científico
- `is_active`: Si está activa

**NOTA**: Modelos ML específicos se gestionarán por separado

#### 10. Alert

**Descripción**: Alertas y recordatorios

**Atributos críticos**:

- `id`: Identificador único
- `user_id`: Referencia al usuario
- `type`: Tipo de alerta
- `title/message`: Contenido de la alerta
- `status`: Estado (Pendiente/Enviada/Leída)

**NOTA**: Tipos específicos de alertas emergerán según feedback de Bruno

## Relaciones Principales

### Relaciones Core

1. **User → Animal** (1:N): Un usuario puede tener múltiples animales
2. **Animal → Weighing** (1:N): Un animal puede tener múltiples pesajes
3. **User → Farm** (1:N): Un usuario puede tener múltiples fincas
4. **Farm → Animal** (1:N): Una finca puede tener múltiples animales

### Relaciones Técnicas

1. **CaptureSession → Animal** (1:1): Una sesión pertenece a un animal
2. **CaptureSession → Image** (1:N): Una sesión puede tener múltiples imágenes
3. **Image → Weighing** (1:1): Una imagen puede generar un pesaje

### Relaciones Normativas

1. **Farm → SENASAGReport** (1:N): Una finca puede tener múltiples reportes
2. **Farm → GMA** (1:N): Una finca puede tener múltiples GMA
3. **GMA → Animal** (N:N): Un GMA puede incluir múltiples animales

## Validaciones por Entidad

### Sprint 1: Entidades Core

- **Animal**: ¿Bruno puede registrar animales fácilmente?
- **Weighing**: ¿Los pesajes se registran automáticamente?
- **User**: ¿La autenticación es simple y segura?

### Sprint 2: Entidades Técnicas

- **CaptureSession**: ¿La captura continua funciona en campo?
- **Image**: ¿Las imágenes se almacenan eficientemente?

### Sprint 3: Entidades Normativas

- **SENASAGReport**: ¿Los reportes cumplen normativa?
- **GMA**: ¿La integración Gran Paitití funciona?
- **Farm**: ¿Los datos de finca son completos?

## Campos Emergentes por Sprint

### Sprint 1: Mínimo Viable

```javascript
// Animal (mínimo)
{
  id: ObjectId,
  tag_number: String,
  breed: String, // Una de las 7 razas
  birth_date: Date,
  gender: String,
  status: String
}

// Weighing (mínimo)
{
  id: ObjectId,
  animal_id: ObjectId,
  estimated_weight: Number,
  weighing_date: Date,
  method: String,
  confidence_score: Number
}
```

### Sprint 2: Funcionalidad Completa

```javascript
// Agregar a Animal
{
  // ... campos Sprint 1
  color: String,
  weight_goal: Number,
  created_at: Date,
  updated_at: Date
}

// Agregar a Weighing
{
  // ... campos Sprint 1
  image_id: ObjectId,
  capture_session_id: ObjectId,
  location: GeoJSON,
  notes: String
}
```

### Sprint 3: Integración Normativa

```javascript
// Agregar a Animal
{
  // ... campos Sprint 2
  asocebu_registered: Boolean,
  asocebu_id: String,
  competition_history: Array
}

// Agregar a Weighing
{
  // ... campos Sprint 2
  breed_model_version: String,
  processing_time_ms: Number,
  was_offline: Boolean,
  synced_at: Date
}
```

## Consideraciones de Implementación

### Base de Datos

- **Tipo**: POR DEFINIR (MongoDB, PostgreSQL, SQLite)
- **Estrategia**: Emergente según necesidades de sincronización
- **Índices**: Se crearán según patrones de consulta reales

### Sincronización

- **Estrategia**: Last-write-wins (candidato inicial)
- **Conflictos**: Se resolverán según feedback de Bruno
- **Offline**: Funcionamiento completo sin conexión

### Seguridad

- **Autenticación**: JWT (candidato inicial)
- **Autorización**: Basada en roles (Admin/Usuario)
- **Encriptación**: TLS en tránsito, por definir en reposo

---

**IMPORTANTE**: Este es el modelo conceptual mínimo. Los campos específicos, tipos de datos, índices y relaciones detalladas se definen durante el desarrollo según necesidades reales.

**Próximo paso**: Sprint 1 - Implementar entidades core (Animal, Weighing, User) con campos mínimos y validar con Bruno Brito Macedo.
