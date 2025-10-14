# Estándares de Entrenamiento ML

## Contexto del Proyecto

**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Tecnología**: TensorFlow 2.13+ / Keras / MLflow  
**Objetivo**: Modelos CNN con precisión ≥95% (R² ≥0.95), error <5 kg

## Principios Fundamentales ML

1. **Un modelo por raza**: 7 modelos TFLite específicos (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)
2. **Precisión ≥95% obligatoria**: R² ≥ 0.95, MAE < 5 kg, MAPE < 5%
3. **Reproducibilidad**: MLflow tracking de todos los experimentos
4. **Versionado de datos**: DVC para datasets por raza
5. **Validación en campo**: Mínimo 50 animales reales de Hacienda Gamelera

---

## Stack Tecnológico ML

### Herramientas Core

| Propósito | Herramienta | Justificación | Versión |
|-----------|-------------|---------------|---------|
| **Framework ML** | TensorFlow + Keras | Entrenamiento CNN, exportación TFLite | 2.13+ |
| **Tracking experimentos** | MLflow | Métricas R², MAE, MAPE por modelo | 2.8+ |
| **Versionado datos** | DVC | Control de versiones de imágenes por raza | 3.30+ |
| **Visualización** | Matplotlib + Seaborn | Análisis exploratorio, curvas aprendizaje | 3.8+, 0.13+ |
| **Métricas** | scikit-learn + pandas | Cálculo R², MAE, MAPE, análisis | 1.3+, 2.1+ |
| **Data augmentation** | albumentations | Variaciones luz, ángulo, rotación | 1.3+ |
| **Preprocesamiento** | OpenCV (cv2) | Segmentación silueta, mejora imágenes | 4.8+ |
| **Notebooks** | Jupyter Lab | Análisis exploratorio iterativo | 4.0+ |
| **Testing** | pytest + nbval | Validación notebooks, métricas reproducibles | 7.4+, 0.11+ |

---

## Estructura de Carpetas ML Training

```
ml-training/
├── data/                                  # Datasets
│   ├── raw/                               # Imágenes originales con peso real
│   │   ├── brahman/                       # Mínimo 100 imágenes
│   │   │   ├── img_001.jpg                # Nombre: {id}_{peso_kg}.jpg
│   │   │   ├── img_002.jpg
│   │   │   └── metadata.csv               # id, peso_kg, edad_meses, fecha
│   │   ├── nelore/
│   │   ├── angus/
│   │   ├── cebuinas/
│   │   ├── criollo/
│   │   ├── pardo-suizo/
│   │   └── jersey/
│   │
│   ├── processed/                         # Imágenes preprocesadas
│   │   └── [misma estructura por raza]
│   │
│   ├── annotations.csv                    # Consolidado todas las razas
│   └── .dvc/                              # DVC metadata
│
├── notebooks/                             # Jupyter notebooks
│   ├── 01-eda-exploratory-analysis.ipynb  # Análisis exploratorio
│   ├── 02-preprocessing-opencv.ipynb      # Preprocesamiento OpenCV
│   ├── 03-model-training-brahman.ipynb    # Training modelo Brahman
│   ├── 04-model-training-nelore.ipynb     # Training modelo Nelore
│   ├── 05-model-training-angus.ipynb      # Training modelo Angus
│   ├── 06-model-training-cebuinas.ipynb   # Training modelo Cebuinas
│   ├── 07-model-training-criollo.ipynb    # Training modelo Criollo
│   ├── 08-model-training-pardo-suizo.ipynb # Training modelo Pardo Suizo
│   ├── 09-model-training-jersey.ipynb     # Training modelo Jersey
│   └── 10-model-evaluation-all-breeds.ipynb # Evaluación conjunta
│
├── src/                                   # Código fuente Python
│   ├── data/
│   │   ├── dataset_builder.py             # Construcción dataset por raza
│   │   ├── augmentation.py                # Data augmentation
│   │   ├── preprocessing.py               # OpenCV preprocessing
│   │   └── validation.py                  # Validación calidad datos
│   │
│   ├── models/
│   │   ├── cnn_architecture.py            # Arquitectura CNN custom
│   │   ├── transfer_learning.py           # MobileNetV2/EfficientNet
│   │   ├── model_builder.py               # Builder pattern
│   │   └── breed_specific_models.py       # Configuraciones por raza
│   │
│   ├── training/
│   │   ├── trainer.py                     # Training loop
│   │   ├── callbacks.py                   # Callbacks custom (MLflow)
│   │   ├── hyperparameters.py             # Grid search hiperparámetros
│   │   └── breed_trainer.py               # Entrenador específico por raza
│   │
│   ├── evaluation/
│   │   ├── metrics.py                     # Cálculo R², MAE, MAPE
│   │   ├── visualizations.py              # Curvas, matrices confusión
│   │   └── field_validation.py            # Validación campo Hacienda
│   │
│   ├── export/
│   │   ├── tflite_converter.py            # TensorFlow → TFLite
│   │   ├── quantization.py                # Post-training quantization
│   │   └── manifest_generator.py          # manifest.json
│   │
│   └── utils/
│       ├── image_utils.py
│       └── mlflow_utils.py
│
├── experiments/                           # MLflow experiments
│   └── mlruns/
│       ├── 0/                             # Experimento: Brahman
│       ├── 1/                             # Experimento: Nelore
│       └── ...                            # Hasta 6 (7 razas)
│
├── models/                                # Modelos entrenados
│   ├── brahman/
│   │   ├── v1.0.0/
│   │   │   ├── saved_model/               # TensorFlow SavedModel
│   │   │   ├── brahman-v1.0.0.tflite      # TFLite optimizado
│   │   │   ├── brahman-v1.0.0.h5          # Keras model
│   │   │   ├── metrics.json               # R², MAE, MAPE
│   │   │   ├── training_history.json      # Loss, val_loss por epoch
│   │   │   └── model_card.md              # Documentación modelo
│   │   └── v1.1.0/
│   ├── nelore/
│   ├── angus/
│   ├── cebuinas/
│   ├── criollo/
│   ├── pardo-suizo/
│   └── jersey/
│
├── scripts/                               # Scripts automatizados
│   ├── train_all_breeds.py                # Entrenar 7 modelos
│   ├── evaluate_all_breeds.py             # Evaluar 7 modelos
│   ├── export_all_tflite.py               # Exportar 7 TFLite
│   └── generate_manifest.py               # manifest.json con 7 modelos
│
├── tests/                                 # Tests
│   ├── test_dataset_builder.py
│   ├── test_preprocessing.py
│   ├── test_model_inference.py
│   └── test_metrics_calculation.py
│
├── requirements.txt                       # Dependencies ML
├── .dvcignore                             # DVC ignore patterns
├── dvc.yaml                               # DVC pipeline
├── MLproject                              # MLflow project
└── README.md
```

