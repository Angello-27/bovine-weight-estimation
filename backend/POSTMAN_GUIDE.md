# 📬 Guía de Pruebas con Postman - Backend ML

Guía completa para probar los endpoints de Machine Learning usando Postman.

---

## 🎯 Endpoints de ML con Modelo TFLite

### 1. **POST `/api/v1/ml/predict`** - Predicción (Móvil - Sin guardar)

**Descripción**: Usa el modelo TFLite para predecir peso. **NO guarda** la estimación en la base de datos.

**Uso**: Para pruebas rápidas o aplicación móvil.

### 2. **POST `/api/v1/ml/estimate`** - Estimación (Web - Guarda en BD)

**Descripción**: Usa el modelo TFLite para estimar peso y **GUARDA** automáticamente en la base de datos.

**Uso**: Para panel web donde se necesita historial.

---

## 📋 Configuración en Postman

### Variables de Entorno (Opcional pero recomendado)

Crea variables en Postman:
- `base_url`: `http://localhost:8000`
- `token`: (se llenará después del login)

---

## 🧪 Prueba 1: Verificar Estado del Modelo

### Request

**Método**: `GET`  
**URL**: `http://localhost:8000/api/v1/ml/models/status`

### Response Esperada

```json
{
  "status": "ok",
  "total_loaded": 1,
  "breeds_loaded": ["generic"],
  "all_breeds": ["nelore", "brahman", "guzerat", "senepol", "girolando", "gyr_lechero", "sindi"],
  "strategies": {
    "total_strategies": 2,
    "available_strategies": ["deep_learning_tflite", "morphometric_yolo_detection"]
  },
  "note": "Sistema de estrategias activo: ML entrenado + híbrido YOLO como fallback",
  "method": "strategy_based"
}
```

---

## 🧪 Prueba 2: Predicción de Peso (NO guarda) - `/predict`

### Configuración en Postman

1. **Método**: `POST`
2. **URL**: `http://localhost:8000/api/v1/ml/predict`
3. **Body**: Seleccionar `form-data`

### Parámetros del Body

| Key | Type | Value | Descripción |
|-----|------|-------|-------------|
| `image` | **File** | Seleccionar archivo | Imagen del bovino (JPG/PNG) |
| `breed` | **Text** | `nelore` | Raza: `nelore`, `brahman`, `guzerat`, `senepol`, `girolando`, `gyr_lechero`, `sindi` |
| `animal_id` | **Text** | (opcional) | UUID del animal (si existe) |
| `device_id` | **Text** | `postman-test-001` | ID del dispositivo |

### Ejemplo de Body

```
image: [Seleccionar archivo: test_cow.jpg]
breed: nelore
device_id: postman-test-001
```

### Response Esperada

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "animal_id": null,
  "breed": "nelore",
  "estimated_weight_kg": 485.75,
  "confidence": 0.92,
  "confidence_level": "high",
  "processing_time_ms": 2100,
  "ml_model_version": "1.0.0",
  "method": "strategy_based",
  "meets_quality_criteria": true,
  "timestamp": "2024-11-30T10:30:00.123456"
}
```

---

## 🧪 Prueba 3: Estimación de Peso (SÍ guarda) - `/estimate`

### Configuración en Postman

1. **Método**: `POST`
2. **URL**: `http://localhost:8000/api/v1/ml/estimate`
3. **Headers**: 
   - `Authorization: Bearer YOUR_TOKEN` (si requieres autenticación)
4. **Body**: Seleccionar `form-data`

### Parámetros del Body

| Key | Type | Value | Descripción |
|-----|------|-------|-------------|
| `image` | **File** | Seleccionar archivo | Imagen del bovino (JPG/PNG/WEBP) |
| `breed` | **Text** | `nelore` | Raza del animal |
| `animal_id` | **Text** | (opcional) | UUID del animal |

### Ejemplo de Body

```
image: [Seleccionar archivo: test_cow.jpg]
breed: brahman
animal_id: 550e8400-e29b-41d4-a716-446655440000
```

### Response Esperada

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "breed": "brahman",
  "estimated_weight": 487.50,
  "estimated_weight_kg": 487.50,
  "confidence_score": 0.93,
  "confidence": 0.93,
  "breed_confidence": 0.93,
  "ml_model_version": "1.0.0",
  "processing_time_ms": 2150,
  "image_path": "web_uploads/550e8400-e29b-41d4-a716-446655440000_test_cow.jpg",
  "method": "strategy_based",
  "meets_quality_criteria": true,
  "timestamp": "2024-11-30T10:30:00.123456"
}
```

---

## 🧪 Prueba 4: Health Check ML

### Request

**Método**: `GET`  
**URL**: `http://localhost:8000/api/v1/ml/health`

### Response Esperada

```json
{
  "status": "healthy",
  "service": "ml_inference",
  "method": "strategy_based",
  "description": "Sistema de estrategias: ML entrenado + híbrido YOLO como fallback",
  "note": "Sistema funcional con múltiples estrategias de estimación"
}
```

---

## 📸 Preparar Imagen de Prueba

### Requisitos de la Imagen

