# 🔌 Guía de Integración API - Backend FastAPI

**Objetivo**: Documentación completa de todos los endpoints implementados en el backend para integración con **Flutter Mobile** y **Panel Web Frontend**.

**Base URL**: `http://localhost:8000` (desarrollo) | `https://api.haciendagamelera.com` (producción)

**Versión API**: `v1`

**Autenticación**: JWT Bearer Token (excepto `/auth/login`)

---

## 📋 Índice

1. [Autenticación](#autenticación-ambos) (Ambos clientes)
2. [Endpoints Mobile](#endpoints-mobile)
3. [Endpoints Web](#endpoints-web)
4. [Endpoints Compartidos](#endpoints-compartidos-ambos)
5. [Códigos de Estado HTTP](#códigos-de-estado-http)
6. [Manejo de Errores](#manejo-de-errores)

---

## 🔐 Autenticación (Ambos)

### POST `/auth/login`

**Descripción**: Autentica un usuario y retorna un token JWT.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: No requerida

**Request Body**:
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response 200**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "admin",
  "email": "admin@hacienda.com",
  "role": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Administrador",
    "priority": "Administrador"
  },
  "role_id": "660e8400-e29b-41d4-a716-446655440001",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response 401** (Credenciales inválidas):
```json
{
  "detail": "Credenciales inválidas"
}
```

**Uso en Frontend**:
```javascript
// Guardar token para uso posterior
localStorage.setItem('access_token', response.access_token);
```

---

## 📱 Endpoints Mobile

### 🤖 Machine Learning

#### POST `/api/v1/ml/predict`

**Descripción**: Predice peso de bovino con IA **SIN guardar** en base de datos.

**Cliente**: ✅ Mobile

**Autenticación**: Opcional

**Content-Type**: `multipart/form-data`

**Request**:
- `image` (File, required): Imagen del bovino (JPEG/PNG)
- `breed` (string, required): Raza (`nelore`, `brahman`, `guzerat`, `senepol`, `girolando`, `gyr_lechero`, `sindi`)
- `animal_id` (UUID, optional): ID del animal si existe
- `device_id` (string, optional): ID del dispositivo móvil

**Response 200**:
```json
{
  "id": "2e0a53d6-86c0-4ae8-b402-ae09233861b7",
  "animal_id": null,
  "breed": "nelore",
  "estimated_weight_kg": 289.25,
  "confidence": 0.92,
  "confidence_level": "high",
  "processing_time_ms": 397,
  "ml_model_version": "1.0.0-deep_learning_tflite",
  "method": "strategy_based",
  "meets_quality_criteria": true,
  "timestamp": "2025-11-30T14:54:25.964158"
}
```

**Notas**:
- Este endpoint **NO guarda** la estimación en BD
- Úsalo para estimaciones rápidas durante la captura
- La estimación se guarda luego mediante sincronización

---

### 🔄 Sincronización

#### GET `/api/v1/sync/health`

**Descripción**: Verifica que el servicio de sincronización esté online.

**Cliente**: ✅ Mobile

**Autenticación**: No requerida

**Timeout recomendado**: 2-3 segundos

**Response 200**:
```json
{
  "status": "online",
  "database": "connected",
  "timestamp": "2024-12-20T10:30:00Z",
  "version": "1.0.0"
}
```

---

#### POST `/api/v1/sync/cattle`

**Descripción**: Sincroniza un batch de hasta 100 animales desde mobile.

**Cliente**: ✅ Mobile

**Autenticación**: No requerida (pero recomendado)

**Estrategia**: Last-Write-Wins (el dato más reciente prevalece)

**Request Body**:
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "ear_tag": "HG-BRA-001",
      "name": "Brahman #1",
      "breed": "brahman",
      "birth_date": "2022-03-15T00:00:00Z",
      "gender": "male",
      "color": "Rojo",
      "birth_weight": 35.5,
      "mother_id": null,
      "father_id": null,
      "observations": "Animal de prueba",
      "status": "active",
      "registration_date": "2024-12-20T10:00:00Z",
      "last_updated": "2024-12-20T10:30:00Z",
      "photo_path": "/storage/frames/animal_001.jpg",
      "operation": "create"
    }
  ],
  "device_id": "android-device-123",
  "sync_timestamp": "2024-12-20T10:30:00Z"
}
```

**Response 200**:
```json
{
  "success": true,
  "total_items": 1,
  "synced_count": 1,
  "failed_count": 0,
  "conflict_count": 0,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "synced",
      "message": "Animal creado exitosamente",
      "conflict_data": null,
      "synced_at": "2024-12-20T10:30:05Z"
    }
  ],
  "sync_timestamp": "2024-12-20T10:30:00Z",
  "message": "✓ 1 de 1 items sincronizados exitosamente"
}
```

**Estados posibles**:
- `synced`: Sincronizado exitosamente
- `error`: Error durante sincronización
- `conflict`: Conflicto (backend tiene versión más reciente)

---

#### POST `/api/v1/sync/weight-estimations`

**Descripción**: Sincroniza un batch de hasta 100 estimaciones de peso desde mobile.

**Cliente**: ✅ Mobile

**Autenticación**: No requerida (pero recomendado)

**Request Body**:
```json
{
  "items": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "cattle_id": "550e8400-e29b-41d4-a716-446655440000",
      "breed": "brahman",
      "estimated_weight": 487.3,
      "confidence_score": 0.97,
      "frame_image_path": "/storage/frames/estimation_001.jpg",
      "timestamp": "2024-12-20T10:25:00Z",
      "gps_latitude": -15.859500,
      "gps_longitude": -60.797889,
      "method": "tflite",
      "ml_model_version": "1.0.0",
      "processing_time_ms": 2543,
      "operation": "create"
    }
  ],
  "device_id": "android-device-123",
  "sync_timestamp": "2024-12-20T10:30:00Z"
}
```

**Response 200**:
```json
{
  "success": true,
  "total_items": 1,
  "synced_count": 1,
  "failed_count": 0,
  "conflict_count": 0,
  "results": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "status": "synced",
      "message": "Estimación creada exitosamente",
      "conflict_data": null,
      "synced_at": "2024-12-20T10:30:05Z"
    }
  ],
  "sync_timestamp": "2024-12-20T10:30:00Z",
  "message": "✓ 1 de 1 items sincronizados exitosamente"
}
```

**Notas**:
- Las estimaciones son típicamente inmutables (solo CREATE)
- Si ya existe, se marca como ya sincronizado
- Batch processing para optimizar red en zonas rurales

---

## 💻 Endpoints Web

### 🤖 Machine Learning

#### POST `/api/v1/ml/estimate`

**Descripción**: Estima peso desde imagen subida **Y guarda** automáticamente en base de datos.

**Cliente**: ✅ Web

**Autenticación**: Requerida (JWT Bearer Token)

**Content-Type**: `multipart/form-data`

**Request**:
- `image` (File, required): Imagen del bovino (JPEG/PNG/WEBP)
- `breed` (string, required): Raza
- `animal_id` (UUID, optional): ID del animal si existe

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response 200**:
```json
{
  "id": "2e0a53d6-86c0-4ae8-b402-ae09233861b7",
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "breed": "nelore",
  "estimated_weight": 289.25,
  "estimated_weight_kg": 289.25,
  "confidence_score": 0.92,
  "confidence": 0.92,
  "breed_confidence": 0.92,
  "ml_model_version": "1.0.0-deep_learning_tflite",
  "processing_time_ms": 397,
  "image_path": "web_uploads/550e8400.../cow.jpg",
  "method": "strategy_based",
  "meets_quality_criteria": true,
  "timestamp": "2025-11-30T14:54:25.964158"
}
```

**Diferencia con `/predict`**:
- `/predict` (Mobile): Solo inferencia, NO guarda
- `/estimate` (Web): Inferencia + guardado automático en BD

---

#### GET `/api/v1/ml/models/status`

**Descripción**: Obtiene información de modelos ML cargados.

**Cliente**: ✅ Web | ✅ Mobile

**Autenticación**: No requerida

**Response 200**:
```json
{
  "status": "ok",
  "total_loaded": 1,
  "breeds_loaded": ["generic"],
  "all_breeds": [
    "nelore",
    "brahman",
    "guzerat",
    "senepol",
    "girolando",
    "gyr_lechero",
    "sindi"
  ],
  "missing_breeds": [],
  "strategies": {
    "total_strategies": 2,
    "available_strategies": ["morphometric_yolo_detection"],
    "strategy_details": [
      {
        "strategy_name": "deep_learning_tflite",
        "available": true
      },
      {
        "strategy_name": "morphometric_yolo_detection",
        "available": true
      }
    ]
  },
  "available_strategies": ["deep_learning_tflite", "morphometric_yolo_detection"],
  "note": "Sistema de estrategias activo: ML entrenado + híbrido YOLO como fallback",
  "method": "strategy_based"
}
```

---

### 🏛️ Gestión de Fincas

#### POST `/farm`

**Descripción**: Crea una nueva finca.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "name": "Hacienda Gamelera",
  "owner_id": "550e8400-e29b-41d4-a716-446655440000",
  "location": "Santa Cruz, Bolivia",
  "latitude": -15.859500,
  "longitude": -60.797889,
  "capacity": 500,
  "description": "Finca ganadera especializada"
}
```

