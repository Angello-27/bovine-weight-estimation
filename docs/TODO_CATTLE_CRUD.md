# 📋 Análisis de Pendientes: CRUD de Cattle (Animales)

**Fecha**: 2025-01-02  
**Basado en**: `CRUD_PATTERN_REFERENCE.md`, `API_INTEGRATION_GUIDE.md`, `FRONTEND_INTEGRATION_GUIDE.md`

---

## ✅ **LO QUE ESTÁ IMPLEMENTADO**

### 1. **Estructura de Archivos** ✅
- ✅ `views/cattle/CattleView.js` - Vista principal
- ✅ `views/cattle/CattleDetailView.js` - Vista de detalle
- ✅ `templates/cattle/CattleTemplate.js` - Template de lista
- ✅ `templates/cattle/CattleDetailTemplate.js` - Template de detalle
- ✅ `containers/cattle/` - Todos los hooks necesarios
- ✅ `services/cattle/` - Todos los servicios API
- ✅ `components/organisms/CattleList/` - Componente de lista
- ✅ `components/organisms/CreateCattle/` - Componente de formulario

### 2. **Servicios API** ✅
- ✅ `getAllCattle.js` - Listar con paginación
- ✅ `getCattleById.js` - Obtener por ID
- ✅ `createCattle.js` - Crear
- ✅ `updateCattle.js` - Actualizar
- ✅ `deleteCattle.js` - Eliminar
- ✅ `getAnimalsByCriteria.js` - Búsqueda con filtros
- ✅ `getAnimalTimeline.js` - Timeline de eventos
- ✅ `getAnimalLineage.js` - Linaje (padre/madre)
- ✅ `index.js` - Exportaciones centralizadas

### 3. **Containers (Hooks)** ✅
- ✅ `GetAllCattle.js` - Hook para obtener lista con paginación
- ✅ `CreateNewCattle.js` - Hook para crear/editar con validación
- ✅ `ManageCattleForm.js` - Hook para gestión de formulario
- ✅ `useAnimalView.js` - Hook principal de la vista
- ✅ `useAnimalDetail.js` - Hook para vista de detalle
- ✅ `TransformCattleDetailData.js` - Transformador de datos

### 4. **Componentes** ✅
- ✅ `CattleList` - Lista con DataTable, acciones (Ver, Editar, Eliminar)
- ✅ `CreateCattle` - Formulario completo con validación
- ✅ `CattleTraceabilityTimeline` - Timeline de eventos
- ✅ `CattleLineageTree` - Árbol genealógico
- ✅ `CattleWeightHistoryChart` - Historial de pesos
- ✅ Iconografía completa en formularios
- ✅ `DateField` - Componente de fecha elegante (MUI DatePicker)
- ✅ `TextAreaField` - Componente para observaciones

### 5. **Funcionalidades CRUD Básicas** ✅
- ✅ **CREATE**: Crear animal con validación completa
- ✅ **READ**: Listar animales con paginación
- ✅ **READ**: Ver detalle de animal
- ✅ **UPDATE**: Editar animal existente
- ✅ **DELETE**: Eliminar animal con confirmación
- ✅ Validación de campos requeridos
- ✅ Manejo de errores robusto
- ✅ Notificaciones (Snackbar)
- ✅ Paginación funcional

### 6. **Vista de Detalle** ✅
- ✅ Información completa del animal
- ✅ Timeline de eventos ordenado (más reciente primero)
- ✅ Historial de pesos
- ✅ Linaje (padre/madre)
- ✅ Galería de imágenes
- ✅ Navegación a entidades relacionadas (farm, padre, madre)
- ✅ Card de estimación de peso por imagen
- ✅ Generación de reportes PDF

---

## ⚠️ **LO QUE ESTÁ PENDIENTE**

### 1. **Búsqueda y Filtros en UI** ⚠️ PARCIAL

**Estado Actual**:
- ✅ Componente `CattleFilters` existe pero **NO está integrado en `CattleTemplate.js`**
- ✅ Hook `FilterCattle.js` existe pero **NO está siendo usado**
- ✅ Servicio `getAnimalsByCriteria.js` soporta filtros pero **NO se están pasando desde la UI**
- ✅ `GetAllCattle.js` solo filtra por `farm_id`, no por otros criterios

**Pendiente**:
- [ ] **Integrar `CattleFilters` en `CattleTemplate.js`** (antes de la lista)
- [ ] **Integrar `SearchBar` en `CattleTemplate.js`** (búsqueda por texto)
- [ ] **Conectar filtros con `GetAllCattle.js`** para que se apliquen en el backend
- [ ] **Agregar filtro por estado** (`active`, `inactive`, `sold`, `deceased`)
- [ ] **Agregar filtro por farm_id** (si el usuario tiene múltiples farms)
- [ ] **Implementar búsqueda por texto** (caravana, nombre) que se envíe al backend

