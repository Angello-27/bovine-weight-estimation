# Product Backlog - Bovine Weight Estimation System

**Product Owner**: Miguel Angel Escobar Lazcano  
**Cliente**: Bruno Brito Macedo - Hacienda Gamelera  
**Ubicación**: San Ignacio de Velasco, Chiquitanía, Santa Cruz, Bolivia  
**Escala**: 500 cabezas de ganado bovino, 8 razas  
**📅 Última actualización**: 28 octubre 2024

---

## 📊 Estado General del Backlog (28 octubre 2024)

| Métrica | Valor |
|---------|-------|
| **Sprint actual** | Sprint 2 (50% completado) |
| **Story Points completados** | 47/78 (60%) |
| **User Stories completadas** | 4/6 prioritarias (67%) |
| **Sprint 1** | ✅ 100% completado (26/26 SP) |
| **Sprint 2** | 🔄 50% completado (21/52 SP) |
| **Sprint 3** | 📋 Planificado - Presentación académica |

### Timeline Real

| Sprint | Período | Estado | Story Points | Valor Entregado |
|--------|---------|--------|--------------|-----------------|
| **Sprint 1** | 30 sep - 13 oct | ✅ **Completado** | 26/26 (100%) | Captura + Registro + Arquitectura ML |
| **Sprint 2** | 14 oct - 28 oct | 🔄 **En progreso** | 21/52 (40%) | Historial + Sync + Refactorización |
| **Sprint 3** | 29 oct - 10 nov | 📋 **Planificado** | ~30 SP estimado | Presentación + Demo + Video |

---

## ✅ Sprint 1: Validación Core (COMPLETADO 100%)

**Objetivo**: Validar funcionalidad core con Bruno - Captura, Registro, Arquitectura ML  
**Estado**: ✅ **100% Completado** (26/26 Story Points)  
**Fecha culminación**: 13 octubre 2024

### User Stories Completadas

#### US-001: Captura Continua de Fotogramas ✅

**Como** ganadero de Hacienda Gamelera  
**Quiero** capturar fotogramas continuos de bovinos mediante cámara de smartphone  
**Para** estimar peso con IA sin básculas tradicionales, ahorrando tiempo y eliminando estrés animal

**Criterios de aceptación cumplidos**:
- ✅ Captura continua 10-15 FPS durante 3-5 segundos automática
- ✅ Evaluación tiempo real: nitidez, iluminación, contraste, silueta, ángulo
- ✅ Selección automática mejor fotograma (score ponderado)
- ✅ Funciona en condiciones campo reales (luz solar, movimiento, 2-5m)
- ✅ Interfaz intuitiva con feedback visual
- ✅ Almacenamiento local SQLite automático
- ✅ Indicador progreso: "Capturando... 30/45"
- ✅ Confirmación visual fotograma seleccionado

**Story Points**: 8 ✅  
**Sprint**: Sprint 1  
**Estado**: ✅ Completado (Commit: `5d0841f`, `b20ac44`, `4c2031d`)

**Implementación**: 31 archivos creados (2,743 líneas), Clean Architecture + SOLID + Atomic Design

---

#### US-002: Estimación de Peso por IA ✅ (Arquitectura Completada)

**Como** ganadero  
**Quiero** estimación automática de peso según raza específica usando IA  
**Para** precisión >95% superior a fórmula Schaeffer manual (error actual 5-20 kg)

**Criterios de aceptación Sprint 1 (Arquitectura)**:
- ✅ Soporte para 8 razas bovinas
- ✅ Pipeline TFLite con 8 slots preparados para modelos por raza
- ✅ Sistema **HÍBRIDO** implementado (Sprint 1): YOLO + Fórmulas morfométricas
- ✅ Tiempo procesamiento <3 segundos
- ✅ Confidence score visible: "Precisión: 97%" con colores
- ✅ Funcionamiento 100% offline
- ✅ Selección de raza con iconos visuales
- ✅ Histórico almacenado localmente

