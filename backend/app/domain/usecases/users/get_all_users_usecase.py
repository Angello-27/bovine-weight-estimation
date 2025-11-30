"""
Get All Users Use Case - Domain Layer
Caso de uso para obtener todos los usuarios
"""

from ...entities.user import User
from ...repositories.user_repository import UserRepository


class GetAllUsersUseCase:
    """
    Caso de uso para obtener todos los usuarios.

    Single Responsibility: Listar usuarios del dominio.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            user_repository: Repositorio de usuarios
        """
        self._user_repository = user_repository

    async def execute(self, skip: int = 0, limit: int = 50) -> list[User]:
        """
        Ejecuta el caso de uso para obtener todos los usuarios.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de User
        """
        return await self._user_repository.get_all(skip=skip, limit=limit)