**Response 201**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "name": "Hacienda Gamelera",
  "owner_id": "550e8400-e29b-41d4-a716-446655440000",
  "location": "Santa Cruz, Bolivia",
  "latitude": -15.859500,
  "longitude": -60.797889,
  "capacity": 500,
  "total_animals": 0,
  "description": "Finca ganadera especializada",
  "created_at": "2024-12-20T10:00:00Z",
  "updated_at": "2024-12-20T10:00:00Z"
}
```

---

#### GET `/farm`

**Descripción**: Lista fincas con paginación.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Query Parameters**:
- `skip` (int, optional, default: 0): Registros a saltar
- `limit` (int, optional, default: 50, max: 100): Máximo de registros
- `owner_id` (UUID, optional): Filtrar por propietario

**Response 200**:
```json
{
  "total": 1,
  "farms": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "name": "Hacienda Gamelera",
      "owner_id": "550e8400-e29b-41d4-a716-446655440000",
      "location": "Santa Cruz, Bolivia",
      "latitude": -15.859500,
      "longitude": -60.797889,
      "capacity": 500,
      "total_animals": 0,
      "description": "Finca ganadera especializada",
      "created_at": "2024-12-20T10:00:00Z",
      "updated_at": "2024-12-20T10:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 50
}
```

---

#### GET `/farm/{farm_id}`

**Descripción**: Obtiene una finca específica.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Response 200**: Ver POST `/farm`

---

#### PUT `/farm/{farm_id}`

**Descripción**: Actualiza una finca.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Request Body**: Mismo formato que POST `/farm` (campos opcionales)

**Response 200**: Ver POST `/farm`

---

#### DELETE `/farm/{farm_id}`

**Descripción**: Elimina una finca.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Response 204**: Sin contenido

**Validaciones**: La finca no debe tener animales registrados

---

### 👥 Gestión de Usuarios

#### POST `/user`

**Descripción**: Crea un nuevo usuario.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "username": "nuevo_usuario",
  "email": "usuario@hacienda.com",
  "password": "password123",
  "role_id": "660e8400-e29b-41d4-a716-446655440001",
  "full_name": "Nombre Completo"
}
```

