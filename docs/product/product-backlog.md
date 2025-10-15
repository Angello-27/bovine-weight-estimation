# Product Backlog

## Contexto del Proyecto

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Ubicación**: San Ignacio de Velasco, Bolivia  
**Escala**: 500 cabezas de ganado bovino  
**Razas soportadas**: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey  
**Product Owner**: Miguel Angel Escobar Lazcano  
**Scrum Master**: Rodrigo Escobar Morón  

## Cronograma Académico

- **Sprint 0** (Planificación): Completado antes del 30 septiembre 2024 ✅
- **Sprint 1**: 30 septiembre - 13 octubre 2024 (2 semanas) - Validación Core
- **Sprint 2**: 14 octubre - 27 octubre 2024 (2 semanas) - **Presentación: 23 octubre**
- **Sprint 3**: 28 octubre - 10 noviembre 2024 (2 semanas) - **Presentación: 6 noviembre** 🎯

## Problema Actual

- **Método tradicional**: Fórmula Schaeffer con cinta bovinométrica
- **Error**: 5-20 kg por animal
- **Tiempo**: 2-3 días para procesar 20 animales
- **Personal requerido**: 3-4 personas (capataz, vaquero, peón)
- **Calibración diaria**: 30-45 minutos
- **Tasa de reintentos**: 10% de animales requieren 2-3 intentos

## Objetivo del Sistema

- **Precisión**: >95% (R² ≥ 0.95, error <5 kg)
- **Tiempo**: <2 horas para 20 animales (reducción 80%)
- **Personal**: 1 operador con smartphone (reducción 75%)
- **Funcionamiento**: 100% offline-first para zona rural
- **Captura**: Continua 10-15 FPS durante 3-5 segundos
- **Procesamiento**: <3 segundos por estimación
- **Calibración**: Eliminada completamente

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

#### US-001: Captura Continua de Fotogramas ✅ COMPLETADA

**Como** ganadero de Hacienda Gamelera  
**Quiero** capturar fotogramas continuos de bovinos mediante la cámara de mi smartphone  
**Para** estimar peso con IA sin necesidad de básculas tradicionales, ahorrando tiempo y eliminando estrés animal

**Criterios de aceptación**:

- [x] Captura continua de 10-15 FPS durante 3-5 segundos automáticamente ✅
- [x] Evaluación en tiempo real de calidad: nitidez, iluminación, contraste, visibilidad de silueta, ángulo ✅
- [x] Selección automática del mejor fotograma con score ponderado (Silueta 40%, Nitidez 30%, Iluminación 20%, Ángulo 10%) ✅
- [x] Funciona en condiciones de campo reales (luz solar, movimiento animal, distancia 2-5 metros) ✅
- [x] Interfaz intuitiva: botón único "Capturar" con feedback visual durante proceso ✅
- [x] Almacenamiento local automático de fotogramas en SQLite ✅
- [x] Indicador de progreso: "Capturando... 30/45 fotogramas" ✅
- [x] Confirmación visual del fotograma seleccionado antes de procesamiento ✅

**Story Points**: 8  
**Prioridad**: Crítica  
**Dependencias**: Ninguna  
**Sprint**: Sprint 1  
**Estado**: ✅ **COMPLETADA** (28 Oct 2024)

**Implementación**:
- 📦 Clean Architecture: Domain → Data → Presentation (31 archivos)
- 🏗️ Atomic Design: 8 componentes reutilizables
- 🎯 SOLID Principles: Aplicado en toda la arquitectura
- 📱 UI/UX: Material Design 3 + tema completo
- 🗄️ SQLite: Schema con tablas e índices
- 🔧 Config: DI Container, Router, Theme separados
- ✅ Tests: Unit test baseline (expandir a >80%)

**Archivos**: Ver `docs/sprints/sprint-01/sprint-progress.md`  
**Commits**: `5d0841f`, `b20ac44`, `4c2031d`

#### US-002: Estimación de Peso por Raza

**Como** ganadero  
**Quiero** que el sistema estime automáticamente el peso del animal según su raza específica usando IA  
**Para** obtener precisión >95% superior a la fórmula Schaeffer manual (error actual 5-20 kg)

**Criterios de aceptación**:

