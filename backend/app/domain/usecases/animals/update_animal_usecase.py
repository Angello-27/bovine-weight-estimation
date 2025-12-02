"""
Update Animal Use Case - Domain Layer
Caso de uso para actualizar un animal
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.animal import Animal
from ...repositories.animal_repository import AnimalRepository


class UpdateAnimalUseCase:
    """
    Caso de uso para actualizar un animal.

    Single Responsibility: Actualizar un animal en el dominio.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales (inyección de dependencia)
        """
        self._animal_repository = animal_repository

    async def execute(
        self,
        animal_id: UUID,
        name: str | None = None,
        color: str | None = None,
        observations: str | None = None,
        status: str | None = None,
        photo_url: str | None = None,
        mother_id: UUID | None = None,
        father_id: UUID | None = None,
    ) -> Animal:
        """
        Ejecuta el caso de uso para actualizar un animal.

        Args:
            animal_id: ID del animal
            name: Nombre (opcional)
            color: Color (opcional)
            observations: Observaciones (opcional)
            status: Estado (opcional)
            photo_url: URL de foto (opcional)
            mother_id: ID de la madre (opcional)
            father_id: ID del padre (opcional)

        Returns:
            Animal actualizado

        Raises:
            NotFoundException: Si el animal no existe
        """
        # Obtener animal existente
        animal = await self._animal_repository.get_by_id(animal_id)

        if animal is None:
            raise NotFoundException(resource="Animal", field="id", value=str(animal_id))

        # Actualizar solo campos proporcionados
        if name is not None:
            animal.name = name
        if color is not None:
            animal.color = color
        if observations is not None:
            animal.observations = observations
        if status is not None:
            animal.status = status
        if photo_url is not None:
            animal.photo_url = photo_url
        if mother_id is not None:
            animal.mother_id = str(mother_id)
        if father_id is not None:
            animal.father_id = str(father_id)

        # Actualizar timestamp
        animal.update_timestamp()

        # Guardar cambios
        return await self._animal_repository.save(animal)
