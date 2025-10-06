# 04. Modelo de Datos

## Entidades del Sistema

### 1. Animal

**Descripción**: Representa un bovino individual en el sistema.

#### Atributos Animal

- `id` (ObjectId): Identificador único del animal
- `tag_number` (String): Número de caravana/arete
- `name` (String): Nombre del animal (opcional)
- `breed_id` (ObjectId): **Referencia a Breed** (una de las 7 razas)
- `birth_date` (Date): Fecha de nacimiento
- `age_category_id` (ObjectId): **Referencia a AgeCategory** (calculado automáticamente)
- `gender` (Enum): Sexo (Macho/Hembra)
- `color` (String): Color del animal
- `status` (Enum): Estado (Activo/Inactivo/Vendido/Muerto)
- `owner_id` (ObjectId): Referencia al propietario
- `farm_id` (ObjectId): Referencia a la finca
- `weight_goal` (Number): Meta de peso objetivo
- `asocebu_registered` (Boolean): **Si está registrado en ASOCEBU**
- `asocebu_id` (String): **ID de registro ASOCEBU**
- `competition_history` (Array): **Historial de competencias**
- `created_at` (Date): Fecha de creación
- `updated_at` (Date): Fecha de última actualización
- `metadata` (Object): Datos adicionales flexibles

#### Índices Animal

- `tag_number` (único)
- `owner_id`
- `farm_id`
- `status`
- `created_at`
- `breed_id`
- `age_category_id`

### 2. Weighing (Pesaje)

**Descripción**: Registro de estimación de peso de un animal.

#### Atributos Weighing

- `id` (ObjectId): Identificador único del pesaje
- `animal_id` (ObjectId): Referencia al animal
- `estimated_weight` (Number): Peso estimado en kg
- `confidence_score` (Number): Nivel de confianza (0-1)
- `weighing_date` (Date): Fecha del pesaje
- `weighing_method` (Enum): Método (IA/Manual/Báscula)
- `image_id` (ObjectId): Referencia a la imagen utilizada
- `capture_session_id` (ObjectId): **Referencia a sesión de captura**
- `breed_model_version` (String): **Versión del modelo usado**
- `frames_evaluated` (Number): **Fotogramas evaluados**
- `selected_frame_index` (Number): **Índice del fotograma seleccionado**
- `quality_score` (Number): **Score de calidad del fotograma seleccionado**
- `processing_time_ms` (Number): **Tiempo de procesamiento**
- `was_offline` (Boolean): **Si se procesó offline**
- `synced_at` (Date): **Cuando se sincronizó al servidor**
- `location` (GeoJSON): Ubicación GPS (opcional)
- `weather_conditions` (String): Condiciones climáticas
- `notes` (String): Notas adicionales
- `created_by` (ObjectId): Usuario que realizó el pesaje
- `created_at` (Date): Fecha de creación
- `updated_at` (Date): Fecha de última actualización

#### Índices Weighing

- `animal_id`
- `weighing_date`
- `created_by`
- `weighing_method`
- `estimated_weight`
- `capture_session_id`

### 3. Image (Imagen)

**Descripción**: Imagen capturada para estimación de peso.

#### Atributos Image

- `id` (ObjectId): Identificador único de la imagen
- `filename` (String): Nombre del archivo
- `original_path` (String): Ruta del archivo original
- `processed_path` (String): Ruta del archivo procesado
- `s3_url` (String): URL en S3 (opcional)
- `file_size` (Number): Tamaño del archivo en bytes
- `width` (Number): Ancho de la imagen
- `height` (Number): Alto de la imagen
- `format` (String): Formato de la imagen (JPEG/PNG)
- `capture_date` (Date): Fecha de captura
- `capture_session_id` (ObjectId): **Sesión a la que pertenece**
- `frame_index` (Number): **Índice en la secuencia**
- `quality_metrics` (Object): **Métricas de calidad**
  - `sharpness` (Number): **Nitidez (0-1)**
  - `brightness` (Number): **Brillo (0-1)**
  - `contrast` (Number): **Contraste (0-1)**
  - `silhouette_visibility` (Number): **Visibilidad de silueta (0-1)**
  - `angle_score` (Number): **Score de ángulo (0-1)**
  - `overall_score` (Number): **Score general (0-1)**
