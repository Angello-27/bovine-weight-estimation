"""
Conversor de modelos TensorFlow a TensorFlow Lite.
Optimizado para móvil con quantización.
"""

import contextlib
import os
import sys
from pathlib import Path
from typing import Callable, Optional, Tuple

import numpy as np
import tensorflow as tf  # type: ignore


@contextlib.contextmanager
def suppress_tf_messages():
    """
    Suprime mensajes verbosos de TensorFlow/TFLite durante la conversión.
    Oculta mensajes de stderr y ajusta el nivel de logging de TensorFlow.
    """
    # Guardar estado original
    old_stderr = sys.stderr
    old_verbosity = None

    try:
        # Reducir verbosidad de TensorFlow
        try:
            old_verbosity = tf.get_logger().level
            tf.get_logger().setLevel("ERROR")
        except Exception:
            pass

        # Suprimir stderr
        with open(os.devnull, "w", encoding="utf-8") as devnull:
            sys.stderr = devnull
            yield
    finally:
        # Restaurar estado original
        sys.stderr = old_stderr
        if old_verbosity is not None:
            try:
                tf.get_logger().setLevel(old_verbosity)
            except Exception:
                pass


class TFLiteExporter:
    """
    Exporta modelos TensorFlow a TFLite con optimizaciones.
    """

    @staticmethod
    def convert_to_tflite(
        saved_model_path: Optional[str] = None,
        output_path: Optional[str] = None,
        optimization: str = "default",
        representative_dataset: Optional[Callable] = None,
        model: Optional[tf.keras.Model] = None,
    ) -> int:
        """
        Convierte modelo TensorFlow a TFLite.

        Args:
            saved_model_path: Ruta al modelo guardado (opcional si se proporciona model)
            output_path: Ruta de salida para .tflite
            optimization: 'none', 'default', 'int8'
            representative_dataset: Dataset representativo para INT8
            model: Modelo Keras en memoria (opcional, evita guardar/recargar)

        Returns:
            int: Tamaño del modelo en bytes
        """
        # Determinar si usar modelo en memoria o cargar desde archivo
        use_saved_model = False
        saved_model_path_str = None

        if saved_model_path:
            # Si se proporciona saved_model_path, verificar si es un SavedModel
            saved_model_path_obj = Path(saved_model_path)

            # Un SavedModel es un directorio (no un archivo .keras, .h5, etc.)
            # Si es un directorio, asumimos que es un SavedModel
            if saved_model_path_obj.exists() and saved_model_path_obj.is_dir():
                # Es un directorio SavedModel, usar from_saved_model (más robusto)
                use_saved_model = True
                saved_model_path_str = str(saved_model_path)
            else:
                # Es un archivo (probablemente .keras o .h5), intentar cargar como modelo Keras
                try:
                    keras_model = tf.keras.models.load_model(saved_model_path)
                except Exception:
                    try:
                        keras_model = tf.keras.models.load_model(
                            saved_model_path,
                            custom_objects={"mse": tf.keras.losses.MeanSquaredError()},
                        )
                    except Exception as e2:
                        print(f"❌ Error cargando modelo: {e2}")
                        raise
        elif model is not None:
            keras_model = model
        else:
            raise ValueError("Debe proporcionar 'model' o 'saved_model_path'")

        # Crear conversor según el tipo de entrada
        if use_saved_model:
            # Usar from_saved_model que es más robusto para SavedModel
            converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path_str)
        else:
            # Usar from_keras_model para modelos Keras
            converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)

        # Aplicar optimizaciones según método
        if optimization == "none":
            # Sin optimizaciones (modelo float32 completo)
            pass

        elif optimization == "default":
            # FP16: Reduce 2x el tamaño, mantiene precisión
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_types = [tf.float16]

        elif optimization == "int8":
            # INT8: Reduce 4x el tamaño, puede perder precisión
            converter.optimizations = [tf.lite.Optimize.DEFAULT]

            if representative_dataset is not None:
                converter.representative_dataset = representative_dataset
                converter.target_spec.supported_ops = [
                    tf.lite.OpsSet.TFLITE_BUILTINS_INT8
                ]
                converter.inference_input_type = tf.uint8
                converter.inference_output_type = tf.float32
            else:
                converter.target_spec.supported_types = [tf.float16]

        # Convertir con reintentos si falla por operaciones no soportadas
        tflite_model = None
        conversion_error = None

        try:
            # Suprimir mensajes verbosos durante la conversión (mensajes "unknown")
            with suppress_tf_messages():
                tflite_model = converter.convert()
        except Exception as e:
            conversion_error = str(e)
            error_lower = conversion_error.lower()

            # Si el error es por operaciones no soportadas (flex ops), intentar con flex ops
            if (
                "needs_flex_ops" in error_lower
                or "custom op" in error_lower
                or "flex op" in error_lower
                or "error_needs_flex_ops" in error_lower
            ):
                print(
                    "⚠️ Algunas operaciones requieren flex ops. Reintentando con soporte flex..."
                )

                # Reintentar con flex ops habilitadas
                if use_saved_model:
                    converter = tf.lite.TFLiteConverter.from_saved_model(
                        saved_model_path_str
                    )
                else:
                    converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)

                # Aplicar optimizaciones nuevamente
                if optimization == "default":
                    converter.optimizations = [tf.lite.Optimize.DEFAULT]
                    converter.target_spec.supported_types = [tf.float16]

                # Habilitar flex ops (permite usar operaciones de TensorFlow no nativas en TFLite)
                converter.target_spec.supported_ops = [
                    tf.lite.OpsSet.TFLITE_BUILTINS,
                    tf.lite.OpsSet.SELECT_TF_OPS,  # Habilita flex ops
                ]

                try:
                    # Suprimir mensajes verbosos durante la conversión
                    with suppress_tf_messages():
                        tflite_model = converter.convert()
                    print("✅ Conversión exitosa con flex ops habilitadas")
                except Exception as e2:
                    # Mostrar solo el error final, no todos los mensajes "unknown"
                    error_msg = str(e2).split("\n")[0] if "\n" in str(e2) else str(e2)
                    print(f"❌ Error en conversión: {error_msg}")
                    raise RuntimeError(
                        "Error en conversión a TFLite incluso con flex ops habilitadas."
                    )
            else:
                # Otro tipo de error, mostrar solo el mensaje principal
                error_msg = str(e).split("\n")[0] if "\n" in str(e) else str(e)
                print(f"❌ Error en conversión: {error_msg}")
                raise

        # Guardar modelo
        if output_path is None:
            raise ValueError("output_path es requerido")

        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(tflite_model)

        # Información del modelo
        model_size_kb = len(tflite_model) / 1024
        model_size_mb = model_size_kb / 1024

        print(f"✅ Modelo exportado: {output_path_obj.name} ({model_size_mb:.2f} MB)")

        return len(tflite_model)

    @staticmethod
    def create_representative_dataset(
        generator_fn: Callable, n_samples: int = 100
    ) -> Callable:
        """
        Crea dataset representativo para quantización INT8.

        Args:
            generator_fn: Función que genera batches de datos
            n_samples: Número de muestras representativas

        Returns:
            Callable: Dataset representativo para conversor
        """

        def representative_dataset():
            count = 0
            for data in generator_fn():
                if count >= n_samples:
                    break
                # TFLite espera batches de 1 elemento
                for sample in data:
                    yield [np.expand_dims(sample, axis=0).astype(np.float32)]
                    count += 1
                    if count >= n_samples:
                        break

        return representative_dataset

    @staticmethod
    def test_tflite_model(
        tflite_path: str, test_image: np.ndarray
    ) -> Tuple[float, np.ndarray]:
        """
        Probar modelo TFLite cargado.

        Args:
            tflite_path: Ruta al modelo .tflite
            test_image: Imagen de prueba

        Returns:
            Tuple[float, np.ndarray]: (tiempo_inferencia_ms, predicción)
        """
        import time

        # Cargar modelo TFLite
        interpreter = tf.lite.Interpreter(model_path=tflite_path)
        interpreter.allocate_tensors()

        # Obtener tensores de entrada y salida
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Preparar imagen
        if len(test_image.shape) == 3:
            test_image = np.expand_dims(test_image, axis=0)

        # Configurar tensor de entrada
        interpreter.set_tensor(
            input_details[0]["index"], test_image.astype(input_details[0]["dtype"])
        )

        # Inferencia
        start = time.time()
        interpreter.invoke()
        inference_time = (time.time() - start) * 1000  # ms

        # Obtener predicción
        prediction = interpreter.get_tensor(output_details[0]["index"])[0][0]

        return inference_time, prediction


def save_model_metadata(
    output_dir: Path,
    model_name: str,
    metrics: dict,
    breed_type: str,
    version: str = "v1.0.0",
) -> dict:
    """
    Guardar metadata del modelo (metrics.json).

    Args:
        output_dir: Directorio de salida
        model_name: Nombre del modelo
        metrics: Diccionario de métricas
        breed_type: Tipo de raza
        version: Versión del modelo

    Returns:
        dict: Metadata guardado
    """
    metadata = {
        "model_name": model_name,
        "breed_type": breed_type,
        "version": version,
        "metrics": metrics,
        "requirements": {
            "target_r2": 0.95,
            "max_mae_kg": 5.0,
            "max_inference_time_sec": 3.0,
        },
    }

    metadata_path = output_dir / "metrics.json"
    with open(metadata_path, "w") as f:
        import json

        json.dump(metadata, f, indent=2)

    return metadata
