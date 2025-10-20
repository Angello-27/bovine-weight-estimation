"""
Animal Service - Business Logic
Lógica de negocio para gestión de animales
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..core.errors import AlreadyExistsException, NotFoundException, ValidationException
from ..models import AnimalModel
from ..schemas.animal_schemas import (
    AnimalCreateRequest,
    AnimalResponse,
    AnimalUpdateRequest,
)


class AnimalService:
    """
    Servicio de gestión de animales.

    Single Responsibility: Business logic de animales.
    No contiene lógica de persistencia (delegada a Beanie Model).
    """

    async def create_animal(self, request: AnimalCreateRequest) -> AnimalResponse:
        """
        Crea un nuevo animal.

        Args:
            request: Datos del animal a crear

        Returns:
            AnimalResponse con el animal creado

        Raises:
            AlreadyExistsException: Si la caravana ya existe
            ValidationException: Si los datos son inválidos
        """
        # Validar que la caravana no exista
        existing = await AnimalModel.find_one(
            AnimalModel.ear_tag == request.ear_tag,
            AnimalModel.farm_id == request.farm_id,
        )

        if existing is not None:
            raise AlreadyExistsException(
                resource="Animal", field="ear_tag", value=request.ear_tag
            )

        # Crear modelo
        animal = AnimalModel(
            ear_tag=request.ear_tag,
            breed=request.breed,
            birth_date=request.birth_date,
            gender=request.gender,
            name=request.name,
            color=request.color,
            birth_weight_kg=request.birth_weight_kg,
            mother_id=request.mother_id,
            father_id=request.father_id,
            observations=request.observations,
            photo_url=request.photo_url,
            farm_id=request.farm_id,
            status="active",
        )

        # Guardar en MongoDB
        await animal.insert()

        # Convertir a response
        return self._to_response(animal)

    async def get_animal(self, animal_id: UUID) -> AnimalResponse:
        """
        Obtiene un animal por ID.

        Args:
            animal_id: ID del animal

        Returns:
            AnimalResponse

        Raises:
            NotFoundException: Si el animal no existe
        """
        animal = await AnimalModel.get(animal_id)

        if animal is None:
            raise NotFoundException(resource="Animal", identifier=str(animal_id))

        return self._to_response(animal)

    async def get_animals_by_farm(
        self,
        farm_id: UUID,
        skip: int = 0,
        limit: int = 50,
        status: Optional[str] = None,
    ) -> List[AnimalResponse]:
        """
        Obtiene animales de una hacienda.

        Args:
            farm_id: ID de la hacienda
            skip: Offset para paginación
            limit: Límite de resultados
            status: Filtro opcional por estado

        Returns:
            Lista de AnimalResponse
        """
        query = AnimalModel.find(AnimalModel.farm_id == farm_id)

        if status:
            query = query.find(AnimalModel.status == status)

        animals = await query.skip(skip).limit(limit).to_list()

        return [self._to_response(animal) for animal in animals]

    async def update_animal(
        self, animal_id: UUID, request: AnimalUpdateRequest
    ) -> AnimalResponse:
        """
        Actualiza un animal existente.

        Args:
            animal_id: ID del animal
            request: Datos a actualizar

        Returns:
            AnimalResponse actualizado

        Raises:
            NotFoundException: Si el animal no existe
        """
        animal = await AnimalModel.get(animal_id)

        if animal is None:
            raise NotFoundException(resource="Animal", identifier=str(animal_id))

        # Actualizar solo campos proporcionados
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(animal, field, value)

        animal.update_timestamp()
        await animal.save()

        return self._to_response(animal)

    async def delete_animal(self, animal_id: UUID) -> bool:
        """
        Elimina un animal (soft delete).

        Args:
            animal_id: ID del animal

        Returns:
            True si se eliminó exitosamente

        Raises:
            NotFoundException: Si el animal no existe
        """
        animal = await AnimalModel.get(animal_id)

        if animal is None:
            raise NotFoundException(resource="Animal", identifier=str(animal_id))

        # Soft delete (marcar como inactive)
        animal.status = "inactive"
        animal.update_timestamp()
        await animal.save()

        return True

    def _to_response(self, animal: AnimalModel) -> AnimalResponse:
        """
        Convierte AnimalModel a AnimalResponse.

        Args:
            animal: Modelo de MongoDB

        Returns:
            AnimalResponse con campos calculados
        """
        return AnimalResponse(
            id=animal.id,
            ear_tag=animal.ear_tag,
            breed=animal.breed,
            birth_date=animal.birth_date,
            gender=animal.gender,
            name=animal.name,
            color=animal.color,
            birth_weight_kg=animal.birth_weight_kg,
            status=animal.status,
            farm_id=animal.farm_id,
            registration_date=animal.registration_date,
            last_updated=animal.last_updated,
            age_months=animal.calculate_age_months(),
            age_category=animal.calculate_age_category().value,
        )

