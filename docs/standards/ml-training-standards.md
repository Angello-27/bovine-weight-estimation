# Estándares ML Training

> **VERSIÓN OPTIMIZADA** - Reducido de 1,294 líneas a ~700 líneas (~46% reducción)  
> Mantiene: 7 modelos TFLite, métricas R²≥0.95, MAE<5kg, proceso entrenamiento

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Stack**: TensorFlow 2.19+ | MLflow | DVC | Albumentations 2.0.8  
**Platform**: Google Colab (GPU T4 gratuita)

📅 **Última actualización**: 28 octubre 2024

---

## 🆕 Estrategia Multinivel de Entrenamiento por Escenario

> **Decisión Sprint 1-2**: Adaptar estrategia según cantidad real de imágenes disponibles

### Escenario A: >1000 imágenes por raza 🟢 IDEAL

**Estrategia**:
- Modelo base EfficientNetB1 pre-entrenado (todas las 8 razas)
- Fine-tuning específico para Brahman, Nelore, Angus (prioridad alta)
- Data augmentation 5x
- **Target**: MAE 12-18kg, R² ≥0.95

**Timeline**: 4-6 semanas  
**Modelos**: 8 modelos específicos por raza  
**Validación**: ≥50 animales por raza

---

### Escenario B: 500-1000 imágenes por raza 🟡 VIABLE

**Estrategia**:
- Modelo base único MobileNetV2 pre-entrenado
- Fine-tuning 1 raza principal (Brahman o Nelore)
- Data augmentation 10x  
- **Target**: MAE 15-25kg, R² ≥0.85

**Timeline**: 2-3 semanas  
**Modelos**: 1-2 modelos priorizados  
**Validación**: ≥30 animales total

**Alternativa**: Sistema híbrido para razas con <500 imágenes

---

### Escenario C: 200-500 imágenes por raza ⚠️ MVP ACADÉMICO

**Estrategia**:
- Modelo base único MobileNetV2
- Data augmentation 15-20x agresiva
- **Target**: MAE 25-35kg, R² ≥0.75
- Enfoque: **Proceso de entrenamiento > Precisión perfecta**

**Timeline**: 1-2 semanas  
**Modelos**: 1 modelo académico  
**Validación**: ≥20 animales con báscula

**Justificación académica**: Demostrar conocimiento de ML pipeline completo

---

### Escenario D: <200 imágenes por raza ❌ NO ENTRENAR

**Estrategia**:
- **NO entrenar modelo ML**
- **Mantener sistema híbrido** (YOLO + fórmulas)
- Calibrar mejores coeficientes con 20-30 fotos reales
- **Target**: MAE <25kg con sistema híbrido

**Timeline**: 2-3 días calibración  
**Validación**: ≥20 animales con báscula

**Justificación**: No hay suficiente data para ML confiable

---

## Principios ML

1. Un modelo por raza (8 modelos TFLite objetivo)
2. Precisión adaptada según escenario (Escenario A: MAE 12-18kg, Escenario C: MAE 25-35kg)
3. MLflow tracking todos los experimentos
4. DVC versionado datasets
5. Validación campo ≥50 animales Hacienda Gamelera (Escenario A)

---

## Stack ML

| Propósito | Herramienta | Versión |
|-----------|-------------|---------|
| Framework ML | TensorFlow + Keras | 2.19+ |
| Tracking | MLflow | 2.8+ |
| Versionado datos | DVC | 3.30+ |
| Visualización | Matplotlib + Seaborn | 3.8+, 0.13+ |
| Métricas | scikit-learn | 1.3+ |
| Augmentation | albumentations | 2.0.8 |
| Preprocesamiento | OpenCV | 4.8+ |

---

## Estructura Carpetas

```
ml-training/
├── data/
│   ├── raw/
│   │   ├── brahman/      # Mín 100 imágenes
│   │   ├── nelore/
│   │   ... (7 razas)
│   └── processed/
│
├── notebooks/
│   ├── 01-eda.ipynb
│   ├── 03-training-brahman.ipynb
│   ... (7 notebooks, uno por raza)
│
├── src/
│   ├── data/             # dataset_builder.py, augmentation.py
│   ├── models/           # cnn_architecture.py, transfer_learning.py
│   ├── training/         # trainer.py, callbacks.py
│   ├── evaluation/       # metrics.py
│   └── export/           # tflite_converter.py, manifest_generator.py
│
└── models/
    ├── brahman/v1.0.0/
    │   ├── brahman-v1.0.0.tflite
    │   └── metrics.json
    ... (7 razas)
```

---

## 7 Modelos TFLite (Config por Raza)

```python
# src/models/breed_specific_models.py

@dataclass
class BreedModelConfig:
    breed_type: BreedType
    model_filename: str
    expected_weight_range_kg: Tuple[float, float]
    target_r2: float = 0.95
    target_mae_kg: float = 5.0

CONFIGS = {
    BreedType.BRAHMAN: BreedModelConfig(
        breed_type=BreedType.BRAHMAN,
        model_filename="brahman-v1.0.0.tflite",
        expected_weight_range_kg=(150.0, 800.0),
    ),
    # ... resto de 6 razas
}
```

---

## Métricas Obligatorias

