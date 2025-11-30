"""
Get Role By ID Use Case - Domain Layer
Caso de uso para obtener un rol por ID
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.role import Role
from ...repositories.role_repository import RoleRepository


class GetRoleByIdUseCase:
    """
    Caso de uso para obtener un rol por ID.

    Single Responsibility: Obtener un rol del dominio.
    """

    def __init__(self, role_repository: RoleRepository):
        """
        Inicializa el caso de uso.

        Args:
            role_repository: Repositorio de roles
        """
        self._role_repository = role_repository

    async def execute(self, role_id: UUID) -> Role:
        """
        Ejecuta el caso de uso para obtener un rol.

        Args:
            role_id: ID del rol

        Returns:
            Role encontrado

        Raises:
            NotFoundException: Si el rol no existe
        """
        role = await self._role_repository.get_by_id(role_id)
        if role is None:
            raise NotFoundException(resource="Role", field="id", value=str(role_id))
        return role
