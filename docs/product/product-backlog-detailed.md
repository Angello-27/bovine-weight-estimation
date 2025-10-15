# Product Backlog - Detalle Académico (Formato 3C)

> **Documento académico**: Especificación completa de User Stories  
> **Proyecto**: Sistema de Estimación de Peso Bovino con IA  
> **Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
> **Fecha**: 28 octubre 2024

## Metodología de Especificación 3C

Este documento contiene la especificación completa de todas las User Stories en formato académico **3C (Card, Conversation, Confirmation)** requerido por metodología Scrum:

- **Card (Tarjeta)**: Descripción breve con ID, prioridad, story points, rol/acción/beneficio
- **Conversation (Conversación)**: Contexto Hacienda Gamelera, restricciones técnicas, dependencias, riesgos identificados, Q&A con Product Owner
- **Confirmation (Confirmación)**: Criterios de aceptación testeables, validación con Bruno Brito Macedo, métricas cuantificables, DoD aplicable, prototipos/mockups

**Referencia rápida**: Ver `product-backlog.md` para resumen ejecutivo de todas las US.

---

## US-001: Captura Continua de Fotogramas ✅ COMPLETADA

### Card (Tarjeta)

| Campo | Valor |
|-------|-------|
| **ID** | US-001 |
| **Nombre** | Captura Continua de Fotogramas |
| **Prioridad** | Crítica |
| **Story Points** | 8 |
| **Sprint** | Sprint 1 |
| **Estado** | ✅ **COMPLETADA** (28 Oct 2024) |
| **Como** | Ganadero de Hacienda Gamelera |
| **Quiero** | Capturar fotogramas continuos de bovinos con cámara de smartphone |
| **Para** | Estimar peso con IA sin básculas, ahorrando tiempo y eliminando estrés animal |

### Conversation (Conversación)

**Contexto de negocio (Hacienda Gamelera)**:  
Bruno Brito Macedo y equipo requieren actualmente 2-3 días para pesar 20 animales con método tradicional:
- 30-45 minutos calibración diaria
- 1-2 horas coordinación personal (capataz, vaquero, peón)
- 5-10 minutos/animal captura y aseguramiento
- 10% reintentos por lecturas inestables

Captura continua elimina cuellos de botella: 30-75 fotogramas en 3-5 segundos sin intervención manual compleja.

**Restricciones técnicas**:
- Offline-first (zona rural sin conectividad)
- Condiciones campo (luz solar variable, movimiento animal, distancia 2-5m)
- Smartphones comunes (no equipos especializados)
- Performance fluida (<100ms entre fotogramas)

**Dependencias**: Ninguna (US fundacional)

**Riesgos**: Performance dispositivos gama baja, animales en movimiento, UX intuitivo para personal rural

**Q&A Product Owner**:
- Q: ¿Cuántos fotogramas garantizan captura óptima? → R: 30-75 (10-15 FPS × 3-5s)
- Q: ¿Criterios fotograma óptimo? → R: nitidez >0.7, iluminación 0.4-0.8, contraste >0.5, silueta >0.8, ángulo >0.6
- Q: ¿Qué hacer si ninguno cumple? → R: Reintento inmediato con feedback visual

### Confirmation (Confirmación)

**Criterios de aceptación** (8 críticos):
1. Captura 10-15 FPS durante 3-5s automática
2. Evaluación tiempo real: nitidez, iluminación, contraste, silueta, ángulo
3. Selección automática score ponderado (40% silueta, 30% nitidez, 20% iluminación, 10% ángulo)
4. Funciona en campo real (luz solar, movimiento, 2-5m)
5. Interfaz intuitiva: botón "Capturar" con feedback visual
6. Almacenamiento local SQLite automático
7. Indicador progreso: "Capturando... 30/45"
8. Confirmación visual fotograma seleccionado

