"""
Get Animal Lineage Use Case
Caso de uso para obtener linaje de un animal (padres y descendientes)
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...repositories.animal_repository import AnimalRepository


class GetAnimalLineageUseCase:
    """
    Caso de uso para obtener linaje de un animal.

    Single Responsibility: Obtener información de linaje (padres y descendientes).
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales
        """
        self.animal_repository = animal_repository

    async def execute(self, animal_id: UUID) -> dict:
        """
        Ejecuta el caso de uso.

        Args:
            animal_id: ID del animal

        Returns:
            Dict con información de linaje:
            {
                "animal": Animal,
                "mother": Animal | None,
                "father": Animal | None,
                "descendants": list[Animal]
            }

        Raises:
            NotFoundException: Si el animal no existe
        """
        # 1. Obtener animal principal
        animal = await self.animal_repository.get_by_id(animal_id)
        if animal is None:
            raise NotFoundException(resource="Animal", field="id", value=str(animal_id))

        # 2. Obtener madre si existe
        mother = None
        if animal.mother_id:
            mother = await self.animal_repository.find_by_mother_id(animal.mother_id)

        # 3. Obtener padre si existe
        father = None
        if animal.father_id:
            father = await self.animal_repository.find_by_father_id(animal.father_id)

        # 4. Obtener descendientes (hijos)
        descendants = await self.animal_repository.find_descendants(
            animal_id, parent_role="both"
        )

        return {
            "animal": animal,
            "mother": mother,
            "father": father,
            "descendants": descendants,
        }
