# Sprint 2 - Sprint Goal

## Información del Sprint

**Duración**: 2 semanas  
**Fecha inicio**: 14 octubre 2024  
**Fecha fin**: 27 octubre 2024  
**Fecha presentación**: **23 octubre 2024** 🎯  
**Scrum Master**: Rodrigo Escobar Morón  
**Product Owner**: Miguel Angel Escobar Lazcano  
**Cliente**: Bruno Brito Macedo (Hacienda Gamelera)

## Contexto del Proyecto

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Ubicación**: San Ignacio de Velasco, Bolivia  
**Escala**: 500 cabezas de ganado bovino  
**Razas**: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Guzerat, Holstein

**Incremento de Sprint 1**: Captura continua y estimación de peso validados  
**Próximo nivel**: Gestión completa del hato con análisis, sincronización y búsqueda

## Sprint Goal

**"Completar funcionalidades esenciales de análisis, sincronización offline y búsqueda para permitir gestión completa del hato bovino de 500 cabezas en Hacienda Gamelera, preparando demostración profesional para presentación del 23 de octubre."**

## Objetivos Específicos

### 1. Implementar Análisis y Reportes

- **Objetivo**: Proporcionar visualización histórica y análisis de crecimiento
- **Criterio de éxito**: Bruno puede generar gráficos de evolución de peso y reportes comparativos
- **Validación**: Historial completo de al menos 50 animales con gráficos intuitivos

### 2. Garantizar Sincronización Offline-First

- **Objetivo**: Funcionamiento confiable sin conexión a internet en zona rural
- **Criterio de éxito**: Sincronización automática sin pérdida de datos con señal intermitente
- **Validación**: Testing en condiciones reales de Hacienda Gamelera con conectividad limitada
- **Estado**: ✅ COMPLETADO (18 Oct 2024)

### 3. Aplicar Principios SOLID y Atomic Design

- **Objetivo**: Código mantenible, extensible y siguiendo mejores prácticas
- **Criterio de éxito**: ProviderConfiguration creado, refactorización HomePage y CapturePage
- **Validación**: Reducción de código, 100% composición pura, 0 métodos `_build...()`
- **Estado**: ✅ COMPLETADO (28 Oct 2024)

### 4. Integración ML Real (Pendiente)

- **Objetivo**: Entrenar modelos reales con datasets descargados (CID, Kaggle, Roboflow)
- **Criterio de éxito**: Modelos TFLite operativos con precisión MAE <20kg
- **Estrategia**: Depende de cantidad de imágenes (Transfer Learning o MVP académico)
- **Estado**: ⏳ Pendiente (requiere descarga de datasets)

## User Stories del Sprint

### US-004: Historial de Pesajes

**Story Points**: 8  
**Prioridad**: Alta

**Descripción**:  
Como ganadero  
Quiero ver el historial completo de pesajes por animal  
Para analizar crecimiento y tomar decisiones de manejo

**Criterios de aceptación**:
- [ ] Lista cronológica de todos los pesajes por animal
- [ ] Gráfico de evolución de peso con línea de tendencia
- [ ] Comparativa visual entre animales seleccionados
- [ ] Exportación de historial en formato PDF y CSV
- [ ] Indicador de ganancia diaria promedio (GDP)
- [ ] Filtros por período (última semana, mes, trimestre, año)

### US-005: Sincronización Offline

**Story Points**: 13  
**Prioridad**: Alta

**Descripción**:  
Como ganadero en zona rural  
Quiero que mis datos se sincronicen automáticamente cuando hay conexión  
Para no perder información y tener respaldo en la nube

**Criterios de aceptación**:
- [ ] Funcionamiento 100% offline sin errores
- [ ] Sincronización automática en background al detectar conexión
- [ ] Indicador visual claro de estado: offline/sincronizando/sincronizado
- [ ] Resolución de conflictos con estrategia last-write-wins
- [ ] Queue de sincronización con reintentos automáticos
- [ ] Notificación al usuario de sincronización exitosa

### US-006: Búsqueda y Filtros

**Story Points**: 5  
**Prioridad**: Media

**Descripción**:  
Como ganadero  
Quiero buscar animales por múltiples criterios  
Para encontrar rápidamente animales específicos en mi hato de 500 cabezas

