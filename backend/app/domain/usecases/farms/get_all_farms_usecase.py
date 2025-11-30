"""
Get All Farms Use Case - Domain Layer
Caso de uso para obtener todas las fincas
"""

from uuid import UUID

from ...entities.farm import Farm
from ...repositories.farm_repository import FarmRepository


class GetAllFarmsUseCase:
    """
    Caso de uso para obtener todas las fincas.

    Single Responsibility: Listar fincas del dominio.
    """

    def __init__(self, farm_repository: FarmRepository):
        """
        Inicializa el caso de uso.

        Args:
            farm_repository: Repositorio de fincas
        """
        self._farm_repository = farm_repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 50,
        owner_id: UUID | None = None,
    ) -> list[Farm]:
        """
        Ejecuta el caso de uso para obtener todas las fincas.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados
            owner_id: Filtrar por propietario (opcional)

        Returns:
            Lista de Farm
        """
        return await self._farm_repository.get_all(
            skip=skip, limit=limit, owner_id=owner_id
        )
