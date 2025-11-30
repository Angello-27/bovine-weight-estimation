"""
Get Weight Estimation By ID Use Case - Domain Layer
Caso de uso para obtener una estimación por ID
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.weight_estimation import WeightEstimation
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class GetWeightEstimationByIdUseCase:
    """
    Caso de uso para obtener una estimación por ID.

    Single Responsibility: Obtener una estimación del dominio por ID.
    """

    def __init__(self, weight_estimation_repository: WeightEstimationRepository):
        """
        Inicializa el caso de uso.

        Args:
            weight_estimation_repository: Repositorio de estimaciones
        """
        self._weight_estimation_repository = weight_estimation_repository

    async def execute(self, estimation_id: UUID) -> WeightEstimation:
        """
        Ejecuta el caso de uso para obtener una estimación por ID.

        Args:
            estimation_id: ID de la estimación

        Returns:
            WeightEstimation encontrada

        Raises:
            NotFoundException: Si la estimación no existe
        """
        estimation = await self._weight_estimation_repository.find_by_id(estimation_id)

        if estimation is None:
            raise NotFoundException(
                resource="WeightEstimation", field="id", value=str(estimation_id)
            )

        return estimation