---

## Datos Críticos del Modelo

### 7 Modelos TFLite (UNO POR RAZA - EXACTOS)

```python
# src/models/breed_specific_models.py

from dataclasses import dataclass
from typing import Dict, Tuple

from app.core.constants.breeds import BreedType

@dataclass
class BreedModelConfig:
    """Configuración de modelo específico por raza."""
    breed_type: BreedType
    model_filename: str
    version: str
    input_shape: Tuple[int, int, int]  # (height, width, channels)
    expected_weight_range_kg: Tuple[float, float]  # (min, max)
    target_precision_r2: float  # R² objetivo
    target_mae_kg: float        # MAE objetivo

class BreedModelConfigs:
    """
    Configuraciones de los 7 modelos TFLite de Hacienda Gamelera.
    
    IMPORTANTE: Un modelo por raza para maximizar precisión.
    NO usar modelo genérico multi-raza.
    """
    
    CONFIGS: Dict[BreedType, BreedModelConfig] = {
        BreedType.BRAHMAN: BreedModelConfig(
            breed_type=BreedType.BRAHMAN,
            model_filename="brahman-v1.0.0.tflite",
            version="v1.0.0",
            input_shape=(224, 224, 3),
            expected_weight_range_kg=(150.0, 800.0),  # Terneros a toros adultos
            target_precision_r2=0.95,
            target_mae_kg=5.0,
        ),
        BreedType.NELORE: BreedModelConfig(
            breed_type=BreedType.NELORE,
            model_filename="nelore-v1.0.0.tflite",
            version="v1.0.0",
            input_shape=(224, 224, 3),
            expected_weight_range_kg=(140.0, 750.0),
            target_precision_r2=0.95,
            target_mae_kg=5.0,
        ),
        BreedType.ANGUS: BreedModelConfig(
            breed_type=BreedType.ANGUS,
            model_filename="angus-v1.0.0.tflite",
            version="v1.0.0",
            input_shape=(224, 224, 3),
            expected_weight_range_kg=(160.0, 900.0),
            target_precision_r2=0.95,
            target_mae_kg=5.0,
        ),
        BreedType.CEBUINAS: BreedModelConfig(
            breed_type=BreedType.CEBUINAS,
            model_filename="cebuinas-v1.0.0.tflite",
            version="v1.0.0",
            input_shape=(224, 224, 3),
            expected_weight_range_kg=(145.0, 780.0),
            target_precision_r2=0.95,
            target_mae_kg=5.0,
        ),
        BreedType.CRIOLLO: BreedModelConfig(
            breed_type=BreedType.CRIOLLO,
            model_filename="criollo-v1.0.0.tflite",
            version="v1.0.0",
            input_shape=(224, 224, 3),
            expected_weight_range_kg=(130.0, 650.0),
            target_precision_r2=0.95,
            target_mae_kg=5.0,
        ),
        BreedType.PARDO_SUIZO: BreedModelConfig(
            breed_type=BreedType.PARDO_SUIZO,
            model_filename="pardo-suizo-v1.0.0.tflite",
            version="v1.0.0",
            input_shape=(224, 224, 3),
            expected_weight_range_kg=(170.0, 950.0),
            target_precision_r2=0.95,
            target_mae_kg=5.0,
        ),
        BreedType.JERSEY: BreedModelConfig(
            breed_type=BreedType.JERSEY,
            model_filename="jersey-v1.0.0.tflite",
            version="v1.0.0",
            input_shape=(224, 224, 3),
            expected_weight_range_kg=(120.0, 600.0),
            target_precision_r2=0.95,
            target_mae_kg=5.0,
        ),
    }
    
    @classmethod
    def get_config(cls, breed_type: BreedType) -> BreedModelConfig:
        """Retorna configuración del modelo para raza específica."""
        if breed_type not in cls.CONFIGS:
            raise ValueError(
                f"Raza {breed_type.value} no tiene modelo configurado. "
                f"Solo las 7 razas de Hacienda Gamelera son soportadas."
            )
        return cls.CONFIGS[breed_type]
```

