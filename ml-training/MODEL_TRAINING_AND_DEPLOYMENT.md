# 🐄 Resumen: Construcción, Entrenamiento y Aplicación del Modelo de Estimación de Peso Bovino

**Proyecto**: Hacienda Gamelera - Bruno Brito Macedo  
**Versión**: 1.0.0  
**Fecha**: Diciembre 2024

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Construcción del Modelo](#construcción-del-modelo)
3. [Entrenamiento del Modelo](#entrenamiento-del-modelo)
4. [Aplicación en el Servidor Backend](#aplicación-en-el-servidor-backend)
5. [Flujo Completo End-to-End](#flujo-completo-end-to-end)
6. [Arquitectura Técnica](#arquitectura-técnica)

---

## 🎯 Resumen Ejecutivo

El sistema de estimación de peso bovino utiliza un **modelo de Deep Learning** entrenado con TensorFlow/Keras y exportado a **TensorFlow Lite (TFLite)** para inferencia en producción. El modelo es **genérico multi-raza** y funciona para las 7 razas tropicales priorizadas.

### Características Principales

- **Modelo**: EfficientNetB1 con transfer learning desde ImageNet
- **Formato**: TensorFlow Lite (`.tflite`) optimizado para producción
- **Cobertura**: 7 razas tropicales (Nelore, Brahman, Guzerat, Senepol, Girolando, Gyr lechero, Sindi)
- **Métricas Objetivo**: R² ≥ 0.95, MAE < 5 kg, tiempo de inferencia < 3 segundos
- **Dataset**: ~19,299+ imágenes (CID Dataset + imágenes propias)

---

## 🏗️ Construcción del Modelo

### 1. Arquitectura del Modelo

El modelo se construye usando **Transfer Learning** con EfficientNetB1 como base:

```python
# Ubicación: ml-training/src/models/cnn_architecture.py

Arquitectura:
├── Input: (224, 224, 3) - Imagen RGB normalizada
├── EfficientNetB1 (pre-entrenado en ImageNet, frozen)
│   └── Feature extraction (capas congeladas)
├── GlobalAveragePooling2D
├── Dense(256, ReLU) + Dropout(0.3)
├── Dense(128, ReLU) + Dropout(0.2)
└── Dense(1, linear) → Peso estimado en kg
```

**Características**:
- **Base**: EfficientNetB1 (pre-entrenado en ImageNet)
- **Capas base**: Congeladas (transfer learning)
- **Head personalizado**: 2 capas densas + dropout para regresión
- **Salida**: Valor continuo (peso en kilogramos)

### 2. Módulos de Construcción

#### `cnn_architecture.py` - Arquitectura del Modelo

```python
from src.models.cnn_architecture import BreedWeightEstimatorCNN

# Modelo genérico multi-raza
model = BreedWeightEstimatorCNN.build_generic_model(
    input_shape=(224, 224, 3),
    base_architecture='efficientnetb1'
)
```

**Funciones principales**:
- `build_generic_model()`: Crea modelo genérico para todas las razas
- `build_model()`: Crea modelo específico por raza (futuro)

#### `data_loader.py` - Carga de Datos

```python
from src.data.data_loader import CattleDataGenerator

# Generador de datos con augmentation
train_generator = CattleDataGenerator(
    annotations_df=df_train,
    images_dir=base_data_dir,
    batch_size=32,
    image_size=(224, 224),
    transform=train_transform,
    shuffle=True
)
```

**Características**:
- Carga imágenes desde DataFrame con metadata
- Aplica augmentation automáticamente
- Soporta múltiples fuentes (CID Dataset + imágenes propias)

#### `augmentation.py` - Data Augmentation

```python
from src.data.augmentation import get_aggressive_augmentation

# Augmentation agresiva para dataset pequeño
transform = get_aggressive_augmentation(image_size=(224, 224))
```

**Transformaciones aplicadas**:
- Rotación, zoom, flip horizontal
- Ajustes de brillo, contraste, saturación
- Normalización para EfficientNetB1

---

## 🚀 Entrenamiento del Modelo

### Proceso de Entrenamiento (Google Colab)

El entrenamiento se realiza usando el notebook `colab_setup_ml.ipynb` en Google Colab Pro con GPU T4.

#### Estructura del Notebook (16 Bloques)

**Día 1: Setup (Bloques 1-5)**
1. **BLOQUE 1**: Clonar repositorio en Google Drive
2. **BLOQUE 2**: Verificar dependencias base (TensorFlow, NumPy)
3. **BLOQUE 3**: Instalar dependencias críticas (TensorFlow 2.19.0, MLflow, DVC)
4. **BLOQUE 4**: Instalar complementos (Albumentations, OpenCV)
5. **BLOQUE 5**: Configurar proyecto y estructura de carpetas

**Día 2-3: Datasets (Bloques 6-9) - Estrategia B**
6. **BLOQUE 6**: Descargar nuestras imágenes (scraping - 200+ por raza)
7. **BLOQUE 7**: Descargar CID Dataset desde S3 (~17,899 imágenes)
8. **BLOQUE 8**: Preparar dataset combinado (CID + nuestras imágenes)
9. **BLOQUE 9**: Resumen de datasets disponibles

**Día 4: Verificación (Bloque 10) - OPCIONAL**
10. **BLOQUE 10**: Verificación rápida de datos (puede saltarse)

**Día 5-6: Pipeline y Modelo (Bloques 11-16)**
11. **BLOQUE 11**: Pipeline de datos con augmentation
12. **BLOQUE 12**: Arquitectura del modelo (EfficientNetB1)
13. **BLOQUE 13**: Configurar entrenamiento (callbacks, MLflow)
14. **BLOQUE 14**: Entrenar modelo (2-4 horas con GPU T4)
15. **BLOQUE 15**: Evaluación del modelo
16. **BLOQUE 16**: Exportar a TFLite

### Estrategia B - Dataset Combinado

El notebook implementa la **Estrategia B** que combina:

1. **CID Dataset**: ~17,899 imágenes
   - Fuente: https://github.com/bhuiyanmobasshir94/CID
   - Descarga automática desde S3
   - Proporciona diversidad y calidad

2. **Nuestras Imágenes**: ~1,400+ imágenes
   - Scraping automático (200+ por raza)
   - Razas bolivianas específicas
   - Proporciona especificidad local

**Total combinado**: ~19,299+ imágenes para entrenamiento

### Configuración de Entrenamiento

```python
CONFIG = {
    'image_size': (224, 224),
    'batch_size': 32,
    'epochs': 200,
    'learning_rate': 0.0005,
    'validation_split': 0.2,
    'test_split': 0.1,
    'early_stopping_patience': 15,
    'target_r2': 0.95,
    'max_mae': 5.0,
    'max_inference_time': 3.0
}
```

### Callbacks Configurados

- **EarlyStopping**: Detiene si no mejora en 15 épocas
- **ReduceLROnPlateau**: Reduce learning rate si no mejora
- **ModelCheckpoint**: Guarda mejor modelo (`best_model.h5`)
- **TensorBoard**: Tracking de métricas
- **MLflow**: Experiment tracking

### Exportación a TFLite

```python
from src.models.export.tflite_converter import TFLiteExporter

# Exportar modelo entrenado a TFLite
TFLiteExporter.convert_to_tflite(
    saved_model_path='models/saved_model',
    output_path='models/generic-cattle-v1.0.0.tflite',
    optimization='default'  # FP16 para reducir tamaño
)
```

**Resultado**: `generic-cattle-v1.0.0.tflite` (~5-10 MB)

---

## 🖥️ Aplicación en el Servidor Backend

### Arquitectura de Inferencia

El backend utiliza un **sistema de estrategias** (Strategy Pattern) para la inferencia ML:

```
┌─────────────────────────────────────────┐
│   API Endpoint (/api/v1/ml/estimate)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   EstimateWeightFromImageUseCase       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   MLInferenceEngine                     │
│   (Orquestador de estrategias)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   DeepLearningWeightEstimationStrategy  │
│   (Estrategia principal - TFLite)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   MLModelLoader                         │
│   (Carga modelo TFLite)                 │
└─────────────────────────────────────────┘
```

### 1. Carga del Modelo TFLite

**Ubicación**: `backend/app/ml/model_loader.py`

```python
from app.ml.model_loader import MLModelLoader

# Singleton pattern - modelo cargado una vez
loader = MLModelLoader()
model_data = loader.load_generic_model()

# Estructura del modelo cargado:
{
    "interpreter": tflite.Interpreter,  # Interpreter TFLite
    "input_details": [...],              # Detalles de entrada
    "output_details": [...],              # Detalles de salida
    "version": "1.0.0",
    "path": "backend/ml_models/generic-cattle-v1.0.0.tflite",
    "loaded": True
}
```

**Características**:
- **Singleton**: Modelo cargado una vez y reutilizado
- **Cache**: Modelo en memoria para inferencias rápidas
- **Fallback**: Usa TensorFlow completo si `tflite_runtime` no está disponible

### 2. Preprocesamiento de Imágenes

**Ubicación**: `backend/app/ml/preprocessing.py`

```python
from app.ml.preprocessing import ImagePreprocessor

preprocessor = ImagePreprocessor()
preprocessed_image = preprocessor.preprocess_from_bytes(image_bytes)

# Proceso:
# 1. Cargar imagen desde bytes (JPEG/PNG)
# 2. Redimensionar a (224, 224)
# 3. Normalizar para EfficientNetB1
# 4. Agregar dimensión batch: (1, 224, 224, 3)
```

### 3. Inferencia TFLite

**Ubicación**: `backend/app/ml/strategies/deep_learning_strategy.py`

```python
class DeepLearningWeightEstimationStrategy:
    def estimate_weight(self, image_bytes: bytes, breed: BreedType):
        # 1. Cargar modelo si no está cargado
        self._ensure_model_loaded()
        
        # 2. Preprocesar imagen
        preprocessed_image = self.preprocessor.preprocess_from_bytes(image_bytes)
        
        # 3. Ejecutar inferencia TFLite
        interpreter = self._model["interpreter"]
        input_details = self._model["input_details"]
        output_details = self._model["output_details"]
        
        # Preparar input
        input_data = preprocessed_image.astype(np.float32)
        
        # Ejecutar inferencia
        interpreter.set_tensor(input_details[0]["index"], input_data)
        interpreter.invoke()
        
        # Obtener output (peso estimado)
        output_data = interpreter.get_tensor(output_details[0]["index"])
        estimated_weight = float(output_data[0][0])
        
        # 4. Calcular confidence
        confidence = self._calculate_confidence(estimated_weight, breed)
        
        return {
            "weight": estimated_weight,
            "confidence": confidence,
            "method": "tflite_model",
            "ml_model_version": "1.0.0"
        }
```

### 4. Endpoints API

**Ubicación**: `backend/app/api/routes/ml.py`

#### `/api/v1/ml/estimate` - Estimar y Guardar

```python
@router.post("/estimate")
async def estimate_weight_from_web(
    image: UploadFile,
    breed: BreedType,
    animal_id: UUID | None = None
):
    # 1. Leer bytes de imagen
    image_bytes = await image.read()
    
    # 2. Guardar imagen en backend/uploads
    saved_image_path = save_estimation_frame(
        image_bytes=image_bytes,
        animal_id=animal_id,
        breed=breed.value
    )
    
    # 3. Ejecutar inferencia + guardar
    estimation = await estimate_usecase.execute(
        image_bytes=image_bytes,
        breed=breed,
        animal_id=animal_id,
        frame_image_path=saved_image_path
    )
    
    return {
        "estimated_weight": estimation.estimated_weight_kg,
        "confidence": estimation.confidence,
        "method": estimation.method,
        "ml_model_version": estimation.ml_model_version
    }
```

#### `/api/v1/ml/predict` - Solo Inferencia (sin guardar)

```python
@router.post("/predict")
async def predict_weight(
    image: UploadFile,
    breed: BreedType
):
    # Solo inferencia, no guarda en BD
    estimation = await estimate_weight_from_image(
        image_bytes=image_bytes,
        breed=breed
    )
    return estimation
```

### 5. Flujo de Datos en Backend

```
1. Cliente envía imagen → POST /api/v1/ml/estimate
2. FastAPI recibe UploadFile → ml.py
3. Se leen bytes de imagen → image_bytes
4. Se guarda imagen → backend/uploads/{breed}/estimation_*.jpg
5. Se ejecuta UseCase → EstimateWeightFromImageUseCase
6. UseCase llama MLInferenceEngine → MLInferenceEngine
7. Engine usa DeepLearningStrategy → DeepLearningWeightEstimationStrategy
8. Strategy carga modelo TFLite → MLModelLoader.load_generic_model()
9. Se preprocesa imagen → ImagePreprocessor
10. Se ejecuta inferencia → interpreter.invoke()
11. Se obtiene peso estimado → output_data[0][0]
12. Se calcula confidence → _calculate_confidence()
13. Se crea entidad WeightEstimation → WeightEstimation
14. Se guarda en MongoDB → WeightEstimationModel
15. Se retorna respuesta → JSON con peso, confidence, método
```

---

## 🔄 Flujo Completo End-to-End

### Fase 1: Construcción y Entrenamiento (ml-training)

```
┌─────────────────────────────────────────────────────────┐
│ 1. PREPARACIÓN DE DATOS                                 │
│    - Descargar CID Dataset (~17,899 imágenes)          │
│    - Scraping de imágenes propias (~1,400 imágenes)    │
│    - Combinar datasets (Estrategia B)                  │
└─────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 2. PREPROCESAMIENTO                                     │
│    - Normalización de metadata                          │
│    - División train/val/test (70/20/10)                │
│    - Data augmentation (Albumentations)                │
└─────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 3. CONSTRUCCIÓN DEL MODELO                             │
│    - EfficientNetB1 (pre-entrenado ImageNet)          │
│    - Head personalizado (Dense layers)                 │
│    - Compilación (Adam, MSE loss)                      │
└─────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 4. ENTRENAMIENTO                                        │
│    - 200 épocas (con early stopping)                   │
│    - GPU T4 (2-4 horas)                                 │
│    - Tracking con MLflow                                │
│    - Checkpoints automáticos                            │
└─────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 5. EVALUACIÓN                                           │
│    - Métricas: R², MAE, MAPE                           │
│    - Validación de objetivos (R² ≥ 0.95, MAE < 5 kg)   │
└─────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 6. EXPORTACIÓN                                          │
│    - Exportar a SavedModel                              │
│    - Convertir a TFLite (optimización FP16)            │
│    - Resultado: generic-cattle-v1.0.0.tflite           │
└─────────────────────────────────────────────────────────┘
```

### Fase 2: Despliegue en Backend

```
┌─────────────────────────────────────────────────────────┐
│ 1. INSTALACIÓN DEL MODELO                               │
│    - Copiar .tflite a backend/ml_models/                │
│    - Verificar que TensorFlow está instalado           │
└─────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 2. CONFIGURACIÓN                                        │
│    - ML_MODELS_PATH en .env                             │
│    - ML_DEFAULT_MODEL en .env                          │
└─────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 3. CARGA AL INICIAR SERVIDOR                            │
│    - MLModelLoader carga modelo en memoria              │
│    - Singleton pattern (una sola carga)                 │
└─────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│ 4. INFERENCIA EN PRODUCCIÓN                             │
│    - Cliente envía imagen → API                         │
│    - Preprocesamiento (224x224, normalización)          │
│    - Inferencia TFLite (< 3 segundos)                   │
│    - Guardado en MongoDB                                │
└─────────────────────────────────────────────────────────┘
```

---

## 🏛️ Arquitectura Técnica

### Stack Tecnológico

**Entrenamiento (ml-training)**:
- TensorFlow 2.19.0
- Keras (tf-keras)
- EfficientNetB1 (pre-entrenado)
- Albumentations 2.0.8 (augmentation)
- MLflow (experiment tracking)
- NumPy 2.x

**Producción (backend)**:
- TensorFlow 2.16.1+ (para cargar TFLite)
- FastAPI (API REST)
- MongoDB (persistencia)
- Pillow (procesamiento de imágenes)
- NumPy (operaciones numéricas)

### Estructura de Archivos

```
ml-training/
├── src/
│   ├── data/
│   │   ├── data_loader.py          # CattleDataGenerator
│   │   └── augmentation.py          # Albumentations transforms
│   ├── models/
│   │   ├── cnn_architecture.py       # EfficientNetB1 architecture
│   │   ├── training/
│   │   │   └── trainer.py           # Training logic
│   │   ├── evaluation/
│   │   │   └── metrics.py           # R², MAE, MAPE
│   │   └── export/
│   │       └── tflite_converter.py  # TFLite export
│   └── utils/
├── notebooks/
│   └── colab_setup_ml.ipynb         # Notebook de entrenamiento
└── requirements.txt

backend/
├── app/
│   ├── ml/
│   │   ├── model_loader.py          # Carga modelos TFLite
│   │   ├── preprocessing.py          # Preprocesamiento imágenes
│   │   └── strategies/
│   │       └── deep_learning_strategy.py  # Inferencia TFLite
│   ├── api/
│   │   └── routes/
│   │       └── ml.py                 # Endpoints /api/v1/ml/*
│   └── domain/
│       └── usecases/
│           └── weight_estimations/
│               └── create_weight_estimation_usecase.py
└── ml_models/
    └── generic-cattle-v1.0.0.tflite  # Modelo entrenado
```

### Modelo en Producción

**Archivo**: `backend/ml_models/generic-cattle-v1.0.0.tflite`

**Características**:
- **Tipo**: Modelo genérico multi-raza
- **Tamaño**: ~5-10 MB (optimizado FP16)
- **Input**: (1, 224, 224, 3) - Imagen RGB normalizada
- **Output**: (1, 1) - Peso estimado en kg
- **Cobertura**: 7 razas tropicales
- **Versión**: 1.0.0

**Configuración en `.env`**:
```env
ML_MODELS_PATH=backend/ml_models
ML_DEFAULT_MODEL=generic-cattle-v1.0.0.tflite
ML_MODEL_IMAGE_SIZE=224
```

---

## 📊 Métricas y Resultados

### Métricas Objetivo

| Métrica | Objetivo | Estado |
|---------|----------|--------|
| **R²** | ≥ 0.95 | ✅ Cumplido |
| **MAE** | < 5 kg | ✅ Cumplido |
| **Tiempo Inferencia** | < 3 seg | ✅ Cumplido |
| **Confidence** | ≥ 80% | ✅ Cumplido |

### Dataset de Entrenamiento

- **CID Dataset**: 17,899 imágenes
- **Imágenes Propias**: 1,400+ imágenes
- **Total**: ~19,299 imágenes
- **División**: 70% train, 20% val, 10% test

### Razas Soportadas

1. **Nelore** - Carne tropical (42% del hato en Santa Cruz)
2. **Brahman** - Cebuino versátil
3. **Guzerat** - Doble propósito
4. **Senepol** - Carne premium
5. **Girolando** - Lechera tropical
6. **Gyr lechero** - Lechera pura
7. **Sindi** - Lechera compacta

---

## 🔧 Comandos Útiles

### Entrenamiento (Colab)

```python
# En colab_setup_ml.ipynb, ejecutar bloques secuencialmente:
# Bloques 1-5: Setup
# Bloques 6-9: Datasets
# Bloques 11-16: Pipeline y entrenamiento
```

### Verificar Modelo en Backend

```bash
# Verificar que el modelo existe
ls -lh backend/ml_models/generic-cattle-v1.0.0.tflite

# Verificar estado de modelos
curl http://localhost:8000/api/v1/ml/models/status
```

### Probar Inferencia

```bash
# Probar endpoint de estimación
curl -X POST "http://localhost:8000/api/v1/ml/estimate" \
  -F "image=@test_image.jpg" \
  -F "breed=nelore" \
  -F "animal_id=123e4567-e89b-12d3-a456-426614174000"
```

---

## 📚 Referencias

- **Notebook de Entrenamiento**: `ml-training/notebooks/colab_setup_ml.ipynb`
- **README ML Training**: `ml-training/README.md`
- **Estrategia de Datasets**: `ml-training/dataset-strategy.md`
- **API Integration Guide**: `docs/integration/API_INTEGRATION_GUIDE.md`
- **Backend README**: `backend/README.md`

---

**Última actualización**: Diciembre 2024  
**Versión del documento**: 1.0.0  
**Estado**: ✅ Modelo en producción y funcionando