- [ ] Soporte para 7 razas bovinas: Brahman, Nelore, Angus, Cebuinas (Bos indicus), Criollo, Pardo Suizo, Jersey
- [ ] Modelo ML específico por raza implementado con TensorFlow Lite
- [ ] Precisión >95% (R² ≥ 0.95) validada con al menos 3 razas principales (Brahman, Nelore, Angus)
- [ ] Error absoluto <5 kg por animal en condiciones controladas
- [ ] Tiempo procesamiento <3 segundos desde fotograma hasta resultado
- [ ] Confidence score visible: "Precisión: 97%" con código de colores (Verde >90%, Amarillo 80-90%, Rojo <80%)
- [ ] Funcionamiento 100% offline sin conexión a internet
- [ ] Selección de raza antes de captura con iconos visuales intuitivos
- [ ] Histórico de estimaciones almacenado localmente con timestamp, GPS, raza, peso, confidence

**Story Points**: 13  
**Prioridad**: Crítica
**Dependencias**: US-001 (requiere fotogramas capturados)  
**Sprint**: Sprint 1

#### US-003: Registro Automático de Animales

**Como** ganadero  
**Quiero** registrar animales de forma rápida y simple en el sistema  
**Para** mantener control organizado de mi hato de 500 cabezas en Hacienda Gamelera

**Criterios de aceptación**:

- [ ] Formulario de registro con campos obligatorios: número de caravana/arete (único), raza, fecha nacimiento, género
- [ ] Selección de raza desde lista visual con 7 opciones: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey
- [ ] Validación de número de caravana único (no duplicados en base de datos)
- [ ] Cálculo automático de edad y categoría: Ternero (<8 meses), Vaquillona/Torillo (6-18 meses), Vaquillona/Torete (19-30 meses), Vaca/Toro (>30 meses)
- [ ] Campos opcionales: color, peso al nacer, madre ID, padre ID, observaciones
- [ ] Búsqueda rápida por número de caravana con autocompletado
- [ ] Lista de animales registrados ordenada cronológicamente (más recientes primero)
- [ ] Indicador visual de estado: Activo (verde), Inactivo (gris), Vendido (azul), Muerto (rojo)
- [ ] Edición de datos básicos de animal existente
- [ ] Almacenamiento local en SQLite funcionando offline

**Story Points**: 5  
**Prioridad**: Alta
**Dependencias**: Ninguna (independiente de captura/estimación)  
**Sprint**: Sprint 1

### Sprint 2: Funcionalidad Completa (2 semanas)

#### US-004: Historial de Pesajes

**Como** ganadero  
**Quiero** visualizar el historial completo de pesajes de cada animal con gráficos de evolución  
**Para** analizar patrones de crecimiento, detectar problemas de salud y tomar decisiones informadas de manejo nutricional

**Criterios de aceptación**:

- [ ] Lista cronológica detallada de todos los pesajes por animal: fecha, hora, peso, método (IA/Manual/Báscula), confidence, ubicación GPS
- [ ] Gráfico de líneas de evolución de peso con eje X (tiempo) y eje Y (kg) renderizado en <2 segundos
- [ ] Línea de tendencia con regresión lineal mostrando ganancia diaria promedio (GDP)
- [ ] Indicadores clave: peso actual, peso inicial, ganancia total, GDP, proyección a 30/60/90 días
- [ ] Filtros por período: última semana, último mes, último trimestre, último año, rango personalizado
- [ ] Comparativa visual entre 2-5 animales seleccionados en mismo gráfico con colores diferenciados
- [ ] Detección automática de anomalías: pérdida de peso >5%, estancamiento >15 días, bajo GDP para categoría
- [ ] Exportación de historial individual en PDF profesional con logo, datos animal, gráficos, tabla de pesajes
- [ ] Exportación masiva en CSV para análisis en Excel: animal_id, fecha, peso, método, confidence, GPS
- [ ] Funcionalidad offline completa con sincronización de datos históricos

**Story Points**: 8  
**Prioridad**: Alta
**Dependencias**: US-002 (requiere pesajes almacenados), US-003 (requiere animales registrados)  
**Sprint**: Sprint 2

#### US-005: Sincronización Offline