**Validación Bruno**: ¿Captura en <30s sin dificultad? ¿Interfaz simple? ¿Fotogramas claros? ¿Prefiere esto vs báscula?

**Métricas**: FPS ≥10, fotogramas ≥30, selección <500ms

**DoD**: Tests >80%, performance 10-15 FPS en gama media, validación campo con Bruno

**Mockup**: Pantalla cámara con botón "Capturar", overlay contador, fotograma seleccionado con score

**Implementación realizada**:
- ✅ Commits: 5d0841f, b20ac44, 4c2031d
- ✅ 31 archivos creados (2,743 líneas)
- ✅ Clean Architecture + SOLID + Atomic Design
- ✅ Documentación: docs/sprints/sprint-01/sprint-progress.md

---

## US-002: Estimación de Peso por Raza ✅ COMPLETADA

### Card (Tarjeta)

| Campo | Valor |
|-------|-------|
| **ID** | US-002 |
| **Nombre** | Estimación de Peso por Raza con IA |
| **Prioridad** | Crítica |
| **Story Points** | 13 |
| **Sprint** | Sprint 1 |
| **Estado** | ✅ **COMPLETADA** (28 Oct 2024) |
| **Como** | Ganadero Hacienda Gamelera |
| **Quiero** | Estimación automática peso por IA según raza específica |
| **Para** | Precisión >95% superior a Schaeffer (error actual 5-20 kg) |

### Conversation (Conversación)

**Contexto**: Método actual (Schaeffer) con error 5-20 kg causa:
- Errores dosificación veterinaria
- Cruces subóptimos (vaquillas subpesadas → complicaciones parto)
- Preparación inadecuada competencias (solo 10/15 hembras procesadas para 3ª Faena 2024)

IA con modelos por raza: precisión >95% considerando morfología única de cada raza.

**Restricciones**: 7 razas exactas (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey), offline TFLite, <3s procesamiento, R² ≥0.95

**Dependencias**: US-001 (fotogramas calidad)

**Riesgos**: Dataset limitado puede no alcanzar >95%, razas mixtas, conseguir imágenes etiquetadas

**Q&A PO**:
- Q: ¿Cómo validar >95%? → R: Mínimo 50 animales con báscula en Hacienda Gamelera
- Q: ¿Razas mixtas? → R: Selección manual antes de captura, usar modelo más cercano
- Q: ¿Cuántas imágenes/raza? → R: 100 training + 30 validation = ~1000 total

### Confirmation

**Criterios** (9 críticos):
1. 7 razas bovinas con modelos ML específicos
2. TensorFlow Lite CNN (MobileNetV2/EfficientNet)
3. R² ≥0.95 validado con ≥3 razas principales
4. Error absoluto <5 kg
5. Procesamiento <3s
6. Confidence score visual con colores (Verde >90%, Amarillo 80-90%, Rojo <80%)
7. 100% offline
8. Selección raza pre-captura con iconos
9. Histórico local con timestamp, GPS, raza, peso, confidence

**Validación Bruno**: ¿Más preciso que Schaeffer? ¿±5 kg vs báscula? ¿Confiable para decisiones veterinarias? ¿Más rápido?

**Métricas**: R² ≥0.95, MAE <5kg, MAPE <5%, inferencia <3s, N ≥50 animales validación

**DoD**: Modelo entrenado ≥700 imágenes, R² ≥0.95 validation, TFLite <50MB, performance <3s, code review, validación campo ≥20 animales

**Mockup**: Grid 3x3 razas con iconos, resultado peso grande + confidence color

**Implementación realizada**:
- ✅ Commit: df08f9a
- ✅ 10 archivos nuevos, 5 modificados (1,968 líneas)
- ✅ TFLiteDataSource con 7 modelos por raza
- ✅ BreedSelectorGrid (organism Atomic Design)
- ✅ SQLite tabla weight_estimations con 4 índices
- ✅ Confidence score con colores (Verde/Amarillo/Rojo)
- ✅ Integración US-001 → US-002 completa

