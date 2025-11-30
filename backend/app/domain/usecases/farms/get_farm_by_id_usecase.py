"""
Get Farm By ID Use Case - Domain Layer
Caso de uso para obtener una finca por ID
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.farm import Farm
from ...repositories.farm_repository import FarmRepository


class GetFarmByIdUseCase:
    """
    Caso de uso para obtener una finca por ID.

    Single Responsibility: Obtener una finca del dominio.
    """

    def __init__(self, farm_repository: FarmRepository):
        """
        Inicializa el caso de uso.

        Args:
            farm_repository: Repositorio de fincas
        """
        self._farm_repository = farm_repository

    async def execute(self, farm_id: UUID) -> Farm:
        """
        Ejecuta el caso de uso para obtener una finca.

        Args:
            farm_id: ID de la finca

        Returns:
            Farm encontrada

        Raises:
            NotFoundException: Si la finca no existe
        """
        farm = await self._farm_repository.get_by_id(farm_id)
        if farm is None:
            raise NotFoundException(resource="Farm", field="id", value=str(farm_id))
        return farm

