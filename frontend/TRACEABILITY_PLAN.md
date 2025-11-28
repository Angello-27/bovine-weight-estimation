# 🐄 Plan de Trazabilidad del Ganado - Panel Web

## 📋 Objetivo
Implementar un sistema completo de trazabilidad que permita rastrear el historial completo de cada animal desde su registro hasta el presente, cumpliendo con normativas bolivianas (SENASAG, REGENSA, ASOCEBU).

---

## 🎯 Funcionalidades de Trazabilidad

### 1. **Vista de Trazabilidad Individual (CattleDetailView)**

#### Timeline Completo del Animal
- 📅 **Registro**: Fecha de registro, origen (comprado/nacido en hacienda)
- 👶 **Nacimiento**: Fecha, peso al nacer, raza, género
- 👨‍👩‍👧 **Linaje**: Padre y madre (si están registrados)
- 📸 **Fotos**: Galería de fotos del animal a lo largo del tiempo
- ⚖️ **Historial de Pesos**: Todas las estimaciones con gráfico de evolución
- 📍 **Ubicaciones GPS**: Dónde se hicieron las estimaciones (si hay GPS)
- 🏥 **Eventos**: Cambios de estado (active → sold, deceased, etc.)
- 📝 **Observaciones**: Notas y observaciones históricas

#### Información de Trazabilidad
- **Caravana**: Número único de identificación
- **Estado actual**: Active, Inactive, Sold, Deceased
- **Edad**: Cálculo automático desde fecha de nacimiento
- **Categoría de edad**: Ternero, Vaquillona/Torillo, etc.
- **Última actualización**: Timestamp de última modificación

---

### 2. **Búsqueda y Filtros Avanzados**

#### Búsqueda
- 🔍 Por caravana (búsqueda exacta)
- 🔍 Por nombre (búsqueda parcial)
- 🔍 Por raza
- 🔍 Por género
- 🔍 Por rango de edad
- 🔍 Por estado (active, sold, deceased)

#### Filtros
- 📅 Rango de fechas de registro
- 🏷️ Múltiples razas
- 📊 Rango de peso actual
- 📍 Con/sin GPS en estimaciones
- 🔄 Con/sin estimaciones recientes

---

### 3. **Reportes de Trazabilidad**

#### Reporte Individual
- Certificado de trazabilidad de un animal
- Incluye: Datos completos, linaje, historial de pesos, eventos
- Formato: PDF profesional
- Cumple normativas SENASAG

#### Reporte de Inventario
- Lista completa de animales
- Filtrado por criterios
- Exportación: PDF, CSV, Excel
- Cumple normativas SENASAG (inventario mensual/trimestral)

#### Reporte de Movimientos
- Animales vendidos (con fechas)
- Animales fallecidos (con fechas)
- Formato: PDF, CSV
- Para REGENSA (GMA - Guía de Movimiento Animal)

#### Reporte de Crecimiento
- Evolución de peso por animal
- GDP (Ganancia Diaria Promedio)
- Gráficos de crecimiento
- Para ASOCEBU (competencias ganaderas)

---

### 4. **Visualización de Linaje**

#### Árbol Genealógico
- Mostrar padre y madre del animal
- Navegación a padres (si están registrados)
- Visualización de descendencia (hijos del animal)
- Generaciones: Abuelos, bisabuelos (si están registrados)

#### Información de Linaje
- Raza del padre
- Raza de la madre
- Raza resultante (cruzamiento)
- Porcentaje de pureza (si aplica)

---

### 5. **Historial de Eventos**

#### Tipos de Eventos
- ✅ **Registro**: Animal registrado en el sistema
- 👶 **Nacimiento**: Fecha de nacimiento
- ⚖️ **Estimación de Peso**: Cada estimación realizada
- 📸 **Foto Agregada**: Nueva foto del animal
- 📝 **Observación Agregada**: Nueva nota
- 🔄 **Estado Cambiado**: Active → Sold, Deceased, etc.
- 📍 **Ubicación Registrada**: GPS en estimación
- 🔄 **Actualización**: Cualquier cambio en datos

