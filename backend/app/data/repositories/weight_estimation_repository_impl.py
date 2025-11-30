"""
Weight Estimation Repository Implementation - Data Layer
Implementación del repositorio usando Beanie ODM
"""

from uuid import UUID

from ...domain.entities.weight_estimation import WeightEstimation
from ...domain.repositories.weight_estimation_repository import (
    WeightEstimationRepository,
)
from ..models.weight_estimation_model import WeightEstimationModel


class WeightEstimationRepositoryImpl(WeightEstimationRepository):
    """
    Implementación del repositorio de estimaciones usando Beanie.

    Single Responsibility: Persistencia de estimaciones en MongoDB.
    """

    async def find_by_id(self, estimation_id: UUID) -> WeightEstimation | None:
        """Busca una estimación por ID."""
        model = await WeightEstimationModel.get(estimation_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def create(self, estimation: WeightEstimation) -> WeightEstimation:
        """Crea una nueva estimación."""
        model = self._to_model(estimation)
        await model.insert()
        return self._to_entity(model)

    async def update(self, estimation: WeightEstimation) -> WeightEstimation:
        """Actualiza una estimación existente."""
        model = await WeightEstimationModel.get(estimation.id)
        if model is None:
            raise ValueError(f"Estimación {estimation.id} no encontrada")

        # Actualizar campos
        model.animal_id = estimation.animal_id
        model.breed = estimation.breed
        model.estimated_weight_kg = estimation.estimated_weight_kg
        model.confidence = estimation.confidence
        model.method = estimation.method
        model.model_version = estimation.model_version
        model.processing_time_ms = estimation.processing_time_ms
        model.frame_image_path = estimation.frame_image_path
        model.latitude = estimation.latitude
        model.longitude = estimation.longitude
        model.timestamp = estimation.timestamp
        model.device_id = estimation.device_id
        model.synced_at = estimation.synced_at

        await model.save()
        return self._to_entity(model)

    async def count(self) -> int:
        """Retorna el conteo total de estimaciones."""
        return await WeightEstimationModel.count()

    def _to_entity(self, model: WeightEstimationModel) -> WeightEstimation:
        """Convierte Model a Entity."""
        return WeightEstimation(
            id=model.id,
            animal_id=model.animal_id,
            breed=model.breed,
            estimated_weight_kg=model.estimated_weight_kg,
            confidence=model.confidence,
            method=model.method,
            model_version=model.model_version,
            processing_time_ms=model.processing_time_ms,
            frame_image_path=model.frame_image_path,
            latitude=model.latitude,
            longitude=model.longitude,
            timestamp=model.timestamp,
            device_id=model.device_id,
            synced_at=model.synced_at,
        )

    def _to_model(self, entity: WeightEstimation) -> WeightEstimationModel:
        """Convierte Entity a Model."""
        return WeightEstimationModel(
            id=entity.id,
            animal_id=entity.animal_id,
            breed=entity.breed,
            estimated_weight_kg=entity.estimated_weight_kg,
            confidence=entity.confidence,
            method=entity.method,
            model_version=entity.model_version,
            processing_time_ms=entity.processing_time_ms,
            frame_image_path=entity.frame_image_path,
            latitude=entity.latitude,
            longitude=entity.longitude,
            timestamp=entity.timestamp,
            device_id=entity.device_id,
            synced_at=entity.synced_at,
        )
