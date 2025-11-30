"""
Get User By ID Use Case - Domain Layer
Caso de uso para obtener un usuario por ID
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.user import User
from ...repositories.user_repository import UserRepository


class GetUserByIdUseCase:
    """
    Caso de uso para obtener un usuario por ID.

    Single Responsibility: Obtener un usuario del dominio.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            user_repository: Repositorio de usuarios
        """
        self._user_repository = user_repository

    async def execute(self, user_id: UUID) -> User:
        """
        Ejecuta el caso de uso para obtener un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            User encontrado

        Raises:
            NotFoundException: Si el usuario no existe
        """
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(resource="User", field="id", value=str(user_id))
        return user