---

## US-003: Registro Automático de Animales

### Card

| Campo | Valor |
|-------|-------|
| **ID** | US-003 |
| **Nombre** | Registro de Animales |
| **Prioridad** | Alta |
| **Story Points** | 5 |
| **Sprint** | Sprint 1 |
| **Como** | Ganadero Hacienda Gamelera |
| **Quiero** | Registrar animales rápido y simple |
| **Para** | Control organizado de 500 cabezas |

### Conversation

**Contexto**: Bruno registra en cuadernos/Excel → dificulta búsqueda rápida, trazabilidad histórica, cumplimiento SENASAG, escalabilidad 500 cabezas.

Registro digital vincula animal con historial pesajes → análisis crecimiento + cumplimiento normativo.

**Restricciones**: Offline-first, escalable 500+, caravana única, edad/categoría automática

**Dependencias**: Ninguna

**Riesgos**: Formulario complejo para personal rural, duplicados caravana, búsqueda <500ms en 500 animales

**Q&A PO**:
- Q: ¿Campos obligatorios? → R: Caravana, raza, fecha nacimiento, género. Opcionales: color, peso nacer, madre/padre, observaciones
- Q: ¿Cálculo categoría? → R: <8m Ternero, 6-18m Vaquillona/Torillo, 19-30m Vaquillona/Torete, >30m Vaca/Toro
- Q: ¿Editar/eliminar? → R: Sí editar. Eliminar = cambiar estado "Muerto/Vendido" (no borrar)

### Confirmation

**Criterios** (10):
1. Formulario: caravana único, raza (7 opciones), fecha nacimiento, género
2. Selección raza visual con iconos
3. Validación único en BD
4. Cálculo automático edad/categoría (4 categorías)
5. Campos opcionales: color, peso nacer, madre/padre, observaciones
6. Búsqueda rápida autocompletado (<500ms)
7. Lista ordenada cronológica con scroll
8. Indicador estado: Activo (verde), Inactivo (gris), Vendido (azul), Muerto (rojo)
9. Edición datos básicos
10. Almacenamiento SQLite offline

**Validación Bruno**: 10 animales en <30min? Búsqueda rápida? Lista 500 navegable? Campos cubren necesidades?

**DoD**: Formulario validado, tests unicidad, performance <500ms en 1000 animales, índices BD, queries optimizadas, registrar 20 animales sin errores

**Mockup**: Formulario vertical, botones grandes táctil. Lista: tarjetas con foto placeholder, caravana, raza, edad, estado

---

## US-004: Historial de Pesajes

### Card

| **ID** | US-004 | **Sprint** | Sprint 2 |
| **Nombre** | Historial de Pesajes con Gráficos | **Prioridad** | Alta |
| **Story Points** | 8 | **Dependencias** | US-002, US-003 |

**Como** ganadero quiero visualizar historial completo con gráficos de evolución para analizar crecimiento y tomar decisiones informadas nutricionales.

### Conversation

**Contexto**: Necesidad de análisis histórico para detectar problemas salud, optimizar nutrición, preparar competencias.

**Restricciones**: Gráficos <2s renderizado, offline completo, exportación PDF/CSV

**Riesgos**: Performance gráficos con muchos datos, complejidad exportación PDF

**Q&A PO**: Período análisis: 12 meses. Comparativas: 2-5 animales simultáneos. Anomalías: >5% pérdida, >15 días estancamiento.

### Confirmation

**Criterios** (10): Lista cronológica detallada, gráfico evolución <2s, línea tendencia GDP, indicadores clave, filtros período, comparativa 2-5 animales, detección anomalías automática, PDF profesional, CSV Excel, offline completo.

**Validación**: Historial ≥50 animales con gráficos intuitivos

---

## US-005: Sincronización Offline

### Card