**Como** ganadero en zona rural sin conectividad estable  
**Quiero** que el sistema funcione completamente offline y sincronice automáticamente cuando detecte conexión  
**Para** no perder ningún dato importante y tener respaldo en la nube sin depender de señal de internet

**Criterios de aceptación**:

- [ ] Funcionamiento 100% offline sin errores: captura, estimación, registro, historial, búsqueda
- [ ] Base de datos local SQLite como fuente primaria de verdad (offline-first)
- [ ] Sincronización automática en background al detectar conexión WiFi/3G/4G sin intervención del usuario
- [ ] Queue de sincronización con reintentos automáticos (backoff exponencial: 5s, 15s, 30s, 1m, 5m)
- [ ] Indicador visual claro en header: "Offline" (rojo), "Sincronizando..." (amarillo animado), "Sincronizado" (verde con check)
- [ ] Detalle de estado: "50 de 127 registros sincronizados" con barra de progreso
- [ ] Resolución de conflictos con estrategia last-write-wins basada en timestamp UTC
- [ ] Notificación al usuario de sincronización exitosa: "Todos tus datos están respaldados"
- [ ] Modo manual: botón "Sincronizar ahora" para forzar sincronización inmediata
- [ ] Log de errores de sincronización con reintentos pendientes visible para debugging
- [ ] Compresión de datos para optimizar consumo de datos móviles en zona rural
- [ ] Tiempo de sincronización <30 segundos para 50 registros con conexión 3G

**Story Points**: 13  
**Prioridad**: Alta (CRÍTICA para zona rural)  
**Dependencias**: US-002, US-003, US-004 (requiere datos para sincronizar)  
**Sprint**: Sprint 2

#### US-006: Búsqueda y Filtros

**Como** ganadero con 500 cabezas de ganado  
**Quiero** buscar y filtrar animales rápidamente por múltiples criterios  
**Para** encontrar animales específicos en segundos sin revisar listas extensas manualmente

**Criterios de aceptación**:

- [ ] Barra de búsqueda principal con autocompletado instantáneo (<500ms) por número de caravana/arete
- [ ] Filtro por raza: checkboxes para las 7 razas (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)
- [ ] Filtro por categoría de edad: Terneros (<8m), Vaquillonas/Torillos (6-18m), Vaquillonas/Toretes (19-30m), Vacas/Toros (>30m)
- [ ] Filtro por género: Macho, Hembra, Ambos
- [ ] Filtro por estado: Activo, Inactivo, Vendido, Muerto (múltiple selección)
- [ ] Filtro por rango de peso: slider "150 kg - 600 kg"
- [ ] Filtro por fecha último pesaje: "Última semana", "Último mes", "Hace más de 1 mes", "Sin pesajes"
- [ ] Combinación de múltiples filtros simultáneos con lógica AND
- [ ] Contador de resultados: "25 de 500 animales"
- [ ] Botón "Limpiar filtros" para resetear búsqueda
- [ ] Resultados en <3 segundos para 500 animales con índices optimizados
- [ ] Persistencia de filtros al navegar: mantiene búsqueda activa

**Story Points**: 5  
**Prioridad**: Media
**Dependencias**: US-003 (requiere animales registrados)  
**Sprint**: Sprint 2

### Sprint 3: Integración Normativa (28 oct - 10 nov 2024, Presentación: 6 nov)

**Objetivo del Sprint**: Integrar con entidades normativas bolivianas (SENASAG, REGENSA/Gran Paitití, ASOCEBU) para cumplimiento legal obligatorio.

**Total Story Points**: 26 (US-007: 8 pts + US-008: 13 pts + US-009: 5 pts)

**Dependencias de Sprint 2**: Requiere US-004 (historial completo), US-005 (sincronización), US-006 (búsqueda) completadas.

#### US-007: Reportes SENASAG

**Como** ganadero boliviano  
**Quiero** generar reportes automáticos de trazabilidad ganadera para SENASAG  
**Para** cumplir con normativas bolivianas obligatorias sin procesos manuales complejos

**Criterios de aceptación**:

