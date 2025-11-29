"""
User Service - Business Logic
Lógica de negocio para gestión de usuarios
"""

from uuid import UUID

from ..core.exceptions import AlreadyExistsException, NotFoundException
from ..models import FarmModel, RoleModel, UserModel
from ..schemas.user_schemas import (
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)
from .auth_service import AuthService


class UserService:
    """
    Servicio de gestión de usuarios.

    Single Responsibility: Business logic de usuarios.
    """

    def __init__(self):
        self.auth_service = AuthService()

    async def create_user(self, request: UserCreateRequest) -> UserResponse:
        """
        Crea un nuevo usuario.

        Args:
            request: Datos del usuario a crear

        Returns:
            UserResponse con el usuario creado

        Raises:
            AlreadyExistsException: Si el username o email ya existe
            NotFoundException: Si el rol no existe
        """
        # Validar que el username no exista
        existing_username = await UserModel.find_one(
            UserModel.username == request.username
        )
        if existing_username is not None:
            raise AlreadyExistsException(
                resource="User", field="username", value=request.username
            )

        # Validar que el email no exista
        existing_email = await UserModel.find_one(UserModel.email == request.email)
        if existing_email is not None:
            raise AlreadyExistsException(
                resource="User", field="email", value=request.email
            )

        # Validar que el rol exista
        role = await RoleModel.find_one(RoleModel.id == request.role_id)
        if role is None:
            raise NotFoundException(
                resource="Role", field="id", value=str(request.role_id)
            )

        # Validar que la finca exista si se proporciona
        if request.farm_id is not None:
            farm = await FarmModel.get(request.farm_id)
            if farm is None:
                raise NotFoundException(
                    resource="Farm", field="id", value=str(request.farm_id)
                )

        # Crear usuario
        hashed_password = self.auth_service.get_password_hash(request.password)
        user = UserModel(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            role_id=request.role_id,
            farm_id=request.farm_id,
        )
        await user.insert()

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role_id=user.role_id,
            farm_id=user.farm_id,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            last_updated=user.last_updated,
            last_login=user.last_login,
        )

    async def get_user_by_id(self, user_id: UUID) -> UserResponse:
        """
        Obtiene un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            UserResponse con el usuario

        Raises:
            NotFoundException: Si el usuario no existe
        """
        user = await UserModel.get(user_id)
        if user is None:
            raise NotFoundException(resource="User", field="id", value=str(user_id))

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role_id=user.role_id,
            farm_id=user.farm_id,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            last_updated=user.last_updated,
            last_login=user.last_login,
        )

    async def get_all_users(self, skip: int = 0, limit: int = 50) -> list[UserResponse]:
        """
        Obtiene todos los usuarios con paginación.

        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar

        Returns:
            Lista de UserResponse
        """
        users = await UserModel.find_all().skip(skip).limit(limit).to_list()
        return [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                role_id=user.role_id,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                last_updated=user.last_updated,
                last_login=user.last_login,
            )
            for user in users
        ]

    async def update_user(
        self, user_id: UUID, request: UserUpdateRequest
    ) -> UserResponse:
        """
        Actualiza un usuario.

        Args:
            user_id: ID del usuario
            request: Datos a actualizar

        Returns:
            UserResponse con el usuario actualizado

        Raises:
            NotFoundException: Si el usuario no existe
            AlreadyExistsException: Si el email ya existe
        """
        user = await UserModel.get(user_id)
        if user is None:
            raise NotFoundException(resource="User", field="id", value=str(user_id))

        # Validar email único si se está actualizando
        if request.email is not None and request.email != user.email:
            existing_email = await UserModel.find_one(UserModel.email == request.email)
            if existing_email is not None:
                raise AlreadyExistsException(
                    resource="User", field="email", value=request.email
                )
            user.email = request.email

        # Actualizar contraseña si se proporciona
        if request.password is not None:
            user.hashed_password = self.auth_service.get_password_hash(request.password)

        # Actualizar rol si se proporciona
        if request.role_id is not None:
            role = await RoleModel.find_one(RoleModel.id == request.role_id)
            if role is None:
                raise NotFoundException(
                    resource="Role", field="id", value=str(request.role_id)
                )
            user.role_id = request.role_id

        # Actualizar finca si se proporciona
        if request.farm_id is not None:
            farm = await FarmModel.get(request.farm_id)
            if farm is None:
                raise NotFoundException(
                    resource="Farm", field="id", value=str(request.farm_id)
                )
            user.farm_id = request.farm_id

        # Actualizar estado activo si se proporciona
        if request.is_active is not None:
            user.is_active = request.is_active

        user.update_timestamp()
        await user.save()

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role_id=user.role_id,
            farm_id=user.farm_id,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            last_updated=user.last_updated,
            last_login=user.last_login,
        )

    async def delete_user(self, user_id: UUID) -> None:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario

        Raises:
            NotFoundException: Si el usuario no existe
        """
        user = await UserModel.get(user_id)
        if user is None:
            raise NotFoundException(resource="User", field="id", value=str(user_id))

        await user.delete()
