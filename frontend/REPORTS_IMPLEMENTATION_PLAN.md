# 📄 Plan de Implementación de Reportes - Trazabilidad

## 🎯 Objetivo
Implementar generador de reportes PDF, CSV y Excel para cumplir con normativas bolivianas (SENASAG, REGENSA, ASOCEBU).

---

## 📋 Funcionalidades a Implementar

### 1. **Reporte Individual de Trazabilidad** (Alta Prioridad)
- Certificado de trazabilidad de un animal
- Incluye: Datos completos, linaje, historial de pesos, eventos, fotos
- Formato: PDF profesional con logo
- Cumple normativas SENASAG

### 2. **Reporte de Inventario** (Alta Prioridad)
- Lista completa de animales
- Filtrado por criterios
- Exportación: PDF, CSV, Excel
- Cumple normativas SENASAG (inventario mensual/trimestral)

### 3. **Reporte de Movimientos** (Media Prioridad)
- Animales vendidos (con fechas)
- Animales fallecidos (con fechas)
- Formato: PDF, CSV
- Para REGENSA (GMA - Guía de Movimiento Animal)

### 4. **Reporte de Crecimiento** (Media Prioridad)
- Evolución de peso por animal
- GDP (Ganancia Diaria Promedio)
- Gráficos de crecimiento
- Para ASOCEBU (competencias ganaderas)

---

## 🏗️ Estructura de Implementación

### Servicios (`src/services/reports/`)

#### `generateCattleTraceabilityReport.js`
- Genera reporte PDF individual de un animal
- Usa biblioteca de generación PDF (jsPDF o react-pdf)

#### `generateInventoryReport.js`
- Genera reporte de inventario
- Soporta PDF, CSV, Excel

#### `generateMovementReport.js`
- Genera reporte de movimientos
- Soporta PDF, CSV

#### `generateGrowthReport.js`
- Genera reporte de crecimiento
- Incluye gráficos

### Organisms (`src/components/organisms/`)

#### `CattleReportGenerator/`
- Componente para seleccionar tipo de reporte
- Opciones de formato (PDF, CSV, Excel)
- Botón de descarga

### Vistas

#### Agregar botón de reporte en:
- `CattleDetailView` - Reporte individual
- `CattleView` - Reporte de inventario

---

## 📦 Dependencias Necesarias

### Para PDF:
- `jspdf` - Generación de PDFs
- `jspdf-autotable` - Tablas en PDF
- `html2canvas` (opcional) - Para capturar gráficos

### Para Excel:
- `xlsx` - Generación de archivos Excel

### Para CSV:
- No requiere dependencias adicionales (nativo)

---

## 🎨 UI Components

### Botón de Reporte en CattleDetailView
```jsx
<ActionButton
    icon={<PictureAsPdfIcon />}
    label="Generar Reporte PDF"
    onClick={handleGenerateReport}
/>
```

### Dialog de Opciones de Reporte
```jsx
<Dialog>
  <DialogTitle>Generar Reporte</DialogTitle>
  <DialogContent>
    <RadioGroup>
      <FormControlLabel value="traceability" control={<Radio />} label="Trazabilidad Individual" />
      <FormControlLabel value="inventory" control={<Radio />} label="Inventario" />
      <FormControlLabel value="growth" control={<Radio />} label="Crecimiento" />
    </RadioGroup>
    <FormControl>
      <InputLabel>Formato</InputLabel>
      <Select>
        <MenuItem value="pdf">PDF</MenuItem>
        <MenuItem value="csv">CSV</MenuItem>
        <MenuItem value="excel">Excel</MenuItem>
      </Select>
    </FormControl>
  </DialogContent>
</Dialog>
```

---

## ✅ Checklist de Implementación

### Fase 1: Reporte Individual PDF (MVP)
- [ ] Instalar dependencias (jspdf, jspdf-autotable)
- [ ] Crear servicio `generateCattleTraceabilityReport.js`
- [ ] Crear template de PDF con logo y datos básicos
- [ ] Agregar botón en `CattleDetailView`
- [ ] Probar generación y descarga

### Fase 2: Reporte de Inventario
- [ ] Crear servicio `generateInventoryReport.js`
- [ ] Soporte PDF, CSV, Excel
- [ ] Agregar botón en `CattleView`
- [ ] Aplicar filtros al reporte

### Fase 3: Reportes Avanzados
- [ ] Reporte de movimientos
- [ ] Reporte de crecimiento
- [ ] Templates normativos (SENASAG, REGENSA, ASOCEBU)

---

## 🎯 Prioridades

### Alta Prioridad (Implementar Primero)
1. ✅ Reporte Individual PDF - Trazabilidad completa de un animal
2. ✅ Reporte de Inventario PDF/CSV - Lista de todos los animales

### Media Prioridad
3. Reporte de Movimientos
4. Reporte de Crecimiento
5. Templates normativos específicos

---

## 📝 Notas de Implementación

### Estructura del PDF Individual
1. **Encabezado**: Logo, título "Certificado de Trazabilidad"
2. **Datos del Animal**: Caravana, nombre, raza, género, edad
3. **Linaje**: Padre y madre
4. **Historial de Pesos**: Tabla con fechas y pesos
5. **Timeline de Eventos**: Lista cronológica
6. **Fotos**: Miniaturas de fotos del animal
7. **Pie de Página**: Fecha de generación, cumplimiento normativo

### Cumplimiento Normativo
- **SENASAG**: Incluir todos los datos requeridos
- **REGENSA**: Formato GMA para movimientos
- **ASOCEBU**: Métricas de crecimiento y GDP

