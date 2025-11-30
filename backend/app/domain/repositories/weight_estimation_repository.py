"""
Weight Estimation Repository Interface - Domain Layer
Interfaz para repositorio de estimaciones de peso
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.weight_estimation import WeightEstimation


class WeightEstimationRepository(ABC):
    """
    Interfaz para repositorio de estimaciones de peso.

    Single Responsibility: Definir operaciones de persistencia de estimaciones.
    """

    @abstractmethod
    async def find_by_id(self, estimation_id: UUID) -> WeightEstimation | None:
        """
        Busca una estimación por ID.

        Args:
            estimation_id: ID de la estimación

        Returns:
            WeightEstimation si existe, None si no existe
        """
        pass

    @abstractmethod
    async def create(self, estimation: WeightEstimation) -> WeightEstimation:
        """
        Crea una nueva estimación.

        Args:
            estimation: Estimación a crear

        Returns:
            WeightEstimation creada
        """
        pass

    @abstractmethod
    async def update(self, estimation: WeightEstimation) -> WeightEstimation:
        """
        Actualiza una estimación existente.

        Args:
            estimation: Estimación a actualizar

        Returns:
            WeightEstimation actualizada
        """
        pass

    @abstractmethod
    async def count(self) -> int:
        """
        Retorna el conteo total de estimaciones.

        Returns:
            Número total de estimaciones
        """
        pass
