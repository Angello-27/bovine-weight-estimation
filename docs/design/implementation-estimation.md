# Estimación de Implementación: Alert con Cronograma

**Fecha**: 2024-12-XX  
**Alcance**: Backend + Frontend + Mobile  
**Basado en**: Velocity histórica del proyecto (13 SP/semana)

---

## 📊 Resumen Ejecutivo

| Componente | Story Points | Tiempo Estimado | Complejidad |
|------------|--------------|-----------------|-------------|
| **Backend** | 13 SP | 1 semana | Media-Alta |
| **Frontend** | 8 SP | 3-4 días | Media |
| **Mobile** | 13 SP | 1 semana | Media-Alta |
| **TOTAL** | **34 SP** | **2.5-3 semanas** | **Media-Alta** |

---

## 🔧 Desglose por Nivel

### 1. Backend (FastAPI + MongoDB)

#### Fase 1: Modelo y Schemas (3 SP - 1 día)

**Tareas**:
- [ ] Crear `AlertModel` con campos de cronograma
- [ ] Crear enums: `AlertType`, `AlertStatus`, `RecurrenceType`
- [ ] Crear schemas: `AlertCreateRequest`, `AlertUpdateRequest`, `AlertResponse`
- [ ] Validaciones Pydantic

**Archivos**:
```
backend/app/models/alert_model.py          (~150 líneas)
backend/app/schemas/alert_schemas.py       (~100 líneas)
```

**Complejidad**: Baja  
**Tiempo**: 4-6 horas

---

#### Fase 2: Servicio (5 SP - 2 días)

**Tareas**:
- [ ] Crear `AlertService` con CRUD básico
- [ ] Lógica de validación (user_id, farm_id)
- [ ] Queries por usuario, estado, tipo
- [ ] Paginación

**Archivos**:
```
backend/app/services/alert_service.py       (~200 líneas)
```

**Complejidad**: Media  
**Tiempo**: 8-12 horas

---

#### Fase 3: Rutas API (3 SP - 1 día)

**Tareas**:
- [ ] Crear `alert.py` router
- [ ] Endpoints: GET, POST, PUT, DELETE
- [ ] Filtros: por usuario, estado, tipo, fecha
- [ ] Autenticación y autorización

**Archivos**:
```
backend/app/api/routes/alert.py            (~150 líneas)
```

**Complejidad**: Baja  
**Tiempo**: 4-6 horas

---

#### Fase 4: Cron Job y Recordatorios (2 SP - 1 día)

**Tareas**:
- [ ] Crear tarea programada (APScheduler o Celery)
- [ ] Procesar alertas programadas (`scheduled_at`)
- [ ] Enviar recordatorios (`reminder_before_days`)
- [ ] Generar eventos recurrentes

**Archivos**:
```
backend/app/core/tasks/alert_processor.py  (~150 líneas)
backend/app/core/config/scheduler.py       (~50 líneas)
```

**Complejidad**: Alta  
**Tiempo**: 6-8 horas

**Dependencias**: 
- Configurar scheduler (APScheduler recomendado)
- Sistema de notificaciones (email/push)

---

### 2. Frontend (React)

#### Fase 1: Servicios API (2 SP - 1 día)

**Tareas**:
- [ ] Crear servicios: `getAllAlerts`, `createAlert`, `updateAlert`, `deleteAlert`
- [ ] Filtros: por usuario, estado, tipo, fecha
- [ ] Manejo de errores

**Archivos**:
```
frontend/src/services/alert/
├── getAllAlerts.js
├── getAlertById.js
├── createAlert.js
├── updateAlert.js
├── deleteAlert.js
└── index.js
```

**Complejidad**: Baja  
**Tiempo**: 3-4 horas

---

#### Fase 2: Componentes Base (3 SP - 1.5 días)

**Tareas**:
- [ ] `AlertList` - Lista de alertas
- [ ] `AlertCard` - Card individual
- [ ] `CreateAlertForm` - Formulario creación
- [ ] `AlertFilters` - Filtros avanzados

**Archivos**:
```
frontend/src/components/organisms/
├── AlertList/index.js
├── AlertCard/index.js
└── CreateAlertForm/index.js
```

**Complejidad**: Media  
**Tiempo**: 6-8 horas

---

#### Fase 3: Vista de Calendario (3 SP - 1.5 días)