- [ ] Generación automática de reporte de inventario mensual/trimestral según configuración
- [ ] Formato PDF profesional con logo SENASAG, datos de Hacienda Gamelera, período reportado
- [ ] Exportación CSV con estructura estándar SENASAG: animal_id, caravana, raza, edad, peso_actual, último_pesaje, estado
- [ ] Exportación XML compatible con sistema de SENASAG (si especificación disponible)
- [ ] Datos incluidos: inventario actual, altas (nacimientos/compras), bajas (ventas/muertes), movimientos, pesajes
- [ ] Certificado digital de trazabilidad por animal con historial completo de pesajes
- [ ] Envío automático por email a dirección configurada (bruno@haciendagamelera.com, senasag@gov.bo)
- [ ] Historial de reportes generados: fecha generación, período reportado, tipo, estado (Generado/Enviado/Confirmado)
- [ ] Vista previa de reporte antes de envío oficial
- [ ] Firma digital del propietario: Bruno Brito Macedo (opcional según normativa)
- [ ] Validación de datos antes de generación: alertar si faltan datos críticos

**Story Points**: 8  
**Prioridad**: Alta
**Dependencias**: US-004 (requiere historial completo), US-003 (requiere inventario actualizado)  
**Sprint**: Sprint 3

#### US-008: Integración Gran Paitití

**Como** ganadero boliviano  
**Quiero** integrar el sistema con la plataforma gubernamental Gran Paitití  
**Para** cumplir con normativas REGENSA (Reglamento General de Sanidad Animal) capítulos 3.10 y 7.1 obligatorios

**Criterios de aceptación**:

- [ ] Conexión autenticada con API REST de Gran Paitití (credenciales de Hacienda Gamelera)
- [ ] Generación automática de GMA (Guía de Movimiento Animal) digital con número único
- [ ] Formulario GMA: animal_ids (múltiples), origen (Hacienda Gamelera GPS), destino, motivo (Venta/Traslado/Sacrificio), fecha movimiento
- [ ] Registro digital obligatorio de todos los pesajes con timestamp UTC y ubicación GPS
- [ ] Cumplimiento capítulo 3.10: Requisitos de infraestructura (datos de rampas, corrales, sistemas desinfección)
- [ ] Cumplimiento capítulo 7.1: Control veterinario (campos para registrar inspecciones sanitarias)
- [ ] Validación de datos antes de envío: alertar si faltan campos obligatorios según normativa
- [ ] Sincronización bidireccional: enviar datos locales y recibir confirmaciones/actualizaciones de Gran Paitití
- [ ] Historial de GMA generadas: fecha, destino, animales incluidos, estado (Pendiente/Aprobada/Rechazada/Completada)
- [ ] Manejo de errores de API: reintentos automáticos, notificaciones de fallos, queue de GMAs pendientes
- [ ] Exportación de GMA en PDF oficial con código QR para verificación digital
- [ ] Modo offline: permitir creación de GMA offline y sincronizar cuando haya conexión

**Story Points**: 13  
**Prioridad**: Alta (Crítica para cumplimiento normativo)  
**Dependencias**: US-003 (inventario), US-005 (sincronización), contacto con REGENSA para credenciales API  
**Sprint**: Sprint 3

#### US-009: Exportación ASOCEBU

**Como** ganadero participante en competencias de ASOCEBU  
**Quiero** exportar automáticamente datos históricos de mis animales para eventos ganaderos  
**Para** preparar eficientemente animales para ferias, cumplir requisitos de inscripción y optimizar resultados competitivos

**Criterios de aceptación**:

- [ ] Exportación de historial completo de crecimiento: pesajes, GDP (Ganancia Diaria Promedio), gráficos de evolución
- [ ] Certificación oficial de peso actual y proyección a fecha de competencia
- [ ] Formato Excel/PDF compatible con formularios de inscripción ASOCEBU
- [ ] Datos incluidos: caravana, raza, edad precisa, peso actual, historial 6 meses, GDP promedio, proyección
- [ ] Sección "Preparación para competencias": selección de animales candidatos, tracking de metas de peso
- [ ] Comparativa con estándares ASOCEBU por categoría: "Tu animal está 15 kg sobre el promedio de su categoría"
- [ ] Generación de certificados con datos de Hacienda Gamelera y firma digital de Bruno Brito Macedo
- [ ] Historial de participación en eventos: 3ª Faena Técnica 2024 (medalla bronce - "Mejor lote de carcasas de hembras en confinamiento")
- [ ] Lista de verificación pre-competencia: pesajes recientes, documentación, ajustes nutricionales sugeridos
- [ ] Exportación masiva para lotes completos (ej: 15 hembras para faena)