---

## Métricas Obligatorias del Modelo

### Definición de Métricas

```python
# src/evaluation/metrics.py

import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_absolute_percentage_error
from typing import NamedTuple

class ModelMetrics(NamedTuple):
    """
    Métricas de evaluación de modelo de peso bovino.
    
    Todas las métricas son OBLIGATORIAS según requisitos de Hacienda Gamelera.
    """
    r2_score: float          # Coeficiente de determinación (≥0.95)
    mae_kg: float            # Mean Absolute Error en kg (<5 kg)
    mape_percent: float      # Mean Absolute Percentage Error (<5%)
    rmse_kg: float           # Root Mean Squared Error
    n_samples: int           # Número de muestras evaluadas
    breed_type: str          # Raza evaluada (una de las 7)

class MetricsCalculator:
    """Calculadora de métricas para modelos de estimación de peso."""
    
    @staticmethod
    def calculate_metrics(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        breed_type: str,
    ) -> ModelMetrics:
        """
        Calcula todas las métricas de evaluación del modelo.
        
        Args:
            y_true: Pesos reales en kg (de báscula)
            y_pred: Pesos estimados por modelo en kg
            breed_type: Raza del modelo (una de las 7)
            
        Returns:
            ModelMetrics con todas las métricas calculadas
            
        Raises:
            AssertionError: Si R² <0.95 o MAE >5 kg (no cumple requisitos)
        """
        # Calcular métricas
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred) * 100  # Convertir a %
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
        
        metrics = ModelMetrics(
            r2_score=r2,
            mae_kg=mae,
            mape_percent=mape,
            rmse_kg=rmse,
            n_samples=len(y_true),
            breed_type=breed_type,
        )
        
        # Validar que cumple requisitos del sistema
        assert r2 >= 0.95, (
            f"R² = {r2:.4f} < 0.95 requerido para {breed_type}. "
            f"Modelo NO cumple precisión mínima para Hacienda Gamelera."
        )
        
        assert mae < 5.0, (
            f"MAE = {mae:.2f} kg > 5 kg máximo para {breed_type}. "
            f"Modelo NO cumple error máximo para Hacienda Gamelera."
        )
        
        return metrics
    
    @staticmethod
    def print_metrics_report(metrics: ModelMetrics) -> None:
        """Imprime reporte de métricas formateado."""
        print(f"\n{'='*60}")
        print(f"MÉTRICAS DEL MODELO - {metrics.breed_type.upper()}")
        print(f"{'='*60}")
        print(f"R² Score:              {metrics.r2_score:.4f} {'✅' if metrics.r2_score >= 0.95 else '❌'} (objetivo: ≥0.95)")
        print(f"MAE (Error Absoluto):  {metrics.mae_kg:.2f} kg {'✅' if metrics.mae_kg < 5.0 else '❌'} (objetivo: <5 kg)")
        print(f"MAPE (Error %):        {metrics.mape_percent:.2f}% {'✅' if metrics.mape_percent < 5.0 else '❌'} (objetivo: <5%)")
        print(f"RMSE:                  {metrics.rmse_kg:.2f} kg")
        print(f"Muestras evaluadas:    {metrics.n_samples}")
        print(f"{'='*60}\n")
        
        if metrics.r2_score >= 0.95 and metrics.mae_kg < 5.0:
            print("✅ MODELO APROBADO para producción en Hacienda Gamelera")
        else:
            print("❌ MODELO RECHAZADO - No cumple requisitos mínimos")
```

---

## Arquitectura CNN

### Modelo Base (Transfer Learning)

