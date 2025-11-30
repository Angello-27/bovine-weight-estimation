"""
User Repository Interface - Domain Layer
Contrato para persistencia de usuarios (Dependency Inversion)
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.user import User


class UserRepository(ABC):
    """
    Interfaz para repositorio de usuarios.

    Dependency Inversion: Domain define el contrato, Data lo implementa.
    """

    @abstractmethod
    async def save(self, user: User) -> User:
        """
        Guarda o actualiza un usuario.

        Args:
            user: Entidad User a persistir

        Returns:
            User guardado con ID asignado
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Obtiene un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            User si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> User | None:
        """
        Busca un usuario por username.

        Args:
            username: Nombre de usuario

        Returns:
            User si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        """
        Busca un usuario por email.

        Args:
            email: Email del usuario

        Returns:
            User si existe, None si no existe
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 50,
    ) -> list[User]:
        """
        Obtiene todos los usuarios con paginación.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de User
        """
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            True si se eliminó exitosamente
        """
        pass