**Story Points**: 8  
**Prioridad**: Media (Alta si hay competencia próxima)  
**Dependencias**: US-004 (historial de pesajes), US-003 (datos de animales)  
**Sprint**: Sprint 3 (o priorizar si hay evento ASOCEBU cercano)

### Sprint 4: Optimización y Alertas (2 semanas)

#### US-010: Alertas Inteligentes

**Como** ganadero  
**Quiero** recibir alertas automáticas inteligentes sobre situaciones críticas de mis animales  
**Para** tomar acciones preventivas inmediatas y mejorar rendimiento del hato sin revisar manualmente 500 cabezas

**Criterios de aceptación**:

- [ ] Alerta automática por pérdida de peso significativa: ">5% en última semana" con nivel crítico (rojo)
- [ ] Alerta por estancamiento en crecimiento: "Sin ganancia de peso en 15 días" para categorías en crecimiento
- [ ] Alerta por bajo GDP (Ganancia Diaria Promedio): "GDP <0.5 kg/día" comparado con promedio esperado por raza y categoría
- [ ] Recordatorios de pesaje programado: "Hace 30 días del último pesaje del animal #1234"
- [ ] Alertas de eventos importantes: "Vaquilla #456 lista para primer servicio (18 meses, 350 kg)"
- [ ] Configuración personalizada de umbrales: por raza, categoría, y objetivos específicos de Bruno
- [ ] Notificaciones push en dispositivo móvil con sonido y vibración (configurable)
- [ ] Centro de notificaciones en app: lista de alertas pendientes, resueltas, ignoradas
- [ ] Priorización de alertas: Críticas (rojo), Importantes (naranja), Informativas (azul)
- [ ] Acción rápida desde alerta: "Ver animal", "Registrar peso manual", "Ignorar", "Marcar como resuelto"
- [ ] Historial de alertas: tracking de cuándo se generaron y cómo se resolvieron
- [ ] Alertas inteligentes de preparación: "15 animales candidatos para próxima competencia ASOCEBU"

**Story Points**: 8  
**Prioridad**: Media
**Dependencias**: US-004 (historial para detectar anomalías), US-003 (datos de animales)  
**Sprint**: Sprint 4 (Futuro)

#### US-011: Planificación de Sesiones

**Como** ganadero con 500 cabezas distribuidas en 48.5 hectáreas  
**Quiero** planificar sesiones masivas de pesaje con rutas optimizadas  
**Para** reducir tiempo operativo, minimizar desplazamientos y procesar eficientemente lotes completos

**Criterios de aceptación**:

- [ ] Calendario mensual integrado con vista de sesiones de pesaje programadas
- [ ] Creación de sesión masiva: seleccionar 10-50 animales, fecha, hora, ubicación inicial
- [ ] Agrupación inteligente por ubicación: animales del mismo potrero juntos
- [ ] Rutas optimizadas: algoritmo calcula orden óptimo de pesaje por cercanía geográfica (usando GPS de potreros)
- [ ] Estimación de tiempo por sesión: "20 animales = aprox. 1.5 horas" basado en <5 minutos por animal
- [ ] Recordatorios automáticos: notificación 1 día antes y 1 hora antes de sesión programada
- [ ] Modo "Sesión activa": interfaz especial para procesar lista de animales uno por uno con progreso visual
- [ ] Indicador de progreso: "8 de 20 animales completados (40%)" con tiempo transcurrido y estimado restante
- [ ] Exportación de reporte de sesión: animales procesados, pesos obtenidos, duración total, anomalías detectadas
- [ ] Historial de sesiones pasadas: fecha, número de animales, tiempo total, eficiencia (animales/hora)
- [ ] Sugerencias inteligentes: "Sesión óptima: 25 animales del Potrero Norte este viernes 8:00 AM"

**Story Points**: 5  
**Prioridad**: Baja
**Dependencias**: US-003 (animales con ubicaciones), US-006 (búsqueda y filtros)  
**Sprint**: Sprint 4 (Futuro)

