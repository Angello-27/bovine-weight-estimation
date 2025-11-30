"""
Get User By Token Use Case - Domain Layer
Caso de uso para obtener usuario desde token JWT
"""

from uuid import UUID

from ....core.exceptions import AuthenticationException, NotFoundException
from ...entities.user import User
from ...repositories.user_repository import UserRepository


class GetUserByTokenUseCase:
    """
    Caso de uso para obtener un usuario desde token JWT decodificado.

    Single Responsibility: Obtener usuario desde datos del token.
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
        Ejecuta el caso de uso para obtener un usuario desde token.

        Args:
            user_id: ID del usuario desde el token

        Returns:
            User encontrado y activo

        Raises:
            NotFoundException: Si el usuario no existe
            AuthenticationException: Si el usuario está inactivo
        """
        # Buscar usuario
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(resource="User", field="id", value=str(user_id))

        # Verificar que el usuario esté activo
        if not user.is_active:
            raise AuthenticationException("Usuario inactivo")

        return user
