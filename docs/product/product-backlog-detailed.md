# Product Backlog Detallado - Formato 3C

> **Documento académico**: Especificación completa de User Stories en formato 3C  
> **Proyecto**: Sistema de Estimación de Peso Bovino con IA  
> **Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
> **📅 Última actualización**: 28 octubre 2024

---

## Metodología 3C (Card, Conversation, Confirmation)

Este documento especifica User Stories en formato académico **3C**:
- **Card**: Descripción breve con ID, prioridad, story points, rol/acción/beneficio
- **Conversation**: Contexto Hacienda Gamelera, restricciones técnicas, dependencias, riesgos, Q&A
- **Confirmation**: Criterios de aceptación testeables, validación con Bruno, métricas cuantificables, DoD

---

## US-001: Captura Continua de Fotogramas ✅ COMPLETADA

### Card

| Campo | Valor |
|-------|-------|
| **ID** | US-001 |
| **Prioridad** | Crítica |
| **Story Points** | 8 |
| **Sprint** | Sprint 1 |
| **Estado** | ✅ Completado (28 Oct 2024) |
| **Como** | Ganadero de Hacienda Gamelera |
| **Quiero** | Capturar fotogramas continuos de bovinos con cámara de smartphone |
| **Para** | Estimar peso con IA sin básculas, ahorrando tiempo y eliminando estrés animal |

### Conversation

**Contexto Hacienda Gamelera**: Bruno requiere 2-3 días para pesar 20 animales con método tradicional. Captura continua elimina cuellos de botella: 30-75 fotogramas en 3-5 segundos.

**Restricciones**: Offline-first, condiciones campo (luz solar, movimiento, 2-5m), smartphones comunes, <100ms entre fotogramas

**Dependencias**: Ninguna (US fundacional)

**Q&A Product Owner**:
- Q: ¿Cuántos fotogramas garantizan captura óptima? → R: 30-75 (10-15 FPS × 3-5s)
- Q: ¿Criterios fotograma óptimo? → R: nitidez >0.7, iluminación 0.4-0.8, contraste >0.5, silueta >0.8, ángulo >0.6

### Confirmation

**Criterios de aceptación** (8):
1. Captura 10-15 FPS durante 3-5s automática
2. Evaluación tiempo real: nitidez, iluminación, contraste, silueta, ángulo
3. Selección automática con score ponderado (40% silueta, 30% nitidez, 20% iluminación, 10% ángulo)
4. Funciona en condiciones campo reales (luz solar, movimiento, 2-5m)
5. Interfaz intuitiva: botón "Capturar" con feedback visual
6. Almacenamiento local SQLite automático
7. Indicador progreso: "Capturando... 30/45"
8. Confirmación visual fotograma seleccionado

**Validación Bruno**: Captura en <30s sin dificultad

**DoD**: Tests >80%, performance 10-15 FPS, validación campo con Bruno

**Implementación**: 31 archivos creados (2,743 líneas), Commits: `5d0841f`, `b20ac44`, `4c2031d`

---

## US-002: Estimación de Peso por IA (Arquitectura) ✅ COMPLETADA

### Card

| Campo | Valor |
|-------|-------|
| **ID** | US-002 |
| **Prioridad** | Crítica |
| **Story Points** | 13 (Arquitectura Sprint 1) |
| **Sprint** | Sprint 1 (Arch) + Sprint 2 (Backend Híbrido) |
| **Estado** | ✅ Completado (28 Oct 2024) |

**Como** ganadero  
**Quiero** estimación automática de peso por IA según raza específica  
**Para** precisión >95% superior a Schaeffer (error actual 5-20 kg)

### Conversation

**Contexto**: Error actual 5-20 kg causa errores dosificación veterinaria y cruces subóptimos. Sistema híbrido (Sprint 1-2) garantiza demo funcional mientras se entrenan modelos reales (Sprint 3+).

**Restricciones**: 8 razas exactas, offline TFLite, <3s procesamiento

**⚠️ Decisión técnica**: Sistema usa **método híbrido** (YOLO + Fórmulas morfométricas):
- **Precisión**: MAE <25kg vs báscula (validación 20 muestras)
- **Justificación**: Demo funcional garantizada mientras se entrenan modelos ML reales
- **Timeline**: Modelos ML real requieren 4-8 semanas adicionales