- `was_selected` (Boolean): **Si fue el fotograma seleccionado**
- `rejection_reason` (String): **Si fue rechazado**
- `device_info` (Object): Información del dispositivo
- `camera_settings` (Object): Configuraciones de cámara
- `processing_status` (Enum): Estado del procesamiento
- `created_by` (ObjectId): Usuario que capturó la imagen
- `created_at` (Date): Fecha de creación
- `updated_at` (Date): Fecha de última actualización

#### Índices Image

- `created_by`
- `capture_date`
- `processing_status`
- `s3_url`
- `capture_session_id`
- `was_selected`

### 4. User (Usuario)

**Descripción**: Usuario del sistema (ganadero).

#### Atributos User

- `id` (ObjectId): Identificador único del usuario
- `email` (String): Correo electrónico (único)
- `password_hash` (String): Hash de la contraseña
- `first_name` (String): Nombre
- `last_name` (String): Apellido
- `phone` (String): Teléfono
- `role` (Enum): Rol (Admin/Usuario/Invitado)
- `status` (Enum): Estado (Activo/Inactivo/Suspendido)
- `farm_name` (String): Nombre de la finca
- `farm_location` (GeoJSON): Ubicación de la finca
- `preferences` (Object): **Preferencias del usuario**
  - `ui_theme` (String): **"light" \| "dark"**
  - `text_size` (String): **"small" \| "medium" \| "large"**
  - `language` (String): **"es" \| "en"**
  - `camera_flash` (Boolean): **Flash de cámara**
  - `frame_evaluation_sensitivity` (String): **"low" \| "medium" \| "high"**
  - `measurement_unit` (String): **"kg" \| "lb" \| "arrobas"**
  - `date_format` (String): **"DD/MM/YYYY" \| "MM/DD/YYYY"**
  - `auto_sync` (Boolean): **Sincronización automática**
  - `sync_only_wifi` (Boolean): **Solo sincronizar con WiFi**
  - `push_notifications` (Boolean): **Notificaciones push**
  - `email_notifications` (Boolean): **Notificaciones email**
- `last_login` (Date): Último inicio de sesión
- `created_at` (Date): Fecha de creación
- `updated_at` (Date): Fecha de última actualización

#### Índices User

- `email` (único)
- `role`
- `status`
- `farm_location`

### 5. Meta (Metadatos)

**Descripción**: Metadatos del sistema y configuraciones.

#### Atributos Meta

- `id` (ObjectId): Identificador único
- `key` (String): Clave del metadato
- `value` (Mixed): Valor del metadato
- `type` (String): Tipo de dato (String/Number/Boolean/Object)
- `category` (String): Categoría (System/User/ML/Config)
- `description` (String): Descripción del metadato
- `is_public` (Boolean): Si es público o privado
- `created_at` (Date): Fecha de creación
- `updated_at` (Date): Fecha de última actualización

#### Índices Meta

- `key` (único)
- `category`
- `is_public`

### 6. Alert (Alerta)

**Descripción**: Alertas y recordatorios del sistema.

#### Atributos Alert

- `id` (ObjectId): Identificador único de la alerta
- `user_id` (ObjectId): Referencia al usuario
- `animal_id` (ObjectId): Referencia al animal (opcional)
- `type` (Enum): **Tipo de alerta**
  - `Pesaje` | `Recordatorio` | `Sistema` |
  - `PerdidaPeso` | `BajoRendimiento` | `Estancamiento` |
  - `Vacunacion` | `RevisionVeterinaria` | `Inseminacion` |
  - `Competencia` | `SincronizacionFallida` | `ModeloActualizado`
- `title` (String): Título de la alerta
- `message` (String): Mensaje de la alerta
- `priority` (Enum): Prioridad (Baja/Media/Alta/Crítica)
- `status` (Enum): Estado (Pendiente/Enviada/Leída/Archivada)
- `scheduled_date` (Date): Fecha programada
- `sent_date` (Date): Fecha de envío
- `read_date` (Date): Fecha de lectura
- `action_required` (Boolean): Si requiere acción
- `action_url` (String): URL de acción (opcional)
- `created_at` (Date): Fecha de creación
- `updated_at` (Date): Fecha de última actualización

#### Índices Alert

- `user_id`
- `animal_id`
- `type`
- `status`
- `scheduled_date`
- `priority`

### 7. Farm (Finca)