**Response 201**:
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440000",
  "username": "nuevo_usuario",
  "email": "usuario@hacienda.com",
  "role_id": "660e8400-e29b-41d4-a716-446655440001",
  "role": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Administrador",
    "priority": "Administrador"
  },
  "full_name": "Nombre Completo",
  "is_active": true,
  "created_at": "2024-12-20T10:00:00Z",
  "updated_at": "2024-12-20T10:00:00Z"
}
```

---

#### GET `/user`

**Descripción**: Lista usuarios con paginación.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Query Parameters**: `skip`, `limit`

**Response 200**:
```json
{
  "total": 1,
  "users": [
    {
      "id": "880e8400-e29b-41d4-a716-446655440000",
      "username": "nuevo_usuario",
      "email": "usuario@hacienda.com",
      "role_id": "660e8400-e29b-41d4-a716-446655440001",
      "role": {...},
      "full_name": "Nombre Completo",
      "is_active": true,
      "created_at": "2024-12-20T10:00:00Z",
      "updated_at": "2024-12-20T10:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 50
}
```

---

#### GET `/user/{user_id}`

**Descripción**: Obtiene un usuario específico.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Response 200**: Ver POST `/user`

---

#### PUT `/user/{user_id}`

**Descripción**: Actualiza un usuario.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Request Body**: Mismo formato que POST `/user` (campos opcionales)

**Response 200**: Ver POST `/user`

---

#### DELETE `/user/{user_id}`

**Descripción**: Elimina un usuario.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Response 204**: Sin contenido

---

### 🔑 Gestión de Roles

#### POST `/role`

**Descripción**: Crea un nuevo rol.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "name": "Veterinario",
  "priority": "Invitado"
}
```

**Response 201**:
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440000",
  "name": "Veterinario",
  "priority": "Invitado",
  "created_at": "2024-12-20T10:00:00Z",
  "updated_at": "2024-12-20T10:00:00Z"
}
```

---

#### GET `/role`

**Descripción**: Lista roles con paginación.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Query Parameters**: `skip`, `limit`

**Response 200**: Similar a otros listados

---

#### GET `/role/{role_id}`

**Descripción**: Obtiene un rol específico.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Response 200**: Ver POST `/role`

---

#### PUT `/role/{role_id}`

**Descripción**: Actualiza un rol.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Response 200**: Ver POST `/role`

---

#### DELETE `/role/{role_id}`

**Descripción**: Elimina un rol.

**Cliente**: ✅ Web

**Autenticación**: Requerida

**Response 204**: Sin contenido

---

## 🔄 Endpoints Compartidos (Ambos)

### 🐄 Gestión de Animales

#### POST `/api/v1/animals`

**Descripción**: Crea un nuevo animal.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "ear_tag": "HG-BRA-001",
  "name": "Brahman #1",
  "breed": "brahman",
  "birth_date": "2022-03-15T00:00:00Z",
  "gender": "male",
  "color": "Rojo",
  "birth_weight": 35.5,
  "mother_id": null,
  "father_id": null,
  "observations": "Animal de prueba",
  "status": "active",
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "photo_path": "/storage/frames/animal_001.jpg"
}
```

**Response 201**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "ear_tag": "HG-BRA-001",
  "name": "Brahman #1",
  "breed": "brahman",
  "birth_date": "2022-03-15T00:00:00Z",
  "gender": "male",
  "color": "Rojo",
  "birth_weight": 35.5,
  "mother_id": null,
  "father_id": null,
  "observations": "Animal de prueba",
  "status": "active",
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "photo_path": "/storage/frames/animal_001.jpg",
  "registration_date": "2024-12-20T10:00:00Z",
  "last_updated": "2024-12-20T10:00:00Z"
}
```

**Validaciones**:
- Caravana (`ear_tag`) única por hacienda
- Raza debe ser una de las 7 exactas
- Fecha de nacimiento no puede ser futura
- Género: `male` o `female`

---

#### GET `/api/v1/animals`

**Descripción**: Lista animales con filtros y paginación.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Query Parameters**:
- `page` (int, default: 1): Número de página
- `page_size` (int, default: 50, max: 100): Tamaño de página
- `farm_id` (UUID, optional): Filtrar por finca
- `breed` (string, optional): Filtrar por raza
- `gender` (string, optional): Filtrar por género
- `status` (string, optional): Filtrar por estado

**Response 200**:
```json
{
  "total": 1,
  "animals": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "ear_tag": "HG-BRA-001",
      "name": "Brahman #1",
      "breed": "brahman",
      ...
    }
  ],
  "page": 1,
  "page_size": 50
}
```

---

#### GET `/api/v1/animals/{animal_id}`

**Descripción**: Obtiene un animal específico.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Response 200**: Ver POST `/api/v1/animals`

---

#### PUT `/api/v1/animals/{animal_id}`

**Descripción**: Actualiza un animal.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Request Body**: Mismo formato que POST (campos opcionales)

**Response 200**: Ver POST `/api/v1/animals`

---

#### DELETE `/api/v1/animals/{animal_id}`

**Descripción**: Elimina un animal.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Response 204**: Sin contenido

---

#### GET `/api/v1/animals/{animal_id}/timeline`

**Descripción**: Obtiene timeline de eventos de un animal.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Response 200**:
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "events": [
    {
      "type": "registration",
      "date": "2024-12-20T10:00:00Z",
      "description": "Animal registrado"
    },
    {
      "type": "weight_estimation",
      "date": "2024-12-20T10:25:00Z",
      "description": "Peso estimado: 487.3 kg",
      "weight_kg": 487.3
    }
  ]
}
```

