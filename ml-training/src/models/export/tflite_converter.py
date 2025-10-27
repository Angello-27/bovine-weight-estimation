"""
Conversor de modelos TensorFlow a TensorFlow Lite.
Optimizado para móvil con quantización.
"""

from pathlib import Path
from typing import Optional, Callable, Tuple
import tensorflow as tf
import numpy as np


class TFLiteExporter:
    """
    Exporta modelos TensorFlow a TFLite con optimizaciones.
    """
    
    @staticmethod
    def convert_to_tflite(
        saved_model_path: str,
        output_path: str,
        optimization: str = 'default',
        representative_dataset: Optional[Callable] = None
    ) -> int:
        """
        Convierte modelo TensorFlow a TFLite.
        
        Args:
            saved_model_path: Ruta al modelo guardado
            output_path: Ruta de salida para .tflite
            optimization: 'none', 'default', 'int8'
            representative_dataset: Dataset representativo para INT8
        
        Returns:
            int: Tamaño del modelo en bytes
        """
        print(f"📱 Convirtiendo a TFLite: {Path(saved_model_path).name}")
        
        # Cargar modelo
        model = tf.keras.models.load_model(saved_model_path)
        
        # Crear conversor
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        
        # Aplicar optimizaciones según método
        if optimization == 'none':
            # Sin optimizaciones (modelo float32 completo)
            pass
            
        elif optimization == 'default':
            # FP16: Reduce 2x el tamaño, mantiene precisión
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_types = [tf.float16]
            
        elif optimization == 'int8':
            # INT8: Reduce 4x el tamaño, puede perder precisión
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            
            if representative_dataset is not None:
                converter.representative_dataset = representative_dataset
                converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
                converter.inference_input_type = tf.uint8
                converter.inference_output_type = tf.float32
            else:
                print("⚠️ Dataset representativo requerido para INT8. Usando FP16")
                converter.target_spec.supported_types = [tf.float16]
        
        # Convertir
        try:
            tflite_model = converter.convert()
        except Exception as e:
            print(f"❌ Error en conversión: {e}")
            raise
        
        # Guardar modelo
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        # Información del modelo
        model_size_kb = len(tflite_model) / 1024
        model_size_mb = model_size_kb / 1024
        
        print(f"✅ Modelo exportado: {output_path_obj.name}")
        print(f"📏 Tamaño: {model_size_kb:.1f} KB ({model_size_mb:.2f} MB)")
        print(f"🎯 Optimización: {optimization}")
        
        return len(tflite_model)
    
    @staticmethod
    def create_representative_dataset(
        generator_fn: Callable,
        n_samples: int = 100
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
        tflite_path: str,
        test_image: np.ndarray
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
        interpreter.set_tensor(input_details[0]['index'], test_image.astype(input_details[0]['dtype']))
        
        # Inferencia
        start = time.time()
        interpreter.invoke()
        inference_time = (time.time() - start) * 1000  # ms
        
        # Obtener predicción
        prediction = interpreter.get_tensor(output_details[0]['index'])[0][0]
        
        print(f"⏱️ Inferencia TFLite: {inference_time:.2f} ms")
        print(f"📊 Predicción: {prediction:.2f} kg")
        
        return inference_time, prediction


def save_model_metadata(
    output_dir: Path,
    model_name: str,
    metrics: dict,
    breed_type: str,
    version: str = "v1.0.0"
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
        'model_name': model_name,
        'breed_type': breed_type,
        'version': version,
        'metrics': metrics,
        'requirements': {
            'target_r2': 0.95,
            'max_mae_kg': 5.0,
            'max_inference_time_sec': 3.0,
        }
    }
    
    metadata_path = output_dir / 'metrics.json'
    with open(metadata_path, 'w') as f:
        import json
        json.dump(metadata, f, indent=2)
    
    print(f"💾 Metadata guardado: {metadata_path}")
    
    return metadata

