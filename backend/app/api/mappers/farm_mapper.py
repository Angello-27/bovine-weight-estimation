"""
Farm Mapper - DTO ↔ Entity Conversion
Convierte entre Farm DTOs y Farm Entities
"""

from uuid import UUID

from ...domain.entities.farm import Farm
from ...schemas.farm_schemas import (
    FarmCreateRequest,
    FarmResponse,
    FarmUpdateRequest,
)


class FarmMapper:
    """
    Mapper para convertir entre Farm DTOs y Entities.

    Single Responsibility: Conversión entre capas Presentation y Domain.
    """

    @staticmethod
    def to_response(farm: Farm) -> FarmResponse:
        """
        Convierte Farm Entity a FarmResponse DTO.

        Args:
            farm: Entidad Farm del dominio

        Returns:
            FarmResponse DTO
        """
        if farm.owner_id is None:
            raise ValueError("Farm must have an owner_id")
        owner_id: UUID = farm.owner_id  # Type assertion after None check
        return FarmResponse(
            id=farm.id,
            name=farm.name,
            owner_id=owner_id,
            latitude=farm.latitude,
            longitude=farm.longitude,
            capacity=farm.capacity,
            total_animals=farm.total_animals,
            created_at=farm.created_at,
            last_updated=farm.last_updated,
        )

    @staticmethod
    def create_request_to_params(request: FarmCreateRequest) -> dict:
        """
        Convierte FarmCreateRequest a parámetros para CreateFarmUseCase.

        Args:
            request: FarmCreateRequest DTO

        Returns:
            Dict con parámetros para use case
        """
        return {
            "name": request.name,
            "owner_id": request.owner_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "capacity": request.capacity,
        }

    @staticmethod
    def update_request_to_params(request: FarmUpdateRequest) -> dict:
        """
        Convierte FarmUpdateRequest a parámetros para UpdateFarmUseCase.

        Args:
            request: FarmUpdateRequest DTO

        Returns:
            Dict con parámetros para use case
        """
        params: dict = {}
        if request.name is not None:
            params["name"] = request.name
        if request.latitude is not None:
            params["latitude"] = request.latitude
        if request.longitude is not None:
            params["longitude"] = request.longitude
        if request.capacity is not None:
            params["capacity"] = request.capacity
        return params
