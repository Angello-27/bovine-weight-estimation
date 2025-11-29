"""
Delete Animal Use Case - Domain Layer
Caso de uso para eliminar un animal (soft delete)
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...repositories.animal_repository import AnimalRepository


class DeleteAnimalUseCase:
    """
    Caso de uso para eliminar un animal (soft delete).

    Single Responsibility: Eliminar un animal en el dominio.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales (inyección de dependencia)
        """
        self._animal_repository = animal_repository

    async def execute(self, animal_id: UUID) -> bool:
        """
        Ejecuta el caso de uso para eliminar un animal (soft delete).

        Args:
            animal_id: ID del animal

        Returns:
            True si se eliminó exitosamente

        Raises:
            NotFoundException: Si el animal no existe
        """
        # Obtener animal existente
        animal = await self._animal_repository.get_by_id(animal_id)

        if animal is None:
            raise NotFoundException(resource="Animal", field="id", value=str(animal_id))

        # Soft delete (marcar como inactive)
        animal.status = "inactive"
        animal.update_timestamp()

        # Guardar cambios
        await self._animal_repository.save(animal)

        return True