| **ID** | US-005 | **Sprint** | Sprint 2 |
| **Nombre** | Sincronización Offline-First | **Prioridad** | Alta (CRÍTICA rural) |
| **Story Points** | 13 | **Dependencias** | US-002, US-003, US-004 |

**Como** ganadero en zona rural quiero funcionamiento offline completo con sincronización automática para no perder datos sin depender de internet.

### Conversation

**Contexto**: San Ignacio de Velasco sin conectividad estable. Crítico para pesajes en potreros alejados.

**Restricciones**: SQLite fuente primaria, sincronización background automática, last-write-wins, queue con backoff exponencial

**Riesgos**: Conflictos de datos, pérdida información, complejidad resolución

**Q&A PO**: Estrategia conflictos: last-write-wins timestamp UTC. Compresión datos: optimizar 3G. No intervención manual usuario.

### Confirmation

**Criterios** (12): 100% offline sin errores, SQLite fuente primaria, sincronización automática background, queue reintentos (backoff 5s/15s/30s/1m/5m), indicador visual estado, detalle "50 de 127 sincronizados", last-write-wins UTC, notificación éxito, botón manual "Sincronizar ahora", log errores visible, compresión datos, <30s para 50 registros 3G.

**Validación**: Testing real Hacienda Gamelera sin conexión

---

## US-006: Búsqueda y Filtros

### Card

| **ID** | US-006 | **Sprint** | Sprint 2 |
| **Nombre** | Búsqueda Optimizada 500 Animales | **Prioridad** | Media |
| **Story Points** | 5 | **Dependencias** | US-003 |

**Como** ganadero con 500 cabezas quiero búsqueda rápida multi-criterio para encontrar animales específicos en segundos.

### Conversation

**Contexto**: 500 cabezas requieren búsqueda eficiente (no listas manuales).

**Restricciones**: <3s para 500 animales, índices optimizados, múltiples filtros simultáneos

**Riesgos**: Performance degradada sin índices, complejidad UI con muchos filtros

**Q&A PO**: Filtros principales: caravana (autocompletado), raza (7 checkboxes), edad (4 categorías), género, estado, rango peso, fecha último pesaje.

### Confirmation

**Criterios** (12): Autocompletado <500ms, filtro 7 razas, filtro 4 categorías edad, filtro género, filtro estado múltiple, slider peso 150-600kg, filtro fecha pesaje, combinación AND múltiple, contador resultados, botón limpiar, <3s para 500, persistencia navegación.

**Validación**: Búsqueda fluida en dataset 500 animales

---

## US-007: Reportes SENASAG

### Card

| **ID** | US-007 | **Sprint** | Sprint 3 |
| **Nombre** | Reportes SENASAG Automáticos | **Prioridad** | Alta (legal obligatorio) |
| **Story Points** | 8 | **Dependencias** | US-004, US-003 |

**Como** ganadero boliviano quiero generar reportes automáticos trazabilidad SENASAG para cumplir normativa sin procesos manuales.

### Conversation

**Contexto**: SENASAG (Servicio Nacional Sanidad Agropecuaria) requiere trazabilidad obligatoria.

**Restricciones**: PDF profesional logo SENASAG, CSV estructura estándar, XML compatible, datos Hacienda Gamelera correctos

**Riesgos**: Especificación SENASAG poco documentada, formatos pueden cambiar

**Q&A PO**: Frecuencia: mensual/trimestral. Envío: automático email. Firma digital: Bruno Brito Macedo opcional. Validación: estructura antes generación.

### Confirmation

**Criterios** (11): Generación automática mensual/trimestral, PDF logo SENASAG + datos Hacienda, CSV estándar, XML compatible, datos inventario/altas/bajas/movimientos, certificado digital trazabilidad, email automático bruno@/senasag@, historial reportes con estados, vista previa, firma digital Bruno opcional, validación datos críticos.

**Validación**: Reporte 500 cabezas en <5min, estructura contra spec SENASAG

---

