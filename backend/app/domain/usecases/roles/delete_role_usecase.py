"""
Delete Role Use Case - Domain Layer
Caso de uso para eliminar un rol
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...repositories.role_repository import RoleRepository


class DeleteRoleUseCase:
    """
    Caso de uso para eliminar un rol.

    Single Responsibility: Eliminar un rol del dominio.
    """

    def __init__(self, role_repository: RoleRepository):
        """
        Inicializa el caso de uso.

        Args:
            role_repository: Repositorio de roles
        """
        self._role_repository = role_repository

    async def execute(self, role_id: UUID) -> None:
        """
        Ejecuta el caso de uso para eliminar un rol.

        Args:
            role_id: ID del rol

        Raises:
            NotFoundException: Si el rol no existe
        """
        # Verificar que el rol existe
        role = await self._role_repository.get_by_id(role_id)
        if role is None:
            raise NotFoundException(resource="Role", field="id", value=str(role_id))

        # Eliminar
        await self._role_repository.delete(role_id)