**Story Points**: 13 ✅  
**Sprint**: Sprint 1 (Arquitectura) + Sprint 2 (Backend Híbrido)  
**Estado**: ✅ **Arquitectura completada**, Sistema Híbrido implementado (Commit: `df08f9a`)

**Nota importante**: Sistema usa **método híbrido** (YOLO + fórmulas) como demo funcional mientras se entrenan modelos ML reales en Sprint 3+.

**Precisión híbrida**: MAE <25kg vs báscula (validación 20 muestras)  
**Demostración**: Sistema funcional para presentación académica

---

#### US-003: Registro Automático de Animales ✅

**Como** ganadero  
**Quiero** registrar animales de forma rápida y simple  
**Para** mantener control organizado de mi hato de 500 cabezas

**Criterios de aceptación cumplidos**:
- ✅ Formulario con campos: caravana (único), raza, fecha nacimiento, género
- ✅ Selección visual 8 razas con iconos
- ✅ Validación unicidad caravana
- ✅ Cálculo automático edad y categoría (4 categorías)
- ✅ Búsqueda rápida con autocompletado
- ✅ Lista ordenada cronológicamente
- ✅ Indicador visual de estado
- ✅ Edición datos básicos
- ✅ Almacenamiento SQLite offline

**Story Points**: 5 ✅  
**Sprint**: Sprint 1  
**Estado**: ✅ Completado (Commit: `4f6b864`)

---

## 🔄 Sprint 2: Funcionalidad Completa (50% EN PROGRESO)

**Objetivo**: Completar gestión del hato - Historial, Sincronización, Búsqueda  
**Estado**: 🔄 **50% Completado** (21/52 Story Points estimados)  
**Timeline**: 14 octubre - 28 octubre 2024

### User Stories Completadas

#### US-004: Historial de Pesajes ✅

**Como** ganadero  
**Quiero** visualizar historial completo de pesajes con gráficos de evolución  
**Para** analizar crecimiento, detectar problemas de salud y tomar decisiones nutricionales

**Criterios de aceptación cumplidos**:
- ✅ Lista cronológica detallada con timestamp, peso, método, confidence, GPS
- ✅ Gráfico de líneas con eje X (tiempo) y eje Y (kg) renderizado <2s
- ✅ Línea de tendencia con regresión lineal mostrando GDP (Ganancia Diaria Promedio)
- ✅ Indicadores clave: peso actual, peso inicial, ganancia total, GDP
- ✅ Filtros por período
- ✅ Comparativa visual entre 2-5 animales
- ✅ Detección automática anomalías
- ✅ Exportación PDF profesional con logo y gráficos
- ✅ Exportación CSV para análisis Excel
- ✅ Funcionalidad offline completa

**Story Points**: 8 ✅  
**Sprint**: Sprint 2  
**Estado**: ✅ Completado (20 Oct 2024, Commit: `0c80b62`)  
**Implementación**: 15 archivos modificados, 5 nuevos (2,207 líneas)

---

#### US-005: Sincronización Offline ✅

**Como** ganadero en zona rural sin conectividad estable  
**Quiero** sistema funcional 100% offline con sincronización automática  
**Para** no perder datos sin depender de internet

**Criterios de aceptación cumplidos**:
- ✅ Funcionamiento 100% offline sin errores
- ✅ SQLite como fuente primaria (offline-first)
- ✅ Sincronización automática background al detectar conexión
- ✅ Queue con reintentos automáticos (backoff exponencial)
- ✅ Indicador visual claro: "Offline", "Sincronizando...", "Sincronizado"
- ✅ Detalle progreso: "50 de 127 registros sincronizados"
- ✅ Estrategia last-write-wins basada en timestamp UTC
- ✅ Notificación sincronización exitosa
- ✅ Botón manual "Sincronizar ahora"
- ✅ Log errores visible
- ✅ Compresión datos para 3G
- ✅ <30 segundos para 50 registros con 3G

**Story Points**: 13 ✅  
**Sprint**: Sprint 2  
**Estado**: ✅ Completado (18 Oct 2024, Commit: `e3317d0`)  
**Implementación**: 19 archivos creados/modificados (2,338 líneas)

