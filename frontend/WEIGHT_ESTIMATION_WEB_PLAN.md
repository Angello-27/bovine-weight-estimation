# ⚖️ Plan de Implementación - Estimación de Peso desde Web

## 📋 Resumen
Implementar funcionalidad para hacer estimaciones de peso desde el panel web subiendo imágenes.

---

## 🎯 Funcionalidad

### Flujo de Usuario
1. Usuario accede a "Estimar Peso" desde el panel web
2. Usuario selecciona un animal (opcional) o deja en blanco
3. Usuario sube una imagen del animal
4. Sistema procesa imagen en backend con modelo ML
5. Sistema muestra resultado: peso estimado, confianza, raza detectada
6. Usuario puede guardar la estimación asociada al animal

---

## 🔧 Implementación Backend

### Endpoint Requerido
```
POST /api/v1/ml/estimate
```

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `image`: File (imagen del animal)
  - `cattle_id`: UUID (opcional) - ID del animal
  - `breed`: string (opcional) - Raza si se conoce

**Response:**
```json
{
  "estimated_weight": 350.5,
  "confidence_score": 0.92,
  "breed": "nelore",
  "breed_confidence": 0.88,
  "model_version": "1.0.0",
  "processing_time_ms": 1200,
  "image_path": "/uploads/estimations/xxx.jpg"
}
```

**Errores:**
- `400`: Imagen inválida o formato no soportado
- `422`: Imagen no contiene animal detectable
- `500`: Error en procesamiento ML

---

## 🎨 Implementación Frontend

### Servicio API
**Archivo:** `src/services/weight-estimations/estimateWeightFromImage.js`

```javascript
import apiClient from '../../api/axiosClient';

const estimateWeightFromImage = async (imageFile, cattleId = null, breed = null) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  if (cattleId) formData.append('cattle_id', cattleId);
  if (breed) formData.append('breed', breed);

  const response = await apiClient.post('/ml/estimate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export default estimateWeightFromImage;
```

### Vista
**Archivo:** `src/views/WeightEstimationFromWebView.js`

**Características:**
- Formulario de upload de imagen
- Selector de animal (opcional)
- Selector de raza (opcional, ayuda al modelo)
- Preview de imagen antes de enviar
- Mostrar resultado de estimación
- Botón para guardar estimación

### Template
**Archivo:** `src/templates/WeightEstimationTemplate.js`

**Secciones:**
1. **Formulario de Upload**
   - Drag & drop o botón de selección
   - Preview de imagen
   - Selector de animal (opcional)
   - Selector de raza (opcional)

2. **Resultado de Estimación**
   - Peso estimado (destacado)
   - Nivel de confianza (barra de progreso)
   - Raza detectada
   - Tiempo de procesamiento
   - Imagen procesada (si el backend la retorna)

3. **Acciones**
   - Guardar estimación
   - Estimar otra vez
   - Ver historial del animal (si se seleccionó)

### Organism
**Archivo:** `src/components/organisms/CreateWeightEstimation/`

**Componentes:**
- `ImageUploader.js` - Componente de upload con drag & drop
- `CattleSelector.js` - Selector de animal (opcional)
- `BreedSelector.js` - Selector de raza (opcional)
- `EstimationResult.js` - Muestra resultado de estimación
- `EstimationForm.js` - Formulario completo

### Container
**Archivo:** `src/containers/weight-estimations/EstimateWeightFromImage.js`

**Lógica:**
- Manejo de estado del formulario
- Validación de imagen
- Llamada a API de estimación
- Manejo de errores
- Guardado de estimación

---

## 📊 Estructura de Datos

### Request de Estimación
```javascript
{
  image: File,           // Archivo de imagen
  cattle_id: "uuid",     // Opcional
  breed: "nelore"        // Opcional
}
```

### Response de Estimación
```javascript
{
  estimated_weight: 350.5,
  confidence_score: 0.92,
  breed: "nelore",
  breed_confidence: 0.88,
  model_version: "1.0.0",
  processing_time_ms: 1200,
  image_path: "/uploads/estimations/xxx.jpg"
}
```

