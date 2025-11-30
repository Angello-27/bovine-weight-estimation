"""
ML Inference Engine
Motor de inferencia para estimación de peso bovino

Single Responsibility: Ejecutar inferencia con modelos ML usando Strategy Pattern
"""

import time

import numpy as np

from app.core.exceptions import MLModelException, ValidationException
from app.domain.shared.constants import BreedType, SystemMetrics

from .model_loader import MLModelLoader
from .preprocessing import ImagePreprocessor
from .strategy_context import WeightEstimationContext


class MLInferenceResult:
    """Resultado de inferencia ML."""

    def __init__(
        self,
        estimated_weight_kg: float,
        confidence: float,
        processing_time_ms: int,
        ml_model_version: str,
        breed: BreedType,
    ):
        self.estimated_weight_kg = estimated_weight_kg
        self.confidence = confidence
        self.processing_time_ms = processing_time_ms
        self.ml_model_version = ml_model_version
        self.breed = breed

    def to_dict(self) -> dict:
        """Convierte a diccionario."""
        return {
            "estimated_weight_kg": self.estimated_weight_kg,
            "confidence": self.confidence,
            "processing_time_ms": self.processing_time_ms,
            "ml_model_version": self.ml_model_version,
            "breed": self.breed.value,
            "meets_quality_criteria": self.confidence >= SystemMetrics.MIN_CONFIDENCE
            and self.processing_time_ms < SystemMetrics.MAX_PROCESSING_TIME_MS,
        }


class MLInferenceEngine:
    """
    Motor de inferencia ML para estimación de peso bovino.

    Coordina: carga modelo → preprocesamiento → inferencia → validación.
    """

    def __init__(self):
        """Inicializa engine."""
        self.model_loader = MLModelLoader()
        self.preprocessor = ImagePreprocessor()
        self.strategy_context = WeightEstimationContext()

    async def estimate_weight(
        self, image_bytes: bytes, breed: BreedType
    ) -> MLInferenceResult:
        """
        Estima peso de un bovino desde imagen.

        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)
            breed: Raza del animal (una de las 7)

        Returns:
            MLInferenceResult con peso, confidence, tiempo

        Raises:
            MLModelException: Si hay error en inferencia
            ValidationException: Si imagen es inválida
        """
        start_time = time.time()

        try:
            # 1. Validar raza
            breed_value = breed.value if hasattr(breed, "value") else breed
            if not BreedType.is_valid(breed_value):
                raise ValidationException(
                    f"Raza inválida: {breed_value}. "
                    f"Razas válidas: {[b.value for b in BreedType]}"
                )

            # 2. Usar contexto de estrategias para estimación
            # Esto reemplaza el sistema híbrido anterior con Strategy Pattern
            strategy_result = self.strategy_context.estimate_weight(
                image_bytes, breed_value
            )

            estimated_weight = strategy_result["weight"]
            confidence = strategy_result["confidence"]
            selected_strategy = strategy_result.get("selected_strategy", "unknown")

            # 3. Calcular tiempo de procesamiento
            processing_time_ms = int((time.time() - start_time) * 1000)

            # 4. Validar que cumpla métricas del sistema
            if processing_time_ms > SystemMetrics.MAX_PROCESSING_TIME_MS:
                print(
                    f"⚠️ ADVERTENCIA: Procesamiento {processing_time_ms}ms > 3000ms objetivo"
                )

            if confidence < SystemMetrics.MIN_CONFIDENCE:
                print(f"⚠️ ADVERTENCIA: Confidence {confidence:.2%} < 80% mínimo")

            # 5. Crear resultado
            return MLInferenceResult(
                estimated_weight_kg=estimated_weight,
                confidence=confidence,
                processing_time_ms=processing_time_ms,
                ml_model_version=f"1.0.0-{selected_strategy}",  # Indicar estrategia usada
                breed=breed,
            )

        except ValidationException:
            raise
        except MLModelException:
            raise
        except Exception as e:
            raise MLModelException(
                f"Error inesperado en inferencia para {breed_value}: {str(e)}"
            )

    def _mock_inference(
        self, breed: BreedType, image: np.ndarray
    ) -> tuple[float, float]:
        """
        Inferencia mock (MVP - reemplazar con modelo real).

        Genera estimación basada en rangos típicos por raza.
        Simula variabilidad realista.

        Args:
            breed: Raza del animal
            image: Imagen preprocesada (no se usa en mock)

        Returns:
            (peso_estimado_kg, confidence)
        """
        # Rangos típicos por raza (alineados con entrenamiento ML)
        breed_weight_ranges = {
            BreedType.NELORE: (250, 650),
            BreedType.BRAHMAN: (260, 680),
            BreedType.GUZERAT: (240, 650),
            BreedType.SENEPOL: (280, 620),
            BreedType.GIROLANDO: (240, 640),
            BreedType.GYR_LECHERO: (220, 620),
            BreedType.SINDI: (150, 380),
        }

        # Obtener rango de la raza
        weight_min, weight_max = breed_weight_ranges.get(
            breed,
            (400, 600),  # Default si no está en map
        )

        # Generar peso pseudo-aleatorio en el rango
        # Usar suma de píxeles de la imagen como "seed" para variabilidad
        pixel_sum = float(np.sum(image))
        normalized_seed = (pixel_sum % 1000) / 1000  # Normalizar a [0-1]

        estimated_weight = weight_min + (weight_max - weight_min) * normalized_seed

        # Confidence mock (alto para simular modelo bueno)
        # Variar ligeramente basado en la "calidad" de la imagen
        base_confidence = 0.93
        confidence_variation = normalized_seed * 0.05  # ±2.5%
        confidence = min(0.98, base_confidence + confidence_variation)

        return round(estimated_weight, 1), round(confidence, 4)

    def get_loaded_models_info(self) -> dict:
        """
        Obtiene información de modelos cargados.

        Returns:
            Diccionario con info de modelos y estrategias
        """
        loaded_breeds = self.model_loader.get_loaded_breeds()
        strategy_info = self.strategy_context.get_strategy_info()

        return {
            "total_loaded": len(loaded_breeds),
            "breeds_loaded": [breed.value for breed in loaded_breeds],
            "all_breeds": [breed.value for breed in BreedType],
            "missing_breeds": [
                breed.value for breed in BreedType if breed not in loaded_breeds
            ],
            "strategies": strategy_info,
            "available_strategies": self.strategy_context.get_available_strategies(),
        }