```python
# src/models/transfer_learning.py

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple

class BreedWeightEstimatorCNN:
    """
    Arquitectura CNN para estimación de peso bovino por raza.
    
    Basado en transfer learning de MobileNetV2 (optimizado para móviles).
    Modificado para regresión de peso continuo (kg).
    """
    
    @staticmethod
    def build_model(
        input_shape: Tuple[int, int, int] = (224, 224, 3),
        breed_name: str = "brahman",
    ) -> keras.Model:
        """
        Construye modelo CNN con transfer learning.
        
        Args:
            input_shape: Dimensiones de entrada (224x224x3)
            breed_name: Nombre de la raza para identificación
            
        Returns:
            Modelo Keras compilado listo para entrenamiento
            
        Architecture:
            1. MobileNetV2 base (preentrenada ImageNet, frozen)
            2. GlobalAveragePooling2D
            3. Dense(256, relu) + Dropout(0.3)
            4. Dense(128, relu) + Dropout(0.2)
            5. Dense(1, linear) → Peso en kg
        """
        # Base: MobileNetV2 preentrenada
        base_model = keras.applications.MobileNetV2(
            input_shape=input_shape,
            include_top=False,
            weights='imagenet',
        )
        base_model.trainable = False  # Congelar pesos preentrenados
        
        # Modelo completo
        inputs = keras.Input(shape=input_shape, name=f"{breed_name}_input")
        
        # Preprocesamiento para MobileNetV2
        x = keras.applications.mobilenet_v2.preprocess_input(inputs)
        
        # Base convolucional
        x = base_model(x, training=False)
        
        # Pooling global
        x = layers.GlobalAveragePooling2D(name="global_avg_pooling")(x)
        
        # Capas densas para regresión
        x = layers.Dense(256, activation='relu', name="dense_256")(x)
        x = layers.Dropout(0.3, name="dropout_30")(x)
        
        x = layers.Dense(128, activation='relu', name="dense_128")(x)
        x = layers.Dropout(0.2, name="dropout_20")(x)
        
        # Salida: peso en kg (regresión)
        outputs = layers.Dense(1, activation='linear', name="weight_kg_output")(x)
        
        # Crear modelo
        model = keras.Model(inputs=inputs, outputs=outputs, name=f"{breed_name}_weight_estimator")
        
        # Compilar
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mean_squared_error',
            metrics=[
                'mae',  # Mean Absolute Error
                'mape', # Mean Absolute Percentage Error
                keras.metrics.RootMeanSquaredError(name='rmse'),
            ],
        )
        
        return model
    
    @staticmethod
    def unfreeze_and_fine_tune(
        model: keras.Model,
        learning_rate: float = 0.0001,
    ) -> keras.Model:
        """
        Descongelar últimas capas y hacer fine-tuning.
        
        Args:
            model: Modelo con base congelada
            learning_rate: Learning rate reducido para fine-tuning
            
        Returns:
            Modelo listo para fine-tuning
        """
        # Descongelar últimas 30 capas de MobileNetV2
        base_model = model.layers[1]  # MobileNetV2
        base_model.trainable = True
        
        for layer in base_model.layers[:-30]:
            layer.trainable = False
        
        # Recompilar con learning rate reducido
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss='mean_squared_error',
            metrics=['mae', 'mape', keras.metrics.RootMeanSquaredError(name='rmse')],
        )
        
        return model
```

---

## Preprocesamiento con OpenCV

```python
# src/data/preprocessing.py

import cv2
import numpy as np
from typing import Tuple

class ImagePreprocessor:
    """
    Preprocesamiento de imágenes de bovinos con OpenCV.
    
    Técnicas aplicadas:
    1. Segmentación de silueta
    2. Eliminación de ruido
    3. Normalización
    4. Redimensionamiento (224x224)
    """
    
    @staticmethod
    def preprocess_for_inference(
        image: np.ndarray,
        target_size: Tuple[int, int] = (224, 224),
    ) -> np.ndarray:
        """
        Preprocesa imagen para inferencia del modelo.
        
        Args:
            image: Imagen BGR de OpenCV (cualquier tamaño)
            target_size: Tamaño objetivo (224, 224) para MobileNetV2
            
        Returns:
            Imagen normalizada (224, 224, 3) lista para modelo
            
        Steps:
            1. Convertir BGR → RGB
            2. Redimensionar a 224x224 manteniendo aspect ratio
            3. Normalizar pixeles a rango [0, 1]
            4. Agregar batch dimension: (1, 224, 224, 3)
        """
        # BGR → RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Redimensionar con aspect ratio
        image_resized = cv2.resize(image_rgb, target_size, interpolation=cv2.INTER_LANCZOS4)
        
        # Normalizar a [0, 1]
        image_normalized = image_resized.astype(np.float32) / 255.0
        
        # Agregar batch dimension
        image_batch = np.expand_dims(image_normalized, axis=0)
        
        return image_batch
    
    @staticmethod
    def segment_bovine_silhouette(image: np.ndarray) -> np.ndarray:
        """
        Segmenta silueta del bovino usando técnicas de visión computacional.
        
        Técnicas:
        1. Conversión a escala de grises
        2. GaussianBlur para eliminar ruido
        3. Thresholding adaptativo
        4. Detección de contornos
        5. Filtrado por área (eliminar pequeños objetos)
        
        Returns:
            Máscara binaria de silueta del bovino
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Eliminar ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Thresholding adaptativo
        thresh = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )
        
        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar por área (bovino es objeto más grande)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [largest_contour], -1, 255, -1)
            return mask
        
        return thresh
```

---

## MLflow Tracking