#### Timeline Visual
- Cronología completa de eventos
- Filtros por tipo de evento
- Búsqueda por fecha
- Exportación del historial

---

### 6. **Exportación y Cumplimiento Normativo**

#### Formatos de Exportación
- **PDF**: Reportes profesionales con logo
- **CSV**: Para análisis en Excel
- **Excel**: Con formato y gráficos
- **XML**: Para integración con sistemas SENASAG/REGENSA

#### Cumplimiento Normativo

**SENASAG (Trazabilidad Ganadera)**
- ✅ Certificado de trazabilidad individual
- ✅ Reporte de inventario mensual/trimestral
- ✅ Altas y bajas de animales
- ✅ Historial de pesajes con fecha/hora

**REGENSA (Capítulos 3.10 y 7.1)**
- ✅ GMA (Guía de Movimiento Animal) digital
- ✅ Registro de pesajes con GPS y timestamp UTC
- ✅ Certificación de movilización

**ASOCEBU (Competencias Ganaderas)**
- ✅ Historial de crecimiento (6 meses mínimo)
- ✅ GDP (Ganancia Diaria Promedio)
- ✅ Certificación de peso con proyecciones

---

## 🏗️ Estructura de Implementación

### Vistas (`src/views/`)

#### `CattleDetailView.js` - Vista Principal de Trazabilidad
- Tabs/Sections:
  1. **Información General**: Datos básicos, foto, estado
  2. **Trazabilidad**: Timeline completo, linaje
  3. **Historial de Pesos**: Gráfico + tabla de estimaciones
  4. **Eventos**: Timeline de todos los eventos
  5. **Documentos**: Reportes generados

#### `CattleView.js` - Lista con Búsqueda Avanzada
- Tabla de animales con filtros
- Búsqueda en tiempo real
- Acciones: Ver detalle, Editar, Exportar reporte

### Organisms (`src/components/organisms/`)

#### `CattleTraceabilityTimeline/`
- Componente de timeline visual
- Muestra todos los eventos del animal
- Filtros por tipo de evento

#### `CattleLineageTree/`
- Árbol genealógico visual
- Navegación a padres/hijos
- Información de linaje

#### `CattleWeightHistoryChart/`
- Gráfico de evolución de peso
- Línea de tiempo con todas las estimaciones
- Proyecciones de crecimiento

#### `CattleReportGenerator/`
- Generador de reportes PDF/CSV/Excel
- Selección de datos a incluir
- Formatos normativos (SENASAG, REGENSA, ASOCEBU)

### Servicios (`src/services/`)

#### `reports/`
- `generateCattleTraceabilityReport.js` - Reporte individual PDF
- `generateInventoryReport.js` - Reporte de inventario
- `generateMovementReport.js` - Reporte de movimientos
- `generateGrowthReport.js` - Reporte de crecimiento

#### `traceability/`
- `getCattleLineage.js` - Obtener linaje (padres, hijos)
- `getCattleEvents.js` - Obtener historial de eventos
- `getCattleTimeline.js` - Obtener timeline completo

---

## 📊 Datos Disponibles para Trazabilidad

### Del Backend (Animal)
```javascript
{
  id: "uuid",
  ear_tag: "string",           // Caravana única
  name: "string | null",
  breed: "string",            // 7 razas exactas
  birth_date: "ISO date",
  gender: "male | female",
  color: "string | null",
  birth_weight_kg: "number | null",
  mother_id: "uuid | null",   // ⭐ Para linaje
  father_id: "uuid | null",   // ⭐ Para linaje
  status: "active | inactive | sold | deceased", // ⭐ Para eventos
  farm_id: "uuid",
  registration_date: "ISO date",
  last_updated: "ISO date",
  photo_url: "string | null",
  observations: "string | null"
}
```