**Tareas**:
- [ ] Integrar librería de calendario (react-big-calendar o similar)
- [ ] `CalendarView` - Vista mensual/semanal
- [ ] Eventos clickeables
- [ ] Crear evento desde calendario

**Archivos**:
```
frontend/src/views/CalendarView.js
frontend/src/components/organisms/Calendar/index.js
```

**Complejidad**: Media-Alta  
**Tiempo**: 8-10 horas

**Dependencias**:
- Instalar librería de calendario
- Estilos personalizados

---

### 3. Mobile (Flutter)

#### Fase 1: Domain Layer (3 SP - 1 día)

**Tareas**:
- [ ] Crear `Alert` entity
- [ ] Crear `AlertRepository` interface
- [ ] Crear use cases: `GetAlerts`, `CreateAlert`, `MarkAsRead`

**Archivos**:
```
mobile/lib/domain/entities/alert.dart
mobile/lib/domain/repositories/alert_repository.dart
mobile/lib/domain/usecases/
├── get_alerts_usecase.dart
├── create_alert_usecase.dart
└── mark_alert_read_usecase.dart
```

**Complejidad**: Media  
**Tiempo**: 6-8 horas

---

#### Fase 2: Data Layer (5 SP - 2 días)

**Tareas**:
- [ ] Crear `AlertModel` (extiende entity)
- [ ] Crear `AlertLocalDataSource` (SQLite)
- [ ] Crear `AlertRemoteDataSource` (API)
- [ ] Crear `AlertRepositoryImpl`
- [ ] Migración SQLite (tabla alerts)

**Archivos**:
```
mobile/lib/data/models/alert_model.dart
mobile/lib/data/datasources/
├── alert_local_datasource.dart
└── alert_remote_datasource.dart
mobile/lib/data/repositories/alert_repository_impl.dart
```

**Complejidad**: Media-Alta  
**Tiempo**: 10-12 horas

---

#### Fase 3: Presentation Layer (5 SP - 2 días)

**Tareas**:
- [ ] `AlertsPage` - Lista de alertas
- [ ] `AlertTile` - Widget individual
- [ ] `CreateAlertPage` - Formulario
- [ ] `CalendarPage` - Vista de calendario
- [ ] Notificaciones locales (flutter_local_notifications)

**Archivos**:
```
mobile/lib/presentation/pages/
├── alerts/
│   ├── alerts_page.dart
│   ├── create_alert_page.dart
│   └── calendar_page.dart
└── widgets/
    └── alert_tile.dart
```

**Complejidad**: Media-Alta  
**Tiempo**: 10-12 horas

**Dependencias**:
- flutter_local_notifications para recordatorios
- calendar_widget o similar

---

## ⏱️ Timeline Estimado

### Opción 1: Desarrollo Secuencial (3 semanas)

```
Semana 1: Backend completo
├─ Día 1-2: Modelo y Schemas + Servicio
├─ Día 3: Rutas API
└─ Día 4-5: Cron Job y Recordatorios

Semana 2: Frontend completo
├─ Día 1: Servicios API
├─ Día 2-3: Componentes Base
└─ Día 4-5: Vista de Calendario

Semana 3: Mobile completo
├─ Día 1: Domain Layer
├─ Día 2-3: Data Layer
└─ Día 4-5: Presentation Layer
```

**Total**: 15 días hábiles (3 semanas)

---

### Opción 2: Desarrollo Paralelo (2.5 semanas)

```
Semana 1:
├─ Backend: Modelo + Servicio + Rutas (3 días)
├─ Frontend: Servicios + Componentes Base (3 días)
└─ Mobile: Domain Layer (2 días)

Semana 2:
├─ Backend: Cron Job (2 días)
├─ Frontend: Calendario (2 días)
└─ Mobile: Data Layer (3 días)

Semana 3:
└─ Mobile: Presentation Layer (3 días)
└─ Testing e integración (2 días)
```

**Total**: 12-13 días hábiles (2.5 semanas)

---

## 🎯 Factores de Complejidad

### Complejidad Alta ⚠️

1. **Cron Job y Recordatorios**
   - Configurar scheduler
   - Lógica de recurrencia
   - Manejo de timezones
   - **Riesgo**: +2 días si hay problemas de configuración