- **Formatos**: JPEG, PNG, WEBP
- **Tamaño máximo**: 10 MB
- **Tamaño recomendado**: > 224x224 píxeles
- **Contenido**: Imagen de un bovino (perfil lateral ideal)

### Imagen de Ejemplo

Si no tienes una imagen, puedes usar la que ya tienes en:
- `backend/test_cow.jpg` (si existe)

O descargar una imagen de prueba de bovino desde internet.

---

## 🔄 Flujo Completo de Pruebas

### Paso 1: Verificar Modelo Cargado
```
GET http://localhost:8000/api/v1/ml/models/status
```

### Paso 2: Probar Predicción (Sin guardar)
```
POST http://localhost:8000/api/v1/ml/predict
Body (form-data):
  - image: test_cow.jpg
  - breed: nelore
  - device_id: postman-test-001
```

### Paso 3: Verificar Resultado

Verifica que la respuesta incluya:
- ✅ `estimated_weight_kg`: Peso en kilogramos
- ✅ `confidence`: Entre 0.0 y 1.0 (≥0.80 es bueno)
- ✅ `confidence_level`: "high", "medium" o "low"
- ✅ `processing_time_ms`: < 3000ms (3 segundos)
- ✅ `meets_quality_criteria`: true
- ✅ `ml_model_version`: "1.0.0"

### Paso 4: Probar Estimación (Con guardado)

Si necesitas que se guarde en BD:
```
POST http://localhost:8000/api/v1/ml/estimate
Headers:
  Authorization: Bearer YOUR_TOKEN
Body (form-data):
  - image: test_cow.jpg
  - breed: brahman
  - animal_id: UUID_ANIMAL (opcional)
```

---

## 🎨 Screenshot de Configuración Postman

### Configuración de `/predict`

```
Method: POST
URL: http://localhost:8000/api/v1/ml/predict

Body:
┌─────────────┬──────┬──────────────────┐
│ Key         │ Type │ Value            │
├─────────────┼──────┼──────────────────┤
│ image       │ File │ [Seleccionar...] │
│ breed       │ Text │ nelore           │
│ device_id   │ Text │ postman-test-001 │
└─────────────┴──────┴──────────────────┘
```

---

## 🔍 Valores de Raza Válidos

Usa exactamente uno de estos valores para el campo `breed`:

- `nelore`
- `brahman`
- `guzerat`
- `senepol`
- `girolando`
- `gyr_lechero`
- `sindi`

---

## ⚠️ Troubleshooting

### Error: "Formato de imagen no soportado"

**Solución**: Asegúrate de que el archivo sea JPG, PNG o WEBP.

### Error: "Imagen vacía o inválida"

**Solución**: Verifica que el archivo no esté corrupto y tenga un tamaño razonable.

### Error: "Modelo TFLite no encontrado"

**Solución**: 
```bash
# Verificar que el modelo existe
ls -lh ml_models/generic-cattle-v1.0.0.tflite

# Si no existe, descargarlo
python scripts/download_model_from_drive.py
```

### Response con confidence bajo (<0.80)

**Posibles causas**:
- Imagen de baja calidad
- Bovino no está completo en la imagen
- Iluminación deficiente
- Ángulo de la cámara inadecuado

**Solución**: Usa una imagen de mejor calidad con el bovino de perfil lateral.

### El modelo no se carga (models_loaded: 0)

**Importante**: El modelo se carga bajo demanda (lazy loading). Aparecerá como `total_loaded: 0` hasta que hagas la primera predicción.

**En macOS**: El sistema usa TensorFlow completo como fallback automáticamente si `tensorflow-lite-runtime` no está disponible. Esto es normal y funciona correctamente.

**Para verificar que TensorFlow está instalado**:
```bash
pip install tensorflow
python3 -c "import tensorflow as tf; print(tf.__version__)"
```

**Después de la primera predicción exitosa**, el endpoint `/api/v1/ml/models/status` mostrará:
- `total_loaded: 1` (modelo genérico)
- `breeds_loaded`: todas las 7 razas disponibles

---

## ✅ Checklist de Pruebas

- [ ] Health check responde correctamente
- [ ] Modelo cargado (verificar `/api/v1/ml/models/status`)
- [ ] `/predict` retorna peso estimado con confidence ≥0.80
- [ ] `processing_time_ms` < 3000ms
- [ ] `meets_quality_criteria` es true
- [ ] `/estimate` guarda correctamente en BD (si usas autenticación)
- [ ] Respuestas incluyen todos los campos esperados
- [ ] Manejo de errores funciona (imagen inválida, raza incorrecta, etc.)

---

## 📊 Métricas de Calidad Esperadas

Según los requisitos del proyecto:

| Métrica | Objetivo | Verificar en Response |
|---------|----------|----------------------|
| **Precisión** | R² ≥ 0.95 | N/A (requiere validación con datos reales) |
| **Error** | < 5 kg | Comparar con peso real (si disponible) |
| **Tiempo** | < 3 segundos | `processing_time_ms` < 3000 |
| **Confidence** | ≥ 80% | `confidence` ≥ 0.80 |
| **Criterios** | Cumplidos | `meets_quality_criteria` = true |

---

**Última actualización**: 2024-11-30

