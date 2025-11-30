"""
User Service - Business Logic (Refactorizado para Clean Architecture)
Orquesta casos de uso del dominio
"""

from uuid import UUID

from ..data.repositories.role_repository_impl import RoleRepositoryImpl
from ..data.repositories.user_repository_impl import UserRepositoryImpl
from ..domain.repositories.role_repository import RoleRepository
from ..domain.repositories.user_repository import UserRepository
from ..domain.usecases.users import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
)
from ..schemas.user_schemas import (
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)
from .auth_service import AuthService


class UserService:
    """
    Servicio de gestión de usuarios (refactorizado).

    Single Responsibility: Orquestar casos de uso y convertir entre capas.
    Ahora usa Clean Architecture con Use Cases.
    """

    def __init__(
        self,
        user_repository: UserRepository | None = None,
        role_repository: RoleRepository | None = None,
    ):
        """
        Inicializa el servicio.

        Args:
            user_repository: Repositorio de usuarios (inyección de dependencia)
            role_repository: Repositorio de roles (inyección de dependencia)
        """
        self._user_repository = user_repository or UserRepositoryImpl()
        self._role_repository = role_repository or RoleRepositoryImpl()
        self._auth_service = AuthService(
            user_repository=self._user_repository,
            role_repository=self._role_repository,
        )

        # Inicializar use cases
        self._create_usecase = CreateUserUseCase(
            user_repository=self._user_repository,
            role_repository=self._role_repository,
        )
        self._get_by_id_usecase = GetUserByIdUseCase(self._user_repository)
        self._get_all_usecase = GetAllUsersUseCase(self._user_repository)
        self._update_usecase = UpdateUserUseCase(
            user_repository=self._user_repository,
            role_repository=self._role_repository,
        )
        self._delete_usecase = DeleteUserUseCase(self._user_repository)

    async def create_user(self, request: UserCreateRequest) -> UserResponse:
        """
        Crea un nuevo usuario.

        Args:
            request: Datos del usuario a crear

        Returns:
            UserResponse con el usuario creado
        """
        # Hash de contraseña
        hashed_password = self._auth_service.get_password_hash(request.password)

        # Usar use case
        user = await self._create_usecase.execute(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            role_id=request.role_id,
            farm_id=request.farm_id,
        )

        return self._entity_to_response(user)

    async def get_user_by_id(self, user_id: UUID) -> UserResponse:
        """
        Obtiene un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            UserResponse
        """
        user = await self._get_by_id_usecase.execute(user_id)
        return self._entity_to_response(user)

    async def get_all_users(
        self, skip: int = 0, limit: int = 50
    ) -> list[UserResponse]:
        """
        Obtiene todos los usuarios con paginación.

        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar

        Returns:
            Lista de UserResponse
        """
        users = await self._get_all_usecase.execute(skip=skip, limit=limit)
        return [self._entity_to_response(user) for user in users]

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
        """
        # Hash de contraseña si se proporciona
        hashed_password = None
        if request.password is not None:
            hashed_password = self._auth_service.get_password_hash(request.password)

        # Usar use case
        user = await self._update_usecase.execute(
            user_id=user_id,
            email=request.email,
            hashed_password=hashed_password,
            role_id=request.role_id,
            farm_id=request.farm_id,
            is_active=request.is_active,
        )

        return self._entity_to_response(user)

    async def delete_user(self, user_id: UUID) -> None:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario
        """
        await self._delete_usecase.execute(user_id)

    def _entity_to_response(self, user) -> UserResponse:
        """
        Convierte entidad User a UserResponse.

        Args:
            user: Entidad User del dominio

        Returns:
            UserResponse con campos calculados
        """
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
