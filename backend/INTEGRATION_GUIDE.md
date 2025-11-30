# 🔗 Guía de Integración: Modelo TFLite desde Colab

**Objetivo**: Integrar el modelo TFLite exportado desde Colab al backend FastAPI.

> ✅ **Nota**: El código del backend ya está completamente implementado y listo para usar el modelo TFLite. Solo necesitas descargar el modelo desde Google Drive usando el script proporcionado.

---

## 📋 Resumen del Flujo

```
Colab (BLOQUE 16) → Exporta TFLite → Google Drive → Backend → Carga modelo → Inferencia
```

1. **Colab**: Entrena y exporta `generic-cattle-v1.0.0.tflite` (BLOQUE 16)
2. **Google Drive**: Modelo guardado en `/content/drive/MyDrive/bovine-weight-estimation/ml-training/models/`
3. **Backend**: Descarga/copia modelo a `backend/ml_models/`
4. **Inferencia**: Backend carga modelo y ejecuta predicciones

---

## 🚀 Paso 1: Obtener Modelo desde Colab/Drive

### Opción A: Descargar Manualmente

1. **En Colab**, después del BLOQUE 16:
   ```python
   # El modelo está en:
   /content/drive/MyDrive/bovine-weight-estimation/ml-training/models/generic-cattle-v1.0.0.tflite
   ```

2. **Descargar desde Google Drive**:
   - Abre Google Drive en navegador
   - Navega a: `bovine-weight-estimation/ml-training/models/`
   - Descarga `generic-cattle-v1.0.0.tflite`

3. **Copiar al backend**:
   ```bash
   # Desde el directorio del proyecto
   mkdir -p backend/ml_models
   cp ~/Downloads/generic-cattle-v1.0.0.tflite backend/ml_models/
   ```

### Opción B: Script Automático (Recomendado) ✅

El proyecto ya incluye un script Python que usa la configuración del proyecto:

```bash
# 1. Instalar gdown si no está instalado
pip install gdown

# 2. El FILE_ID ya está configurado en .env (ML_MODEL_FILE_ID)
#    Si necesitas cambiarlo, edita backend/.env

# 3. Ejecutar script (desde el directorio backend/)
cd backend
python scripts/download_model_from_drive.py

# El script automáticamente:
# - Usa ML_MODEL_FILE_ID de .env (ya configurado)
# - Usa ML_MODELS_PATH de settings (./ml_models por defecto)
# - Usa ML_DEFAULT_MODEL de settings (generic-cattle-v1.0.0.tflite)
# - Crea el directorio si no existe
# - Valida que el archivo se descargó correctamente
```

**Ejemplo completo**:
```bash
# Desde el directorio backend/
python scripts/download_model_from_drive.py

# Output esperado:
# 📋 Usando configuración del proyecto:
#    ML_MODELS_PATH: ./ml_models
#    ML_DEFAULT_MODEL: generic-cattle-v1.0.0.tflite
#    ML_MODEL_FILE_ID: 1Mi2C7f4YM6eF4bYhoZkzG2RyaykY3KvM (desde .env)
#
# 📥 Descargando modelo desde Google Drive...
#    File ID: 1Mi2C7f4YM6eF4bYhoZkzG2RyaykY3KvM
#    Output: ml_models/generic-cattle-v1.0.0.tflite
# ...
# ✅ Modelo descargado exitosamente
#    Tamaño: 13.36 MB
#    Ubicación: /path/to/backend/ml_models/generic-cattle-v1.0.0.tflite
```

**Nota**: También puedes proporcionar un FILE_ID diferente usando `--file-id`:
```bash
python scripts/download_model_from_drive.py --file-id OTRO_FILE_ID
```

**Para cambiar el FILE_ID** (si es necesario):
1. El FILE_ID ya está configurado en `backend/.env` como `ML_MODEL_FILE_ID`
2. Si necesitas usar un modelo diferente:
   - Abre el archivo en Drive: `generic-cattle-v1.0.0.tflite`
   - Comparte con "cualquiera con el enlace"
   - Copia el link: `https://drive.google.com/file/d/FILE_ID_AQUI/view?usp=sharing`
   - Extrae el `FILE_ID_AQUI` (es la parte entre `/d/` y `/view`)
   - Actualiza `ML_MODEL_FILE_ID` en `backend/.env`