```python
# src/training/callbacks.py

import mlflow
import mlflow.keras
from tensorflow import keras
from typing import Dict, Any

class MLflowCallback(keras.callbacks.Callback):
    """
    Callback para tracking de experimentos con MLflow.
    
    Registra métricas por epoch y modelo final.
    """
    
    def __init__(self, breed_type: str, run_name: str):
        super().__init__()
        self.breed_type = breed_type
        self.run_name = run_name
    
    def on_train_begin(self, logs=None):
        """Inicia run de MLflow."""
        mlflow.start_run(run_name=self.run_name)
        
        # Log parámetros
        mlflow.log_param("breed_type", self.breed_type)
        mlflow.log_param("hacienda", "Hacienda Gamelera")
        mlflow.log_param("target_r2", 0.95)
        mlflow.log_param("target_mae_kg", 5.0)
    
    def on_epoch_end(self, epoch, logs=None):
        """Log métricas por epoch."""
        if logs:
            mlflow.log_metrics(
                {
                    "loss": logs.get("loss"),
                    "val_loss": logs.get("val_loss"),
                    "mae": logs.get("mae"),
                    "val_mae": logs.get("val_mae"),
                },
                step=epoch,
            )
    
    def on_train_end(self, logs=None):
        """Finaliza run y guarda modelo."""
        # Log modelo final
        mlflow.keras.log_model(self.model, "model")
        
        # Log métricas finales
        final_metrics = {
            "final_loss": logs.get("loss"),
            "final_val_loss": logs.get("val_loss"),
            "final_mae": logs.get("mae"),
            "final_val_mae": logs.get("val_mae"),
        }
        mlflow.log_metrics(final_metrics)
        
        # Finalizar run
        mlflow.end_run()
```

---

## Data Augmentation

```python
# src/data/augmentation.py

import albumentations as A
from albumentations.pytorch import ToTensorV2

class BovineAugmentationPipeline:
    """
    Pipeline de data augmentation para imágenes de bovinos.
    
    Simula condiciones reales de Hacienda Gamelera:
    - Luz solar variable (mañana, mediodía, tarde)
    - Ángulos de cámara (smartphone sostenido a mano)
    - Condiciones climáticas (nublado, soleado)
    """
    
    @staticmethod
    def get_training_transform():
        """
        Transformaciones para entrenamiento (con augmentation).
        
        Técnicas aplicadas:
        - Rotación horizontal (bovino visto desde ambos lados)
        - Ajustes de brillo/contraste (luz solar variable)
        - Ruido gaussiano (calidad de cámara)
        - Recortes aleatorios (enfoque parcial)
        """
        return A.Compose([
            # Geométricas
            A.HorizontalFlip(p=0.5),                    # Bovino de lado izquierdo/derecho
            A.Rotate(limit=15, p=0.3),                  # Smartphone ligeramente rotado
            A.ShiftScaleRotate(
                shift_limit=0.1,
                scale_limit=0.15,
                rotate_limit=10,
                p=0.5,
            ),
            
            # Fotométricas (simular condiciones de campo)
            A.RandomBrightnessContrast(
                brightness_limit=0.2,
                contrast_limit=0.2,
                p=0.7,
            ),
            A.HueSaturationValue(
                hue_shift_limit=10,
                sat_shift_limit=20,
                val_shift_limit=20,
                p=0.5,
            ),
            
            # Calidad de imagen
            A.GaussNoise(var_limit=(10, 50), p=0.3),   # Ruido de cámara
            A.Blur(blur_limit=3, p=0.2),               # Desenfoque leve
            
            # Normalización final
            A.Resize(224, 224),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    
    @staticmethod
    def get_validation_transform():
        """Transformaciones para validación (sin augmentation)."""
        return A.Compose([
            A.Resize(224, 224),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
```

---

## Entrenamiento por Raza