### Estimación Guardada (POST /api/v1/weighings)
```javascript
{
  cattle_id: "uuid",              // Si se seleccionó animal
  breed: "nelore",
  estimated_weight: 350.5,
  confidence_score: 0.92,
  frame_image_path: "/uploads/...",
  timestamp: "2024-01-15T10:30:00Z",
  method: "web_upload",           // Diferente de "tflite"
  model_version: "1.0.0",
  processing_time_ms: 1200
}
```

---

## 🎨 Componentes UI

### ImageUploader
```
┌─────────────────────────────────────┐
│  📷 Arrastra imagen aquí o          │
│     [Seleccionar archivo]           │
│                                     │
│  [Preview de imagen si hay]        │
│                                     │
│  Formatos: JPG, PNG, WEBP          │
│  Tamaño máximo: 10MB               │
└─────────────────────────────────────┘
```

### EstimationResult
```
┌─────────────────────────────────────┐
│  ⚖️ Peso Estimado                   │
│  350.5 kg                           │
│                                     │
│  Confianza: ████████░░ 92%         │
│                                     │
│  Raza: Nelore (88% confianza)      │
│                                     │
│  Tiempo: 1.2 segundos               │
│                                     │
│  [Guardar Estimación]               │
└─────────────────────────────────────┘
```

---

## ✅ Checklist de Implementación

### Backend (Requisito previo)
- [ ] Endpoint `/api/v1/ml/estimate` implementado
- [ ] Modelo ML cargado en backend (TensorFlow/PyTorch)
- [ ] Procesamiento de imágenes funcionando
- [ ] Validación de formatos de imagen
- [ ] Manejo de errores implementado

### Frontend
- [ ] Servicio `estimateWeightFromImage.js` creado
- [ ] Vista `WeightEstimationFromWebView.js` creada
- [ ] Template `WeightEstimationTemplate.js` creado
- [ ] Organism `CreateWeightEstimation/` creado
- [ ] Container `EstimateWeightFromImage.js` creado
- [ ] Componente `ImageUploader` con drag & drop
- [ ] Componente `EstimationResult` para mostrar resultados
- [ ] Integración con selector de animales
- [ ] Integración con selector de razas
- [ ] Guardado de estimación después de procesar
- [ ] Manejo de errores y validaciones
- [ ] Testing

---

## 🔗 Integración con Rutas

**Agregar a `src/config/routes.js`:**
```javascript
{
  path: '/weight-estimations/estimate',
  element: <WeightEstimationFromWebView />
}
```

**Agregar a `src/config/constants.js` (sidebar):**
```javascript
{
  text: 'Estimar Peso',
  icon: <AddCircleIcon />,
  to: '/weight-estimations/estimate',
  roles: ['Administrador', 'Usuario']
}
```

---

## 📝 Notas Técnicas

### Formatos de Imagen Soportados
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WEBP (.webp)

### Tamaño Máximo
- Recomendado: 10MB
- Backend debe validar tamaño

### Validaciones Frontend
- Tipo de archivo válido
- Tamaño de archivo
- Imagen no vacía

### Validaciones Backend
- Formato de imagen válido
- Imagen contiene animal detectable
- Tamaño de archivo
- Procesamiento ML exitoso

---

## 🎯 Prioridades

### Alta Prioridad (MVP)
1. ✅ Servicio API de estimación
2. ✅ Vista básica de upload
3. ✅ Mostrar resultado de estimación
4. ✅ Guardar estimación

### Media Prioridad
1. Selector de animal (opcional)
2. Selector de raza (opcional)
3. Preview de imagen
4. Mejoras de UI/UX

### Baja Prioridad (Futuro)
1. Historial de estimaciones desde web
2. Comparación con estimaciones móviles
3. Batch upload (múltiples imágenes)
4. Análisis de calidad de imagen