**Criterios de aceptación**:
- [ ] Búsqueda instantánea por número de caravana/arete
- [ ] Filtro por raza (7 razas soportadas)
- [ ] Filtro por categoría de edad (terneros, vaquillonas, vacas, etc.)
- [ ] Filtro por estado (Activo/Inactivo/Vendido)
- [ ] Combinación de múltiples filtros simultáneos
- [ ] Resultados en <3 segundos para 500 animales

**Total Story Points**: 26

## Integración con Sprint 1

### Dependencias del Incremento Anterior

**Debe estar completado de Sprint 1**:
- ✅ US-001: Captura continua de fotogramas funcionando
- ✅ US-002: Estimación de peso por IA con precisión >95%
- ✅ US-003: Registro básico de animales operativo

**Incremento acumulativo Sprint 1 + Sprint 2**:
- Captura y estimación de peso (Sprint 1)
- + Análisis histórico y reportes (Sprint 2)
- + Sincronización offline confiable (Sprint 2)
- + Búsqueda eficiente para 500 animales (Sprint 2)
- = **Sistema funcional completo** para gestión diaria del hato

## Criterios de Éxito del Sprint

### Técnicos

- [x] Historial de pesajes con gráficos funcionando fluidamente ✅
- [x] Sincronización offline-first confiable sin pérdida de datos ✅
- [x] Exportación de reportes en PDF/CSV operativa ✅
- [x] Base de datos local (SQLite) escalable a 500+ animales ✅
- [x] Cámara real implementada sin MOCK ✅
- [x] Arquitectura SOLID aplicada (ProviderConfiguration) ✅
- [x] Atomic Design completo en todas las páginas ✅
- [ ] Integración ML real con modelos entrenados (pendiente datasets)

### Criterios de Negocio

- [ ] Bruno puede analizar crecimiento de su hato completo
- [ ] Sistema funciona confiablemente en zona rural sin internet
- [ ] Búsqueda permite gestión ágil de 500 cabezas
- [ ] Reportes son útiles para toma de decisiones
- [ ] Bruno confirma valor agregado vs método tradicional
- [ ] Sistema está listo para demostración profesional

### Validación

- [ ] Demo completa exitosa con datos reales de Hacienda Gamelera
- [ ] Testing en condiciones reales de campo (sin conexión)
- [ ] Feedback positivo de Bruno Brito Macedo
- [ ] Métricas de rendimiento validadas (búsqueda <3s, sincronización <30s)
- [ ] Presentación del 23 octubre preparada y ensayada
- [ ] Incremento funcional demostrable vs Sprint 1

## Riesgos Identificados

### Alto Impacto

1. **Sincronización offline compleja**: Conflictos de datos y pérdida de información
   - **Mitigación**: Implementar estrategia last-write-wins con timestamps, testing exhaustivo con conectividad intermitente
   
2. **Performance con 500 animales**: Búsqueda y consultas lentas
   - **Mitigación**: Índices en base de datos, paginación, caché local, testing de carga con datos reales

3. **Tiempo limitado para presentación**: Solo 9 días hábiles hasta el 23 octubre
   - **Mitigación**: Priorizar US críticas, preparar demo desde día 1, ensayos diarios de presentación

### Medio Impacto

1. **Integración con incremento Sprint 1**: Incompatibilidades o regresiones
   - **Mitigación**: Tests de regresión automáticos, validación continua de funcionalidades Sprint 1

2. **Complejidad de reportes**: Gráficos y exportaciones pueden consumir tiempo
   - **Mitigación**: Usar librerías probadas (charts_flutter, pdf), templates predefinidos

3. **Conectividad limitada en validación**: Dificulta testing de sincronización
   - **Mitigación**: Simular condiciones offline, testing con modo avión activado

## Plan de Validación

### Semana 1: Desarrollo Core (14-20 octubre)

**Día 1 (Lunes 14)**: 
- Daily Scrum: Sprint Planning refinement
- Implementación US-004: Historial base de datos y consultas
- Implementación US-005: Lógica sincronización offline

**Día 2 (Martes 15)**:
- Daily Scrum: Progreso y blockers
- Implementación US-004: Gráficos de evolución de peso
- Implementación US-005: Queue de sincronización con reintentos

**Día 3 (Miércoles 16)**:
- Daily Scrum: Progreso y blockers
- Implementación US-004: Exportación PDF/CSV
- Implementación US-006: Búsqueda y filtros básicos

