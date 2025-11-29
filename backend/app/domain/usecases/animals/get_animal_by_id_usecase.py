"""
Get Animal By ID Use Case - Domain Layer
Caso de uso para obtener un animal por ID
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.animal import Animal
from ...repositories.animal_repository import AnimalRepository


class GetAnimalByIdUseCase:
    """
    Caso de uso para obtener un animal por ID.

    Single Responsibility: Obtener un animal del dominio por ID.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales (inyección de dependencia)
        """
        self._animal_repository = animal_repository

    async def execute(self, animal_id: UUID) -> Animal:
        """
        Ejecuta el caso de uso para obtener un animal por ID.

        Args:
            animal_id: ID del animal

        Returns:
            Animal encontrado

        Raises:
            NotFoundException: Si el animal no existe
        """
        animal = await self._animal_repository.get_by_id(animal_id)

        if animal is None:
            raise NotFoundException(resource="Animal", field="id", value=str(animal_id))

        return animal
