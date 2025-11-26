# 🐄 ML Training - Sistema de Estimación de Peso Bovino

**Proyecto**: Hacienda Gamelera (Bruno Brito Macedo)  
**Objetivo**: Entrenar 8 modelos TensorFlow Lite para estimación de peso por raza  
**Stack**: TensorFlow 2.19+ | MLflow | DVC | Albumentations 2.0.8  
**Estado**: ✅ **Listo para entrenamiento**

---

## 🎯 Razas (7 razas tropicales priorizadas)

1. **Nelore** – Carne tropical dominante en Santa Cruz (≈42% del hato)
2. **Brahman** – Cebuino versátil para cruzamientos y climas extremos
3. **Guzerat** – Doble propósito (carne/leche) con gran rusticidad materna
4. **Senepol** – Carne premium adaptada al calor, ideal para "steer" de alta calidad
5. **Girolando** – Lechera tropical (Holstein × Gyr) muy difundida en sistemas semi-intensivos
6. **Gyr lechero** – Lechera pura clave para genética tropical y sólidos altos
7. **Sindi** – Lechera tropical compacta, de alta fertilidad y leche rica en sólidos

> Estas razas están alineadas con el modelo ML entrenado en Colab y cubren el portafolio real de Santa Cruz (carne tropical + lecheras adaptadas).

---

## 🏗️ Estructura del Proyecto

```
ml-training/
├── src/
│   ├── data/
│   │   └── augmentation.py          # Albumentations 2.0.8
│   ├── models/
│   │   ├── cnn_architecture.py      # MobileNetV2/EfficientNet
│   │   ├── training/
│   │   │   └── trainer.py           # BreedModelTrainer
│   │   ├── evaluation/
│   │   │   └── metrics.py           # R², MAE, MAPE
│   │   └── export/
│   │       └── tflite_converter.py  # Exportación TFLite
│   └── utils/
├── scripts/
│   └── train_all_breeds.py          # Script principal
├── notebooks/
│   └── colab_setup_ml.ipynb         # Setup Colab
├── config/
│   └── config.yaml                   # Configuración
└── requirements.txt
```

---

## 🚀 Uso Rápido

### 1. Instalar Dependencias

```bash
cd ml-training
pip install -r requirements.txt
```

### 2. Entrenar Un Modelo por Raza

```python
from pathlib import Path
from src.models.cnn_architecture import BreedWeightEstimatorCNN
from src.models.export.tflite_converter import TFLiteExporter

# Crear modelo para raza específica
model = BreedWeightEstimatorCNN.build_model(
    breed_name='brahman',
    base_architecture='mobilenetv2'
)

# Entrenar con tus datos
# TODO: Implementar carga de datos real
# model.fit(train_data, validation_data=val_data, epochs=50)

# Exportar a TFLite
TFLiteExporter.convert_to_tflite(
    saved_model_path='models/brahman/saved_model',
    output_path='models/brahman/v1.0.0/brahman-v1.0.0.tflite',
    optimization='default'  # FP16
)
```

### 3. Evaluar Métricas

```python
from src.models.evaluation.metrics import MetricsCalculator
import numpy as np

# Calcular métricas (con validación de objetivos)
metrics = MetricsCalculator.calculate_metrics_with_assertions(
    y_true=np.array([450, 500, 380]),  # Pesos reales
    y_pred=np.array([445, 505, 385]),  # Pesos predichos
    breed_type='brahman',
    target_r2=0.95,
    max_mae=5.0
)

print(f"R²: {metrics.r2_score:.4f}")
print(f"MAE: {metrics.mae_kg:.2f} kg")
```

---

## 📊 Estrategia de Entrenamiento (Según Dataset Disponible)

### Escenario A: >1000 imágenes por raza 🟢 IDEAL

- **Modelo**: EfficientNetB1 pre-entrenado
- **Estrategia**: Entrenamiento directo con fine-tuning
- **Target**: MAE 12-18kg, R² ≥0.95
- **Timeline**: 4-6 semanas

### Escenario B: 500-1000 imágenes por raza 🟡 VIABLE

- **Modelo**: MobileNetV2 pre-entrenado
- **Estrategia**: Fine-tuning específico
- **Target**: MAE 15-25kg, R² ≥0.85
- **Timeline**: 2-3 semanas

### Escenario C: 200-500 imágenes por raza ⚠️ MVP ACADÉMICO

- **Modelo**: MobileNetV2
- **Estrategia**: Augmentation agresiva (15-20x)
- **Target**: MAE 25-35kg, R² ≥0.75
- **Timeline**: 1-2 semanas

### Escenario D: <200 imágenes por raza ❌ NO ENTRENAR

- **Estrategia**: Sistema híbrido (YOLO + fórmulas)
- **Target**: MAE <25kg con sistema híbrido
- **Timeline**: 2-3 días calibración

---

## 🎯 Métricas Objetivo (Requisitos Críticos)

| Métrica | Objetivo | Descripción |
|---------|----------|-------------|
| **R²** | ≥ 0.95 | Explicación de 95% de varianza |
| **MAE** | < 5 kg | Error absoluto promedio |
| **Inference** | < 3 seg | Tiempo en mobile TFLite |

---

## 📦 Datasets Utilizados

**Estrategia B - Combinación de Datasets**:

1. **CID Dataset** (17,899 imágenes)
   - Fuente: https://github.com/bhuiyanmobasshir94/CID
   - Descarga automática desde S3 en BLOQUE 7
   - Proporciona diversidad y calidad

