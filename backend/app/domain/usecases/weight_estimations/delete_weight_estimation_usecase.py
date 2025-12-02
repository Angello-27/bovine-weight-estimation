"""
Delete Weight Estimation Use Case - Domain Layer
Caso de uso para eliminar una estimación de peso
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class DeleteWeightEstimationUseCase:
    """
    Caso de uso para eliminar una estimación de peso.

    Single Responsibility: Validar y eliminar una estimación en el dominio.
    """

    def __init__(
        self,
        weight_estimation_repository: WeightEstimationRepository,
    ):
        """
        Inicializa el caso de uso.

        Args:
            weight_estimation_repository: Repositorio de estimaciones
        """
        self._weight_estimation_repository = weight_estimation_repository

    async def execute(self, estimation_id: UUID) -> bool:
        """
        Ejecuta el caso de uso para eliminar una estimación.

        Args:
            estimation_id: ID de la estimación a eliminar

        Returns:
            True si se eliminó exitosamente

        Raises:
            NotFoundException: Si la estimación no existe
        """
        # Verificar que la estimación existe
        estimation = await self._weight_estimation_repository.find_by_id(estimation_id)
        if estimation is None:
            raise NotFoundException(
                resource="WeightEstimation", field="id", value=str(estimation_id)
            )

        # Eliminar usando el repositorio
        return await self._weight_estimation_repository.delete(estimation_id)