---

## 🔧 Paso 2: Actualizar Dependencias

El backend necesita `tensorflow-lite-runtime` (más ligero que TensorFlow completo):

```bash
cd backend
pip install tensorflow-lite-runtime
```

O actualiza `requirements.txt`:

```txt
# ===== Machine Learning (TFLite) =====
tensorflow-lite-runtime==2.16.0  # Runtime ligero para TFLite (sin TensorFlow completo)
pillow==10.1.0                   # Procesamiento de imágenes
numpy==1.26.2                     # Operaciones numéricas
```

**Nota**: `tensorflow-lite-runtime` es ~10MB vs TensorFlow completo ~500MB.

---

## 📁 Paso 3: Estructura de Directorios

```
backend/
├── ml_models/                    # ← Modelos TFLite aquí
│   └── generic-cattle-v1.0.0.tflite
├── app/
│   ├── ml/
│   │   ├── model_loader.py       # ← Actualizar para cargar TFLite real
│   │   ├── inference.py
│   │   └── strategies/
│   │       └── deep_learning_strategy.py  # ← Actualizar para usar TFLite
│   └── core/
│       └── config.py             # ← Ya tiene ML_MODELS_PATH configurado
```

---

## 💻 Paso 4: Actualizar Código del Backend

### 4.1 Actualizar `model_loader.py`

✅ **Ya implementado**: El código ya carga modelos TFLite reales.

El archivo `backend/app/ml/model_loader.py` ya está completamente implementado con:
- Carga de modelos TFLite usando `tensorflow-lite-runtime`
- Singleton pattern para mantener modelos en memoria
- Cache de modelos cargados
- Manejo de errores adecuado
- Logging informativo

El código actual es funcional y sigue las mejores prácticas. Solo requiere que el modelo TFLite esté descargado en `ml_models/`.

**Ejemplo del código actual** (para referencia):

```python
# backend/app/ml/model_loader.py

import numpy as np
from pathlib import Path
from typing import Optional

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    # Fallback para desarrollo (si no está instalado)
    tflite = None

from ..core.config import settings
from ..core.constants import BreedType
from ..core.errors import MLModelException


class MLModelLoader:
    """Loader de modelos TFLite."""
    
    _instance: Optional["MLModelLoader"] = None
    _models_cache: dict[str, any] = {}  # Cache de modelos
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa loader."""
        self.models_path = Path(settings.ML_MODELS_PATH)
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.model_loaded = False
    
    def load_generic_model(self) -> any:
        """
        Carga modelo genérico TFLite (para todas las razas).
        
        Returns:
            TFLite Interpreter cargado
            
        Raises:
            MLModelException: Si no se puede cargar
        """
        model_name = settings.ML_DEFAULT_MODEL
        model_path = self.models_path / model_name
        
        # Verificar cache
        if "generic" in self._models_cache:
            return self._models_cache["generic"]
        
        # Verificar que existe
        if not model_path.exists():
            raise MLModelException(
                f"Modelo TFLite no encontrado: {model_path}. "
                f"Descarga el modelo desde Colab/Drive a: {self.models_path}/"
            )
        
        try:
            if tflite is None:
                raise MLModelException(
                    "tensorflow-lite-runtime no instalado. "
                    "Ejecuta: pip install tensorflow-lite-runtime"
                )
            
            # Cargar TFLite Interpreter
            interpreter = tflite.Interpreter(model_path=str(model_path))
            interpreter.allocate_tensors()
            
            # Obtener input/output details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            print(f"✅ Modelo TFLite cargado: {model_name}")
            print(f"   Input shape: {input_details[0]['shape']}")
            print(f"   Output shape: {output_details[0]['shape']}")
            
            # Cachear
            self._models_cache["generic"] = {
                "interpreter": interpreter,
                "input_details": input_details,
                "output_details": output_details,
                "version": "1.0.0",
                "path": str(model_path),
            }
            
            self.model_loaded = True
            return self._models_cache["generic"]
            
        except Exception as e:
            raise MLModelException(f"Error al cargar modelo TFLite: {str(e)}")
    
    def is_model_loaded(self) -> bool:
        """Verifica si el modelo genérico está cargado."""
        return "generic" in self._models_cache
    
    def unload_model(self) -> None:
        """Descarga modelo de memoria."""
        if "generic" in self._models_cache:
            del self._models_cache["generic"]
            self.model_loaded = False
            print("🗑️ Modelo descargado de memoria")
```

