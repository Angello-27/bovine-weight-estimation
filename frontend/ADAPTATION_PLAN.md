# Plan de Adaptación del Frontend - Panel Administrativo Bovino

## 📋 Resumen
Adaptar el frontend React existente (sistema de empresas/propiedades) para el proyecto de **Estimación de Peso Bovino**.

### ⚠️ Consideraciones Importantes

1. **Eliminar conceptos de compañía/propiedad**: Este proyecto NO tiene empresas ni propiedades, solo ganado y estimaciones.
2. **Sincronización**: Principalmente para app móvil (offline-first). El panel web puede mostrar estado pero no necesita sincronizar.
3. **Estimación de peso en web**: 
   - ✅ **Opción B (Decidida)**: Permitir subir imágenes y estimar desde backend
   - Requiere endpoint `/api/v1/ml/estimate` en backend
   - Requiere modelo ML en backend (TensorFlow/PyTorch)

---

## 🔄 Cambios Principales

### 1. **Configuración y Constantes**

#### `src/config/constants.js`
- ✅ Cambiar `sidebarItems` de:
  - Empresas → **Ganado (Cattle)**
  - Propiedades → **Estimaciones de Peso (Weight Estimations)**
  - Roles → **Razas (Breeds)** o **Estadísticas (Statistics)**
  - Usuarios → **Sincronización (Sync Status)**
  - Mapa → **Dashboard/Home**