**Descripción**: Hacienda o finca ganadera.

#### Atributos Farm

- `id` (ObjectId): Identificador único de la finca
- `name` (String): Nombre de la finca (ej: "Hacienda Gamelera")
- `location` (GeoJSON): Ubicación GPS de la finca
- `address` (String): Dirección completa
- `city` (String): Ciudad (ej: "San Ignacio de Velasco")
- `state` (String): Departamento (ej: "Santa Cruz")
- `country` (String): País (ej: "Bolivia")
- `owner_id` (ObjectId): Referencia al propietario
- `area_hectares` (Number): Área en hectáreas
- `total_animals` (Number): Total de animales
- `senasag_registered` (Boolean): **Registrada en SENASAG**
- `regensa_compliant` (Boolean): **Cumple REGENSA**
- `gran_paititi_id` (String): **ID en Sistema Gran Paitití**
- `created_at` (Date): Fecha de creación
- `updated_at` (Date): Fecha de última actualización

#### Índices Farm

- `owner_id`
- `location` (geoespacial)
- `name`

### 8. CaptureSession (Sesión de Captura)

**Descripción**: Sesión de captura continua de fotogramas.

#### Atributos CaptureSession

- `id` (ObjectId): Identificador único de la sesión
- `animal_id` (ObjectId): Referencia al animal
- `start_time` (Date): Inicio de captura
- `end_time` (Date): Fin de captura
- `total_frames` (Number): Total de fotogramas capturados
- `frames_evaluated` (Number): Fotogramas evaluados
- `frames_rejected` (Number): Fotogramas rechazados
- `selected_frame_id` (ObjectId): Fotograma seleccionado
- `average_quality_score` (Number): Score promedio de calidad
- `rejection_reasons` (Map): Mapa de razones de rechazo
- `device_info` (Object): Información del dispositivo
- `created_by` (ObjectId): Usuario
- `created_at` (Date): Fecha de creación

#### Índices CaptureSession

- `animal_id`
- `created_by`
- `start_time`

### 9. Breed (Raza Bovina)

**Descripción**: Información de razas bovinas soportadas por el sistema.

#### Atributos Breed

- `id` (ObjectId): Identificador único de la raza
- `name` (Enum): **Nombre de la raza**
  - `Brahman` | `Nelore` | `Angus` | `Cebuinas` | `Criollo` | `Pardo Suizo` | `Jersey`
- `scientific_name` (String): Nombre científico (Bos indicus / Bos taurus)
- `model_version` (String): Versión del modelo ML actual
- `model_url` (String): URL del modelo en S3
- `weight_ranges` (Object): **Rangos de peso por categoría de edad**
  - `ternero` (Object): {min: Number, max: Number} // <8 meses
  - `joven` (Object): {min: Number, max: Number} // 6-18 meses
  - `adulto` (Object): {min: Number, max: Number} // >18 meses
- `growth_rate_avg` (Number): Tasa de crecimiento promedio (kg/día)
- `characteristics` (Array): Características físicas distintivas
- `is_active` (Boolean): Si está activa en el sistema
- `created_at` (Date): Fecha de creación
- `updated_at` (Date): Fecha de última actualización

#### Índices Breed

- `name` (único)
- `is_active`
- `model_version`

### 10. AgeCategory (Categoría de Edad)

**Descripción**: Categorías de edad para clasificación de bovinos.

#### Atributos AgeCategory

- `id` (ObjectId): Identificador único
- `name` (Enum): **Nombre de la categoría**
  - `Ternero` | `VaquillonaTorillo` | `VaquillonaTorete` | `VacaToro`
- `age_min_months` (Number): Edad mínima en meses
- `age_max_months` (Number): Edad máxima en meses
- `description` (String): Descripción de la categoría
- `gender_specific` (Boolean): Si es específica por género
- `created_at` (Date): Fecha de creación

#### Índices AgeCategory

- `name` (único)
- `age_min_months`
- `age_max_months`

### 11. SENASAGReport (Reporte SENASAG)

**Descripción**: Reporte generado para SENASAG.

#### Atributos SENASAGReport

