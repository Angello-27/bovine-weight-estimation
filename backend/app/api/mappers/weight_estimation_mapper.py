"""
Weight Estimation Mapper - DTO ↔ Entity Conversion
Convierte entre Weight Estimation DTOs y Entities
"""

from uuid import UUID

from ...domain.entities.weight_estimation import WeightEstimation
from ...domain.shared.constants import BreedType
from ...schemas.weighing_schemas import (
    WeighingCreateRequest,
    WeighingResponse,
)


class WeightEstimationMapper:
    """
    Mapper para convertir entre Weight Estimation DTOs y Entities.

    Single Responsibility: Conversión entre capas Presentation y Domain.
    """

    @staticmethod
    def to_response(estimation: WeightEstimation) -> WeighingResponse:
        """
        Convierte WeightEstimation Entity a WeighingResponse DTO.

        Args:
            estimation: Entidad WeightEstimation del dominio

        Returns:
            WeighingResponse DTO
        """
        # Convertir breed string a BreedType enum si es necesario
        breed_value = estimation.breed
        if isinstance(breed_value, str):
            try:
                breed = BreedType(breed_value)
            except ValueError:
                breed = BreedType.NELORE  # Default si no se reconoce
        else:
            breed = breed_value

        return WeighingResponse(
            id=estimation.id,
            animal_id=UUID(estimation.animal_id) if estimation.animal_id else None,
            breed=breed,
            estimated_weight_kg=estimation.estimated_weight_kg,
            confidence=estimation.confidence,
            confidence_level=estimation.get_confidence_level(),
            method=estimation.method,
            ml_model_version=estimation.ml_model_version,
            processing_time_ms=estimation.processing_time_ms,
            latitude=estimation.latitude,
            longitude=estimation.longitude,
            timestamp=estimation.timestamp,
            created_at=estimation.timestamp,  # Usar timestamp como created_at
        )

    @staticmethod
    def create_request_to_params(
        request: WeighingCreateRequest,
    ) -> dict:
        """
        Convierte WeighingCreateRequest a parámetros para caso de uso.

        Args:
            request: Request DTO

        Returns:
            Diccionario con parámetros para CreateWeightEstimationUseCase.execute()
        """
        return {
            "animal_id": str(request.animal_id) if request.animal_id else None,
            "breed": (
                request.breed.value
                if hasattr(request.breed, "value")
                else request.breed
            ),
            "estimated_weight_kg": request.estimated_weight_kg,
            "confidence": request.confidence,
            "method": request.method,
            "ml_model_version": request.ml_model_version,
            "processing_time_ms": request.processing_time_ms,
            "frame_image_path": request.frame_image_path,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "device_id": request.device_id,
        }
