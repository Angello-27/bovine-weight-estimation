"""
Delete User Use Case - Domain Layer
Caso de uso para eliminar un usuario
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...repositories.user_repository import UserRepository


class DeleteUserUseCase:
    """
    Caso de uso para eliminar un usuario.

    Single Responsibility: Eliminar un usuario del dominio.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            user_repository: Repositorio de usuarios
        """
        self._user_repository = user_repository

    async def execute(self, user_id: UUID) -> None:
        """
        Ejecuta el caso de uso para eliminar un usuario.

        Args:
            user_id: ID del usuario

        Raises:
            NotFoundException: Si el usuario no existe
        """
        # Verificar que el usuario existe
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(resource="User", field="id", value=str(user_id))

        # Eliminar
        await self._user_repository.delete(user_id)