2. **Vista de Calendario (Frontend)**
   - Integración de librería externa
   - Personalización de estilos
   - Manejo de eventos
   - **Riesgo**: +1 día si la librería no funciona bien

3. **Notificaciones Locales (Mobile)**
   - Permisos Android/iOS
   - Scheduling de notificaciones
   - **Riesgo**: +1 día si hay problemas de permisos

### Complejidad Media ✅

1. **Modelos y Schemas**: Estándar, bien documentado
2. **Servicios y Repositorios**: Patrón conocido
3. **Componentes UI**: Reutilización de componentes existentes

---

## 📈 Estimación por Velocidad Histórica

**Basado en backlog del proyecto**:
- Sprint 1: 26 SP en 2 semanas = **13 SP/semana**
- Sprint 2: 21 SP en 2 semanas = **10.5 SP/semana**

**Promedio**: ~12 SP/semana

**Para 34 SP**:
- **Estimación conservadora**: 34 SP ÷ 12 SP/semana = **2.8 semanas**
- **Estimación optimista**: 34 SP ÷ 15 SP/semana = **2.3 semanas**
- **Estimación pesimista**: 34 SP ÷ 10 SP/semana = **3.4 semanas**

**Rango realista**: **2.5 - 3 semanas**

---

## 🚀 Recomendación de Implementación

### Fase 1: MVP (2 semanas) - 21 SP

**Prioridad Alta**:
- ✅ Backend: Modelo + Servicio + Rutas (11 SP)
- ✅ Frontend: Servicios + Componentes Base (5 SP)
- ✅ Mobile: Domain + Data Layer básico (5 SP)

**Resultado**: CRUD completo funcionando

---

### Fase 2: Funcionalidades Avanzadas (1 semana) - 13 SP

**Prioridad Media**:
- ⏳ Backend: Cron Job y Recordatorios (2 SP)
- ⏳ Frontend: Vista de Calendario (3 SP)
- ⏳ Mobile: Presentation + Notificaciones (8 SP)

**Resultado**: Sistema completo con cronograma

---

## ⚠️ Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Scheduler complejo** | Media | Alto | Usar APScheduler (simple) |
| **Librería calendario** | Baja | Medio | Evaluar antes de implementar |
| **Notificaciones mobile** | Media | Medio | Probar permisos temprano |
| **Recurrencia compleja** | Alta | Medio | Implementar solo tipos básicos primero |

---

## 📋 Checklist de Dependencias

### Antes de Empezar

- [ ] Decidir librería de calendario (frontend)
- [ ] Configurar scheduler (backend)
- [ ] Evaluar librería de notificaciones (mobile)
- [ ] Definir tipos de recurrencia iniciales

### Durante Desarrollo

- [ ] Testing continuo en cada fase
- [ ] Validación con usuario (Bruno) en MVP
- [ ] Documentación actualizada

---

## 💡 Optimizaciones Posibles

### Reducir Complejidad

1. **Simplificar Recurrencia**: Solo diario/semanal/mensual (no custom)
2. **Calendario Básico**: Vista simple sin drag & drop
3. **Notificaciones Básicas**: Solo push, no programadas localmente

**Ahorro estimado**: -5 SP = **29 SP total (2.4 semanas)**

---

## 📊 Comparación con Farm (Ya Implementado)

| Aspecto | Farm | Alert con Cronograma |
|---------|------|----------------------|
| **Backend SP** | 8 SP | 13 SP |
| **Frontend SP** | 5 SP | 8 SP |
| **Mobile SP** | 8 SP | 13 SP |
| **Tiempo Total** | 1.5 semanas | 2.5-3 semanas |
| **Complejidad Extra** | - | Cron Job + Calendario + Notificaciones |

**Conclusión**: Alert es ~2x más complejo que Farm debido a:
- Cronograma y programación
- Recurrencia
- Notificaciones
- Vista de calendario

---

## ✅ Conclusión

**Tiempo Total Estimado**: **2.5 - 3 semanas** (34 Story Points)

**Recomendación**:
1. **MVP en 2 semanas**: CRUD básico sin cronograma avanzado
2. **Completo en 3 semanas**: Con todas las funcionalidades

**Priorización**:
- ✅ **Alta**: Backend CRUD + Frontend básico
- ⏳ **Media**: Cronograma y recordatorios
- 📋 **Baja**: Recurrencia avanzada y notificaciones push

