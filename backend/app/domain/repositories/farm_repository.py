"""
Farm Repository Interface - Domain Layer
Contrato para persistencia de fincas (Dependency Inversion)
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.farm import Farm


class FarmRepository(ABC):
    """
    Interfaz para repositorio de fincas.

    Dependency Inversion: Domain define el contrato, Data lo implementa.
    """

    @abstractmethod
    async def save(self, farm: Farm) -> Farm:
        """
        Guarda o actualiza una finca.

        Args:
            farm: Entidad Farm a persistir

        Returns:
            Farm guardada con ID asignado
        """
        pass

    @abstractmethod
    async def get_by_id(self, farm_id: UUID) -> Farm | None:
        """
        Obtiene una finca por ID.

        Args:
            farm_id: ID de la finca

        Returns:
            Farm si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_name_and_owner(self, name: str, owner_id: UUID) -> Farm | None:
        """
        Busca una finca por nombre y propietario.

        Args:
            name: Nombre de la finca
            owner_id: ID del propietario

        Returns:
            Farm si existe, None si no existe
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Farm]:
        """
        Obtiene todas las fincas con paginación.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de Farm
        """
        pass

    @abstractmethod
    async def find_by_criteria(
        self,
        filters: dict,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Farm]:
        """
        Busca fincas por criterios de filtrado.

        Args:
            filters: Diccionario con criterios de filtrado (ej: {"owner_id": UUID})
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de Farm que coinciden con los criterios
        """
        pass

    @abstractmethod
    async def count_by_criteria(self, filters: dict) -> int:
        """
        Cuenta fincas que coinciden con criterios de filtrado.

        Args:
            filters: Diccionario con criterios de filtrado

        Returns:
            Número total de fincas que coinciden con los criterios
        """
        pass

    @abstractmethod
    async def delete(self, farm_id: UUID) -> bool:
        """
        Elimina una finca.

        Args:
            farm_id: ID de la finca

        Returns:
            True si se eliminó exitosamente
        """
        pass