**Referencia**: Según `FRONTEND_INTEGRATION_GUIDE.md` línea 916:
> "Búsqueda avanzada en CattleView (UI pendiente)"

**Patrón a seguir**: Ver `FarmTemplate.js` o `UserTemplate.js` para ver cómo se integran filtros.

---

### 2. **Ordenamiento (Sorting)** ❌ NO IMPLEMENTADO

**Estado Actual**:
- ❌ No hay UI para ordenar columnas
- ❌ No hay parámetros de ordenamiento en `GetAllCattle.js`
- ❌ El backend soporta ordenamiento pero no se está usando

**Pendiente**:
- [ ] **Agregar UI de ordenamiento** en `CattleList` o `DataTable`
- [ ] **Agregar parámetros de ordenamiento** en `getAnimalsByCriteria.js` (ej: `sort_by`, `sort_order`)
- [ ] **Conectar ordenamiento con backend** en `GetAllCattle.js`
- [ ] **Permitir ordenar por**: caravana, nombre, raza, fecha de nacimiento, estado

**Referencia**: Según `FRONTEND_INTEGRATION_GUIDE.md` línea 917:
> "Ordenamiento (UI pendiente)"

---

### 3. **Campos Faltantes en Formulario** ⚠️ PARCIAL

**Estado Actual**:
- ✅ Campos básicos: caravana, nombre, raza, fecha nacimiento, género, color, peso al nacer, observaciones
- ❌ **Falta campo `farm_id`** (selección de hacienda)
- ❌ **Falta campo `mother_id`** (selección de madre)
- ❌ **Falta campo `father_id`** (selección de padre)
- ❌ **Falta campo `status`** (estado del animal)

**Pendiente**:
- [ ] **Agregar `ComboBox` para `farm_id`** en `CreateCattle/index.js`
- [ ] **Agregar `ComboBox` para `mother_id`** (búsqueda de animales hembra)
- [ ] **Agregar `ComboBox` para `father_id`** (búsqueda de animales macho)
- [ ] **Agregar `ComboBox` para `status`** (active, inactive, sold, deceased)
- [ ] **Validar que `mother_id` sea hembra** y `father_id` sea macho

**Referencia**: Según `API_INTEGRATION_GUIDE.md` líneas 698-714, el backend acepta estos campos.

---

### 4. **Exportación de Datos** ❌ NO IMPLEMENTADO

**Estado Actual**:
- ❌ No hay opción de exportar lista de animales
- ✅ Solo existe exportación de reportes individuales (trazabilidad)

**Pendiente**:
- [ ] **Agregar botón "Exportar"** en `CattleTemplate.js`
- [ ] **Implementar exportación a Excel/CSV** de la lista actual (con filtros aplicados)
- [ ] **Implementar exportación a PDF** de la lista actual
- [ ] **Usar servicio de reportes del backend** si existe endpoint para inventario

**Referencia**: Según `API_INTEGRATION_GUIDE.md` líneas 949-970, existe endpoint `/api/v1/reports/inventory` que puede usarse.

---

### 5. **Optimizaciones y Mejoras** ⚠️ PARCIAL

**Estado Actual**:
- ✅ Manejo de errores robusto
- ✅ Loading states implementados
- ❌ No hay caché de datos
- ❌ No hay debounce en búsqueda
- ❌ No hay memoización de componentes pesados

**Pendiente**:
- [ ] **Implementar debounce en búsqueda** (esperar 300ms antes de buscar)
- [ ] **Agregar caché de datos** (usar React Query o similar)
- [ ] **Memoizar componentes pesados** (`CattleList`, `CreateCattle`)
- [ ] **Optimizar carga de imágenes** (lazy loading, thumbnails)

**Referencia**: Según `FRONTEND_INTEGRATION_GUIDE.md` líneas 923-925:
> "Caché de datos (mejora futura)"  
> "Optimización de imágenes (mejora futura)"

---

### 6. **Validaciones Adicionales** ⚠️ PARCIAL

**Estado Actual**:
- ✅ Validación de campos requeridos
- ✅ Validación de tipos de datos básicos
- ❌ **Falta validar unicidad de caravana** (verificar en backend antes de guardar)
- ❌ **Falta validar que fecha de nacimiento no sea futura**
- ❌ **Falta validar que peso al nacer sea positivo**

**Pendiente**:
- [ ] **Validar unicidad de caravana** (llamar a endpoint de verificación antes de guardar)
- [ ] **Validar fecha de nacimiento** (no puede ser futura)
- [ ] **Validar peso al nacer** (debe ser > 0)
- [ ] **Validar que mother_id y father_id sean diferentes del animal actual**
- [ ] **Validar que mother_id sea hembra y father_id sea macho**