## US-008: Integración Gran Paitití

### Card

| **ID** | US-008 | **Sprint** | Sprint 3 |
| **Nombre** | Integración Gran Paitití (REGENSA) | **Prioridad** | Alta (CRÍTICA normativa) |
| **Story Points** | 13 | **Dependencias** | US-003, US-005, contacto REGENSA |

**Como** ganadero boliviano quiero integrar con Gran Paitití para cumplir REGENSA capítulos 3.10 y 7.1 obligatorios.

### Conversation

**Contexto**: REGENSA (Reglamento General Sanidad Animal) capítulos 3.10 (infraestructura) y 7.1 (sanitario) obligatorios. Gran Paitití: plataforma gubernamental registro.

**Restricciones**: API REST autenticada, GMA número único, código QR verificable, registro pesajes GPS + timestamp UTC, modo offline creación GMA

**Riesgos**: API no disponible/documentada, complejidad normativa capítulos 3.10/7.1, tiempo limitado integración real

**Q&A PO**: Sandbox para desarrollo. Estructura GMA según normativa. Sincronización bidireccional. QR formato estándar.

### Confirmation

**Criterios** (12): API autenticada Gran Paitití, GMA digital número único, formulario (animales múltiples, origen GPS Hacienda, destino, motivo, fecha), registro pesajes GPS + timestamp UTC, capítulo 3.10 (rampas/corrales/desinfección), capítulo 7.1 (veterinario), validación campos obligatorios, sincronización bidireccional, historial GMAs con estados, manejo errores/reintentos/queue, PDF oficial con QR, modo offline.

**Validación**: GMA demo Hacienda Gamelera según normativa

---

## US-009: Exportación ASOCEBU

### Card

| **ID** | US-009 | **Sprint** | Sprint 3 |
| **Nombre** | Exportación Datos ASOCEBU | **Prioridad** | Media (Alta si competencia) |
| **Story Points** | 5 | **Dependencias** | US-004, US-003 |

**Como** ganadero participante competencias ASOCEBU quiero exportar datos históricos automáticamente para preparar eficientemente animales y optimizar resultados.

### Conversation

**Contexto**: ASOCEBU (Asociación Criadores Cebuinos) organiza competencias. Hacienda Gamelera: medalla bronce 3ª Faena Técnica 2024 "Mejor lote carcasas hembras confinamiento".

**Restricciones**: Excel/PDF compatible formularios ASOCEBU, historial 6 meses, GDP, proyecciones

**Riesgos**: Formato ASOCEBU puede variar por evento

**Q&A PO**: Incluir historial 3ª Faena 2024. Proyecciones fecha competencia. Certificación peso oficial. Exportación masiva lotes.

### Confirmation

**Criterios** (10): Historial crecimiento (pesajes, GDP, gráficos), certificación peso + proyección, Excel/PDF compatible ASOCEBU, datos caravana/raza/edad/peso/historial 6m/GDP, sección preparación competencias, comparativa estándares ASOCEBU, certificados firma Bruno, historial 3ª Faena 2024 bronce, checklist pre-competencia, exportación masiva lotes.

**Validación**: Datos 3ª Faena 2024 exportables, certificados profesionales

---

## US-010: Alertas Inteligentes

### Card

| **ID** | US-010 | **Sprint** | Sprint 4 (Futuro) |
| **Nombre** | Alertas Inteligentes Configurables | **Prioridad** | Media |
| **Story Points** | 8 | **Dependencias** | US-004, US-003 |

**Como** ganadero quiero alertas automáticas situaciones críticas para acción preventiva sin revisar 500 cabezas manualmente.

### Conversation

**Contexto**: 500 animales imposibles monitorear manualmente. Alertas automáticas permiten gestión proactiva.

**Restricciones**: Offline (local notifications), configurables por raza/categoría, no invasivas

**Riesgos**: Alertas molestas/irrelevantes, falsos positivos, configuración compleja

