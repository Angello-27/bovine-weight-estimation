"""
Farm Repository Implementation - Data Layer
Implementación del repositorio de fincas usando Beanie ODM
"""

from uuid import UUID

from ...domain.entities.farm import Farm
from ...domain.repositories.farm_repository import FarmRepository
from ..models.farm_model import FarmModel


class FarmRepositoryImpl(FarmRepository):
    """
    Implementación del repositorio de fincas.

    Single Responsibility: Persistencia de fincas usando MongoDB/Beanie.
    """

    async def save(self, farm: Farm) -> Farm:
        """
        Guarda o actualiza una finca.

        Args:
            farm: Entidad Farm a persistir

        Returns:
            Farm guardada con ID asignado
        """
        # Buscar si existe
        existing = await FarmModel.get(farm.id)
        if existing:
            # Actualizar
            existing.name = farm.name
            existing.owner_id = farm.owner_id
            existing.location = farm.get_location_dict()
            existing.capacity = farm.capacity
            existing.total_animals = farm.total_animals
            existing.last_updated = farm.last_updated
            await existing.save()
            return existing.to_entity()
        # Crear nuevo
        model = FarmModel.from_entity(farm)
        await model.insert()
        return model.to_entity()

    async def get_by_id(self, farm_id: UUID) -> Farm | None:
        """
        Obtiene una finca por ID.

        Args:
            farm_id: ID de la finca

        Returns:
            Farm si existe, None si no existe
        """
        model = await FarmModel.get(farm_id)
        if model is None:
            return None
        return model.to_entity()

    async def find_by_name_and_owner(self, name: str, owner_id: UUID) -> Farm | None:
        """
        Busca una finca por nombre y propietario.

        Args:
            name: Nombre de la finca
            owner_id: ID del propietario

        Returns:
            Farm si existe, None si no existe
        """
        model = await FarmModel.find_one(
            FarmModel.name == name, FarmModel.owner_id == owner_id
        )
        if model is None:
            return None
        return model.to_entity()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 50,
        owner_id: UUID | None = None,
    ) -> list[Farm]:
        """
        Obtiene todas las fincas con paginación.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados
            owner_id: Filtrar por propietario (opcional)

        Returns:
            Lista de Farm
        """
        if owner_id:
            models = (
                await FarmModel.find(FarmModel.owner_id == owner_id)
                .skip(skip)
                .limit(limit)
                .to_list()
            )
        else:
            models = await FarmModel.find_all().skip(skip).limit(limit).to_list()

        return [model.to_entity() for model in models]

    async def delete(self, farm_id: UUID) -> bool:
        """
        Elimina una finca.

        Args:
            farm_id: ID de la finca

        Returns:
            True si se eliminó exitosamente
        """
        model = await FarmModel.get(farm_id)
        if model is None:
            return False
        await model.delete()
        return True