## Definición de Ready (DoR)

Una User Story está lista para Sprint Planning cuando cumple TODOS los criterios siguientes:

### Criterios Obligatorios

- [ ] **Descripción clara** en formato: "Como [rol] quiero [acción] para [beneficio]"
- [ ] **Criterios de aceptación** específicos y testeables (mínimo 4, idealmente 6-10)
- [ ] **Story points estimados** por el equipo usando Planning Poker (escala Fibonacci)
- [ ] **Prioridad asignada** por Product Owner: Crítica/Alta/Media/Baja
- [ ] **Dependencias identificadas**: US previas requeridas listadas explícitamente
- [ ] **Sprint asignado**: Sprint 1, 2, 3 o Backlog futuro
- [ ] **Aceptación formal** del Product Owner (Miguel Angel Escobar Lazcano)

### Criterios de Contexto

- [ ] **Validación con usuario**: ¿Bruno Brito Macedo necesita/validó esta funcionalidad?
- [ ] **Valor de negocio claro**: Impacto directo en Hacienda Gamelera documentado
- [ ] **Feasibilidad técnica**: Equipo confirma que es implementable en el sprint
- [ ] **Restricciones consideradas**: Offline-first, zona rural, 7 razas, 500 cabezas

### Criterios Técnicos

- [ ] **Tareas técnicas identificadas**: Backend, Frontend, ML, BD, Tests
- [ ] **Riesgos técnicos documentados**: Complejidad, integraciones, performance
- [ ] **Datos de prueba disponibles**: Datos de Hacienda Gamelera o datos demo
- [ ] **Criterios de performance**: Tiempos de respuesta, límites de carga definidos

### Criterios de Calidad

- [ ] **Estrategia de testing definida**: Unit tests, integration tests, E2E tests
- [ ] **Definition of Done aplicable**: Todos los criterios DoD pueden cumplirse
- [ ] **Métricas de aceptación**: Criterios cuantitativos medibles definidos
- [ ] **Plan de validación**: Cómo se validará con Bruno en Hacienda Gamelera

## Notas sobre Definition of Ready

**¿Cuándo rechazar una User Story?**
- Criterios de aceptación vagos o no testeables
- Dependencias no resueltas de sprints previos
- Estimación imposible por falta de información
- Valor de negocio poco claro para Hacienda Gamelera
- Complejidad excesiva (>13 story points) que requiere división

**Proceso de Refinamiento:**
1. **Product Owner** propone User Story inicial
2. **Equipo** realiza refinamiento en sesión semanal
3. **Discusión técnica**: Clarificación, dependencias, estimación
4. **Validación con Bruno**: Feedback del usuario final (si necesario)
5. **Marcado como Ready**: Todos los criterios DoR cumplidos

## Definición de Done (DoD)

Una User Story está completa cuando cumple TODOS los criterios aplicables:

### Done - Código Individual

- [ ] **Código implementado** según estándares (Flutter/Python)
- [ ] **Tests unitarios** escritos y pasando (cobertura >80%)
- [ ] **Linting** sin errores (Flutter Analyzer, Pylint)
- [ ] **Code review** aprobado por al menos 1 desarrollador
- [ ] **Commits** con mensajes descriptivos (conventional commits)

### Done - Feature Completa

- [ ] **Criterios de aceptación** 100% cumplidos y validados
- [ ] **Tests de integración** pasando
- [ ] **Tests E2E** pasando (si aplica UI)
- [ ] **Performance** dentro de métricas: <3s procesamiento, <3s búsqueda
- [ ] **Funcionamiento offline** validado (si aplica)
- [ ] **Manejo de errores** implementado con mensajes claros

### Done - Sprint

- [ ] **Validación con Bruno Brito Macedo** en Hacienda Gamelera
- [ ] **Testing en condiciones reales** (campo, offline, 500 animales)
- [ ] **Documentación actualizada** (README, comentarios, guías)
- [ ] **Deploy en ambiente de pruebas** exitoso
- [ ] **Demo funcional** para Sprint Review
- [ ] **Aceptación formal** del Product Owner

### Done - Release