```python
# src/evaluation/metrics.py

class MetricsCalculator:
    @staticmethod
    def calculate_metrics(y_true, y_pred, breed_type) -> ModelMetrics:
        """Calcula R², MAE, MAPE. Valida R²≥0.95 y MAE<5kg."""
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred) * 100
        
        # Validar requisitos Hacienda Gamelera
        assert r2 >= 0.95, f"R² {r2:.4f} < 0.95 para {breed_type}"
        assert mae < 5.0, f"MAE {mae:.2f} kg > 5 kg para {breed_type}"
        
        return ModelMetrics(r2_score=r2, mae_kg=mae, mape_percent=mape, ...)
```

---

## Arquitectura CNN

```python
# src/models/transfer_learning.py

class BreedWeightEstimatorCNN:
    @staticmethod
    def build_model(breed_name: str) -> keras.Model:
        """
        CNN con transfer learning MobileNetV2.
        
        Input: (224, 224, 3)
        MobileNetV2 (frozen, ImageNet) → GlobalAvgPooling → 
        Dense(256, relu) + Dropout(0.3) → Dense(128, relu) + Dropout(0.2) →
        Dense(1, linear) → Peso kg
        """
        base = keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet',
        )
        base.trainable = False
        
        inputs = keras.Input(shape=(224, 224, 3))
        x = keras.applications.mobilenet_v2.preprocess_input(inputs)
        x = base(x, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(1, activation='linear')(x)
        
        model = keras.Model(inputs, outputs, name=f"{breed_name}_estimator")
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae', 'mape'],
        )
        return model
```

---

## Data Augmentation

```python
# src/data/augmentation.py

import albumentations as A

def get_training_transform():
    """Simula condiciones Hacienda Gamelera (luz solar, ángulos, ruido)."""
    return A.Compose([
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.7),
        A.GaussNoise(var_limit=(10, 50), p=0.3),
        A.Resize(224, 224),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
```

---

## Exportación TFLite

```python
# src/export/tflite_converter.py

class TFLiteExporter:
    @staticmethod
    def convert_to_tflite(saved_model_path: str, output_path: str):
        """Convierte TF → TFLite con quantization (reduce 4x tamaño)."""
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.float16]
        
        tflite_model = converter.convert()
        
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        print(f"✅ {Path(output_path).name} ({len(tflite_model)/1024/1024:.1f} MB)")
```

---

## Manifest.json (7 Modelos)

```python
# src/export/manifest_generator.py

def generate_manifest(models_dir: Path) -> dict:
    """Genera manifest con los 7 modelos TFLite."""
    manifest = {
        "version": "1.0.0",
        "hacienda": "Hacienda Gamelera",
        "models": []
    }
    
    for breed in BreedType:
        model_path = models_dir / breed.value / "v1.0.0" / f"{breed.value}-v1.0.0.tflite"
        metrics_path = models_dir / breed.value / "v1.0.0" / "metrics.json"
        
        manifest["models"].append({
            "breed_type": breed.value,
            "filename": model_path.name,
            "metrics": json.load(open(metrics_path)),
            "url": f"https://d123.cloudfront.net/{model_path.name}",
        })
    
    assert len(manifest["models"]) == 7, "Deben ser 7 modelos (una por raza)"
    return manifest
```

---

## Script Entrenamiento Completo

```python
# scripts/train_all_breeds.py

"""Entrena los 7 modelos TFLite para Hacienda Gamelera."""

from src.training.breed_trainer import BreedModelTrainer

for breed in BreedType:
    print(f"\n{'#'*60}")
    print(f"# RAZA: {breed.value.upper()}")
    print(f"{'#'*60}")
    
    # 1. Entrenar
    trainer = BreedModelTrainer(breed_type=breed, data_dir="data/processed")
    model = trainer.train(epochs=50)
    
    # 2. Guardar
    model.save(f"models/{breed.value}/v1.0.0/saved_model")
    
    # 3. Exportar TFLite
    TFLiteExporter.convert_to_tflite(
        f"models/{breed.value}/v1.0.0/saved_model",
        f"models/{breed.value}/v1.0.0/{breed.value}-v1.0.0.tflite",
    )

# 4. Generar manifest
generate_manifest(Path("models"))
print("\n✅ 7 modelos entrenados y exportados")
```

---

## Requirements

```txt
# requirements.txt
tensorflow==2.19.0
mlflow==2.8.1
dvc==3.30.0
opencv-python==4.8.1
albumentations==2.0.8  # Versión específica por compatibilidad
scikit-learn==1.3.2
pandas==2.1.3
matplotlib==3.8.2
jupyterlab==4.0.9
pytest==7.4.3
```

---

## Referencias

- 📐 Architecture: `architecture-standards.md`
- 🎯 US-002: Estimación de Peso por Raza
- TensorFlow Lite: https://tensorflow.org/lite

---

## 📊 Optimización

**ANTES**: 1,294 líneas (42 KB)  
**DESPUÉS**: ~700 líneas (~22 KB)  
**Reducción**: ~46%

**MANTENIDO** ✅:
- 7 modelos TFLite config completa
- Métricas obligatorias (R², MAE, MAPE)
- Arquitectura CNN MobileNetV2
- Data augmentation
- Exportación TFLite
- Script train_all_breeds.py

**ELIMINADO** ❌:
- Ejemplos training loop extensos
- Notebooks código completo (solo referencia)
- Comentarios verbose
- Secciones MLflow detalladas

---

**ML Training Standards v2.0 (Optimizado)**  
**Fecha**: 28 octubre 2024  
**7 modelos**: brahman, nelore, angus, cebuinas, criollo, pardo-suizo, jersey