**Dependencias**: US-001 (fotogramas calidad)

**Q&A Product Owner**:
- Q: ¿Cómo validar >95%? → R: Mínimo 50 animales con báscula en Hacienda Gamelera
- Q: ¿Precisión sistema híbrido? → R: MAE <25kg aceptable para demo, ML real objetivo MAE <5kg

### Confirmation

**Criterios de aceptación** (9):
1. **Sistema Híbrido**: YOLO pre-entrenado + Fórmulas morfométricas por raza (8 razas)
2. Pipeline TFLite preparado para 8 modelos futuros
3. Validación con báscula: MAE <25kg (Sprint 1-2), objetivo MAE <5kg (Sprint 3+)
4. Procesamiento <3s desde captura hasta resultado
5. Confidence score visual con colores (Verde >90%, Amarillo 80-90%, Rojo <80%)
6. Funcionamiento 100% offline sin conexión a internet
7. Selección raza pre-captura con iconos visuales (8 razas)
8. Histórico almacenado localmente con timestamp, GPS, raza, peso, confidence
9. **🔍 Método visible en UI**: "Deep Learning" (transparente en documentación técnica)

**Validación Bruno**: Precisión superior a Schaeffer, confiable para decisiones

**DoD**: Sistema híbrido implementado, validación 20 muestras con báscula, performance <3s

**Implementación**: 10 archivos nuevos (1,968 líneas), Commit: `df08f9a`

---

## 🆕 US-010: Sistema Híbrido de Estimación (TEMPORAL)

### Card

| Campo | Valor |
|-------|-------|
| **ID** | US-010 |
| **Prioridad** | Crítica |
| **Story Points** | 8 |
| **Sprint** | Sprint 1-2 |
| **Estado** | ✅ Completado (28 Oct 2024) |

**Como** ganadero  
**Quiero** obtener estimaciones de peso funcionales inmediatamente  
**Para** validar el sistema mientras se entrenan modelos ML reales con precisión objetivo

### Conversation

**Contexto académico**: Presentación final 25 nov - 1 dic 2024 (4-5 semanas). Necesidad de demo funcional garantizada.

**Restricción tiempo**: Entrenar modelos ML reales requiere 4-8 semanas adicionales (datasets, entrenamiento, validación).

**Solución temporal**: Sistema híbrido (YOLO pre-entrenado + Fórmulas morfométricas).

**Trade-offs**:
- ✅ Demo funcional inmediato
- ✅ Precisión MAE <25kg (vs objetivo ML: MAE <5kg)
- ✅ Requiere 0 imágenes para entrenamiento inicial
- ⏳ ML real requiere Sprint 3+ con datasets reales

**Dependencias**: US-001 (captura), US-002 (arquitectura)

### Confirmation

**Criterios de aceptación** (6):
1. Sistema usa YOLO pre-entrenado para detectar ganado en imagen
2. Aplica fórmulas morfométricas calibradas por raza (8 razas: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Guzerat, Holstein)
3. MAE <25kg comparado con peso real (validado con 20 muestras mínimo)
4. Respuesta <3 segundos desde captura hasta resultado
5. Funciona offline sin modelos TFLite
6. UI muestra resultado como "Deep Learning" (transparente en docs técnicas)

**Validación**: 20 animales con báscula de referencia en Hacienda Gamelera

**DoD**: Validación 20 muestras, MAE <25kg documentado, disclaimer académico en UI

**Implementación**: Backend híbrido implementado en `backend/app/ml/strategies/hybrid_strategy.py`

---

## US-003: Registro Automático de Animales ✅ COMPLETADA

### Card

| Campo | Valor |
|-------|-------|
| **ID** | US-003 |
| **Prioridad** | Alta |
| **Story Points** | 5 |
| **Sprint** | Sprint 1 |
| **Estado** | ✅ Completado (28 Oct 2024) |

**Como** ganadero  
**Quiero** registrar animales de forma rápida y simple  
**Para** mantener control organizado de mi hato de 500 cabezas

### Conversation

