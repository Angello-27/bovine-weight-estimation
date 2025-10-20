"""
Training Script - Modelo Genérico MVP
Script para entrenar modelo básico de estimación de peso

NOTA: Este es un MVP genérico. Los 7 modelos específicos por raza
      se entrenarán en ml-training/ con datasets completos.
"""

import os
import sys
from pathlib import Path

# Agregar backend/app al path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from app.core.constants import SystemMetrics


class GenericWeightEstimatorCNN:
    """
    CNN genérico para estimación de peso (MVP).

    Arquitectura simple para demostración.
    Los modelos finales usarán MobileNetV2 + Transfer Learning.
    """

    @staticmethod
    def build_model() -> keras.Model:
        """
        Construye modelo CNN simple.

        Arquitectura:
        - Input: (224, 224, 3)
        - Conv2D(32) + MaxPool
        - Conv2D(64) + MaxPool
        - Conv2D(128) + MaxPool
        - Flatten + Dense(256) + Dropout(0.3)
        - Dense(128) + Dropout(0.2)
        - Dense(1) - Peso kg

        Returns:
            Modelo Keras compilado
        """
        inputs = keras.Input(shape=(224, 224, 3), name="image_input")

        # Block 1
        x = layers.Conv2D(32, (3, 3), activation="relu", padding="same")(inputs)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.BatchNormalization()(x)

        # Block 2
        x = layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.BatchNormalization()(x)

        # Block 3
        x = layers.Conv2D(128, (3, 3), activation="relu", padding="same")(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.BatchNormalization()(x)

        # Dense layers
        x = layers.Flatten()(x)
        x = layers.Dense(256, activation="relu")(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(128, activation="relu")(x)
        x = layers.Dropout(0.2)(x)

        # Output (peso en kg)
        outputs = layers.Dense(1, activation="linear", name="weight_output")(x)

        model = keras.Model(inputs=inputs, outputs=outputs, name="generic_weight_estimator")

        # Compilar
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss="mse",  # Mean Squared Error
            metrics=["mae", "mape"],  # MAE y MAPE
        )

        return model


def generate_mock_data(num_samples: int = 100):
    """
    Genera datos mock para training MVP.

    En producción, estos serían imágenes reales de bovinos
    con pesos medidos en báscula.

    Args:
        num_samples: Número de muestras a generar

    Returns:
        (X_train, y_train): Imágenes y pesos
    """
    print(f"📊 Generando {num_samples} muestras mock...")

    # Imágenes random (224, 224, 3) normalizadas [0-1]
    X = np.random.rand(num_samples, 224, 224, 3).astype(np.float32)

    # Pesos random entre 300-700 kg (rango típico)
    y = np.random.uniform(300, 700, size=(num_samples, 1)).astype(np.float32)

    return X, y


def export_to_tflite(model: keras.Model, output_path: str):
    """
    Exporta modelo Keras a TensorFlow Lite.

    Args:
        model: Modelo Keras entrenado
        output_path: Path de salida (.tflite)
    """
    print(f"📦 Exportando a TFLite: {output_path}")

    # Convertir a TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    # Optimizaciones
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]  # Quantization

    # Convertir
    tflite_model = converter.convert()

    # Guardar
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(tflite_model)

    size_mb = len(tflite_model) / (1024 * 1024)
    print(f"✅ Modelo exportado: {output_path.name} ({size_mb:.2f} MB)")


def main():
    """
    Script principal de training MVP.

    Genera modelo genérico básico para demostración.
    """
    print("=" * 60)
    print("TRAINING MODELO GENÉRICO MVP")
    print("Sistema de Estimación de Peso Bovino - Hacienda Gamelera")
    print("=" * 60)

    # 1. Construir modelo
    print("\n1️⃣ Construyendo modelo CNN...")
    model = GenericWeightEstimatorCNN.build_model()
    model.summary()

    # 2. Generar datos mock
    print("\n2️⃣ Generando datos de entrenamiento mock...")
    X_train, y_train = generate_mock_data(num_samples=500)
    X_val, y_val = generate_mock_data(num_samples=100)

    print(f"   Train: {X_train.shape}, Val: {X_val.shape}")

    # 3. Entrenar (pocas épocas para MVP)
    print("\n3️⃣ Entrenando modelo...")
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=5,  # Solo 5 épocas para MVP
        batch_size=32,
        verbose=1,
    )

    # 4. Evaluar
    print("\n4️⃣ Evaluando modelo...")
    val_loss, val_mae, val_mape = model.evaluate(X_val, y_val, verbose=0)
    print(f"   Validación Loss: {val_loss:.2f}")
    print(f"   Validación MAE: {val_mae:.2f} kg")
    print(f"   Validación MAPE: {val_mape:.2f}%")

    # Nota: Con datos mock, métricas no son reales
    print(
        "\n⚠️ NOTA: Métricas con datos mock, no representan precisión real"
    )
    print(
        "   Para R²≥0.95 y MAE<5kg reales, entrenar con datasets reales en ml-training/"
    )

    # 5. Guardar modelo Keras
    print("\n5️⃣ Guardando modelo...")
    model_path = Path("backend/ml_models/generic/v1.0.0/saved_model")
    model_path.mkdir(parents=True, exist_ok=True)
    model.save(str(model_path))
    print(f"   Modelo guardado en: {model_path}")

    # 6. Exportar a TFLite
    print("\n6️⃣ Exportando a TFLite...")
    tflite_path = "backend/ml_models/generic-v1.0.0.tflite"
    export_to_tflite(model, tflite_path)

    print("\n" + "=" * 60)
    print("✅ MODELO GENÉRICO MVP COMPLETADO")
    print("=" * 60)
    print(f"\nModelo TFLite: {tflite_path}")
    print("\nPRÓXIMOS PASOS:")
    print("1. Probar endpoint: POST /api/v1/ml/predict")
    print("2. Entrenar modelos específicos por raza en ml-training/")
    print("3. Reemplazar modelo genérico con los 7 modelos reales")
    print("=" * 60)


if __name__ == "__main__":
    main()

