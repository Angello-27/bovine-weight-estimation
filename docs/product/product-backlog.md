# Product Backlog

## Contexto del Proyecto

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Product Owner**: Miguel Angel Escobar Lazcano  
**Scrum Master**: Rodrigo Escobar Morón  

## Épicas (Epics)

### Épica 1: Sistema de Estimación de Peso con IA
**Objetivo**: Reemplazar método tradicional con sistema IA que reduzca tiempo de 2-3 días a <2 horas para 20 animales

**Criterios de aceptación**:
- Precisión >95% (R² ≥ 0.95)
- Error absoluto <5 kg por animal
- Tiempo procesamiento <3 segundos
- Funcionamiento 100% offline

### Épica 2: Integración Normativa Boliviana
**Objetivo**: Cumplimiento automático con SENASAG, REGENSA y ASOCEBU

**Criterios de aceptación**:
- Reportes SENASAG automáticos
- Integración sistema Gran Paitití
- Exportación datos ASOCEBU
- Trazabilidad completa

### Épica 3: Gestión Inteligente de Datos
**Objetivo**: Análisis, reportes y alertas para optimización operativa

**Criterios de aceptación**:
- Historial completo de crecimiento
- Alertas automáticas útiles
- Reportes ejecutivos claros
- Planificación optimizada

## User Stories (Priorizadas)

### Sprint 1: Validación Core (2 semanas)

#### US-001: Captura Continua de Fotogramas
**Como** ganadero de Hacienda Gamelera  
**Quiero** capturar fotogramas continuos de bovinos  
**Para** estimar peso con IA en lugar de usar básculas tradicionales

**Criterios de aceptación**:
- [ ] Captura 10-15 FPS durante 3-5 segundos
- [ ] Funciona en condiciones de campo reales
- [ ] Interfaz simple para Bruno Brito Macedo
- [ ] Almacenamiento local automático

**Story Points**: 8  
**Prioridad**: Crítica

#### US-002: Estimación de Peso por Raza
**Como** ganadero  
**Quiero** que el sistema estime peso según la raza específica del animal  
**Para** obtener mayor precisión que la fórmula Schaeffer

**Criterios de aceptación**:
- [ ] Soporte para 7 razas (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)
- [ ] Precisión >95% con al menos 3 razas principales
- [ ] Tiempo procesamiento <3 segundos
- [ ] Confianza score visible para usuario

**Story Points**: 13  
**Prioridad**: Crítica

#### US-003: Registro Automático de Animales
**Como** ganadero  
**Quiero** registrar animales básicos en el sistema  
**Para** mantener control de mi hato de 500 cabezas

**Criterios de aceptación**:
- [ ] Registro por caravana/número de arete
- [ ] Selección de raza bovina
- [ ] Fecha de nacimiento
- [ ] Género (Macho/Hembra)
- [ ] Búsqueda rápida por número

**Story Points**: 5  
**Prioridad**: Alta

### Sprint 2: Funcionalidad Completa (2 semanas)

#### US-004: Historial de Pesajes
**Como** ganadero  
**Quiero** ver el historial completo de pesajes por animal  
**Para** analizar crecimiento y tomar decisiones de manejo

**Criterios de aceptación**:
- [ ] Lista cronológica de pesajes
- [ ] Gráfico de evolución de peso
- [ ] Comparativa entre animales
- [ ] Exportación a PDF/CSV

**Story Points**: 8  
**Prioridad**: Alta

#### US-005: Sincronización Offline
**Como** ganadero en zona rural  
**Quiero** que mis datos se sincronicen cuando hay conexión  
**Para** no perder información y tener respaldo

**Criterios de aceptación**:
- [ ] Funcionamiento 100% offline
- [ ] Sincronización automática con conexión
- [ ] Indicador visual de estado de sincronización
- [ ] Resolución de conflictos (last-write-wins)

**Story Points**: 13  
**Prioridad**: Alta

#### US-006: Búsqueda y Filtros
**Como** ganadero  
**Quiero** buscar animales por múltiples criterios  
**Para** encontrar rápidamente animales específicos

**Criterios de aceptación**:
- [ ] Búsqueda por caravana/nombre
- [ ] Filtro por raza
- [ ] Filtro por categoría de edad
- [ ] Filtro por estado (Activo/Inactivo)

