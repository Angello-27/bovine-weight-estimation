"""
Animal Mapper - DTO ↔ Entity Conversion
Convierte entre Animal DTOs y Animal Entities
"""

from ...domain.entities.animal import Animal
from ...domain.shared.constants import BreedType
from ...schemas.animal_schemas import (
    AnimalCreateRequest,
    AnimalResponse,
    AnimalUpdateRequest,
)


class AnimalMapper:
    """
    Mapper para convertir entre Animal DTOs y Entities.

    Single Responsibility: Conversión entre capas Presentation y Domain.
    """

    @staticmethod
    def to_response(animal: Animal) -> AnimalResponse:
        """
        Convierte Animal Entity a AnimalResponse DTO.

        Args:
            animal: Entidad Animal del dominio

        Returns:
            AnimalResponse DTO con campos calculados

        Raises:
            ValueError: Si farm_id es None
        """
        if animal.farm_id is None:
            raise ValueError("Animal must have a farm_id")

        from uuid import UUID as UUIDType

        return AnimalResponse(
            id=animal.id,
            ear_tag=animal.ear_tag,
            breed=(
                BreedType(animal.breed)
                if isinstance(animal.breed, str)
                else animal.breed
            ),
            birth_date=animal.birth_date,
            gender=animal.gender,
            name=animal.name,
            color=animal.color,
            birth_weight_kg=animal.birth_weight_kg,
            mother_id=UUIDType(animal.mother_id) if animal.mother_id else None,
            father_id=UUIDType(animal.father_id) if animal.father_id else None,
            status=animal.status,
            farm_id=animal.farm_id,
            registration_date=animal.registration_date,
            last_updated=animal.last_updated,
            age_months=animal.calculate_age_months(),
            age_category=animal.calculate_age_category().value,
        )

    @staticmethod
    def create_request_to_params(request: AnimalCreateRequest) -> dict:
        """
        Convierte AnimalCreateRequest a parámetros para CreateAnimalUseCase.

        Args:
            request: AnimalCreateRequest DTO

        Returns:
            Dict con parámetros para use case
        """
        return {
            "ear_tag": request.ear_tag,
            "breed": (
                request.breed.value
                if hasattr(request.breed, "value")
                else str(request.breed)
            ),
            "birth_date": request.birth_date,
            "gender": request.gender,
            "farm_id": request.farm_id,
            "name": request.name,
            "color": request.color,
            "birth_weight_kg": request.birth_weight_kg,
            "mother_id": str(request.mother_id) if request.mother_id else None,
            "father_id": str(request.father_id) if request.father_id else None,
            "observations": request.observations,
            "photo_url": request.photo_url,
        }

    @staticmethod
    def update_request_to_params(request: AnimalUpdateRequest) -> dict:
        """
        Convierte AnimalUpdateRequest a parámetros para UpdateAnimalUseCase.

        Args:
            request: AnimalUpdateRequest DTO

        Returns:
            Dict con parámetros para use case
        """
        params: dict = {}
        if request.name is not None:
            params["name"] = request.name
        if request.color is not None:
            params["color"] = request.color
        if request.observations is not None:
            params["observations"] = request.observations
        if request.status is not None:
            params["status"] = request.status
        if request.mother_id is not None:
            params["mother_id"] = request.mother_id
        if request.father_id is not None:
            params["father_id"] = request.father_id
        if request.photo_url is not None:
            params["photo_url"] = request.photo_url
        return params
