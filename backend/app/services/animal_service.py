"""
Animal Service - Business Logic (Refactorizado para Clean Architecture)
Orquesta casos de uso del dominio
"""

from uuid import UUID

from ..domain.entities.animal import Animal
from ..domain.repositories.animal_repository import AnimalRepository
from ..domain.usecases.animals import (
    CreateAnimalUseCase,
    DeleteAnimalUseCase,
    GetAnimalByIdUseCase,
    GetAnimalsByFarmUseCase,
    UpdateAnimalUseCase,
)
from ..schemas.animal_schemas import (
    AnimalCreateRequest,
    AnimalResponse,
    AnimalUpdateRequest,
)


class AnimalService:
    """
    Servicio de gestión de animales (refactorizado).

    Single Responsibility: Orquestar casos de uso y convertir entre capas.
    Ahora usa Clean Architecture con Use Cases.
    """

    def __init__(self, animal_repository: AnimalRepository | None = None):
        """
        Inicializa el servicio.

        Args:
            animal_repository: Repositorio de animales (inyección de dependencia)
        """
        from ..data.repositories.animal_repository_impl import AnimalRepositoryImpl

        self._repository = animal_repository or AnimalRepositoryImpl()
        self._create_usecase = CreateAnimalUseCase(self._repository)
        self._get_by_id_usecase = GetAnimalByIdUseCase(self._repository)
        self._get_by_farm_usecase = GetAnimalsByFarmUseCase(self._repository)
        self._update_usecase = UpdateAnimalUseCase(self._repository)
        self._delete_usecase = DeleteAnimalUseCase(self._repository)

    async def create_animal(self, request: AnimalCreateRequest) -> AnimalResponse:
        """
        Crea un nuevo animal.

        Args:
            request: Datos del animal a crear

        Returns:
            AnimalResponse con el animal creado
        """
        animal = await self._create_usecase.execute(
            ear_tag=request.ear_tag,
            breed=(
                request.breed.value
                if hasattr(request.breed, "value")
                else str(request.breed)
            ),
            birth_date=request.birth_date,
            gender=request.gender,
            farm_id=request.farm_id,
            name=request.name,
            color=request.color,
            birth_weight_kg=request.birth_weight_kg,
            mother_id=str(request.mother_id) if request.mother_id else None,
            father_id=str(request.father_id) if request.father_id else None,
            observations=request.observations,
            photo_url=request.photo_url,
        )

        return self._entity_to_response(animal)

    async def get_animal(self, animal_id: UUID) -> AnimalResponse:
        """
        Obtiene un animal por ID.

        Args:
            animal_id: ID del animal

        Returns:
            AnimalResponse
        """
        animal = await self._get_by_id_usecase.execute(animal_id)
        return self._entity_to_response(animal)

    async def get_animals_by_farm(
        self,
        farm_id: UUID,
        skip: int = 0,
        limit: int = 50,
        status: str | None = None,
    ) -> list[AnimalResponse]:
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
        animals = await self._get_by_farm_usecase.execute(
            farm_id=farm_id, skip=skip, limit=limit, status=status
        )

        return [self._entity_to_response(animal) for animal in animals]

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
        """
        animal = await self._update_usecase.execute(
            animal_id=animal_id,
            name=request.name,
            color=request.color,
            observations=request.observations,
            status=request.status,
            photo_url=request.photo_url,
        )

        return self._entity_to_response(animal)

    async def delete_animal(self, animal_id: UUID) -> bool:
        """
        Elimina un animal (soft delete).

        Args:
            animal_id: ID del animal

        Returns:
            True si se eliminó exitosamente
        """
        return await self._delete_usecase.execute(animal_id)

    def _entity_to_response(self, animal: Animal) -> AnimalResponse:
        """
        Convierte Animal (Domain Entity) a AnimalResponse (API Schema).

        Args:
            animal: Entidad Animal del dominio

        Returns:
            AnimalResponse con campos calculados
        """
        from ..domain.shared.constants import BreedType

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
            status=animal.status,
            farm_id=(
                animal.farm_id
                if animal.farm_id
                else UUID("00000000-0000-0000-0000-000000000000")
            ),
            registration_date=animal.registration_date,
            last_updated=animal.last_updated,
            age_months=animal.calculate_age_months(),
            age_category=animal.calculate_age_category().value,
        )
