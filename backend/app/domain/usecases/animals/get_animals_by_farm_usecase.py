"""
Get Animals By Farm Use Case - Domain Layer
Caso de uso para obtener animales de una hacienda
"""

from uuid import UUID

from ...entities.animal import Animal
from ...repositories.animal_repository import AnimalRepository


class GetAnimalsByFarmUseCase:
    """
    Caso de uso para obtener animales de una hacienda.

    Single Responsibility: Obtener lista de animales del dominio por hacienda.
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
        farm_id: UUID,
        skip: int = 0,
        limit: int = 50,
        status: str | None = None,
    ) -> list[Animal]:
        """
        Ejecuta el caso de uso para obtener animales de una hacienda.

        Args:
            farm_id: ID de la hacienda
            skip: Offset para paginación
            limit: Límite de resultados
            status: Filtro opcional por estado

        Returns:
            Lista de Animal
        """
        return await self._animal_repository.get_by_farm(
            farm_id=farm_id, skip=skip, limit=limit, status=status
        )
