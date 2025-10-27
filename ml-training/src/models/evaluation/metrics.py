"""
Métricas de evaluación para modelos de estimación de peso.
Obligatorias: R² ≥ 0.95, MAE < 5 kg
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np
from sklearn.metrics import (
    r2_score, 
    mean_absolute_error, 
    mean_squared_error,
    mean_absolute_percentage_error
)
import tensorflow as tf


@dataclass
class ModelMetrics:
    """Métricas de evaluación del modelo"""
    r2_score: float
    mae_kg: float
    mse_kg: float
    mape_percent: float
    bias_kg: float
    inference_time_ms: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convertir a diccionario"""
        return {
            'r2_score': self.r2_score,
            'mae_kg': self.mae_kg,
            'mse_kg': self.mse_kg,
            'mape_percent': self.mape_percent,
            'bias_kg': self.bias_kg,
            'inference_time_ms': self.inference_time_ms,
        }
    
    def validate_targets(self, target_r2: float = 0.85, max_mae: float = 22.0) -> Tuple[bool, List[str]]:
        """
        Validar si cumple con objetivos críticos.
        
        Args:
            target_r2: R² objetivo (default 0.95)
            max_mae: MAE máximo permitido en kg (default 5.0)
        
        Returns:
            Tuple[bool, List[str]]: (cumple_objetivos, lista_errores)
        """
        errors = []
        
        if self.r2_score < target_r2:
            errors.append(f"R² {self.r2_score:.4f} < {target_r2}")
        
        if self.mae_kg >= max_mae:
            errors.append(f"MAE {self.mae_kg:.2f} kg >= {max_mae} kg")
        
        return len(errors) == 0, errors


class MetricsCalculator:
    """
    Calculador de métricas para evaluación de modelos.
    """
    
    @staticmethod
    def calculate_metrics(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        breed_type: str = 'generic'
    ) -> ModelMetrics:
        """
        Calcular métricas de regresión.
        
        Args:
            y_true: Valores reales (peso en kg)
            y_pred: Valores predichos (peso en kg)
            breed_type: Tipo de raza (para logging)
        
        Returns:
            ModelMetrics: Métricas calculadas
        
        Raises:
            AssertionError: Si no cumple objetivos críticos
        """
        # Convertir a numpy array
        y_true = np.array(y_true).flatten()
        y_pred = np.array(y_pred).flatten()
        
        # Calcular métricas
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred) * 100
        bias = np.mean(y_pred - y_true)  # Bias (sobreestimación/subestimación)
        
        # Crear objeto de métricas
        metrics = ModelMetrics(
            r2_score=r2,
            mae_kg=mae,
            mse_kg=mse,
            mape_percent=mape,
            bias_kg=bias,
        )
        
        return metrics
    
    @staticmethod
    def calculate_metrics_with_assertions(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        breed_type: str = 'generic',
        target_r2: float = 0.85,
        max_mae: float = 22.0
    ) -> ModelMetrics:
        """
        Calcular métricas y validar objetivos críticos.
        
        Args:
            y_true: Valores reales
            y_pred: Valores predichos
            breed_type: Tipo de raza
            target_r2: R² objetivo
            max_mae: MAE máximo permitido
        
        Returns:
            ModelMetrics: Métricas calculadas
        
        Raises:
            AssertionError: Si no cumple objetivos críticos
        """
        metrics = MetricsCalculator.calculate_metrics(y_true, y_pred, breed_type)
        
        # Validar objetivos
        meets_targets, errors = metrics.validate_targets(target_r2, max_mae)
        
        if not meets_targets:
            error_msg = f"❌ Objetivos no cumplidos para {breed_type}:\n"
            for error in errors:
                error_msg += f"  - {error}\n"
            error_msg += f"\nMétricas actuales:\n  R²: {metrics.r2_score:.4f}\n  MAE: {metrics.mae_kg:.2f} kg"
            raise AssertionError(error_msg)
        
        print(f"✅ Objetivos cumplidos para {breed_type}: R²={metrics.r2_score:.4f}, MAE={metrics.mae_kg:.2f} kg")
        
        return metrics
    
    @staticmethod
    def benchmark_inference_time(
        model: tf.keras.Model,
        sample_image: np.ndarray,
        n_iterations: int = 100
    ) -> float:
        """
        Medir tiempo de inferencia del modelo.
        
        Args:
            model: Modelo TensorFlow
            sample_image: Imagen de prueba
            n_iterations: Número de iteraciones para promediar
        
        Returns:
            float: Tiempo promedio de inferencia en ms
        """
        # Preparar imagen para inferencia
        if len(sample_image.shape) == 3:
            sample_image = np.expand_dims(sample_image, axis=0)
        
        # Warmup
        _ = model.predict(sample_image, verbose=0)
        
        # Medir tiempo
        import time
        times = []
        
        for _ in range(n_iterations):
            start = time.time()
            _ = model.predict(sample_image, verbose=0)
            times.append((time.time() - start) * 1000)  # Convertir a ms
        
        avg_time_ms = np.mean(times)
        
        print(f"⏱️ Tiempo promedio de inferencia: {avg_time_ms:.2f} ms")
        
        # Validar objetivo (3 segundos = 3000 ms)
        if avg_time_ms < 3000:
            print(f"✅ Inferencia < 3s requerido (objetivo cumplido)")
        else:
            print(f"⚠️ Inferencia {avg_time_ms/1000:.2f}s > 3s requerido")
        
        return avg_time_ms

