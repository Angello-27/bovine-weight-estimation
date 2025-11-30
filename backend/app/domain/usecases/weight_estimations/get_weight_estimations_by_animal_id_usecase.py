"""
Get Weight Estimations By Animal ID Use Case - Domain Layer
Caso de uso para obtener estimaciones de un animal
"""

from uuid import UUID

from ...entities.weight_estimation import WeightEstimation
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class GetWeightEstimationsByAnimalIdUseCase:
    """
    Caso de uso para obtener estimaciones por animal.

    Single Responsibility: Obtener estimaciones de un animal del dominio.
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
        animal_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[WeightEstimation]:
        """
        Ejecuta el caso de uso para obtener estimaciones de un animal.

        Args:
            animal_id: ID del animal
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de WeightEstimation ordenada por fecha DESC
        """
        return await self._weight_estimation_repository.find_by_animal_id(
            animal_id=str(animal_id), skip=skip, limit=limit
        )
