"""
Weighing Service - Business Logic
Lógica de negocio para gestión de pesajes/estimaciones
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..core.errors import NotFoundException, ValidationException
from ..models import WeightEstimationModel
from ..schemas.weighing_schemas import WeighingCreateRequest, WeighingResponse


class WeighingService:
    """
    Servicio de gestión de pesajes.

    Single Responsibility: Business logic de estimaciones de peso.
    """

    async def create_weighing(self, request: WeighingCreateRequest) -> WeighingResponse:
        """
        Crea una nueva estimación de peso.

        Args:
            request: Datos de la estimación

        Returns:
            WeighingResponse con la estimación creada

        Raises:
            ValidationException: Si los datos son inválidos
        """
        # Validar que el animal existe (si se proporciona)
        if request.animal_id:
            from ..models import AnimalModel

            animal = await AnimalModel.get(request.animal_id)
            if animal is None:
                raise NotFoundException(
                    resource="Animal", identifier=str(request.animal_id)
                )

        # Crear modelo
        weighing = WeightEstimationModel(
            animal_id=request.animal_id,
            breed=request.breed,
            estimated_weight_kg=request.estimated_weight_kg,
            confidence=request.confidence,
            method=request.method,
            model_version=request.model_version,
            processing_time_ms=request.processing_time_ms,
            frame_image_path=request.frame_image_path,
            latitude=request.latitude,
            longitude=request.longitude,
            device_id=request.device_id,
        )

        # Guardar en MongoDB
        await weighing.insert()

        # Convertir a response
        return self._to_response(weighing)

    async def get_weighing(self, weighing_id: UUID) -> WeighingResponse:
        """
        Obtiene una estimación por ID.

        Args:
            weighing_id: ID de la estimación

        Returns:
            WeighingResponse

        Raises:
            NotFoundException: Si no existe
        """
        weighing = await WeightEstimationModel.get(weighing_id)

        if weighing is None:
            raise NotFoundException(resource="Weighing", identifier=str(weighing_id))

        return self._to_response(weighing)

    async def get_weighings_by_animal(
        self,
        animal_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[WeighingResponse]:
        """
        Obtiene historial de pesajes de un animal.

        Args:
            animal_id: ID del animal
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de WeighingResponse ordenada por fecha DESC
        """
        weighings = (
            await WeightEstimationModel.find(
                WeightEstimationModel.animal_id == animal_id
            )
            .sort(-WeightEstimationModel.timestamp)
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        return [self._to_response(w) for w in weighings]

    async def get_all_weighings(
        self,
        skip: int = 0,
        limit: int = 50,
    ) -> List[WeighingResponse]:
        """
        Obtiene todos los pesajes (admin).

        Args:
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de WeighingResponse
        """
        weighings = (
            await WeightEstimationModel.find_all()
            .sort(-WeightEstimationModel.timestamp)
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        return [self._to_response(w) for w in weighings]

    def _to_response(self, weighing: WeightEstimationModel) -> WeighingResponse:
        """
        Convierte WeightEstimationModel a WeighingResponse.

        Args:
            weighing: Modelo de MongoDB

        Returns:
            WeighingResponse
        """
        return WeighingResponse(
            id=weighing.id,
            animal_id=weighing.animal_id,
            breed=weighing.breed,
            estimated_weight_kg=weighing.estimated_weight_kg,
            confidence=weighing.confidence,
            confidence_level=weighing.confidence_level,
            method=weighing.method,
            model_version=weighing.model_version,
            processing_time_ms=weighing.processing_time_ms,
            latitude=weighing.latitude,
            longitude=weighing.longitude,
            timestamp=weighing.timestamp,
            created_at=weighing.created_at,
        )

