"""
Get Farms By Criteria Use Case - Domain Layer
Caso de uso para obtener fincas por criterios de filtrado
"""

from ...entities.farm import Farm
from ...repositories.farm_repository import FarmRepository


class GetFarmsByCriteriaUseCase:
    """
    Caso de uso para obtener fincas por criterios de filtrado.

    Single Responsibility: Listar fincas del dominio con filtros específicos.
    """

    def __init__(self, farm_repository: FarmRepository):
        """
        Inicializa el caso de uso.

        Args:
            farm_repository: Repositorio de fincas
        """
        self._farm_repository = farm_repository

    async def execute(
        self, filters: dict, skip: int = 0, limit: int = 50
    ) -> tuple[list[Farm], int]:
        """
        Ejecuta el caso de uso para obtener fincas por criterios.

        Args:
            filters: Diccionario con criterios de filtrado
                     Ejemplos:
                     - {"owner_id": UUID(...)}: Filtrar por propietario
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Tupla con (lista de Farm que coinciden con los criterios, total de registros)
        """
        farms = await self._farm_repository.find_by_criteria(
            filters=filters, skip=skip, limit=limit
        )
        total = await self._farm_repository.count_by_criteria(filters=filters)
        return farms, total