- [ ] **Validación en campo** con datos reales de producción
- [ ] **Cumplimiento normativo** (SENASAG/REGENSA/ASOCEBU si aplica)
- [ ] **Deploy en producción** exitoso
- [ ] **Monitoreo activo** configurado
- [ ] **Plan de soporte** documentado

> **Nota**: Ver documento completo en [docs/product/definition-of-done.md](definition-of-done.md)

## Métricas de Producto

### Métricas de Valor (Impacto en Hacienda Gamelera)

| Métrica | Línea Base (Método Actual) | Objetivo (Sistema IA) | Mejora Esperada |
|---------|----------------------------|----------------------|-----------------|
| **Tiempo pesaje 20 animales** | 2-3 días | <2 horas | **80% reducción** |
| **Error de estimación** | ±5-20 kg | <5 kg | **75% mejora** |
| **Personal requerido** | 3-4 personas | 1 operador | **75% reducción** |
| **Calibración diaria** | 30-45 minutos | Eliminada | **100% ahorro** |
| **Tasa de reintentos** | 10% | 0% | **100% eliminación** |
| **Satisfacción usuario** | N/A | >90% | Bruno Brito Macedo |
| **Cumplimiento normativo** | Manual (propenso a errores) | 100% automático | SENASAG/REGENSA/ASOCEBU |

### Métricas Técnicas (Sistema IA)

| Métrica | Objetivo | Método de Medición | Validación |
|---------|----------|-------------------|------------|
| **Precisión ML** | ≥95% (R² ≥ 0.95) | Comparación con peso real en báscula | 50 animales mínimo |
| **Error absoluto** | <5 kg | Promedio \|peso_estimado - peso_real\| | Por raza |
| **Tiempo procesamiento** | <3 segundos | Desde fotograma hasta resultado | Per animal |
| **Tiempo captura** | 3-5 segundos | Captura 10-15 FPS | 30-75 fotogramas |
| **Disponibilidad offline** | >99% uptime | Sin conexión a internet | 100% funcional |
| **Tiempo sincronización** | <30 segundos | 50 registros con 3G | Condiciones reales |
| **Tiempo búsqueda** | <3 segundos | 500 animales con filtros | Con índices optimizados |
| **Cobertura tests** | >80% | Unit + integration tests | Por componente |

### Métricas de Proceso (Scrum)

| Métrica | Objetivo | Sprint 1 | Sprint 2 | Sprint 3 |
|---------|----------|----------|----------|----------|
| **Velocity** | 26 story points | 26 pts | 26 pts | 26 pts |
| **Burndown** | Lineal | Tracking diario | Tracking diario | Tracking diario |
| **Quality (bugs)** | <5 por sprint | TBD | TBD | TBD |
| **Cycle time** | <3 días | Dev → Validation | Dev → Validation | Dev → Validation |
| **Feedback loop** | <24 horas | Bruno feedback | Bruno feedback | Validación normativa |
| **Code reviews** | 100% | Todos los PRs | Todos los PRs | Todos los PRs |
| **DoD compliance** | 100% | Por US | Por US | Por US + Normativa |

### Métricas de Adopción

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Adopción inicial** | 100% | Bruno usa sistema en Sprint 1 |
| **Frecuencia de uso** | Diaria | Pesajes realizados por semana |
| **Animales registrados** | 500 | Inventario completo en sistema |
| **Pesajes totales** | >100 en Sprint 2 | Acumulativo |
| **Reportes generados** | >5 en Sprint 3 | SENASAG/REGENSA/ASOCEBU |
| **Tiempo ahorrado** | >20 horas/mes | vs método tradicional |

### Métricas de Cumplimiento Normativo

| Entidad | Métrica | Objetivo | Sprint | Validación |
|---------|---------|----------|--------|------------|
| **SENASAG** | Reportes automáticos | 100% | Sprint 3 | Estructura contra spec oficial |
| **REGENSA** | Integración Gran Paitití | Funcional | Sprint 3 | GMA según capítulos 3.10 y 7.1 |
| **ASOCEBU** | Exportación competencias | Disponible | Sprint 3 | Datos 3ª Faena Técnica 2024 |
| **Trazabilidad** | Registros digitales | 100% | Sprint 1-3 | Captura → Reporte completo |
| **Cumplimiento legal** | SENASAG + REGENSA | 100% | Sprint 3 | Validado estructuralmente |

