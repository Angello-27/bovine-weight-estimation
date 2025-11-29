"""
ML Service - Business Logic for ML Inference
Lógica de negocio para inferencia ML

Single Responsibility: Coordinar proceso de estimación de peso con IA
"""

from uuid import UUID

from ..core.constants import BreedType
from ..core.exceptions import ValidationException
from ..ml import MLInferenceEngine
from ..models import WeightEstimationModel


class MLService:
    """
    Servicio de inferencia ML para estimación de peso.

    Coordina: validación → preprocesamiento → inferencia → persistencia.
    """

    def __init__(self):
        """Inicializa servicio ML."""
        self.inference_engine = MLInferenceEngine()

    async def predict_weight(
        self,
        image_bytes: bytes,
        breed: BreedType,
        animal_id: UUID | None = None,
        device_id: str | None = None,
    ) -> WeightEstimationModel:
        """
        Predice peso de un bovino desde imagen.

        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)
            breed: Raza del animal (una de las 7)
            animal_id: ID del animal (opcional)
            device_id: ID del dispositivo (opcional)

        Returns:
            WeightEstimationModel guardado en MongoDB

        Raises:
            ValidationException: Si datos son inválidos
            MLModelException: Si hay error en ML
        """
        # 1. Validar imagen no esté vacía
        if not image_bytes or len(image_bytes) == 0:
            raise ValidationException("Imagen vacía o inválida")

        # 2. Validar tamaño de imagen (max 10 MB)
        max_size_bytes = 10 * 1024 * 1024  # 10 MB
        if len(image_bytes) > max_size_bytes:
            raise ValidationException(
                f"Imagen demasiado grande: {len(image_bytes) / 1024 / 1024:.1f} MB "
                f"(máximo: 10 MB)"
            )

        # 3. Ejecutar inferencia
        result = await self.inference_engine.estimate_weight(
            image_bytes=image_bytes, breed=breed
        )

        # 4. Crear modelo de peso
        # Nota: frame_image_path sería path real en producción
        breed_value = breed.value if hasattr(breed, "value") else breed
        weight_estimation = WeightEstimationModel(
            animal_id=str(animal_id) if animal_id else None,
            breed=breed_value,
            estimated_weight_kg=result.estimated_weight_kg,
            confidence=result.confidence,
            method="strategy_based",  # Indicar método basado en estrategias
            model_version=result.model_version,
            processing_time_ms=result.processing_time_ms,
            frame_image_path=f"temp/frame_{animal_id or 'unknown'}.jpg",  # TODO: S3
            device_id=device_id,
        )

        # 5. Guardar en MongoDB
        await weight_estimation.insert()

        return weight_estimation

    async def get_models_status(self) -> dict:
        """
        Obtiene estado de modelos ML cargados.

        Returns:
            Diccionario con info de modelos
        """
        return self.inference_engine.get_loaded_models_info()
