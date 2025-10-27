# 🐄 ML Training - Sistema de Estimación de Peso Bovino

**Proyecto**: Hacienda Gamelera (Bruno Brito Macedo)  
**Objetivo**: Entrenar 8 modelos TensorFlow Lite para estimación de peso por raza  
**Stack**: TensorFlow 2.19+ | MLflow | DVC | Albumentations 2.0.8  
**Estado**: ✅ **Listo para entrenamiento**

---

## 🎯 Razas (8 totales)

1. Brahman | 2. Nelore | 3. Angus | 4. Cebuinas  
5. Criollo | 6. Pardo Suizo | 7. Jersey | 8. Guzerat | 9. Holstein

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

## 📦 Datasets Requeridos

Ver `dataset-strategy.md` para detalles completos de datasets disponibles.

**Principales**:
- CID Dataset (17,899 imágenes)
- CattleEyeView (30,703 frames - solicitar acceso)
- Mendeley Cattle Weight (20 animales)
- Aberdeen Angus RGB-D (121 animales)

**Recolección propia requerida**:
- Criollo: 3,000+ imágenes (Hacienda Gamelera)
- Pardo Suizo: 3,000+ imágenes (ganaderías asociadas)

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

## 📝 Próximos Pasos

1. **Setup Google Colab** con GPU T4
2. **Descargar datasets** (CID, CattleEyeView, etc.)
3. **Preprocesar datos** (split train/val/test)
4. **Entrenar modelo base** genérico (Escenario A/B/C según datos disponibles)
5. **Fine-tuning por raza** (5 razas con datasets públicos)
6. **Recolección propia** para Criollo y Pardo Suizo
7. **Exportación e integración** en app móvil

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

**Última actualización**: 28 octubre 2024  
**Versión**: 1.0.0  
**Estado**: ✅ Estructura completada, pendiente entrenamiento
