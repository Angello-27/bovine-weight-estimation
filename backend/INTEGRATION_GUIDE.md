# 🔗 Guía de Integración: Modelo TFLite desde Colab

**Objetivo**: Integrar el modelo TFLite exportado desde Colab al backend FastAPI.

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

### Opción B: Script Automático (Recomendado)

Crea un script para descargar desde Drive:

```bash
# backend/scripts/download_model_from_drive.sh
#!/bin/bash

# Configurar variables
DRIVE_FILE_ID="TU_FILE_ID_AQUI"  # Obtener desde link de Drive
MODEL_NAME="generic-cattle-v1.0.0.tflite"
OUTPUT_DIR="ml_models"

# Crear directorio
mkdir -p "$OUTPUT_DIR"

# Descargar usando gdown (instalar: pip install gdown)
gdown "https://drive.google.com/uc?id=$DRIVE_FILE_ID" -O "$OUTPUT_DIR/$MODEL_NAME"

echo "✅ Modelo descargado: $OUTPUT_DIR/$MODEL_NAME"
```

**Para obtener FILE_ID**:
1. Comparte el archivo en Drive (cualquiera con link)
2. Copia el link: `https://drive.google.com/file/d/FILE_ID_AQUI/view?usp=sharing`
3. Extrae el `FILE_ID_AQUI`

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

Reemplazar la carga mock con carga real de TFLite:

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

Usar el modelo TFLite real para inferencia:

```python
# backend/app/ml/strategies/deep_learning_strategy.py

import numpy as np
from typing import Dict, Any
from PIL import Image
import io

from app.core.constants import BreedType
from app.ml.model_loader import MLModelLoader
from app.ml.preprocessing import ImagePreprocessor
from .base_strategy import BaseWeightEstimationStrategy


class DeepLearningWeightEstimationStrategy(BaseWeightEstimationStrategy):
    """Estrategia de Deep Learning usando modelo TFLite."""
    
    def __init__(self):
        """Inicializa la estrategia."""
        self.model_loader = MLModelLoader()
        self.preprocessor = ImagePreprocessor()
        self._model = None
    
    def _ensure_model_loaded(self):
        """Asegura que el modelo esté cargado."""
        if self._model is None:
            self._model = self.model_loader.load_generic_model()
    
    def estimate_weight(self, image_bytes: bytes, breed: BreedType) -> dict:
        """
        Estima peso usando modelo TFLite.
        
        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)
            breed: Raza del animal (usado para validación, modelo es genérico)
            
        Returns:
            Dict con peso estimado, confianza, método y metadatos
        """
        try:
            # 1. Cargar modelo si no está cargado
            self._ensure_model_loaded()
            
            # 2. Preprocesar imagen
            preprocessed_image = self.preprocessor.preprocess_image(
                image_bytes=image_bytes,
                target_size=(224, 224)  # Tamaño esperado por el modelo
            )
            
            # 3. Ejecutar inferencia TFLite
            interpreter = self._model["interpreter"]
            input_details = self._model["input_details"]
            output_details = self._model["output_details"]
            
            # Preparar input (normalizar a float32)
            input_data = np.expand_dims(preprocessed_image, axis=0).astype(np.float32)
            
            # Ejecutar inferencia
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            
            # Obtener output
            output_data = interpreter.get_tensor(output_details[0]['index'])
            estimated_weight = float(output_data[0][0])  # Modelo retorna peso directamente
            
            # 4. Calcular confidence (simulado por ahora, puede mejorarse)
            # En producción, el modelo podría retornar confidence también
            confidence = self._calculate_confidence(estimated_weight, breed)
            
            return {
                'weight': round(estimated_weight, 2),
                'confidence': confidence,
                'method': 'tflite_model',
                'model_version': self._model["version"],
                'strategy': self.get_strategy_name(),
                'detection_quality': 'good' if confidence > 0.85 else 'acceptable',
            }
            
        except Exception as e:
            raise ValueError(f"Error en inferencia TFLite: {str(e)}")
    
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

Asegurar que el preprocesamiento sea compatible con TFLite:

```python
# backend/app/ml/preprocessing.py

import numpy as np
from PIL import Image
import io

from ..core.config import settings


class ImagePreprocessor:
    """Preprocesador de imágenes para modelos ML."""
    
    def preprocess_image(
        self,
        image_bytes: bytes,
        target_size: tuple[int, int] = (224, 224)
    ) -> np.ndarray:
        """
        Preprocesa imagen para modelo TFLite.
        
        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)
            target_size: Tamaño objetivo (height, width)
            
        Returns:
            np.ndarray normalizado (0-1) shape (H, W, 3)
        """
        # 1. Cargar imagen
        image = Image.open(io.BytesIO(image_bytes))
        
        # 2. Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 3. Resize
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        
        # 4. Convertir a numpy array
        image_array = np.array(image, dtype=np.float32)
        
        # 5. Normalizar a [0, 1] (TFLite espera valores 0-1 o 0-255 según modelo)
        # El modelo de Colab usa normalización 0-1
        image_array = image_array / 255.0
        
        return image_array
```

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

### 5.2 Probar Inferencia

```bash
# Probar endpoint de predicción
curl -X POST "http://localhost:8000/api/v1/ml/predict" \
  -F "image=@test_image.jpg" \
  -F "breed=nelore" \
  -F "device_id=test-device"
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
- Verifica que el preprocesamiento genere (224, 224, 3)
- Verifica normalización (0-1 vs 0-255)

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

- [ ] Modelo TFLite descargado desde Colab/Drive
- [ ] Modelo copiado a `backend/ml_models/`
- [ ] `tensorflow-lite-runtime` instalado
- [ ] `model_loader.py` actualizado para cargar TFLite real
- [ ] `deep_learning_strategy.py` actualizado para usar TFLite
- [ ] `preprocessing.py` verificado (normalización 0-1)
- [ ] Backend inicia sin errores
- [ ] Endpoint `/api/v1/ml/models/status` muestra modelo cargado
- [ ] Endpoint `/api/v1/ml/predict` funciona correctamente
- [ ] Métricas de calidad cumplidas (confidence ≥80%, tiempo <3s)

---

**Última actualización**: 2024-12-XX  
**Versión del modelo**: 1.0.0 (genérico)

