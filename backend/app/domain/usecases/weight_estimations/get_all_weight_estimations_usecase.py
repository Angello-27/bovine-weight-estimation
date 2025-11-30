"""
Get All Weight Estimations Use Case - Domain Layer
Caso de uso para obtener todas las estimaciones
"""

from ...entities.weight_estimation import WeightEstimation
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class GetAllWeightEstimationsUseCase:
    """
    Caso de uso para obtener todas las estimaciones.

    Single Responsibility: Obtener todas las estimaciones del dominio.
    """

    def __init__(self, weight_estimation_repository: WeightEstimationRepository):
        """
        Inicializa el caso de uso.

        Args:
            weight_estimation_repository: Repositorio de estimaciones
        """
        self._weight_estimation_repository = weight_estimation_repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 50,
    ) -> list[WeightEstimation]:
        """
        Ejecuta el caso de uso para obtener todas las estimaciones.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de WeightEstimation ordenada por fecha DESC
        """
        return await self._weight_estimation_repository.find_all(skip=skip, limit=limit)