```python
# src/training/breed_trainer.py

import mlflow
from tensorflow import keras
from pathlib import Path

from ..models.transfer_learning import BreedWeightEstimatorCNN
from ..data.dataset_builder import BreedDatasetBuilder
from ..evaluation.metrics import MetricsCalculator
from .callbacks import MLflowCallback
from app.core.constants.breeds import BreedType

class BreedModelTrainer:
    """
    Entrenador de modelos específicos por raza.
    
    Un modelo independiente por cada una de las 7 razas de Hacienda Gamelera.
    """
    
    def __init__(self, breed_type: BreedType, data_dir: Path):
        self.breed_type = breed_type
        self.data_dir = data_dir
        self.breed_name = breed_type.value
    
    def train(
        self,
        epochs: int = 50,
        batch_size: int = 32,
        validation_split: float = 0.2,
    ) -> keras.Model:
        """
        Entrena modelo para raza específica.
        
        Args:
            epochs: Número de epochs (típicamente 50-100)
            batch_size: Tamaño de batch (32 o 64)
            validation_split: Porcentaje para validación (0.2 = 20%)
            
        Returns:
            Modelo entrenado con métricas validadas
            
        Steps:
            1. Cargar dataset de la raza (mínimo 100 imágenes)
            2. Aplicar data augmentation
            3. Construir modelo CNN
            4. Entrenar con early stopping y MLflow tracking
            5. Validar métricas (R² ≥0.95, MAE <5kg)
            6. Fine-tuning (descongelar últimas capas)
            7. Exportar a TFLite
        """
        print(f"\n{'='*60}")
        print(f"ENTRENANDO MODELO: {self.breed_name.upper()}")
        print(f"Hacienda Gamelera - {BreedType.get_display_name(self.breed_type)}")
        print(f"{'='*60}\n")
        
        # 1. Cargar dataset
        dataset_builder = BreedDatasetBuilder(
            breed_type=self.breed_type,
            data_dir=self.data_dir,
        )
        train_ds, val_ds, test_ds = dataset_builder.build_datasets(
            batch_size=batch_size,
            validation_split=validation_split,
        )
        
        print(f"Dataset cargado:")
        print(f"  - Training: {len(train_ds)} batches")
        print(f"  - Validation: {len(val_ds)} batches")
        print(f"  - Test: {len(test_ds)} batches\n")
        
        # 2. Construir modelo
        model = BreedWeightEstimatorCNN.build_model(breed_name=self.breed_name)
        
        # 3. Callbacks
        callbacks = [
            MLflowCallback(breed_type=self.breed_name, run_name=f"{self.breed_name}_v1.0.0"),
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
            ),
            keras.callbacks.ModelCheckpoint(
                filepath=f"models/{self.breed_name}/checkpoints/epoch_{{epoch:02d}}.h5",
                save_best_only=True,
                monitor='val_loss',
            ),
        ]
        
        # 4. Entrenar
        print("Iniciando entrenamiento...\n")
        history = model.fit(
            train_ds,
            epochs=epochs,
            validation_data=val_ds,
            callbacks=callbacks,
            verbose=1,
        )
        
        # 5. Evaluar en test set
        print("\nEvaluando en test set...")
        y_true, y_pred = self._evaluate_on_test_set(model, test_ds)
        
        # 6. Calcular métricas finales
        metrics = MetricsCalculator.calculate_metrics(
            y_true=y_true,
            y_pred=y_pred,
            breed_type=self.breed_name,
        )
        MetricsCalculator.print_metrics_report(metrics)
        
        # 7. Guardar métricas
        self._save_metrics(metrics)
        
        return model
    
    def _evaluate_on_test_set(self, model, test_ds):
        """Evalúa modelo en conjunto de test."""
        y_true = []
        y_pred = []
        
        for images, labels in test_ds:
            predictions = model.predict(images, verbose=0)
            y_true.extend(labels.numpy())
            y_pred.extend(predictions.flatten())
        
        return np.array(y_true), np.array(y_pred)
    
    def _save_metrics(self, metrics):
        """Guarda métricas en archivo JSON."""
        import json
        
        metrics_dict = {
            "breed_type": metrics.breed_type,
            "r2_score": float(metrics.r2_score),
            "mae_kg": float(metrics.mae_kg),
            "mape_percent": float(metrics.mape_percent),
            "rmse_kg": float(metrics.rmse_kg),
            "n_samples": metrics.n_samples,
            "meets_requirements": metrics.r2_score >= 0.95 and metrics.mae_kg < 5.0,
            "hacienda": "Hacienda Gamelera",
            "validated_by": "Bruno Brito Macedo",
        }
        
        output_path = f"models/{self.breed_name}/v1.0.0/metrics.json"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(metrics_dict, f, indent=2)
        
        print(f"\n✅ Métricas guardadas en: {output_path}")
```

---

## Exportación a TensorFlow Lite

```python
# src/export/tflite_converter.py

import tensorflow as tf
from pathlib import Path

class TFLiteExporter:
    """
    Exportador de modelos TensorFlow a TFLite optimizado para móviles.
    
    Aplicaciones:
    - App móvil Flutter (inferencia offline)
    - Optimizado para CPU (no requiere GPU)
    - Post-training quantization para reducir tamaño
    """
    
    @staticmethod
    def convert_to_tflite(
        saved_model_path: str,
        output_path: str,
        quantize: bool = True,
    ) -> None:
        """
        Convierte modelo TensorFlow a TFLite optimizado.
        
        Args:
            saved_model_path: Ruta a SavedModel TensorFlow
            output_path: Ruta de salida .tflite
            quantize: Si aplicar quantization (reduce tamaño ~4x)
            
        Example:
            >>> TFLiteExporter.convert_to_tflite(
            ...     saved_model_path="models/brahman/v1.0.0/saved_model",
            ...     output_path="models/brahman/v1.0.0/brahman-v1.0.0.tflite",
            ...     quantize=True,
            ... )
            ✅ Modelo convertido: brahman-v1.0.0.tflite (2.3 MB)
        """
        # Cargar modelo
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
        
        if quantize:
            # Post-training quantization (reduce tamaño ~4x)
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_types = [tf.float16]
        
        # Convertir
        tflite_model = converter.convert()
        
        # Guardar
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        size_mb = len(tflite_model) / (1024 * 1024)
        print(f"✅ Modelo convertido: {Path(output_path).name} ({size_mb:.1f} MB)")
```

---

## Manifest.json (7 Modelos)