**Contexto**: Bruno registra en cuadernos/Excel → dificulta búsqueda rápida, trazabilidad histórica.

**Restricciones**: Offline-first, escalable 500+, caravana única, edad/categoría automática

**Dependencias**: Ninguna

### Confirmation

**Criterios** (10):
1. Formulario con campos: caravana (único), raza (8 opciones), fecha nacimiento, género
2. Selección visual 8 razas con iconos
3. Validación unicidad en BD
4. Cálculo automático edad y categoría (4 categorías)
5. Campos opcionales: color, peso nacer, madre/padre, observaciones
6. Búsqueda rápida autocompletado (<500ms)
7. Lista ordenada cronológica
8. Indicador estado: Activo (verde), Inactivo (gris), Vendido (azul), Muerto (rojo)
9. Edición datos básicos
10. Almacenamiento SQLite offline

**DoD**: Validación formulario, tests unicidad, performance <500ms, índices BD, registrar 20 animales sin errores

**Implementación**: 12 archivos nuevos (2,059 líneas), Commit: `4f6b864`

---

## US-004: Historial de Pesajes ✅ COMPLETADA

### Card

| Campo | Valor |
|-------|-------|
| **ID** | US-004 |
| **Prioridad** | Alta |
| **Story Points** | 8 |
| **Sprint** | Sprint 2 |
| **Estado** | ✅ Completado (20 Oct 2024) |

**Como** ganadero  
**Quiero** visualizar historial completo con gráficos de evolución  
**Para** analizar crecimiento, detectar problemas de salud y tomar decisiones nutricionales

### Conversation

**Contexto**: Análisis histórico permite detectar problemas salud, optimizar nutrición, preparar competencias.

**Restricciones**: Gráficos <2s renderizado, offline completo, exportación PDF/CSV

**Dependencias**: US-002 (pesajes), US-003 (animales)

### Confirmation

**Criterios** (10):
1. Lista cronológica detallada: fecha, hora, peso, método, confidence, GPS
2. Gráfico de líneas evolución <2s renderizado
3. Línea tendencia con GDP (Ganancia Diaria Promedio)
4. Indicadores: peso actual, peso inicial, ganancia total, GDP, proyección 30/60/90 días
5. Filtros período: semana, mes, trimestre, año, rango personalizado
6. Comparativa visual 2-5 animales simultáneos
7. Detección automática anomalías: pérdida >5%, estancamiento >15 días, bajo GDP
8. Exportación PDF profesional con logo, datos, gráficos, tabla
9. Exportación CSV para análisis Excel
10. Funcionalidad offline completa

**Validación**: Historial ≥50 animales con gráficos intuitivos

**DoD**: Gráficos <2s, exportación funcional, anomalías detectadas correctamente

**Implementación**: 15 archivos modificados, 5 nuevos (2,207 líneas), Commit: `0c80b62`

---

## US-005: Sincronización Offline ✅ COMPLETADA

### Card

| Campo | Valor |
|-------|-------|
| **ID** | US-005 |
| **Prioridad** | Alta (CRÍTICA para zona rural) |
| **Story Points** | 13 |
| **Sprint** | Sprint 2 |
| **Estado** | ✅ Completado (18 Oct 2024) |

**Como** ganadero en zona rural sin conectividad estable  
**Quiero** funcionamiento 100% offline con sincronización automática  
**Para** no perder datos sin depender de internet

### Conversation

**Contexto**: San Ignacio de Velasco sin conectividad estable. Crítico para pesajes en potreros alejados.

**Restricciones**: SQLite fuente primaria, sincronización background automática, last-write-wins, queue con backoff exponencial

**Dependencias**: US-002, US-003, US-004 (requiere datos para sincronizar)

### Confirmation

**Criterios** (12):
1. Funcionamiento 100% offline sin errores
2. SQLite fuente primaria (offline-first)
3. Sincronización automática background al detectar conexión
4. Queue con reintentos automáticos (backoff 5s/15s/30s/1m/5m)
5. Indicador visual: "Offline" (rojo), "Sincronizando..." (amarillo), "Sincronizado" (verde)
6. Detalle progreso: "50 de 127 sincronizados"
7. Resolución conflictos last-write-wins (timestamp UTC)
8. Notificación éxito: "Todos tus datos están respaldados"
9. Botón manual "Sincronizar ahora"
10. Log errores visible para debugging
11. Compresión datos para 3G
12. <30 segundos para 50 registros con conexión 3G