- `id` (ObjectId): Identificador único del reporte
- `farm_id` (ObjectId): Referencia a la finca
- `report_type` (Enum): Tipo de reporte (Inventario/Movilización/Sanitario)
- `period_start` (Date): Inicio del período
- `period_end` (Date): Fin del período
- `total_animals` (Number): Total de animales en el reporte
- `data` (Object): Datos del reporte
- `pdf_url` (String): URL del PDF generado
- `csv_url` (String): URL del CSV generado
- `status` (Enum): Estado (Pendiente/Generado/Enviado)
- `sent_at` (Date): Fecha de envío
- `created_by` (ObjectId): Usuario
- `created_at` (Date): Fecha de creación

#### Índices SENASAGReport

- `farm_id`
- `report_type`
- `status`
- `created_at`

### 12. GMA (Guía de Movimiento Animal)

**Descripción**: Guía de Movimiento Animal para REGENSA.

#### Atributos GMA

- `id` (ObjectId): Identificador único
- `gma_number` (String): Número de GMA (único)
- `animal_ids` (Array): Referencias a animales
- `origin_farm_id` (ObjectId): Finca de origen
- `destination` (String): Destino del movimiento
- `reason` (Enum): Razón (Venta/Feria/Matadero/Traslado)
- `departure_date` (Date): Fecha de salida
- `arrival_date` (Date): Fecha estimada de llegada
- `gran_paititi_id` (String): ID en Sistema Gran Paitití
- `regensa_compliance` (Object): Cumplimiento REGENSA
  - `chapter_3_10_compliant` (Boolean)
  - `chapter_7_1_compliant` (Boolean)
- `status` (Enum): Estado (Pendiente/Aprobada/Rechazada/Completada)
- `created_by` (ObjectId): Usuario
- `created_at` (Date): Fecha de creación

#### Índices GMA

- `gma_number` (único)
- `origin_farm_id`
- `status`
- `departure_date`

## Relaciones entre Entidades

### Relaciones Principales

#### 1. User → Animal (1:N)

- Un usuario puede tener múltiples animales
- Un animal pertenece a un solo usuario
- **Clave foránea**: `animal.owner_id` → `user.id`

#### 2. Animal → Weighing (1:N)

- Un animal puede tener múltiples pesajes
- Un pesaje pertenece a un solo animal
- **Clave foránea**: `weighing.animal_id` → `animal.id`

#### 3. Image → Weighing (1:1)

- Una imagen puede generar un pesaje
- Un pesaje utiliza una imagen
- **Clave foránea**: `weighing.image_id` → `image.id`

#### 4. User → Image (1:N)

- Un usuario puede capturar múltiples imágenes
- Una imagen es capturada por un usuario
- **Clave foránea**: `image.created_by` → `user.id`

#### 5. User → Alert (1:N)

- Un usuario puede tener múltiples alertas
- Una alerta pertenece a un usuario
- **Clave foránea**: `alert.user_id` → `user.id`

#### 6. Animal → Alert (1:N)

- Un animal puede tener múltiples alertas
- Una alerta puede estar asociada a un animal
- **Clave foránea**: `alert.animal_id` → `animal.id`

#### 7. User → Farm (1:N)

- Un usuario puede tener múltiples fincas
- Una finca pertenece a un usuario
- **Clave foránea**: `farm.owner_id` → `user.id`

#### 8. Farm → Animal (1:N)

- Una finca puede tener múltiples animales
- Un animal pertenece a una finca
- **Clave foránea**: `animal.farm_id` → `farm.id`

#### 9. Animal → CaptureSession (1:N)

- Un animal puede tener múltiples sesiones de captura
- Una sesión de captura pertenece a un animal
- **Clave foránea**: `capture_session.animal_id` → `animal.id`

#### 10. CaptureSession → Image (1:N)

- Una sesión de captura puede tener múltiples imágenes
- Una imagen pertenece a una sesión de captura
- **Clave foránea**: `image.capture_session_id` → `capture_session.id`

#### 11. Breed → Animal (1:N)

- Una raza puede tener múltiples animales
- Un animal pertenece a una raza
- **Clave foránea**: `animal.breed_id` → `breed.id`

#### 12. AgeCategory → Animal (1:N)

- Una categoría de edad puede tener múltiples animales
- Un animal pertenece a una categoría de edad
- **Clave foránea**: `animal.age_category_id` → `age_category.id`

### Relaciones Secundarias

#### 13. User → Weighing (1:N)