**Día 4 (Jueves 17)**:
- Daily Scrum: Progreso y blockers
- Implementación US-005: Indicadores visuales de sincronización
- Implementación US-006: Optimización índices y performance

**Día 5 (Viernes 18)**:
- Daily Scrum: Progreso y blockers
- Testing de integración de las 3 US
- Refinamiento y corrección de bugs
- Primera versión demo interna

### Semana 2: Validación y Presentación (21-27 octubre)

**Día 6 (Lunes 21)**:
- Daily Scrum: Status para presentación
- Testing en condiciones reales de campo
- Validación con Bruno Brito Macedo (si disponible)
- Ajustes según feedback

**Día 7 (Martes 22)** - Pre-presentación:
- Daily Scrum: Últimos ajustes
- Ensayo completo de presentación del 23
- Preparación de datos demo realistas
- Verificación de requisitos técnicos (proyector, internet, etc.)

**Día 8 (Miércoles 23)** - **PRESENTACIÓN** 🎯:
- **Demostración académica oficial**
- Mostrar incremento funcional Sprint 1 + Sprint 2
- Evidencia de valor agregado vs método tradicional
- Q&A con evaluadores

**Día 9 (Jueves 24)**:
- Daily Scrum: Retrospectiva de presentación
- Incorporación de feedback de evaluadores
- Refinamiento adicional

**Día 10 (Viernes 25-27)**:
- Sprint Review con Product Owner
- Sprint Retrospective del equipo
- Planificación inicial Sprint 3 (si aplica)

## Métricas de Seguimiento

### Técnicas

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Tiempo búsqueda** | <3 segundos | Búsqueda en base de 500 animales |
| **Tiempo sincronización** | <30 segundos | 50 registros con conexión 3G |
| **Cobertura tests** | >80% | Tests unitarios e integración |
| **Performance gráficos** | <2 segundos | Renderizado de historial de 12 meses |
| **Tamaño BD local** | <50 MB | Base SQLite con 500 animales |
| **Memoria RAM** | <200 MB | Uso promedio de la app |

### Métricas de Negocio

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Satisfacción Bruno** | >9/10 | Escala Likert después de demo |
| **Utilidad reportes** | >90% | Bruno puede tomar decisión con datos |
| **Facilidad de búsqueda** | <10 segundos | Tiempo para encontrar animal específico |
| **Confiabilidad offline** | 100% | Sin pérdida de datos en 10 sesiones |
| **Intención de uso** | 100% | Bruno confirma uso diario del sistema |
| **Calidad presentación** | >85/100 | Evaluación académica |

### Métricas de Proceso

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Velocity** | 26 story points | Completitud al 100% de US planificadas |
| **Burndown** | Lineal | Progreso uniforme durante sprint |
| **Bugs introducidos** | <5 | Defectos por sprint |
| **Code reviews** | 100% | Todos los PRs revisados |
| **Daily attendance** | 100% | Participación en dailies |
| **Cycle time** | <3 días | Desde desarrollo hasta validación |

## Definición de Éxito del Sprint 2

El Sprint 2 es exitoso cuando:

### 1. Funcionalidad Completa ✅

- ✅ **Bruno Brito Macedo puede gestionar completamente su hato de 500 cabezas**
  - Captura y estimación de peso (Sprint 1)
  - Historial y análisis de crecimiento (Sprint 2)
  - Búsqueda rápida de cualquier animal (Sprint 2)
  - Reportes exportables para decisiones (Sprint 2)

### 2. Robustez Técnica ✅

- ✅ **Sistema funciona confiablemente offline en condiciones rurales**
  - Sin pérdida de datos con conectividad intermitente
  - Sincronización automática al recuperar señal
  - Performance aceptable con 500 animales

### 3. Validación con Usuario ✅

- ✅ **Bruno confirma que el sistema es superior al método tradicional**
  - Reducción de tiempo: De 2-3 días a <2 horas
  - Mejora de precisión: De ±5-20 kg a <5 kg
  - Facilidad de uso: Puede usarlo sin entrenamiento formal

### 4. Presentación Exitosa ✅

- ✅ **Demostración académica del 23 octubre es profesional y convincente**
  - Incremento funcional claro Sprint 1 → Sprint 2
  - Evidencia de valor agregado con datos reales
  - Evaluación académica >85/100

### 5. Preparación para Sprint 3 ✅