**Story Points**: 5  
**Prioridad**: Media

### Sprint 3: Integración Normativa (2 semanas)

#### US-007: Reportes SENASAG
**Como** ganadero  
**Quiero** generar reportes automáticos para SENASAG  
**Para** cumplir con normativas de trazabilidad ganadera

**Criterios de aceptación**:
- [ ] Generación automática de reportes
- [ ] Formato PDF/CSV según estándar SENASAG
- [ ] Envío automático por email
- [ ] Historial de reportes enviados

**Story Points**: 8  
**Prioridad**: Alta

#### US-008: Integración Gran Paitití
**Como** ganadero  
**Quiero** integrar con el sistema Gran Paitití  
**Para** cumplir con normativas REGENSA

**Criterios de aceptación**:
- [ ] Conexión con API Gran Paitití
- [ ] Generación automática de GMA
- [ ] Cumplimiento capítulos 3.10 y 7.1
- [ ] Validación de datos antes de envío

**Story Points**: 13  
**Prioridad**: Alta

#### US-009: Exportación ASOCEBU
**Como** ganadero participante en competencias  
**Quiero** exportar datos para eventos ASOCEBU  
**Para** preparar animales para ferias ganaderas

**Criterios de aceptación**:
- [ ] Exportación de historial de crecimiento
- [ ] Certificaciones de peso
- [ ] Formato compatible con ASOCEBU
- [ ] Preparación para competencias

**Story Points**: 8  
**Prioridad**: Media

### Sprint 4: Optimización y Alertas (2 semanas)

#### US-010: Alertas Inteligentes
**Como** ganadero  
**Quiero** recibir alertas automáticas sobre mis animales  
**Para** tomar acciones preventivas y mejorar rendimiento

**Criterios de aceptación**:
- [ ] Alertas por pérdida de peso
- [ ] Alertas por estancamiento en crecimiento
- [ ] Recordatorios de pesaje
- [ ] Configuración de umbrales personalizados

**Story Points**: 8  
**Prioridad**: Media

#### US-011: Planificación de Sesiones
**Como** ganadero  
**Quiero** planificar sesiones masivas de pesaje  
**Para** optimizar tiempo y recursos

**Criterios de aceptación**:
- [ ] Calendario integrado
- [ ] Rutas optimizadas por ubicación
- [ ] Estimación de tiempo por sesión
- [ ] Recordatorios automáticos

**Story Points**: 5  
**Prioridad**: Baja

## Definición de Ready (DoR)

Una User Story está lista para Sprint Planning cuando:

- [ ] Tiene criterios de aceptación claros y testeable
- [ ] Tiene estimación de story points
- [ ] Tiene prioridad asignada
- [ ] Dependencias identificadas y resueltas
- [ ] Aceptación por Product Owner
- [ ] Tareas técnicas identificadas

## Definición de Done (DoD)

Una User Story está completa cuando:

- [ ] Código implementado según estándares
- [ ] Tests unitarios pasando
- [ ] Tests de integración pasando
- [ ] Validación con Bruno Brito Macedo
- [ ] Documentación actualizada
- [ ] Code review aprobado
- [ ] Deploy en ambiente de pruebas
- [ ] Aceptación por Product Owner

## Métricas de Producto

### Métricas de Valor
- **Tiempo de pesaje**: Reducción de 80% (de 2-3 días a <2 horas)
- **Precisión**: Mejora de 75% (de ±5-20 kg a <5 kg error)
- **Satisfacción usuario**: >90% (Bruno Brito Macedo)
- **Cumplimiento normativo**: 100% reportes automáticos

### Métricas Técnicas
- **Precisión ML**: >95% (R² ≥ 0.95)
- **Tiempo procesamiento**: <3 segundos
- **Disponibilidad offline**: >99% uptime
- **Tiempo sincronización**: <30 segundos para 50 registros

### Métricas de Proceso
- **Velocity**: Story points por sprint
- **Burndown**: Progreso diario del sprint
- **Quality**: Defectos por sprint
- **Cycle time**: Tiempo desde desarrollo hasta producción

---

**Próximo Sprint**: Sprint 1 - Validación Core (US-001, US-002, US-003)