---

#### Refactorización Arquitectónica (28 Oct 2024) ✅

**Mejoras Sprint 2 adicionales no planificadas**:

- ✅ **ProviderConfiguration con SOLID**: Centralización providers
- ✅ **Atomic Design en HomePage**: 317 → 71 líneas (-78%)
- ✅ **Atomic Design en CapturePage**: 133 → 61 líneas (-54%)
- ✅ **Cámara real implementada**: Eliminado MOCK
- ✅ **Bug permisos Android 13 corregido**: Recursión infinita solucionada
- ✅ **infoGradient** agregado paleta de colores

**Story Points aproximados**: ~5 SP (no contabilizados oficialmente, valor técnico agregado)  
**Estado**: ✅ Implementado (Commit: `b7b6dc5`)

---

### User Stories Pendientes Sprint 2

#### US-006: Búsqueda y Filtros ⏳ (Movida a Futuro/Opcional)

**Como** ganadero con 500 cabezas  
**Quiero** buscar y filtrar animales rápidamente por múltiples criterios  
**Para** encontrar animales específicos en segundos

**Story Points**: 5  
**Sprint**: Movida fuera de Sprint 2  
**Estado**: ⏳ **Prioridad baja, fuera de alcance académico**

**Justificación**: Sistema ya funcional con lista navegable. Búsqueda avanzada es optimización no requerida para demo académica.

---

## 📋 Sprint 3: Presentación Académica (PLANIFICADO)

**Objetivo**: Preparar demostración completa para presentación final  
**Timeline**: 29 octubre - 10 noviembre 2024  
**Presentación**: 6 noviembre 2024 🎯

### Actividades Planificadas

#### Documentación Completa
- Documento PDF final con arquitectura, decisiones, resultados
- Diagramas de arquitectura actualizados
- Justificación técnica del sistema híbrido
- Roadmap de evolución a ML real

#### Video Demostración
- Captura completa del flujo: registro → captura → estimación → historial
- Validación con datos reales Hacienda Gamelera
- Comparativa sistema híbrido vs método tradicional

#### Optimizaciones Finales
- Performance testing en dispositivo físico
- QA completo con escenarios reales
- Preparación de demo fluida para presentación

**Story Points estimados**: ~15 SP (documentación + demo + optimizaciones)

---

## 🚫 Fuera de Alcance (Decisión 28 oct 2024)

### Features Normativas Eliminadas

**Decisión**: Eliminar integraciones con normativas bolivianas debido a restricción de tiempo académico.

**US eliminadas**:
- ❌ **US-007**: Reportes SENASAG (8 SP)
- ❌ **US-008**: Integración Gran Paitití (13 SP)
- ❌ **US-009**: Exportación ASOCEBU (5 SP)

**Total eliminado**: 26 Story Points

**Justificación**:
- Especificaciones normativas poco documentadas o cambiantes
- Requieren contacto oficial con instituciones gubernamentales
- Complejidad alta para beneficio marginal en demo académica
- Timeline realista: presentación 6 nov (5 semanas)

**Alternativa**: Documentar estructura de integración en arquitectura, mantener infraestructura preparada para futuras integraciones.

---

## 🔮 Backlog Futuro (Post-Académico)

### Mejoras Técnicas

1. **Sistema ML Real**: Entrenar 8 modelos TFLite (uno por raza)
   - R² ≥0.95, MAE <5kg
   - Timeline: 4-8 semanas
   - Datasets requeridos: 200-1000+ imágenes por raza

2. **Backend API**: FastAPI con sincronización bidireccional
   - PostgreSQL o MongoDB cloud
   - Autenticación JWT
   - Deploy en Railway/Render

3. **Búsqueda Avanzada (US-006)**: Filtros multi-criterio
   - Búsqueda por caravana, raza, edad, género, estado
   - Rango de peso, fecha último pesaje
   - <3 segundos para 500 animales