---

#### GET `/api/v1/animals/{animal_id}/lineage`

**Descripción**: Obtiene linaje (padre, madre, descendientes) de un animal.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Response 200**:
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "father": null,
  "mother": null,
  "offspring": []
}
```

---

### ⚖️ Historial de Pesajes

#### GET `/api/v1/weighings/animal/{animal_id}`

**Descripción**: Obtiene historial completo de pesajes de un animal.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Query Parameters**:
- `page` (int, default: 1)
- `page_size` (int, default: 50, max: 100)

**Response 200**:
```json
{
  "total": 5,
  "weighings": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "animal_id": "550e8400-e29b-41d4-a716-446655440000",
      "breed": "brahman",
      "estimated_weight_kg": 487.3,
      "confidence": 0.97,
      "ml_model_version": "1.0.0",
      "processing_time_ms": 2543,
      "timestamp": "2024-12-20T10:25:00Z"
    }
  ],
  "page": 1,
  "page_size": 50
}
```

---

#### GET `/api/v1/weighings/{weighing_id}`

**Descripción**: Obtiene una estimación específica.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Response 200**: Ver GET `/api/v1/weighings/animal/{animal_id}`

---

### 📊 Reportes (PDF/Excel)

Todos los reportes requieren **autenticación** y retornan archivos como `StreamingResponse`.

#### POST `/api/v1/reports/traceability/{animal_id}`

**Descripción**: Genera reporte de trazabilidad individual (PDF o Excel).

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "format": "pdf"  // o "excel"
}
```

