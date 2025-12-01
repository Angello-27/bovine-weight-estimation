"""
Get Animals By Criteria Use Case - Domain Layer
Caso de uso para obtener animales por criterios de filtrado genérico
"""

from ...entities.animal import Animal
from ...repositories.animal_repository import AnimalRepository


class GetAnimalsByCriteriaUseCase:
    """
    Caso de uso para obtener animales por criterios de filtrado genérico.

    Single Responsibility: Listar animales del dominio con filtros específicos.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales
        """
        self._animal_repository = animal_repository

    async def execute(
        self, filters: dict, skip: int = 0, limit: int = 50
    ) -> tuple[list[Animal], int]:
        """
        Ejecuta el caso de uso para obtener animales por criterios.

        Args:
            filters: Diccionario con criterios de filtrado
                     Ejemplos:
                     - {"farm_id": UUID(...)}: Filtrar por finca
                     - {"breed": "nelore"}: Filtrar por raza
                     - {"status": "active"}: Filtrar por estado
                     - {"gender": "female"}: Filtrar por género
                     - {"age_category": "terneros"}: Filtrar por categoría de edad
                     - Combinaciones: {"farm_id": UUID(...), "breed": "nelore", "status": "active"}
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Tupla con (lista de Animal que coinciden con los criterios, total de registros)
        """
        animals = await self._animal_repository.find_by_criteria_dict(
            filters=filters, skip=skip, limit=limit
        )
        total = await self._animal_repository.count_by_criteria(filters=filters)
        return animals, total