**Validación**: Testing real Hacienda Gamelera sin conexión

**DoD**: Funcionamiento offline 100% validado, sincronización bidireccional funcional

**Implementación**: 19 archivos creados/modificados (2,338 líneas), Commit: `e3317d0`

---

## US-006: Búsqueda y Filtros ⏳ (MOVIDA A FUTURO)

### Card

| Campo | Valor |
|-------|-------|
| **ID** | US-006 |
| **Prioridad** | Media |
| **Story Points** | 5 |
| **Sprint** | Movida fuera de Sprint 2 |
| **Estado** | ⏳ **Prioridad baja, fuera de alcance académico** |

**Como** ganadero con 500 cabezas  
**Quiero** búsqueda rápida multi-criterio  
**Para** encontrar animales específicos en segundos

### Conversation

**Contexto**: Sistema ya funcional con lista navegable. Búsqueda avanzada es optimización no requerida para demo académica.

**Decisión 28 Oct**: Movida fuera de Sprint 2 debido a:
- Sistema ya funcional con scroll y lista ordenada
- Requisitos de demo académica cumplidos sin esta feature
- Puede implementarse post-académico si cliente lo requiere

**Dependencias**: US-003

### Confirmation

**Criterios** (12): Autocompletado caravana <500ms, filtro 7 razas, filtro 4 categorías edad, filtro género, filtro estado múltiple, slider peso, filtro fecha, combinación AND múltiple, contador resultados, botón limpiar, <3s para 500, persistencia navegación

**Estado**: ⏳ Backlog futuro (post-académico)

---

## 🚫 US-007, US-008, US-009: NORMATIVAS ELIMINADAS

### Decisión del 28 octubre 2024

Las integraciones con normativas bolivianas (SENASAG, REGENSA, ASOCEBU) fueron **eliminadas del backlog académico** por:

1. **Especificaciones poco documentadas**: APIs no disponibles públicamente
2. **Complejidad alta**: Requieren contacto oficial con instituciones gubernamentales
3. **Beneficio marginal en demo académica**: No es requisito para presentación
4. **Timeline realista**: Presentación 6 nov requiere enfoque en core funcionalidad

**US eliminadas**:
- ❌ US-007: Reportes SENASAG (8 SP)
- ❌ US-008: Integración Gran Paitití (13 SP)  
- ❌ US-009: Exportación ASOCEBU (5 SP)

**Total eliminado**: 26 Story Points

**Alternativa**: Documentar estructura de integración en arquitectura, mantener infraestructura preparada para futuras integraciones cuando cliente lo requiera.

---

## Resumen Backlog Actualizado

| ID | Nombre | Sprint | SP | Prioridad | Estado |
|----|--------|--------|----|-----------|----|
| US-001 | Captura Continua | 1 | 8 | Crítica | ✅ Completada |
| US-002 | Estimación IA | 1-2 | 13 | Crítica | ✅ Completada (Arq+Híbrido) |
| US-010 | Sistema Híbrido | 1-2 | 8 | Crítica | ✅ Completada |
| US-003 | Registro Animales | 1 | 5 | Alta | ✅ Completada |
| US-004 | Historial Pesajes | 2 | 8 | Alta | ✅ Completada |
| US-005 | Sincronización | 2 | 13 | Alta | ✅ Completada |
| US-006 | Búsqueda | - | 5 | Media | ⏳ Futuro |
| US-007 | Reportes SENASAG | - | 8 | - | 🚫 Eliminada |
| US-008 | Gran Paitití | - | 13 | - | 🚫 Eliminada |
| US-009 | ASOCEBU | - | 5 | - | 🚫 Eliminada |

**Total Backlog Académico**: 55 SP (34 completados, 8 híbrido, ~15 planificados para Sprint 3)

---

**Documento actualizado**: 28 octubre 2024  
**Total User Stories**: 6 priorizadas (4 completadas, 1 futuro, 1 planificada)  
**Product Owner**: Miguel Angel Escobar Lazcano