### Del Backend (Weight Estimation)
```javascript
{
  id: "uuid",
  cattle_id: "uuid | null",
  estimated_weight: "number",
  confidence_score: "number",
  timestamp: "ISO date",       // ⭐ Para timeline
  gps_latitude: "number | null", // ⭐ Para ubicación
  gps_longitude: "number | null",
  frame_image_path: "string",
  method: "tflite",
  model_version: "string",
  processing_time_ms: "number"
}
```

---

## 🎨 Componentes de UI para Trazabilidad

### 1. **Timeline Component**
```
┌─────────────────────────────────────┐
│ 📅 2024-01-15 - Registro            │
│    Animal registrado en el sistema   │
├─────────────────────────────────────┤
│ 👶 2024-01-10 - Nacimiento          │
│    Peso: 35 kg, Raza: Nelore         │
├─────────────────────────────────────┤
│ ⚖️ 2024-03-15 - Estimación de Peso  │
│    Peso: 120 kg, Confianza: 92%      │
│    📍 GPS: -15.859, -60.797          │
├─────────────────────────────────────┤
│ ⚖️ 2024-06-20 - Estimación de Peso  │
│    Peso: 280 kg, Confianza: 95%      │
└─────────────────────────────────────┘
```

### 2. **Linaje Component**
```
        [Padre: Nelore]
              │
        ┌─────┴─────┐
        │           │
   [Animal Actual] │
   Nelore          │
        │          │
        └─────┬─────┘
              │
        [Madre: Brahman]
```

### 3. **Gráfico de Evolución de Peso**
```
Peso (kg)
  400 │                    ╱───
      │              ╱───╱
  300 │        ╱───╱
      │  ╱───╱
  200 │╱
      │
  100 │
      └─────────────────────────────── Tiempo
      Nac.  3m   6m   9m   12m
```

---

## 📝 Endpoints Adicionales Necesarios

### Para Trazabilidad Completa

#### Linaje
- `GET /api/v1/animals/:id/lineage` - Obtener linaje (padres, hijos)
- `GET /api/v1/animals/:id/descendants` - Obtener descendencia

#### Eventos/Timeline
- `GET /api/v1/animals/:id/timeline` - Timeline completo de eventos
- `GET /api/v1/animals/:id/events` - Historial de eventos

#### Reportes
- `POST /api/v1/reports/traceability/:cattle_id` - Generar reporte individual
- `POST /api/v1/reports/inventory` - Generar reporte de inventario
- `POST /api/v1/reports/movements` - Generar reporte de movimientos
- `POST /api/v1/reports/growth` - Generar reporte de crecimiento

---

## ✅ Checklist de Implementación

### Fase 1: Vista de Detalle con Trazabilidad
- [ ] Crear `CattleDetailView.js` con tabs
- [ ] Implementar timeline de eventos
- [ ] Mostrar linaje (padre/madre)
- [ ] Gráfico de evolución de peso
- [ ] Galería de fotos

### Fase 2: Búsqueda y Filtros
- [ ] Búsqueda avanzada en `CattleView.js`
- [ ] Filtros múltiples
- [ ] Ordenamiento
- [ ] Paginación

### Fase 3: Reportes
- [ ] Generador de reportes PDF
- [ ] Exportación CSV/Excel
- [ ] Formatos normativos (SENASAG, REGENSA, ASOCEBU)
- [ ] Templates de reportes

### Fase 4: Visualizaciones Avanzadas
- [ ] Árbol genealógico interactivo
- [ ] Gráficos de crecimiento
- [ ] Mapas de ubicación GPS
- [ ] Comparativas entre animales

---

## 🎯 Prioridades

### Alta Prioridad (MVP)
1. ✅ Vista de detalle con información completa
2. ✅ Timeline de eventos básico
3. ✅ Gráfico de evolución de peso
4. ✅ Búsqueda por caravana/nombre
5. ✅ Exportación PDF básica

### Media Prioridad
1. Linaje (padre/madre)
2. Filtros avanzados
3. Reportes normativos completos
4. Galería de fotos

### Baja Prioridad (Futuro)
1. Árbol genealógico completo
2. Comparativas entre animales
3. Proyecciones de crecimiento
4. Integración con Gran Paitití