**Q&A PO**: Umbrales: >5% pérdida peso, >15 días sin ganancia, GDP <0.5 kg/día, >30 días sin pesaje. Configurable por Bruno.

### Confirmation

**Criterios** (12): Pérdida peso >5% (crítico rojo), estancamiento 15 días, bajo GDP vs promedio raza, recordatorios pesaje >30 días, eventos importantes (vaquilla lista servicio), umbrales configurables, notificaciones push, centro notificaciones app, priorización (crítico/importante/info), acciones rápidas desde alerta, historial alertas, preparación competencias.

---

## US-011: Planificación de Sesiones

### Card

| **ID** | US-011 | **Sprint** | Sprint 4 (Futuro) |
| **Nombre** | Planificación Sesiones Masivas | **Prioridad** | Baja |
| **Story Points** | 5 | **Dependencias** | US-003, US-006 |

**Como** ganadero con 500 cabezas en 48.5 hectáreas quiero planificar sesiones masivas con rutas optimizadas para reducir tiempo y desplazamientos.

### Conversation

**Contexto**: Pesajes masivos requieren planificación para minimizar traslados en 48.5 hectáreas.

**Restricciones**: GPS potreros, algoritmo optimización rutas, estimaciones tiempo realistas

**Riesgos**: Complejidad algoritmo rutas, datos GPS potreros incompletos

**Q&A PO**: Sesiones 10-50 animales. Agrupación potrero. Estimación: <5min/animal. Modo sesión activa con progreso.

### Confirmation

**Criterios** (11): Calendario mensual, creación sesión (10-50 animales, fecha/hora/ubicación), agrupación potrero, rutas optimizadas GPS, estimación tiempo (~1.5h para 20), recordatorios (1 día y 1 hora antes), modo sesión activa con progreso, indicador "8/20 (40%)" + tiempo, reporte sesión, historial sesiones, sugerencias inteligentes.

---

## Resumen User Stories

| ID | Nombre | Sprint | Story Points | Prioridad | Formato 3C |
|----|--------|--------|--------------|-----------|------------|
| US-001 | Captura Continua | 1 | 8 | Crítica | ✅ Completo |
| US-002 | Estimación IA Raza | 1 | 13 | Crítica | ✅ Completo |
| US-003 | Registro Animales | 1 | 5 | Alta | ✅ Completo |
| US-004 | Historial Pesajes | 2 | 8 | Alta | ✅ Completo |
| US-005 | Sincronización Offline | 2 | 13 | Alta | ✅ Completo |
| US-006 | Búsqueda/Filtros | 2 | 5 | Media | ✅ Completo |
| US-007 | Reportes SENASAG | 3 | 8 | Alta | ✅ Completo |
| US-008 | Gran Paitití/GMA | 3 | 13 | Alta | ✅ Completo |
| US-009 | Exportación ASOCEBU | 3 | 5 | Media | ✅ Completo |
| US-010 | Alertas Inteligentes | 4 | 8 | Media | ✅ Completo |
| US-011 | Planificación Sesiones | 4 | 5 | Baja | ✅ Completo |

**Total**: 11 User Stories | 105 Story Points

---

## Referencias

- **Product Backlog (Ejecutivo)**: [product-backlog.md](product-backlog.md)
- **Definition of Done**: [definition-of-done.md](definition-of-done.md)
- **Sprint Goals**: [../sprints/sprint-01/](../sprints/sprint-01/), [sprint-02](../sprints/sprint-02/), [sprint-03](../sprints/sprint-03/)

---

**Documento Product Backlog Detallado (Académico) v1.0**  
**Formato**: 3C (Card, Conversation, Confirmation)  
**Fecha**: 28 octubre 2024  
**Product Owner**: Miguel Angel Escobar Lazcano  
**Scrum Master**: Rodrigo Escobar Morón  
**Cliente**: Bruno Brito Macedo - Hacienda Gamelera