```python
# src/export/manifest_generator.py

import json
from pathlib import Path
from datetime import datetime

from app.core.constants.breeds import BreedType

def generate_manifest(models_dir: Path, output_path: Path) -> None:
    """
    Genera manifest.json con información de los 7 modelos TFLite.
    
    El manifest es usado por la app móvil para:
    1. Descargar modelos desde S3
    2. Validar versiones
    3. Cargar modelo correcto por raza
    
    Structure:
    {
      "version": "1.0.0",
      "generated_at": "2024-10-28T10:30:00Z",
      "hacienda": "Hacienda Gamelera",
      "models": [
        {
          "breed_type": "brahman",
          "filename": "brahman-v1.0.0.tflite",
          "version": "v1.0.0",
          "size_mb": 2.3,
          "metrics": {"r2": 0.97, "mae_kg": 3.2},
          "url": "https://s3.../brahman-v1.0.0.tflite"
        },
        ... (7 modelos total)
      ]
    }
    """
    manifest = {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat() + "Z",
        "hacienda": "Hacienda Gamelera",
        "owner": "Bruno Brito Macedo",
        "location": "San Ignacio de Velasco, Bolivia",
        "target_precision": 0.95,
        "max_error_kg": 5.0,
        "models": [],
    }
    
    # Iterar sobre las 7 razas exactas
    for breed in BreedType:
        breed_name = breed.value
        model_path = models_dir / breed_name / "v1.0.0" / f"{breed_name}-v1.0.0.tflite"
        metrics_path = models_dir / breed_name / "v1.0.0" / "metrics.json"
        
        if model_path.exists() and metrics_path.exists():
            # Leer métricas
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            
            # Calcular tamaño
            size_bytes = model_path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            
            # Agregar modelo al manifest
            manifest["models"].append({
                "breed_type": breed_name,
                "breed_display_name": BreedType.get_display_name(breed),
                "filename": f"{breed_name}-v1.0.0.tflite",
                "version": "v1.0.0",
                "size_mb": round(size_mb, 2),
                "metrics": {
                    "r2_score": metrics["r2_score"],
                    "mae_kg": metrics["mae_kg"],
                    "mape_percent": metrics["mape_percent"],
                    "meets_requirements": metrics["meets_requirements"],
                },
                "url": f"https://bovine-ml-models.s3.amazonaws.com/{breed_name}-v1.0.0.tflite",
                "checksum_md5": _calculate_md5(model_path),
            })
    
    # Validar que tenemos los 7 modelos
    assert len(manifest["models"]) == 7, (
        f"Manifest debe tener 7 modelos (uno por raza). "
        f"Encontrados: {len(manifest['models'])}"
    )
    
    # Guardar manifest
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✅ Manifest generado: {output_path}")
    print(f"   Modelos incluidos: {len(manifest['models'])}/7")

def _calculate_md5(file_path: Path) -> str:
    """Calcula checksum MD5 del archivo."""
    import hashlib
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()
```

---

## Validación en Campo

```python
# src/evaluation/field_validation.py

from typing import List, Dict
import pandas as pd
from sklearn.metrics import r2_score

class FieldValidator:
    """
    Validador de modelos con datos reales de Hacienda Gamelera.
    
    Validación obligatoria:
    - Mínimo 50 animales con peso real (báscula) vs peso estimado (IA)
    - Condiciones reales de campo (luz solar, movimiento, distancia)
    - Aprobación de Bruno Brito Macedo
    """
    
    @staticmethod
    def validate_model_in_field(
        validation_data_path: str,
        breed_type: str,
    ) -> Dict[str, float]:
        """
        Valida modelo con datos reales de campo en Hacienda Gamelera.
        
        Args:
            validation_data_path: CSV con columnas:
                - animal_id, tag_number, breed_type, weight_real_kg (báscula),
                  weight_estimated_kg (IA), confidence, date, validated_by
            breed_type: Raza del modelo a validar
            
        Returns:
            Dict con métricas de validación en campo
            
        Raises:
            AssertionError: Si no cumple requisitos mínimos
        """
        # Cargar datos
        df = pd.read_csv(validation_data_path)
        
        # Filtrar por raza
        df_breed = df[df['breed_type'] == breed_type]
        
        # Validar mínimo de muestras
        assert len(df_breed) >= 50, (
            f"Validación requiere ≥50 animales. "
            f"Encontrados: {len(df_breed)} para {breed_type}"
        )
        
        # Calcular métricas
        y_true = df_breed['weight_real_kg'].values
        y_pred = df_breed['weight_estimated_kg'].values
        
        r2 = r2_score(y_true, y_pred)
        mae = np.mean(np.abs(y_true - y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        # Validar que cumple requisitos
        assert r2 >= 0.95, f"R² = {r2:.4f} < 0.95 en campo (Hacienda Gamelera)"
        assert mae < 5.0, f"MAE = {mae:.2f} kg > 5 kg en campo (Hacienda Gamelera)"
        
        results = {
            "breed_type": breed_type,
            "n_animals_validated": len(df_breed),
            "r2_field": r2,
            "mae_field_kg": mae,
            "mape_field_percent": mape,
            "validated_at": datetime.now().isoformat(),
            "validated_by": "Bruno Brito Macedo",
            "hacienda": "Hacienda Gamelera",
            "location": "San Ignacio de Velasco, Bolivia",
            "approved_for_production": r2 >= 0.95 and mae < 5.0,
        }
        
        return results
```

