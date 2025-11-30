"""
ML Inference Utils - Core Layer
Utilidades para inferencia ML

Single Responsibility: Funciones auxiliares para procesamiento ML
"""

from datetime import datetime

from ...core.exceptions import ValidationException
from ...domain.entities.weight_estimation import WeightEstimation
from ...domain.shared.constants import BreedType
from ...ml import MLInferenceEngine


async def estimate_weight_from_image(
    image_bytes: bytes,
    breed: BreedType,
    animal_id: str | None = None,
    device_id: str | None = None,
    frame_image_path: str | None = None,
) -> WeightEstimation:
    """
    Estima peso de un bovino desde imagen usando ML.

    Args:
        image_bytes: Bytes de imagen (JPEG/PNG)
        breed: Raza del animal
        animal_id: ID del animal (opcional)
        device_id: ID del dispositivo (opcional)
        frame_image_path: Path donde se guardará la imagen (opcional)

    Returns:
        WeightEstimation (entidad del dominio, no persistida)

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
    engine = MLInferenceEngine()
    result = await engine.estimate_weight(image_bytes=image_bytes, breed=breed)

    # 4. Crear entidad WeightEstimation (sin persistir)
    breed_value = breed.value if hasattr(breed, "value") else breed
    image_path = frame_image_path or f"temp/frame_{animal_id or 'unknown'}.jpg"

    return WeightEstimation(
        animal_id=str(animal_id) if animal_id else None,
        breed=breed_value,
        estimated_weight_kg=result.estimated_weight_kg,
        confidence=result.confidence,
        method="strategy_based",  # Indicar método basado en estrategias
        model_version=result.model_version,
        processing_time_ms=result.processing_time_ms,
        frame_image_path=image_path,
        device_id=device_id,
        timestamp=datetime.utcnow(),
    )


async def get_ml_models_status() -> dict:
    """
    Obtiene estado de modelos ML cargados.

    Returns:
        Diccionario con info de modelos
    """
    engine = MLInferenceEngine()
    return engine.get_loaded_models_info()
