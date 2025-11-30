"""
Get All Roles Use Case - Domain Layer
Caso de uso para obtener todos los roles
"""

from ...entities.role import Role
from ...repositories.role_repository import RoleRepository


class GetAllRolesUseCase:
    """
    Caso de uso para obtener todos los roles.

    Single Responsibility: Listar roles del dominio.
    """

    def __init__(self, role_repository: RoleRepository):
        """
        Inicializa el caso de uso.

        Args:
            role_repository: Repositorio de roles
        """
        self._role_repository = role_repository

    async def execute(self, skip: int = 0, limit: int = 50) -> list[Role]:
        """
        Ejecuta el caso de uso para obtener todos los roles.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de Role
        """
        return await self._role_repository.get_all(skip=skip, limit=limit)