- Un usuario puede realizar múltiples pesajes
- Un pesaje es realizado por un usuario
- **Clave foránea**: `weighing.created_by` → `user.id`

#### 14. CaptureSession → Weighing (1:1)

- Una sesión de captura puede generar un pesaje
- Un pesaje puede estar asociado a una sesión de captura
- **Clave foránea**: `weighing.capture_session_id` → `capture_session.id`

#### 15. Farm → SENASAGReport (1:N)

- Una finca puede tener múltiples reportes SENASAG
- Un reporte SENASAG pertenece a una finca
- **Clave foránea**: `senasag_report.farm_id` → `farm.id`

#### 16. Farm → GMA (1:N)

- Una finca puede tener múltiples GMA
- Un GMA pertenece a una finca de origen
- **Clave foránea**: `gma.origin_farm_id` → `farm.id`

## Esquema MongoDB

### Colecciones

#### animals

```javascript
{
  _id: ObjectId,
  tag_number: String (único),
  name: String,
  breed_id: ObjectId, // Referencia a breeds
  birth_date: Date,
  age_category_id: ObjectId, // Referencia a age_categories
  gender: String, // "Macho" | "Hembra"
  color: String,
  status: String, // "Activo" | "Inactivo" | "Vendido" | "Muerto"
  owner_id: ObjectId,
  farm_id: ObjectId,
  weight_goal: Number,
  asocebu_registered: Boolean,
  asocebu_id: String,
  competition_history: [{
    event_name: String,
    date: Date,
    category: String,
    position: Number,
    weight_at_event: Number
  }],
  created_at: Date,
  updated_at: Date,
  metadata: Object
}
```

#### weighings

```javascript
{
  _id: ObjectId,
  animal_id: ObjectId,
  estimated_weight: Number,
  confidence_score: Number,
  weighing_date: Date,
  weighing_method: String, // "IA" | "Manual" | "Báscula"
  image_id: ObjectId,
  capture_session_id: ObjectId,
  breed_model_version: String,
  frames_evaluated: Number,
  selected_frame_index: Number,
  quality_score: Number,
  processing_time_ms: Number,
  was_offline: Boolean,
  synced_at: Date,
  location: {
    type: "Point",
    coordinates: [Number, Number]
  },
  weather_conditions: String,
  notes: String,
  created_by: ObjectId,
  created_at: Date,
  updated_at: Date
}
```

#### images

```javascript
{
  _id: ObjectId,
  filename: String,
  original_path: String,
  processed_path: String,
  s3_url: String,
  file_size: Number,
  width: Number,
  height: Number,
  format: String,
  capture_date: Date,
  capture_session_id: ObjectId,
  frame_index: Number,
  quality_metrics: {
    sharpness: Number,
    brightness: Number,
    contrast: Number,
    silhouette_visibility: Number,
    angle_score: Number,
    overall_score: Number
  },
  was_selected: Boolean,
  rejection_reason: String,
  device_info: Object,
  camera_settings: Object,
  processing_status: String, // "Pendiente" | "Procesando" | "Completado" | "Error"
  created_by: ObjectId,
  created_at: Date,
  updated_at: Date
}
```

#### users

```javascript
{
  _id: ObjectId,
  email: String (único),
  password_hash: String,
  first_name: String,
  last_name: String,
  phone: String,
  role: String, // "Admin" | "Usuario" | "Invitado"
  status: String, // "Activo" | "Inactivo" | "Suspendido"
  farm_name: String,
  farm_location: {
    type: "Point",
    coordinates: [Number, Number]
  },
  preferences: {
    ui_theme: String,
    text_size: String,
    language: String,
    camera_flash: Boolean,
    frame_evaluation_sensitivity: String,
    measurement_unit: String,
    date_format: String,
    auto_sync: Boolean,
    sync_only_wifi: Boolean,
    push_notifications: Boolean,
    email_notifications: Boolean
  },
  last_login: Date,
  created_at: Date,
  updated_at: Date
}
```

#### metas

```javascript
{
  _id: ObjectId,
  key: String (único),
  value: Mixed,
  type: String,
  category: String,
  description: String,
  is_public: Boolean,
  created_at: Date,
  updated_at: Date
}
```