---

## Script de Entrenamiento Completo

```python
# scripts/train_all_breeds.py

"""
Script para entrenar los 7 modelos TFLite (uno por raza).

Uso:
    python scripts/train_all_breeds.py --data-dir data/processed --epochs 50

Salida:
    - 7 modelos TFLite en models/{breed}/v1.0.0/
    - Métricas en models/{breed}/v1.0.0/metrics.json
    - manifest.json con 7 modelos
    - MLflow experiments en experiments/mlruns/
"""

import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.training.breed_trainer import BreedModelTrainer
from src.export.tflite_converter import TFLiteExporter
from src.export.manifest_generator import generate_manifest
from app.core.constants.breeds import BreedType

def main():
    parser = argparse.ArgumentParser(
        description="Entrena los 7 modelos de peso bovino para Hacienda Gamelera"
    )
    parser.add_argument("--data-dir", type=str, required=True, help="Directorio de datos procesados")
    parser.add_argument("--epochs", type=int, default=50, help="Número de epochs (default: 50)")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size (default: 32)")
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir)
    models_dir = Path("models")
    
    print("\n" + "="*80)
    print("ENTRENAMIENTO DE MODELOS - HACIENDA GAMELERA")
    print("Cliente: Bruno Brito Macedo")
    print("Ubicación: San Ignacio de Velasco, Bolivia")
    print("Razas: 7 (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)")
    print("Objetivo: Precisión ≥95% (R² ≥0.95), Error <5 kg")
    print("="*80 + "\n")
    
    trained_models = []
    
    # Entrenar cada una de las 7 razas
    for breed in BreedType:
        print(f"\n{'#'*80}")
        print(f"# RAZA {breed.value.upper()} ({BreedType.get_display_name(breed)})")
        print(f"{'#'*80}\n")
        
        # 1. Entrenar modelo
        trainer = BreedModelTrainer(breed_type=breed, data_dir=data_dir)
        model = trainer.train(epochs=args.epochs, batch_size=args.batch_size)
        
        # 2. Guardar SavedModel
        saved_model_path = models_dir / breed.value / "v1.0.0" / "saved_model"
        model.save(str(saved_model_path))
        print(f"✅ SavedModel guardado: {saved_model_path}")
        
        # 3. Exportar a TFLite
        tflite_path = models_dir / breed.value / "v1.0.0" / f"{breed.value}-v1.0.0.tflite"
        TFLiteExporter.convert_to_tflite(
            saved_model_path=str(saved_model_path),
            output_path=str(tflite_path),
            quantize=True,
        )
        
        trained_models.append(breed.value)
    
    # 4. Generar manifest.json con los 7 modelos
    print(f"\n{'='*80}")
    print("GENERANDO MANIFEST.JSON")
    print(f"{'='*80}\n")
    
    generate_manifest(
        models_dir=models_dir,
        output_path=models_dir / "manifest.json",
    )
    
    print(f"\n{'='*80}")
    print("✅ ENTRENAMIENTO COMPLETO")
    print(f"{'='*80}")
    print(f"Modelos entrenados: {len(trained_models)}/7")
    print(f"Razas: {', '.join(trained_models)}")
    print(f"\nPróximo paso:")
    print(f"1. Validar modelos en campo con Bruno Brito Macedo (≥50 animales)")
    print(f"2. Subir modelos a S3: aws s3 sync models/ s3://bovine-ml-models/")
    print(f"3. Actualizar app móvil con manifest.json")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
```

---

## Requirements.txt ML

```txt
# ml-training/requirements.txt

# TensorFlow
tensorflow==2.13.1
tensorflow-datasets==4.9.3

# MLflow tracking
mlflow==2.8.1

# DVC versionado datos
dvc==3.30.0
dvc-s3==2.23.0

# Preprocesamiento
opencv-python==4.8.1.78
albumentations==1.3.1

# Métricas y análisis
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.24.3

# Visualización
matplotlib==3.8.2
seaborn==0.13.0

# Notebooks
jupyter==1.0.0
jupyterlab==4.0.9
ipywidgets==8.1.1

# Utilidades
Pillow==10.1.0
tqdm==4.66.1

# Testing
pytest==7.4.3
nbval==0.11.0

# Export
pyyaml==6.0.1
```

---

## Referencias

- **Fundamentación teórica**: Weber et al. (2020), Toledo (2025) - Mask R-CNN, YOLOv8
- **Arquitectura**: `docs/standards/architecture-standards.md`
- **Product Backlog**: US-002 (Estimación de Peso por Raza)
- **Métricas sistema**: R² ≥0.95, MAE <5kg, MAPE <5%

---

**Documento de Estándares ML Training v1.0**  
**Fecha**: 28 octubre 2024  
**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Modelos**: 7 TFLite (uno por raza bovina)