#### `src/config/colors.js`
- ✅ Ya tiene los colores correctos del proyecto (#255946, #49A760, #EFB443)
- ✅ Mantener como está

#### `src/api/axiosClient.js`
- ✅ Cambiar `baseURL` a la URL del backend bovino
- ✅ Ejemplo: `http://localhost:8000` o la URL de producción

---

### 2. **Rutas (`src/config/routes.js`)**

**Eliminar:**
- `/companies` → CompanyView
- `/properties` → PropertyView
- `/role` → RoleView
- `/users` → UserView
- `/map` → MapView

**Agregar:**
- `/` → LoginView (mantener)
- `/home` o `/dashboard` → DashboardView (nuevo)
- `/cattle` → CattleView (nuevo)
- `/cattle/:id` → CattleDetailView (nuevo)
- `/weight-estimations` → WeightEstimationsView (nuevo)
- `/weight-estimations/:id` → WeightEstimationDetailView (nuevo)
- `/sync` → SyncStatusView (nuevo)
- `/statistics` → StatisticsView (nuevo, opcional)

---

### 3. **Servicios API (`src/services/`)**

**Eliminar:**
- `company/` (createCompany, getAllCompanies)
- `property/` (createProperty, getCompanyProperty, getUserProperty)
- `role/` (createRole, getAllRoles)
- `user/` (createUser)

**Crear:**
- `cattle/`
  - `getAllCattle.js` - GET `/api/v1/animals`
  - `getCattleById.js` - GET `/api/v1/animals/:id`
  - `createCattle.js` - POST `/api/v1/animals`
  - `updateCattle.js` - PUT `/api/v1/animals/:id`
  - `deleteCattle.js` - DELETE `/api/v1/animals/:id`

- `weight-estimations/`
  - `getAllWeightEstimations.js` - GET `/api/v1/weighings`
  - `getWeightEstimationById.js` - GET `/api/v1/weighings/:id`
  - `getWeightEstimationsByCattleId.js` - GET `/api/v1/weighings?cattle_id=:id`
  - `createWeightEstimation.js` - POST `/api/v1/weighings`
  - `estimateWeightFromImage.js` - POST `/api/v1/ml/estimate` (nuevo - estimación desde web)

- `sync/` (Solo lectura - la sincronización es del móvil)
  - `getSyncHealth.js` - GET `/api/v1/sync/health` (verificar estado)
  - `getSyncStats.js` - GET `/api/v1/sync/stats` (estadísticas de sincronización)
  - ~~`syncCattleBatch.js`~~ - NO necesario en web (solo móvil)
  - ~~`syncWeightEstimationsBatch.js`~~ - NO necesario en web (solo móvil)

---

### 4. **Vistas (`src/views/`)**

**Eliminar:**
- `CompanyView.js`
- `PropertyView.js`
- `MapView.js`

**Mantener (adaptar):**
- `RoleView.js` - ✅ Mantener (gestión de roles)
- `UserView.js` - ✅ Mantener (adaptar para eliminar referencias a Company)

**Crear:**
- `DashboardView.js` - Panel principal con estadísticas
- `CattleView.js` - Lista de animales con búsqueda avanzada y filtros
- `CattleDetailView.js` - **Vista completa de trazabilidad**:
  - Información general del animal
  - Timeline completo de eventos
  - Linaje (padre/madre)
  - Historial de pesos con gráfico
  - Galería de fotos
  - Generación de reportes
- `WeightEstimationsView.js` - Lista de estimaciones (del móvil y web)
- `WeightEstimationDetailView.js` - Detalle de una estimación
- `WeightEstimationFromWebView.js` - Vista para hacer estimación subiendo imagen (nuevo)
- `SyncStatusView.js` - Estado de sincronización (solo visualización)
- `StatisticsView.js` - Estadísticas y gráficos (opcional, puede integrarse en Dashboard)

---

### 5. **Templates (`src/templates/`)**

**Eliminar:**
- `CompanyTemplate.js`
- `PropertyTemplate.js`
- `MapTemplate.js`

**Mantener (adaptar):**
- `RoleTemplate.js` - ✅ Mantener
- `UserTemplate.js` - ✅ Mantener (adaptar para eliminar referencias a Company)

**Crear:**
- `DashboardTemplate.js` - Template para dashboard
- `CattleTemplate.js` - Template para gestión de ganado
- `WeightEstimationTemplate.js` - Template para estimaciones
- `SyncStatusTemplate.js` - Template para sincronización

---

### 6. **Organisms (`src/components/organisms/`)**

**Eliminar:**
- `CreateCompany/`
- `CreateProperty/`

**Mantener (adaptar):**
- `CreateRole/` - ✅ Mantener
- `CreateUser/` - ✅ Mantener (adaptar para eliminar referencias a Company)

**Crear:**
- `CreateCattle/` - Formulario para crear/editar animal
- `CreateWeightEstimation/` - Formulario para estimación desde web (upload de imagen)
- `CattleList/` - Lista de animales con filtros y búsqueda avanzada
- `CattleTraceabilityTimeline/` - Timeline visual de eventos del animal
- `CattleLineageTree/` - Árbol genealógico (padre/madre/hijos)
- `CattleWeightHistoryChart/` - Gráfico de evolución de peso
- `CattleReportGenerator/` - Generador de reportes PDF/CSV/Excel
- `WeightEstimationList/` - Lista de estimaciones (solo lectura, con filtros)
- `SyncStatusCard/` - Card de estado de sincronización (solo visualización)
- `StatisticsCards/` - Cards de estadísticas (total animales, peso promedio, razas, etc.)

---

### 7. **Containers (`src/containers/`)**

**Eliminar:**
- `company/`
- `property/`
- `role/`
- `user/`

**Crear:**
- `cattle/`
  - `GetAllCattle.js` - Container para listar animales
  - `GetCattleById.js` - Container para detalle de animal
  - `GetCattleLineage.js` - Container para linaje (padres/hijos)
  - `GetCattleTimeline.js` - Container para timeline de eventos
  - `CreateNewCattle.js` - Container para crear animal
  - `UpdateCattle.js` - Container para actualizar animal
- `weight-estimations/`
  - `GetAllWeightEstimations.js` - Container para listar estimaciones
  - `GetWeightEstimationById.js` - Container para detalle de estimación
  - `GetWeightHistoryByCattle.js` - Container para historial de pesos de un animal
  - ~~`CreateNewWeightEstimation.js`~~ - NO necesario (solo móvil)
- `sync/`
  - `SyncStatusContainer.js` - Container para mostrar estado de sincronización
- `dashboard/`
  - `DashboardStatsContainer.js` - Container para estadísticas del dashboard
- `reports/`
  - `GenerateTraceabilityReport.js` - Container para generar reportes de trazabilidad
  - `GenerateInventoryReport.js` - Container para reportes de inventario
  - `GenerateMovementReport.js` - Container para reportes de movimientos

---

### 8. **Utils/Transformers (`src/utils/transformers/`)**

**Eliminar:**
- `companyToComboBox.js`
- `propertyToRadioButton.js`

**Mantener:**
- `roleToComboBox.js` - ✅ Mantener

**Crear:**
- `breedToComboBox.js` - Transformar razas a formato ComboBox
- `cattleToTableRow.js` - Transformar animales a filas de tabla
- `weightEstimationToChartData.js` - Transformar estimaciones para gráficos
- `cattleToTimelineEvents.js` - Transformar datos del animal a eventos de timeline
- `cattleToLineageData.js` - Transformar datos para árbol genealógico
- `cattleToReportData.js` - Transformar datos para reportes PDF/CSV

---

## 🎨 Estructura de Datos

### Animal (Cattle)
```javascript
{
  id: "uuid",
  ear_tag: "string",
  name: "string | null",
  breed: "nelore" | "brahman" | "guzerat" | "senepol" | "girolando" | "gyr_lechero" | "sindi",
  birth_date: "ISO date",
  gender: "male" | "female",
  color: "string | null",
  birth_weight_kg: "number | null",
  observations: "string | null",
  created_at: "ISO date",
  updated_at: "ISO date"
}
```

### Weight Estimation
```javascript
{
  id: "uuid",
  cattle_id: "uuid | null",
  breed: "string",
  estimated_weight: "number",
  confidence_score: "number (0-1)",
  frame_image_path: "string",
  timestamp: "ISO date",
  gps_latitude: "number | null",
  gps_longitude: "number | null",
  method: "tflite",
  model_version: "string",
  processing_time_ms: "number"
}
```

---

## 📝 Orden de Implementación Recomendado

1. ✅ **Actualizar configuración** (constants, routes, axiosClient) - **COMPLETADO**
2. ✅ **Crear servicios API** (cattle, weight-estimations, sync - solo lectura) - **COMPLETADO**
3. ✅ **Eliminar archivos obsoletos** (company, property) - **COMPLETADO**
4. ✅ **Decidir sobre estimación de peso en web** → Estimación desde web - **COMPLETADO**
5. ✅ **Decidir sobre gestión de usuarios** → Mantener gestión - **COMPLETADO**
6. ✅ **Adaptar gestión de usuarios** (eliminar referencias a Company) - **COMPLETADO**
7. ✅ **Crear servicio de estimación desde web** (`estimateWeightFromImage.js`) - **COMPLETADO**
8. ⏳ **Crear vistas básicas** (Dashboard, Cattle, WeightEstimations, SyncStatus, WeightEstimationFromWeb) - **EN PROGRESO**
9. ⏳ **Crear templates** correspondientes
10. ⏳ **Crear organisms** (formularios, listas)
11. ⏳ **Crear containers** (lógica de negocio)
12. ⏳ **Crear transformers** (breedToComboBox, etc.)
13. ⏳ **Testing y ajustes**

---

## 🔗 Endpoints del Backend

### Animals
- `GET /api/v1/animals` - Listar animales
- `GET /api/v1/animals/:id` - Obtener animal
- `POST /api/v1/animals` - Crear animal
- `PUT /api/v1/animals/:id` - Actualizar animal
- `DELETE /api/v1/animals/:id` - Eliminar animal

### Weight Estimations
- `GET /api/v1/weighings` - Listar estimaciones
- `GET /api/v1/weighings/:id` - Obtener estimación
- `GET /api/v1/weighings?cattle_id=:id` - Estimaciones por animal
- `POST /api/v1/weighings` - Crear estimación

### Sync
- `GET /api/v1/sync/health` - Health check
- `GET /api/v1/sync/stats` - Estadísticas
- `POST /api/v1/sync/cattle` - Sincronizar ganado
- `POST /api/v1/sync/weight-estimations` - Sincronizar estimaciones

### ML Estimation (Nuevo - Estimación desde Web)
- `POST /api/v1/ml/estimate` - Estimar peso desde imagen subida
  - Body: `FormData` con imagen
  - Response: `{ estimated_weight, confidence_score, breed, ... }`

---

## 🎯 Características del Dashboard

1. **Estadísticas Principales:**
   - Total de animales registrados
   - Peso promedio del ganado
   - Número de razas diferentes
   - Total de estimaciones realizadas

2. **Gráficos:**
   - Evolución de peso por animal (línea de tiempo)
   - Distribución por raza (pie chart)
   - Peso promedio por raza (bar chart)

3. **Acciones Rápidas:**
   - Registrar nuevo animal
   - Ver últimas estimaciones
   - Estado de sincronización

---

## ✅ Checklist de Migración

### Configuración
- [x] Actualizar `constants.js` (sidebarItems) ✅
- [x] Actualizar `routes.js` ✅
- [x] Actualizar `axiosClient.js` (baseURL) ✅

### Servicios API
- [x] Crear servicios API para Cattle ✅
- [x] Crear servicios API para Weight Estimations ✅
- [x] Crear servicios API para Sync (solo lectura) ✅

### Limpieza
- [x] Eliminar referencias a Company/Property ✅
- [x] Eliminar servicios obsoletos (company, property) ✅
- [x] Eliminar vistas obsoletas (CompanyView, PropertyView, MapView) ✅
- [x] Eliminar templates obsoletos ✅
- [x] Eliminar containers obsoletos ✅
- [x] Eliminar organisms obsoletos ✅
- [x] Eliminar transformers obsoletos ✅
- [x] Adaptar gestión de usuarios (eliminar referencias a Company) ✅
- [x] Crear servicio de estimación desde web (`estimateWeightFromImage.js`) ✅

### Desarrollo
- [x] Crear vistas básicas (Dashboard, Cattle, WeightEstimations, SyncStatus) ✅
- [x] Crear templates básicos (DashboardTemplate, CattleTemplate, WeightEstimationTemplate, SyncStatusTemplate) ✅
- [x] Crear organisms básicos (CattleList, WeightEstimationList, StatisticsCards, SyncStatusCard) ✅
- [x] Crear containers básicos (GetAllCattle, GetAllWeightEstimations, DashboardStatsContainer, SyncStatusContainer) ✅
- [x] Crear atoms y molecules reutilizables (Card, DataTable, StatCard, ActionButton, LoadingState, ErrorState, PageHeader) ✅
- [x] Adaptar vistas antiguas (RoleView, UserView) con listas siguiendo patrón de Cattle ✅
- [x] Crear organisms para listas (RoleList, UserList) ✅
- [x] Crear servicio y container para usuarios (getAllUsers, GetAllUsers) ✅
- [ ] Crear organisms adicionales (CreateCattle, CattleTraceabilityTimeline, LineageTree, WeightChart)
- [ ] Crear containers adicionales (GetCattleById, GetCattleLineage, GetCattleTimeline, etc.)
- [ ] Crear transformers (breedToComboBox, cattleToTimelineEvents, etc.)
- [ ] Crear vista de detalle (CattleDetailView, WeightEstimationDetailView)
- [ ] Crear vista de estimación desde web (WeightEstimationFromWebView)
- [ ] Testing

## ✅ Decisiones Completadas

1. ✅ **Gestión de Usuarios/Roles**: Mantener gestión
   - ✅ Mantener `UserView.js`, `RoleView.js`, `CreateUser/`, `CreateRole/`
   - ✅ Adaptado para eliminar referencias a Company

2. ✅ **Estimación de Peso en Web**: Opción B - Estimación desde web
   - ✅ Permitir subir imágenes y estimar desde backend
   - ✅ Servicio `estimateWeightFromImage.js` creado
   - ⏳ Pendiente: Endpoint backend `/api/v1/ml/estimate`

