# 🤔 Decisiones de Diseño - Panel Web

## 1. Sincronización en el Panel Web

### ✅ Decisión: Solo Visualización

**La sincronización es exclusiva de la app móvil (offline-first).**

El panel web:
- ✅ **SÍ muestra**: Estado de sincronización, estadísticas, items pendientes
- ❌ **NO sincroniza**: La sincronización se hace desde el móvil

**Servicios de Sync en Web:**
- `getSyncHealth.js` - Verificar estado del servicio ✅
- `getSyncStats.js` - Ver estadísticas de sincronización ✅
- `syncCattleBatch.js` - Disponible pero NO se usa en web ⚠️
- `syncWeightEstimationsBatch.js` - Disponible pero NO se usa en web ⚠️

**Vista de Sincronización:**
- Mostrar estado de conexión
- Mostrar items pendientes de sincronizar desde móviles
- Mostrar última sincronización
- Mostrar estadísticas (total sincronizado, errores, etc.)

---

## 2. Estimación de Peso en el Panel Web

### ✅ Decisión: Estimación desde Web (Opción B)

**El panel web permitirá hacer estimaciones subiendo imágenes.**

**Implementación:**
- ⏳ Backend: Endpoint `/api/v1/ml/estimate` que reciba imagen - **PENDIENTE BACKEND**
- ⏳ Backend: Cargar modelo ML (TensorFlow/PyTorch, no TFLite) - **PENDIENTE BACKEND**
- ✅ Frontend: Servicio `estimateWeightFromImage.js` creado - **COMPLETADO**
- ⏳ Frontend: Componente de upload de imágenes - **PENDIENTE**
- ⏳ Frontend: Vista/formulario para estimación desde web - **PENDIENTE**
- ⏳ Frontend: Mostrar resultado de estimación (peso, confianza, etc.) - **PENDIENTE**

**Consideraciones:**
- El modelo ML debe estar disponible en el backend
- Procesamiento de imágenes en servidor
- Permite estimaciones desde oficina/escritorio (no solo en campo)
- Complementa las estimaciones del móvil (no las reemplaza)

**Flujo:**
1. Usuario sube imagen desde panel web
2. Backend procesa imagen con modelo ML
3. Backend retorna estimación (peso, confianza, raza detectada)
4. Usuario puede guardar la estimación asociada a un animal

---

## 3. Eliminación de Conceptos Antiguos

### ✅ Compañía/Propiedad NO aplican

Este proyecto es para **una sola hacienda** (Hacienda Gamelera), por lo tanto:
- ❌ No hay múltiples empresas
- ❌ No hay múltiples propiedades
- ✅ Solo hay ganado y estimaciones

**Archivos eliminados:**
- ✅ Todas las vistas/templates/servicios de `company` y `property` - **COMPLETADO**
- ✅ Ver historial de commits para detalles de eliminación

---

## 4. Gestión de Usuarios/Roles

### ✅ Decisión: Mantener Gestión de Usuarios/Roles

**El panel web permitirá gestionar usuarios y roles.**

**Mantener:**
- ✅ `UserView.js` - Vista de gestión de usuarios
- ✅ `RoleView.js` - Vista de gestión de roles
- ✅ `CreateUser/` - Formulario para crear/editar usuarios
- ✅ `CreateRole/` - Formulario para crear/editar roles
- ✅ Servicios de `user/` y `role/`

**Adaptaciones completadas:**
- ✅ Eliminar referencias a `Company` en `UserView.js` - **COMPLETADO**
- ✅ Adaptar `UserTemplate.js` para no depender de compañías - **COMPLETADO**
- ✅ Actualizar servicios de usuario para trabajar sin compañías - **COMPLETADO**
- ✅ Mantener sistema de roles: Administrador, Usuario, Invitado
- ✅ Mantener control de acceso basado en roles en sidebar

**Roles del sistema:**
- **Administrador**: Acceso completo (incluye Sincronización)
- **Usuario**: Acceso a Dashboard, Ganado, Estimaciones, Estadísticas
- **Invitado**: Solo Dashboard (lectura)

---

## 📋 Resumen de Decisiones

| Aspecto | Decisión | Estado |
|---------|----------|--------|
| Sincronización en web | Solo visualización | ✅ Definido |
| Estimación de peso en web | **Estimación desde web** (subir imágenes) | ✅ Definido |
| Compañía/Propiedad | Eliminar todo | ✅ Definido |
| Gestión de usuarios | **Mantener gestión** (adaptar sin compañías) | ✅ Definido |
| Trazabilidad | **Sistema completo** | ✅ Plan creado |

## 5. Trazabilidad del Ganado

### ✅ Decisión: Sistema Completo de Trazabilidad

**El panel web debe tener control completo de trazabilidad del ganado.**

**Funcionalidades principales:**
- ✅ Timeline completo de cada animal (desde registro hasta presente)
- ✅ Linaje (padre/madre/hijos)
- ✅ Historial de pesos con gráficos
- ✅ Búsqueda y filtros avanzados
- ✅ Reportes de trazabilidad (PDF, CSV, Excel)
- ✅ Cumplimiento normativo (SENASAG, REGENSA, ASOCEBU)

**Ver `TRACEABILITY_PLAN.md` para plan completo.**

---

## ✅ Estado de Implementación

### Decisiones Completadas
1. ✅ **Decidir sobre estimación de peso en web** → Estimación desde web
2. ✅ **Decidir sobre gestión de usuarios** → Mantener gestión
3. ✅ **Eliminar archivos obsoletos** (company, property) - **COMPLETADO**
4. ✅ **Adaptar gestión de usuarios** (eliminar referencias a Company) - **COMPLETADO**
5. ✅ **Crear servicio de estimación desde web** (`estimateWeightFromImage.js`) - **COMPLETADO**

### Próximos Pasos
6. ⏳ **Crear vistas básicas** (Dashboard, Cattle, WeightEstimations, SyncStatus)
7. ⏳ **Crear vista de estimación desde web** (`WeightEstimationFromWebView.js`)
8. ⏳ **Crear componentes de trazabilidad** (Timeline, LineageTree, WeightChart)
9. ⏳ **Implementar backend para estimación desde web** (endpoint `/api/v1/ml/estimate`)

---

## 📌 Nota sobre este Documento

**Este documento NO debe eliminarse.** Es documentación de diseño que registra las decisiones arquitectónicas tomadas para el panel web. Debe mantenerse como referencia para:
- Futuros desarrolladores
- Documentación del proyecto
- Referencia de decisiones de diseño

Las decisiones aquí documentadas son parte de la arquitectura del sistema y deben preservarse.

