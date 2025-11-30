"""
Role Repository Implementation - Data Layer
Implementación del repositorio de roles usando Beanie ODM
"""

from uuid import UUID

from ...domain.entities.role import Role
from ...domain.repositories.role_repository import RoleRepository
from ..models.role_model import RoleModel


class RoleRepositoryImpl(RoleRepository):
    """
    Implementación del repositorio de roles usando Beanie ODM.

    Single Responsibility: Persistencia de roles en MongoDB.
    """

    def _to_entity(self, model: RoleModel) -> Role:
        """
        Convierte RoleModel (Data) a Role (Domain Entity).

        Args:
            model: Modelo de Beanie

        Returns:
            Entidad Role del dominio
        """
        return Role(
            id=model.id,
            name=model.name,
            description=model.description,
            priority=model.priority,
            permissions=model.permissions,
            created_at=model.created_at,
            last_updated=model.last_updated,
        )

    def _to_model(self, entity: Role) -> RoleModel:
        """
        Convierte Role (Domain Entity) a RoleModel (Data).

        Args:
            entity: Entidad Role del dominio

        Returns:
            Modelo de Beanie
        """
        return RoleModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            priority=entity.priority,
            permissions=entity.permissions,
            created_at=entity.created_at,
            last_updated=entity.last_updated,
        )

    async def save(self, role: Role) -> Role:
        """
        Guarda o actualiza un rol.

        Args:
            role: Entidad Role a persistir

        Returns:
            Role guardado con ID asignado
        """
        model = self._to_model(role)
        await model.save()
        return self._to_entity(model)

    async def get_by_id(self, role_id: UUID) -> Role | None:
        """
        Obtiene un rol por ID.

        Args:
            role_id: ID del rol

        Returns:
            Role si existe, None si no existe
        """
        model = await RoleModel.get(role_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def find_by_name(self, name: str) -> Role | None:
        """
        Busca un rol por nombre.

        Args:
            name: Nombre del rol

        Returns:
            Role si existe, None si no existe
        """
        model = await RoleModel.find_one(RoleModel.name == name)
        if model is None:
            return None
        return self._to_entity(model)

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
        models = await RoleModel.find_all().skip(skip).limit(limit).to_list()
        return [self._to_entity(model) for model in models]

    async def delete(self, role_id: UUID) -> bool:
        """
        Elimina un rol.

        Args:
            role_id: ID del rol

        Returns:
            True si se eliminó exitosamente
        """
        model = await RoleModel.get(role_id)
        if model is None:
            return False
        await model.delete()
        return True