---

### 7. **Testing** ❌ NO IMPLEMENTADO

**Estado Actual**:
- ❌ No hay tests unitarios
- ❌ No hay tests de integración
- ❌ No hay tests E2E

**Pendiente**:
- [ ] **Tests unitarios** para servicios API
- [ ] **Tests unitarios** para hooks (containers)
- [ ] **Tests de componentes** (CreateCattle, CattleList)
- [ ] **Tests de integración** (flujo completo CRUD)
- [ ] **Tests E2E** (usando Cypress o similar)

**Referencia**: Según `FRONTEND_INTEGRATION_GUIDE.md` línea 925:
> "Testing (pendiente)"

---

## 📊 **RESUMEN DE PRIORIDADES**

### 🔴 **ALTA PRIORIDAD** (Funcionalidad básica faltante)
1. **Búsqueda y Filtros en UI** - Integrar `CattleFilters` y `SearchBar` en `CattleTemplate.js`
2. **Campos faltantes en formulario** - Agregar `farm_id`, `mother_id`, `father_id`, `status`
3. **Validaciones adicionales** - Unicidad de caravana, validación de fechas

### 🟡 **MEDIA PRIORIDAD** (Mejoras de UX)
4. **Ordenamiento** - Agregar UI de ordenamiento de columnas
5. **Exportación de datos** - Exportar lista a Excel/CSV/PDF
6. **Optimizaciones** - Debounce, caché, memoización

### 🟢 **BAJA PRIORIDAD** (Mejoras futuras)
7. **Testing** - Tests unitarios, integración, E2E

---

## 📝 **CHECKLIST DE IMPLEMENTACIÓN**

### Fase 1: Búsqueda y Filtros (ALTA PRIORIDAD)
- [ ] Integrar `CattleFilters` en `CattleTemplate.js`
- [ ] Integrar `SearchBar` en `CattleTemplate.js`
- [ ] Modificar `GetAllCattle.js` para aceptar filtros como parámetros
- [ ] Conectar filtros con `getAnimalsByCriteria.js`
- [ ] Agregar filtro por estado
- [ ] Agregar filtro por farm_id (si aplica)
- [ ] Implementar búsqueda por texto en backend

### Fase 2: Campos del Formulario (ALTA PRIORIDAD)
- [ ] Agregar `ComboBox` para `farm_id` en `CreateCattle/index.js`
- [ ] Agregar `ComboBox` para `mother_id` (con búsqueda de animales hembra)
- [ ] Agregar `ComboBox` para `father_id` (con búsqueda de animales macho)
- [ ] Agregar `ComboBox` para `status`
- [ ] Validar que mother_id sea hembra y father_id sea macho
- [ ] Actualizar `CreateNewCattle.js` para manejar estos campos

### Fase 3: Validaciones (ALTA PRIORIDAD)
- [ ] Crear servicio para verificar unicidad de caravana
- [ ] Validar fecha de nacimiento (no futura)
- [ ] Validar peso al nacer (> 0)
- [ ] Validar que mother_id y father_id sean diferentes del animal actual
- [ ] Agregar validaciones en `CreateNewCattle.js`

### Fase 4: Ordenamiento (MEDIA PRIORIDAD)
- [ ] Agregar UI de ordenamiento en `CattleList` o `DataTable`
- [ ] Agregar parámetros `sort_by` y `sort_order` en `getAnimalsByCriteria.js`
- [ ] Conectar ordenamiento con backend en `GetAllCattle.js`

### Fase 5: Exportación (MEDIA PRIORIDAD)
- [ ] Agregar botón "Exportar" en `CattleTemplate.js`
- [ ] Implementar exportación a Excel/CSV
- [ ] Implementar exportación a PDF
- [ ] Usar endpoint `/api/v1/reports/inventory` si está disponible

### Fase 6: Optimizaciones (BAJA PRIORIDAD)
- [ ] Implementar debounce en búsqueda
- [ ] Agregar caché de datos (React Query)
- [ ] Memoizar componentes pesados
- [ ] Optimizar carga de imágenes

### Fase 7: Testing (BAJA PRIORIDAD)
- [ ] Tests unitarios para servicios
- [ ] Tests unitarios para hooks
- [ ] Tests de componentes
- [ ] Tests de integración
- [ ] Tests E2E

---

## 🔗 **REFERENCIAS**

- **Patrón CRUD**: `docs/patterns/CRUD_PATTERN_REFERENCE.md`
- **Guía API**: `docs/integration/API_INTEGRATION_GUIDE.md`
- **Guía Frontend**: `docs/integration/FRONTEND_INTEGRATION_GUIDE.md`
- **Estado Documentación**: `docs/DOCUMENTATION-STATUS.md`

---

**Última actualización**: 2025-01-02

