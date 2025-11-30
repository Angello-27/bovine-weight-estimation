"""
Animal Repository Interface - Domain Layer
Contrato para persistencia de animales (Dependency Inversion)
"""

from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.animal import Animal


class AnimalRepository(ABC):
    """
    Interfaz para repositorio de animales.

    Dependency Inversion: Domain define el contrato, Data lo implementa.
    """

    @abstractmethod
    async def save(self, animal: Animal) -> Animal:
        """
        Guarda o actualiza un animal.

        Args:
            animal: Entidad Animal a persistir

        Returns:
            Animal guardado con ID asignado
        """
        pass

    @abstractmethod
    async def get_by_id(self, animal_id: UUID) -> Animal | None:
        """
        Obtiene un animal por ID.

        Args:
            animal_id: ID del animal

        Returns:
            Animal si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find_by_ear_tag(self, ear_tag: str, farm_id: UUID) -> Animal | None:
        """
        Busca un animal por caravana y hacienda.

        Args:
            ear_tag: Número de caravana
            farm_id: ID de la hacienda

        Returns:
            Animal si existe, None si no existe
        """
        pass

    @abstractmethod
    async def get_by_farm(
        self,
        farm_id: UUID,
        skip: int = 0,
        limit: int = 50,
        status: str | None = None,
    ) -> list[Animal]:
        """
        Obtiene animales de una hacienda con paginación.

        Args:
            farm_id: ID de la hacienda
            skip: Offset para paginación
            limit: Límite de resultados
            status: Filtro opcional por estado

        Returns:
            Lista de Animal
        """
        pass

    @abstractmethod
    async def delete(self, animal_id: UUID) -> bool:
        """
        Elimina un animal (soft delete).

        Args:
            animal_id: ID del animal

        Returns:
            True si se eliminó exitosamente
        """
        pass

    @abstractmethod
    async def find_by_criteria(
        self,
        farm_id: UUID,
        breed: str | None = None,
        age_category: str | None = None,
        gender: str | None = None,
        status: str | None = None,
        limit: int | None = None,
    ) -> list[Animal]:
        """
        Busca animales por múltiples criterios de filtrado.

        Args:
            farm_id: ID de la finca (requerido)
            breed: Raza del animal (opcional)
            age_category: Categoría de edad (opcional)
            gender: Género del animal (opcional)
            status: Estado del animal (opcional)
            limit: Límite de resultados (opcional)

        Returns:
            Lista de Animal que cumplen los criterios
        """
        pass
