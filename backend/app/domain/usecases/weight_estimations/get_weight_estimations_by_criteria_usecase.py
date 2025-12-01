"""
Get Weight Estimations By Criteria Use Case - Domain Layer
Caso de uso para obtener estimaciones de peso por criterios de filtrado
"""

from ...entities.weight_estimation import WeightEstimation
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class GetWeightEstimationsByCriteriaUseCase:
    """
    Caso de uso para obtener estimaciones de peso por criterios de filtrado.

    Single Responsibility: Listar estimaciones del dominio con filtros específicos.
    """

    def __init__(self, weight_estimation_repository: WeightEstimationRepository):
        """
        Inicializa el caso de uso.

        Args:
            weight_estimation_repository: Repositorio de estimaciones de peso
        """
        self._weight_estimation_repository = weight_estimation_repository

    async def execute(
        self, filters: dict, skip: int = 0, limit: int = 50
    ) -> tuple[list[WeightEstimation], int]:
        """
        Ejecuta el caso de uso para obtener estimaciones por criterios.

        Args:
            filters: Diccionario con criterios de filtrado
                     Ejemplos:
                     - {"animal_id": UUID(...)}: Filtrar por animal
                     - {"breed": "nelore"}: Filtrar por raza
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Tupla con (lista de WeightEstimation que coinciden con los criterios, total de registros)
        """
        estimations = await self._weight_estimation_repository.find_by_criteria(
            filters=filters, skip=skip, limit=limit
        )
        total = await self._weight_estimation_repository.count_by_criteria(
            filters=filters
        )
        return estimations, total