### 4.2 Actualizar `deep_learning_strategy.py`

✅ **Ya implementado**: El código ya usa el modelo TFLite real para inferencia.

El archivo `backend/app/ml/strategies/deep_learning_strategy.py` ya está implementado correctamente:
- Usa `MLModelLoader` para cargar el modelo TFLite
- Usa `ImagePreprocessor.preprocess_from_bytes()` para preprocesar imágenes
- Ejecuta inferencia TFLite correctamente
- Retorna `ml_model_version` (no `model_version`) para evitar conflictos con Pydantic
- Incluye fallback a mock solo si hay error (para desarrollo)
    
    def _calculate_confidence(self, weight: float, breed: BreedType) -> float:
        """
        Calcula confidence basado en peso estimado y rango típico de la raza.
        
        TODO: Mejorar con confidence real del modelo si está disponible.
        """
        # Rangos típicos por raza (alineados con entrenamiento ML)
        breed_ranges = {
            BreedType.NELORE: (250, 650),
            BreedType.BRAHMAN: (260, 680),
            BreedType.GUZERAT: (240, 650),
            BreedType.SENEPOL: (280, 620),
            BreedType.GIROLANDO: (240, 640),
            BreedType.GYR_LECHERO: (220, 620),
            BreedType.SINDI: (150, 380),
        }
        
        weight_min, weight_max = breed_ranges.get(breed, (300, 700))
        
        # Si está en rango típico, confidence alto
        if weight_min <= weight <= weight_max:
            return 0.92
        elif weight < weight_min * 0.8 or weight > weight_max * 1.2:
            return 0.75  # Fuera de rango, confidence menor
        else:
            return 0.85  # Cerca del rango
    
    def get_strategy_name(self) -> str:
        """Retorna nombre de la estrategia."""
        return "deep_learning_tflite"
    
    def is_available(self) -> bool:
        """Verifica si la estrategia está disponible."""
        try:
            self._ensure_model_loaded()
            return True
        except:
            return False
```

### 4.3 Actualizar `preprocessing.py`

✅ **Ya implementado**: El preprocesamiento ya es compatible con TFLite.

El archivo `backend/app/ml/preprocessing.py` ya está completamente implementado con:
- Preprocesamiento a 224x224 (tamaño esperado por el modelo)
- Normalización ImageNet (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- Conversión a RGB automática
- Expansión de dimensión de batch para (1, 224, 224, 3)
- Métodos: `preprocess_from_bytes()` y `preprocess_from_pil()`

El código actual es funcional y sigue las mejores prácticas para modelos TFLite con normalización ImageNet.

---

## ✅ Paso 5: Verificar Integración

### 5.1 Verificar Modelo Cargado

```bash
# Ejecutar backend
cd backend
python -m app.main

# En otra terminal, verificar estado
curl http://localhost:8000/api/v1/ml/models/status
```

**Respuesta esperada**:
```json
{
  "status": "ok",
  "total_models": 1,
  "loaded_models": ["generic"],
  "strategy": "deep_learning_tflite",
  "note": "Sistema de estrategias activo: ML entrenado + híbrido YOLO como fallback",
  "method": "strategy_based"
}
```

### 5.2 Probar Inferencia

```bash
# Probar endpoint de estimación (web upload)
curl -X POST "http://localhost:8000/api/v1/ml/estimate" \
  -F "image=@test_image.jpg" \
  -F "breed=nelore" \
  -H "Authorization: Bearer YOUR_TOKEN"

# O probar endpoint de predicción (mobile)
curl -X POST "http://localhost:8000/api/v1/ml/predict" \
  -F "image=@test_image.jpg" \
  -F "breed=nelore" \
  -F "device_id=test-device"
