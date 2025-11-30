"""
User Repository Implementation - Data Layer
Implementación del repositorio de usuarios usando Beanie ODM
"""

from uuid import UUID

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ..models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """
    Implementación del repositorio de usuarios usando Beanie ODM.

    Single Responsibility: Persistencia de usuarios en MongoDB.
    """

    def _to_entity(self, model: UserModel) -> User:
        """
        Convierte UserModel (Data) a User (Domain Entity).

        Args:
            model: Modelo de Beanie

        Returns:
            Entidad User del dominio
        """
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            role_id=model.role_id,
            farm_id=model.farm_id,
            is_active=model.is_active,
            is_superuser=model.is_superuser,
            created_at=model.created_at,
            last_updated=model.last_updated,
            last_login=model.last_login,
        )

    def _to_model(self, entity: User) -> UserModel:
        """
        Convierte User (Domain Entity) a UserModel (Data).

        Args:
            entity: Entidad User del dominio

        Returns:
            Modelo de Beanie
        """
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            role_id=entity.role_id,
            farm_id=entity.farm_id,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
            created_at=entity.created_at,
            last_updated=entity.last_updated,
            last_login=entity.last_login,
        )

    async def save(self, user: User) -> User:
        """
        Guarda o actualiza un usuario.

        Args:
            user: Entidad User a persistir

        Returns:
            User guardado con ID asignado
        """
        model = self._to_model(user)
        await model.save()
        return self._to_entity(model)

    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Obtiene un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            User si existe, None si no existe
        """
        model = await UserModel.get(user_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def find_by_username(self, username: str) -> User | None:
        """
        Busca un usuario por username.

        Args:
            username: Nombre de usuario

        Returns:
            User si existe, None si no existe
        """
        model = await UserModel.find_one(UserModel.username == username)
        if model is None:
            return None
        return self._to_entity(model)

    async def find_by_email(self, email: str) -> User | None:
        """
        Busca un usuario por email.

        Args:
            email: Email del usuario

        Returns:
            User si existe, None si no existe
        """
        model = await UserModel.find_one(UserModel.email == email)
        if model is None:
            return None
        return self._to_entity(model)

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
        models = await UserModel.find_all().skip(skip).limit(limit).to_list()
        return [self._to_entity(model) for model in models]

    async def delete(self, user_id: UUID) -> bool:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            True si se eliminó exitosamente
        """
        model = await UserModel.get(user_id)
        if model is None:
            return False
        await model.delete()
        return True