2. **Nuestras Imágenes** (~1,400+ imágenes)
   - Scraping automático en BLOQUE 6 (200+ por raza)
   - Razas bolivianas: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey
   - Proporciona especificidad local y contexto real

3. **Imágenes Locales** (opcional)
   - Fotos manuales o descargadas
   - Se combinan automáticamente en BLOQUE 8

**Total combinado**: ~19,299+ imágenes para entrenamiento

---

## 🔧 Módulos Principales

### `augmentation.py` - Data Augmentation

```python
from src.data.augmentation import get_training_transform

# Augmentation estándar
transform = get_training_transform(image_size=(224, 224))

# Augmentation agresiva (para datasets pequeños)
transform_aggressive = get_aggressive_augmentation(image_size=(224, 224))
```

### `cnn_architecture.py` - Arquitecturas CNN

```python
from src.models.cnn_architecture import BreedWeightEstimatorCNN

# Modelo para raza específica
model = BreedWeightEstimatorCNN.build_model(
    breed_name='brahman',
    base_architecture='mobilenetv2'
)

# Modelo genérico multi-raza
model_generic = BreedWeightEstimatorCNN.build_generic_model()
```

### `metrics.py` - Evaluación

```python
from src.models.evaluation.metrics import MetricsCalculator

# Calcular métricas
metrics = MetricsCalculator.calculate_metrics(y_true, y_pred, 'brahman')

# Calcular y validar objetivos críticos
metrics = MetricsCalculator.calculate_metrics_with_assertions(
    y_true, y_pred, 'brahman', target_r2=0.95, max_mae=5.0
)
```

### `tflite_converter.py` - Exportación TFLite

```python
from src.models.export.tflite_converter import TFLiteExporter

# Convertir a TFLite
TFLiteExporter.convert_to_tflite(
    saved_model_path='models/brahman/saved_model',
    output_path='models/brahman/v1.0.0/brahman-v1.0.0.tflite',
    optimization='default'  # 'none', 'default', 'int8'
)
```

---

## 📓 Notebook de Setup: `colab_setup_ml.ipynb`

El notebook está diseñado para ejecutarse en Google Colab Pro y prepara todo el entorno de entrenamiento de forma secuencial.

### Estructura del Notebook (16 Bloques)

**Día 1: Setup (Bloques 1-5)**
- BLOQUE 1: Clonar repositorio en Google Drive
- BLOQUE 2: Verificar dependencias base
- BLOQUE 3: Instalar dependencias críticas (TensorFlow 2.19.0, MLflow, DVC)
- BLOQUE 4: Instalar complementos (Albumentations, OpenCV)
- BLOQUE 5: Configurar proyecto y estructura de carpetas

**Día 2-3: Datasets (Bloques 6-9) - Estrategia B**
- BLOQUE 6: Descargar nuestras imágenes (scraping - razas bolivianas)
- BLOQUE 7: Descargar CID Dataset desde S3 (complementario - 17,899+ imágenes)
- BLOQUE 8: Preparar dataset combinado (Estrategia B: CID + nuestras imágenes)
- BLOQUE 9: Resumen de datasets disponibles

**Día 4: Verificación (Bloque 10) - OPCIONAL**
- BLOQUE 10: Verificación rápida de datos (puede saltarse para entrenar más rápido)

**Día 5-6: Pipeline y Modelo (Bloques 11-16)**
- BLOQUE 11: Pipeline de datos con augmentation (usa dataset combinado - Estrategia B)
- BLOQUE 12: Arquitectura del modelo (EfficientNetB1)
- BLOQUE 13: Configurar entrenamiento (callbacks, MLflow)
- BLOQUE 14: Entrenar modelo (2-4 horas con GPU T4)
- BLOQUE 15: Evaluación del modelo
- BLOQUE 16: Exportar a TFLite

### 🎯 Estrategia B - Dataset Combinado

El notebook implementa la **Estrategia B** que combina:
- **CID Dataset**: ~17,899 imágenes (diversidad y calidad)
- **Nuestras Imágenes**: ~1,400+ imágenes (especificidad local - razas bolivianas)
- **Total**: ~19,299+ imágenes para mejor generalización y precisión

### Uso del Notebook

1. Abrir `notebooks/colab_setup_ml.ipynb` en Google Colab Pro
2. Ejecutar bloques secuencialmente (1-16)
3. El BLOQUE 10 es opcional y puede saltarse
4. El entrenamiento (BLOQUE 14) requiere GPU T4 y tarda 2-4 horas

---

## 🔬 MLflow Tracking

Los experimentos se trackean automáticamente con MLflow:

```python
import mlflow
mlflow.set_tracking_uri("file://./experiments/mlflow")
mlflow.set_experiment("bovine-weight-estimation")

# Los entrenamientos loguean automáticamente:
# - Parámetros (epochs, batch_size, learning_rate)
# - Métricas (R², MAE, MSE)
# - Modelos entrenados
```

---

## 📚 Referencias

- 📐 **Estándares ML**: `docs/standards/ml-training-standards.md`
- 🗺️ **Estrategia Datasets**: `dataset-strategy.md`
- 📊 **Arquitectura**: `docs/standards/architecture-standards.md`

---

**Última actualización**: Diciembre 2024  
**Versión**: 1.0.0  
**Estado**: ✅ Notebook optimizado y listo para entrenamiento con Estrategia B