```

**Respuesta esperada**:
```json
{
  "id": "...",
  "animal_id": null,
  "breed": "nelore",
  "estimated_weight_kg": 485.75,
  "confidence": 0.92,
  "confidence_level": "high",
  "ml_model_version": "1.0.0",
  "method": "strategy_based",
  "processing_time_ms": 2100,
  "meets_quality_criteria": true,
  "timestamp": "2024-..."
}
```

---

## 🔄 Paso 6: Actualizar Modelo (Cuando haya nueva versión)

Cuando entrenes un nuevo modelo en Colab:

1. **Exportar nuevo modelo** (BLOQUE 16)
2. **Descargar desde Drive** (Paso 1)
3. **Reemplazar en backend**:
   ```bash
   cp ~/Downloads/generic-cattle-v2.0.0.tflite backend/ml_models/
   ```
4. **Actualizar configuración** (opcional):
   ```python
   # backend/.env
   ML_DEFAULT_MODEL=generic-cattle-v2.0.0.tflite
   ```
5. **Reiniciar backend** para cargar nuevo modelo

---

## 📊 Paso 7: Monitoreo y Logs

El backend ya tiene logging integrado. Verifica:

- **Logs de carga de modelo**: Al iniciar el servidor
- **Logs de inferencia**: En cada request de predicción
- **Métricas**: `processing_time_ms`, `confidence`, `estimated_weight_kg`

---

## 🐛 Troubleshooting

### Error: "Modelo TFLite no encontrado"
- Verifica que el archivo esté en `backend/ml_models/`
- Verifica permisos de lectura

### Error: "tensorflow-lite-runtime no instalado"
```bash
pip install tensorflow-lite-runtime
```

### Error: "Input shape mismatch"
- El modelo espera: `(None, 224, 224, 3), dtype=tf.float32`
- El preprocessing ya está configurado correctamente:
  - Redimensiona a 224x224 ✓
  - Normaliza con ImageNet stats (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) ✓
  - Expande batch dimension para (1, 224, 224, 3) ✓
  - Convierte a float32 ✓
- Si hay problemas, verifica que el modelo fue entrenado con preprocesamiento ImageNet estándar

### Modelo muy lento
- Verifica que estés usando `tensorflow-lite-runtime` (no TensorFlow completo)
- Considera optimización del modelo (cuantización INT8)

---

## 📝 Notas Importantes

1. **Modelo Genérico**: El notebook exporta un modelo genérico (no por raza). El backend puede usar este modelo para todas las razas.

2. **Futuro**: Si entrenas modelos específicos por raza, actualiza `model_loader.py` para cargar modelos por raza.

3. **Performance**: `tensorflow-lite-runtime` es ~10x más ligero que TensorFlow completo.

4. **Confidence**: Por ahora se calcula basado en rangos. Mejora futura: que el modelo retorne confidence directamente.

---

## ✅ Checklist de Integración

- [x] **Código del backend implementado** ✅ (model_loader.py, deep_learning_strategy.py, preprocessing.py)
- [x] **Script de descarga disponible** ✅ (download_model_from_drive.py)
- [x] **Configuración lista** ✅ (ML_MODELS_PATH, ML_DEFAULT_MODEL en settings)
- [ ] Modelo TFLite exportado desde Colab (BLOQUE 16)
- [ ] Modelo compartido en Google Drive con acceso público
- [ ] FILE_ID extraído del link de Drive
- [ ] Script `download_model_from_drive.py` ejecutado exitosamente
- [ ] Modelo descargado en `backend/ml_models/generic-cattle-v1.0.0.tflite` (~13-14 MB)
- [ ] `tensorflow-lite-runtime` instalado (`pip install tensorflow-lite-runtime`) - Nota: puede no estar disponible en macOS
- [ ] Backend inicia sin errores (verifica logs de carga de modelo)
- [ ] Endpoint `/api/v1/ml/models/status` muestra modelo cargado
- [ ] Endpoint `/api/v1/ml/predict` funciona correctamente (mobile)
- [ ] Endpoint `/api/v1/ml/estimate` funciona para web uploads
- [ ] Métricas de calidad cumplidas (confidence ≥80%, tiempo <3s)

---

**Última actualización**: 2024-12-XX  
**Versión del modelo**: 1.0.0 (genérico)