**Response 200**: Archivo PDF o Excel descargable

**Headers de respuesta**:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="trazabilidad_{animal_id}.pdf"
```

---

#### POST `/api/v1/reports/inventory`

**Descripción**: Genera reporte de inventario de animales (PDF o Excel).

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "format": "excel",
  "status": "active",
  "breed": "brahman",
  "date_from": "2024-01-01T00:00:00Z",
  "date_to": "2024-12-31T23:59:59Z"
}
```

**Response 200**: Archivo PDF o Excel descargable

---

#### POST `/api/v1/reports/movements`

**Descripción**: Genera reporte de movimientos (ventas, fallecimientos).

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "format": "pdf",
  "movement_type": "sold",  // "sold", "deceased", o null (todos)
  "date_from": "2024-01-01T00:00:00Z",
  "date_to": "2024-12-31T23:59:59Z"
}
```

**Response 200**: Archivo PDF o Excel descargable

---

#### POST `/api/v1/reports/growth`

**Descripción**: Genera reporte de crecimiento y GDP.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",  // Opcional
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",  // Opcional (si no animal_id)
  "format": "excel"
}
```

**Response 200**: Archivo PDF o Excel descargable

---

### 🔔 Alertas y Cronograma

#### POST `/api/v1/alerts`

**Descripción**: Crea una nueva alerta o evento programado.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Request Body**:
```json
{
  "title": "Pesaje masivo programado",
  "description": "Pesaje mensual de hato",
  "type": "scheduled_weighing",
  "status": "pending",
  "scheduled_date": "2024-12-25T08:00:00Z",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "farm_id": "770e8400-e29b-41d4-a716-446655440000"
}
```