#### alerts

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  animal_id: ObjectId,
  type: String, // "Pesaje" | "Recordatorio" | "Sistema" | "PerdidaPeso" | "BajoRendimiento" | "Estancamiento" | "Vacunacion" | "RevisionVeterinaria" | "Inseminacion" | "Competencia" | "SincronizacionFallida" | "ModeloActualizado"
  title: String,
  message: String,
  priority: String, // "Baja" | "Media" | "Alta" | "Crítica"
  status: String, // "Pendiente" | "Enviada" | "Leída" | "Archivada"
  scheduled_date: Date,
  sent_date: Date,
  read_date: Date,
  action_required: Boolean,
  action_url: String,
  created_at: Date,
  updated_at: Date
}
```

#### farms

```javascript
{
  _id: ObjectId,
  name: String, // Ejemplo: "Hacienda Gamelera"
  location: {
    type: "Point",
    coordinates: [Number, Number] // Ejemplo: [-60.79788889, -15.85950000] (15°51′34.2′′S, 60°47′52.4′′W)
  },
  address: String,
  city: String, // Ejemplo: "San Ignacio de Velasco"
  state: String, // Ejemplo: "Santa Cruz"
  country: String, // Ejemplo: "Bolivia"
  owner_id: ObjectId,
  area_hectares: Number, // Ejemplo: 48.5
  total_animals: Number, // Ejemplo: 500
  senasag_registered: Boolean,
  regensa_compliant: Boolean,
  gran_paititi_id: String,
  created_at: Date,
  updated_at: Date
}
```

#### capture_sessions

```javascript
{
  _id: ObjectId,
  animal_id: ObjectId,
  start_time: Date,
  end_time: Date,
  total_frames: Number,
  frames_evaluated: Number,
  frames_rejected: Number,
  selected_frame_id: ObjectId,
  average_quality_score: Number,
  rejection_reasons: Map,
  device_info: Object,
  created_by: ObjectId,
  created_at: Date
}
```

#### breeds

```javascript
{
  _id: ObjectId,
  name: String, // "Brahman" | "Nelore" | "Angus" | "Cebuinas" | "Criollo" | "Pardo Suizo" | "Jersey"
  scientific_name: String,
  model_version: String,
  model_url: String,
  weight_ranges: {
    ternero: {min: Number, max: Number},
    joven: {min: Number, max: Number},
    adulto: {min: Number, max: Number}
  },
  growth_rate_avg: Number,
  characteristics: [String],
  is_active: Boolean,
  created_at: Date,
  updated_at: Date
}
```

#### age_categories

```javascript
{
  _id: ObjectId,
  name: String, // "Ternero" | "VaquillonaTorillo" | "VaquillonaTorete" | "VacaToro"
  age_min_months: Number,
  age_max_months: Number,
  description: String,
  gender_specific: Boolean,
  created_at: Date
}
```

#### senasag_reports

```javascript
{
  _id: ObjectId,
  farm_id: ObjectId,
  report_type: String,
  period_start: Date,
  period_end: Date,
  total_animals: Number,
  data: Object,
  pdf_url: String,
  csv_url: String,
  status: String,
  sent_at: Date,
  created_by: ObjectId,
  created_at: Date
}
```

#### gmas

```javascript
{
  _id: ObjectId,
  gma_number: String (único),
  animal_ids: [ObjectId],
  origin_farm_id: ObjectId,
  destination: String,
  reason: String,
  departure_date: Date,
  arrival_date: Date,
  gran_paititi_id: String,
  regensa_compliance: {
    chapter_3_10_compliant: Boolean,
    chapter_7_1_compliant: Boolean
  },
  status: String,
  created_by: ObjectId,
  created_at: Date
}
```

### Índices Compuestos

#### Índices Compuestos Animals

- `{owner_id: 1, status: 1}`
- `{farm_id: 1, created_at: -1}`
- `{tag_number: 1, owner_id: 1}`
- `{breed_id: 1, status: 1}`
- `{age_category_id: 1, breed_id: 1}`

#### Índices Compuestos Weighings

- `{animal_id: 1, weighing_date: -1}`
- `{created_by: 1, weighing_date: -1}`
- `{weighing_method: 1, confidence_score: -1}`
- `{capture_session_id: 1, created_at: -1}`

#### Índices Compuestos Images

- `{created_by: 1, capture_date: -1}`
- `{processing_status: 1, created_at: 1}`
- `{capture_session_id: 1, frame_index: 1}`
- `{was_selected: 1, overall_score: -1}`

#### Índices Compuestos Alerts

- `{user_id: 1, status: 1, scheduled_date: 1}`
- `{animal_id: 1, type: 1, priority: -1}`

### Agregaciones Comunes

#### Crecimiento de Animal

```javascript
db.weighings.aggregate([
  { $match: { animal_id: ObjectId("...") } },
  { $sort: { weighing_date: 1 } },
  { $group: {
    _id: "$animal_id",
    weights: { $push: "$estimated_weight" },
    dates: { $push: "$weighing_date" }
  }}
])
```

#### Estadísticas por Usuario

```javascript
db.animals.aggregate([
  { $match: { owner_id: ObjectId("...") } },
  { $lookup: {
    from: "weighings",
    localField: "_id",
    foreignField: "animal_id",
    as: "weighings"
  }},
  { $group: {
    _id: "$owner_id",
    total_animals: { $sum: 1 },
    total_weighings: { $sum: { $size: "$weighings" } }
  }}
])
```

#### Animales por Encima/Debajo de Meta

```javascript
db.weighings.aggregate([
  { $lookup: {
    from: "animals",
    localField: "animal_id",
    foreignField: "_id",
    as: "animal"
  }},
  { $unwind: "$animal" },
  { $group: {
    _id: "$animal_id",
    current_weight: { $last: "$estimated_weight" },
    weight_goal: { $first: "$animal.weight_goal" }
  }},
  { $project: {
    above_goal: { $gt: ["$current_weight", "$weight_goal"] },
    difference: { $subtract: ["$current_weight", "$weight_goal"] }
  }}
])
```

#### Precisión del Sistema por Raza

```javascript
db.weighings.aggregate([
  { $lookup: {
    from: "animals",
    localField: "animal_id",
    foreignField: "_id",
    as: "animal"
  }},
  { $unwind: "$animal" },
  { $match: { weighing_method: "IA" } },
  { $group: {
    _id: "$animal.breed",
    avg_confidence: { $avg: "$confidence_score" },
    total_weighings: { $sum: 1 },
    avg_quality_score: { $avg: "$quality_score" }
  }},
  { $sort: { avg_confidence: -1 } }
])
```

#### Uso Offline vs Online

```javascript
db.weighings.aggregate([
  { $group: {
    _id: "$was_offline",
    count: { $sum: 1 },
    avg_sync_delay: { 
      $avg: { 
        $subtract: ["$synced_at", "$weighing_date"] 
      } 
    }
  }}
])
```

#### Distribución de Animales por Raza

```javascript
db.animals.aggregate([
  { $lookup: {
    from: "breeds",
    localField: "breed_id",
    foreignField: "_id",
    as: "breed"
  }},
  { $unwind: "$breed" },
  { $group: {
    _id: "$breed.name",
    count: { $sum: 1 },
    avg_weight: { $avg: "$current_weight" }
  }},
  { $sort: { count: -1 } }
])
// Resultado esperado para Hacienda Gamelera:
// Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey
```

#### Rendimiento por Categoría de Edad

```javascript
db.animals.aggregate([
  { $lookup: {
    from: "age_categories",
    localField: "age_category_id",
    foreignField: "_id",
    as: "category"
  }},
  { $unwind: "$category" },
  { $lookup: {
    from: "weighings",
    localField: "_id",
    foreignField: "animal_id",
    as: "weighings"
  }},
  { $group: {
    _id: "$category.name",
    count: { $sum: 1 },
    avg_weight: { $avg: { $last: "$weighings.estimated_weight" } },
    avg_growth_rate: { $avg: "$growth_rate" }
  }}
])
// Categorías: Ternero, VaquillonaTorillo, VaquillonaTorete, VacaToro
```

#### Cumplimiento Normativo por Finca

```javascript
db.farms.aggregate([
  { $lookup: {
    from: "gmas",
    localField: "_id",
    foreignField: "origin_farm_id",
    as: "gmas"
  }},
  { $project: {
    name: 1,
    total_animals: 1,
    regensa_compliant: 1,
    total_gmas: { $size: "$gmas" },
    pending_gmas: {
      $size: {
        $filter: {
          input: "$gmas",
          cond: { $eq: ["$$this.status", "Pendiente"] }
        }
      }
    }
  }}
])
```