4. **Alertas Inteligentes**: Notificaciones proactivas
   - Pérdida peso significativa
   - Estancamiento en crecimiento
   - Recordatorios pesaje programado

5. **Integraciones Normativas** (si requerido por cliente):
   - SENASAG reportes automáticos
   - Gran Paitití GMA digital
   - ASOCEBU exportación competencias

---

## 📊 Métricas de Progreso

### Story Points por Sprint

| Sprint | Story Points Planificados | Story Points Completados | % Completitud | Estado |
|--------|---------------------------|--------------------------|---------------|--------|
| **Sprint 1** | 26 | 26 | 100% | ✅ Completado |
| **Sprint 2** | 26 | 21 | 81% | 🔄 En progreso |
| **Sprint 3** | ~15 | 0 | 0% | 📋 Planificado |

**Total**: 67 SP completados de 95 SP planificados (71% del backlog académico)

### User Stories por Estado

| Estado | Cantidad | Story Points |
|--------|----------|--------------|
| ✅ Completadas | 4 | 34 SP |
| 🔄 En progreso | 1 | 0 SP |
| 📋 Planificadas | 1 | ~15 SP |
| ⏳ Movidas a futuro | 1 | 5 SP |
| 🚫 Eliminadas | 3 | 26 SP |

---

## 🎯 Valor Entregado Hasta Ahora

### Funcionalidades Operativas

✅ **Captura de fotogramas continua** (US-001)  
✅ **Registro de animales completo** (US-003)  
✅ **Estimación de peso (sistema híbrido)** (US-002)  
✅ **Historial de pesajes con gráficos** (US-004)  
✅ **Sincronización offline-first** (US-005)  
✅ **Arquitectura solida y escalable** (Clean Architecture + SOLID + Atomic Design)

### Métricas Validadas

- ✅ Tiempo captura: 3-5 segundos (10-15 FPS)
- ✅ Tiempo procesamiento: <3 segundos por estimación
- ✅ Funcionamiento offline: 100% funcional
- ✅ Base datos local: SQLite con 5 tablas optimizadas
- ✅ 8 razas bovinas soportadas
- ✅ Arquitectura preparada para ML real

### Calidad Técnica

- ✅ Clean Architecture aplicada (3 capas)
- ✅ SOLID principles cumplidos
- ✅ Atomic Design implementado
- ✅ Provider pattern para state management
- ✅ Dependency Injection configurado
- ✅ Cero código MOCK (eliminado)
- ✅ 0 errores linter

---

## 📝 Notas Importantes

### Sistema Híbrido (Decisión Técnica Crítica)

**Sprint 1-2 utiliza sistema híbrido** (YOLO pre-entrenado + fórmulas morfométricas):
- **Precisión**: MAE <25kg (vs objetivo ML real: MAE <5kg)
- **Justificación**: Demo funcional mientras se entrenan modelos reales
- **Timeline**: Sistema ML real requiere 4-8 semanas adicionales (Sprint 3+)
- **Trade-off aceptado**: Precisión menor vs demo funcional garantizada

Ver ADR-003 y ADR-011 en `docs/design/architecture-decisions.md`

### 8 Razas Actualizadas

Las razas fueron actualizadas de 7 a 8:
- ❌ **Eliminada**: Jersey (poca relevancia región)
- ✅ **Añadidas**: Guzerat, Holstein (mayor prevalencia región Chiquitana)

Ver `docs/design/database-schema.md` para esquemas actualizados.

---

**Documento actualizado**: 28 octubre 2024  
**Próxima revisión**: Daily Scrum  
**Total Story Points Backlog Académico**: 95 SP (de 121 SP originales)  
**Completitud General**: 67/95 (71%)

**Documentación relacionada**:
- 📄 Detalle User Stories (3C): [product-backlog-detailed.md](product-backlog-detailed.md)
- ✅ Definition of Done: [definition-of-done.md](definition-of-done.md)
- 🎯 Sprint Progress: [docs/sprints/sprint-02/sprint-progress.md](../sprints/sprint-02/sprint-progress.md)