**Response 201**:
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440000",
  "title": "Pesaje masivo programado",
  "description": "Pesaje mensual de hato",
  "type": "scheduled_weighing",
  "status": "pending",
  "scheduled_date": "2024-12-25T08:00:00Z",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-12-20T10:00:00Z"
}
```

---

#### GET `/api/v1/alerts`

**Descripción**: Lista alertas con filtros.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Query Parameters**:
- `page` (int, default: 1)
- `page_size` (int, default: 50, max: 100)
- `user_id` (UUID, optional)
- `farm_id` (UUID, optional)
- `type` (string, optional)
- `status` (string, optional)
- `scheduled_from` (datetime, optional)
- `scheduled_to` (datetime, optional)

**Response 200**: Lista de alertas paginada

---

#### GET `/api/v1/alerts/today`

**Descripción**: Obtiene alertas programadas para el día de hoy.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Query Parameters**:
- `user_id` (UUID, optional)
- `farm_id` (UUID, optional)

**Response 200**: Lista de alertas de hoy

---

#### GET `/api/v1/alerts/upcoming`

**Descripción**: Obtiene alertas programadas para los próximos N días.

**Cliente**: ✅ Mobile | ✅ Web

**Autenticación**: Requerida

**Query Parameters**:
- `days_ahead` (int, default: 7, max: 30): Días hacia adelante
- `user_id` (UUID, optional)
- `farm_id` (UUID, optional)

**Response 200**: Lista de alertas próximas

---

## 📊 Códigos de Estado HTTP

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 | OK | Request exitoso |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Eliminación exitosa (sin body) |
| 400 | Bad Request | Request inválido (validación fallida) |
| 401 | Unauthorized | No autenticado o token inválido |
| 403 | Forbidden | Sin permisos |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error interno del servidor |

---

## ⚠️ Manejo de Errores

### Formato de Error

Todas las respuestas de error siguen este formato:

```json
{
  "detail": "Mensaje de error descriptivo"
}
```

### Ejemplos

**400 Bad Request**:
```json
{
  "detail": "Raza inválida. Válidas: ['nelore', 'brahman', 'guzerat', 'senepol', 'girolando', 'gyr_lechero', 'sindi']"
}
```

**401 Unauthorized**:
```json
{
  "detail": "No se pudo validar las credenciales"
}
```

**404 Not Found**:
```json
{
  "detail": "Animal no encontrado"
}
```

---

## 🔒 Autenticación JWT

### Cómo usar el token

Después de hacer login en `/auth/login`, guarda el `access_token` y úsalo en todas las requests que requieran autenticación:

```javascript
// Ejemplo en JavaScript/TypeScript
const token = localStorage.getItem('access_token');

fetch('http://localhost:8000/api/v1/animals', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
```

### Flutter/Dart

```dart
// Ejemplo en Flutter
final response = await dio.get(
  '/api/v1/animals',
  options: Options(
    headers: {
      'Authorization': 'Bearer $accessToken',
    },
  ),
);
```

### Tiempo de expiración

El token expira después de un tiempo configurado (por defecto: configurable en `settings.ACCESS_TOKEN_EXPIRE_MINUTES`). Si el token expira, recibirás un 401 y deberás hacer login nuevamente.

---

## 📝 Notas Importantes

1. **Timestamps**: Todos los timestamps están en formato ISO 8601 UTC (ej: `2024-12-20T10:30:00Z`)

2. **UUIDs**: Todos los IDs son UUIDs v4 (ej: `550e8400-e29b-41d4-a716-446655440000`)

3. **Paginación**: La mayoría de listados soportan paginación con `page` y `page_size`. El máximo `page_size` es generalmente 100.

4. **Razas válidas**: Solo estas 7 razas están permitidas:
   - `nelore`
   - `brahman`
   - `guzerat`
   - `senepol`
   - `girolando`
   - `gyr_lechero`
   - `sindi`

5. **Estados de animales**: `active`, `sold`, `deceased`, `inactive`

6. **Géneros**: `male`, `female`

7. **Formatos de imagen**: JPEG, PNG, WEBP (para estimaciones)

8. **Sincronización móvil**: Los endpoints de sincronización no requieren autenticación por defecto (para permitir sincronización offline), pero es recomendable implementarla en producción.

---

## 🚀 Próximos Pasos

1. **Integrar en Flutter Mobile**: Usar endpoints de ML y sincronización
2. **Integrar en Panel Web**: Usar endpoints de ML, CRUD y reportes
3. **Testing**: Probar todos los endpoints con Postman o similares
4. **Manejo de errores**: Implementar manejo robusto de errores en ambos clientes

---

**Última actualización**: 2024-12-30  
**Versión API**: 1.0.0  
**Backend**: FastAPI (Python 3.11+)