## Orden de Priorización (Justificación)

### Sprint 1: Validación Core (CRÍTICO)
**¿Por qué?** Sin captura y estimación precisa, el sistema no tiene valor. Validación temprana con Bruno.

- **US-001** (8 pts): Captura continua → Fundamento del sistema
- **US-002** (13 pts): Estimación IA → Core value proposition
- **US-003** (5 pts): Registro animales → Gestión básica

### Sprint 2: Funcionalidad Completa (ALTO VALOR)
**¿Por qué?** Completar gestión del hato para demostración del 23 octubre.

- **US-004** (8 pts): Historial → Decisiones informadas
- **US-005** (13 pts): Sincronización → Crítico para zona rural
- **US-006** (5 pts): Búsqueda → Escalabilidad 500 animales

### Sprint 3: Integración Normativa (OBLIGATORIO LEGAL)
**¿Por qué?** Cumplimiento normativo boliviano obligatorio.

- **US-007** (8 pts): SENASAG → Trazabilidad obligatoria
- **US-008** (13 pts): Gran Paitití → Capítulos 3.10 y 7.1
- **US-009** (8 pts): ASOCEBU → Competitividad (medalla bronce 3ª Faena)

### Sprint 4+: Optimización (NICE TO HAVE)
**¿Por qué?** Mejoras de eficiencia y experiencia de usuario.

- **US-010** (8 pts): Alertas → Proactividad
- **US-011** (5 pts): Planificación → Optimización operativa

---

## Próximos Pasos

### Sprint 1 (30 sept - 13 oct 2024) ✅
**Objetivo**: Validación Core con Bruno Brito Macedo  
**User Stories**: US-001, US-002, US-003 (26 story points)  
**Entregable**: App funcional con captura, estimación y registro  
**Estado**: Completado

### Sprint 2 (14 oct - 27 oct 2024) ✅
**Objetivo**: Funcionalidad completa para presentación 23 octubre  
**User Stories**: US-004, US-005, US-006 (26 story points)  
**Entregable**: Sistema completo con historial, sincronización y búsqueda  
**Evento crítico**: **Presentación académica 23 octubre** 🎯  
**Estado**: Completado

### Sprint 3 (28 oct - 10 nov 2024) 🎯
**Objetivo**: Integración normativa boliviana completa  
**User Stories**: US-007, US-008, US-009 (26 story points)  
**Entregable**: Cumplimiento SENASAG/REGENSA/ASOCEBU + Sistema listo para producción  
**Evento crítico**: **Presentación FINAL 6 noviembre** 🎯  
**Estado**: En planificación

---

**Documento actualizado**: 28 octubre 2024  
**Próxima revisión**: Daily Scrum y Sprint Review  
**Product Owner**: Miguel Angel Escobar Lazcano  
**Scrum Master**: Rodrigo Escobar Morón

---

## Documentación Complementaria

### User Stories Detalladas (Formato Académico 3C)

Para especificación completa de cada User Story en formato académico 3C (Card, Conversation, Confirmation), ver:

📄 **[product-backlog-detailed.md](product-backlog-detailed.md)**

Ese documento incluye para US-001 a US-011:
- **Card**: ID, prioridad, story points, rol/acción/beneficio
- **Conversation**: Contexto Hacienda Gamelera, restricciones, dependencias, riesgos, Q&A Product Owner
- **Confirmation**: 8-10 criterios aceptación, validación Bruno, métricas cuantificables, DoD aplicable, mockups

---

**Documento Product Backlog v3.0 (Ejecutivo)**  
**Última actualización**: 28 octubre 2024  
**Product Owner**: Miguel Angel Escobar Lazcano  
**Scrum Master**: Rodrigo Escobar Morón  
**Total User Stories**: 11  
**Total Story Points**: 105 (Sprint 1: 26, Sprint 2: 26, Sprint 3: 26, Sprint 4+: 27)

**Documentación relacionada**:
- 📄 Detalle US (3C): [product-backlog-detailed.md](product-backlog-detailed.md)
- ✅ Definition of Done: [definition-of-done.md](definition-of-done.md)
- 🎯 Sprint Goals: [../sprints/](../sprints/)