- ✅ **Backlog refinado para integración normativa boliviana**
  - Próximas US claramente definidas (SENASAG/REGENSA/ASOCEBU)
  - Feedback de presentación incorporado
  - Lecciones aprendidas documentadas

## Preparación para Presentación del 23 Octubre

### Estructura de la Demo (15-20 minutos)

#### 1. Contexto y Problema (3 minutos)
- Hacienda Gamelera: 500 cabezas, San Ignacio de Velasco
- Método tradicional: 2-3 días, error 5-20 kg, 3-4 personas
- Impacto: Errores médicos, preparación subóptima para competencias

#### 2. Solución Propuesta (2 minutos)
- Sistema IA con captura continua (10-15 FPS)
- Precisión >95%, error <5 kg
- Tiempo <2 horas, 1 operador
- Offline-first para zona rural

#### 3. Demo Técnica Sprint 1 (4 minutos)
- **US-001**: Captura continua de fotogramas en acción
- **US-002**: Estimación de peso en tiempo real (3 razas)
- **US-003**: Registro rápido de animales
- Mostrar precisión con datos reales validados

#### 4. Demo Técnica Sprint 2 (5 minutos)
- **US-004**: Historial completo de animal con gráficos de evolución
- **US-004**: Comparativa entre animales, exportación PDF
- **US-005**: Funcionamiento offline, sincronización automática
- **US-006**: Búsqueda instantánea en 500 animales

#### 5. Resultados y Métricas (3 minutos)
- Comparativa: Método tradicional vs Sistema IA
- Métricas técnicas: Precisión, tiempo, performance
- Feedback de Bruno Brito Macedo
- Cumplimiento normativo (SENASAG/REGENSA)

#### 6. Q&A y Próximos Pasos (3 minutos)
- Sprint 3: Integración normativa completa
- Escalabilidad: Colonias Menonitas, Frigorífico BFC S.A.
- Impacto social: Sector ganadero boliviano

### Materiales de Soporte

- [ ] Presentación PowerPoint/Google Slides
- [ ] Video de captura en campo real (Hacienda Gamelera)
- [ ] Datos demostrativos: 50+ animales con historial
- [ ] Gráficos comparativos: Antes vs Después
- [ ] Documentación técnica: Arquitectura, DoD, Backlog
- [ ] Informe de validación: Feedback de Bruno
- [ ] Demo en vivo: App funcionando en dispositivo real

## Próximos Pasos Según Resultados

### Si Sprint 2 es exitoso (esperado):
- **Sprint 3**: Integración normativa completa (SENASAG/REGENSA/ASOCEBU)
- US-007: Reportes SENASAG automáticos
- US-008: Integración sistema Gran Paitití
- US-009: Exportación datos ASOCEBU
- US-010: Alertas inteligentes
- Validación con entidades regulatorias

### Si Sprint 2 es parcialmente exitoso:
- Refinamiento de funcionalidades según feedback de presentación
- Ajustes de performance si búsqueda/sincronización no cumplen métricas
- Iteración adicional con Bruno antes de integración normativa

### Si Sprint 2 requiere ajustes:
- Retrospectiva profunda para identificar blockers
- Replantear prioridades según aprendizajes
- Considerar reducción de alcance normativo en Sprint 3

## Retrospectiva Sprint 1 (Aprendizajes)

### ¿Qué funcionó bien?
- [Completar después de Sprint 1]

### ¿Qué se puede mejorar?
- [Completar después de Sprint 1]

### Acciones de mejora para Sprint 2:
- [Completar después de Sprint 1]

---

## Compromiso del Equipo

**Todos los miembros del equipo Scrum nos comprometemos a:**

1. ✅ Completar las 3 User Stories del Sprint 2 (26 story points)
2. ✅ Validar funcionalidades con Bruno Brito Macedo en condiciones reales
3. ✅ Preparar demostración profesional para el 23 de octubre
4. ✅ Mantener calidad técnica según Definition of Done
5. ✅ Participar activamente en Daily Scrums y eventos Scrum
6. ✅ Comunicar blockers inmediatamente al Scrum Master
7. ✅ Colaborar para entregar incremento funcional de valor

**Nota**: Este Sprint Goal se actualiza diariamente durante el Daily Scrum según progreso y aprendizajes del equipo.

---

**🎯 FECHA CRÍTICA: Presentación 23 octubre 2024**

**🐄 Sprint 2 es clave para demostrar el valor completo del sistema para la ganadería boliviana.**

