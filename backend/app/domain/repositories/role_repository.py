"""
Role Repository Interface - Domain Layer
Contrato para persistencia de roles (Dependency Inversion)
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.role import Role


class RoleRepository(ABC):
    """
    Interfaz para repositorio de roles.

    Dependency Inversion: Domain define el contrato, Data lo implementa.
    """

    @abstractmethod
    async def save(self, role: Role) -> Role:
        """
        Guarda o actualiza un rol.

        Args:
            role: Entidad Role a persistir

        Returns:
            Role guardado con ID asignado
        """
        pass

    @abstractmethod
    async def get_by_id(self, role_id: UUID) -> Role | None:
        """
        Obtiene un rol por ID.

        Args:
            role_id: ID del rol

        Returns:
            Role si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Role | None:
        """
        Busca un rol por nombre.

        Args:
            name: Nombre del rol

        Returns:
            Role si existe, None si no existe
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Role]:
        """
        Obtiene todos los roles con paginación.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de Role
        """
        pass

    @abstractmethod
    async def delete(self, role_id: UUID) -> bool:
        """
        Elimina un rol.

        Args:
            role_id: ID del rol

        Returns:
            True si se eliminó exitosamente
        """
        pass
