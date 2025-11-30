"""
Role Service - Business Logic (Refactorizado para Clean Architecture)
Orquesta casos de uso del dominio
"""

from uuid import UUID

from ..data.repositories.role_repository_impl import RoleRepositoryImpl
from ..domain.repositories.role_repository import RoleRepository
from ..domain.usecases.roles import (
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetAllRolesUseCase,
    GetRoleByIdUseCase,
    UpdateRoleUseCase,
)
from ..schemas.role_schemas import (
    RoleCreateRequest,
    RoleResponse,
    RoleUpdateRequest,
)


class RoleService:
    """
    Servicio de gestión de roles (refactorizado).

    Single Responsibility: Orquestar casos de uso y convertir entre capas.
    Ahora usa Clean Architecture con Use Cases.
    """

    def __init__(self, role_repository: RoleRepository | None = None):
        """
        Inicializa el servicio.

        Args:
            role_repository: Repositorio de roles (inyección de dependencia)
        """
        self._repository = role_repository or RoleRepositoryImpl()

        # Inicializar use cases
        self._create_usecase = CreateRoleUseCase(self._repository)
        self._get_by_id_usecase = GetRoleByIdUseCase(self._repository)
        self._get_all_usecase = GetAllRolesUseCase(self._repository)
        self._update_usecase = UpdateRoleUseCase(self._repository)
        self._delete_usecase = DeleteRoleUseCase(self._repository)

    async def create_role(self, request: RoleCreateRequest) -> RoleResponse:
        """
        Crea un nuevo rol.

        Args:
            request: Datos del rol a crear

        Returns:
            RoleResponse con el rol creado
        """
        role = await self._create_usecase.execute(
            name=request.name,
            description=request.description,
            priority=request.priority,
            permissions=request.permissions,
        )

        return self._entity_to_response(role)

    async def get_role_by_id(self, role_id: UUID) -> RoleResponse:
        """
        Obtiene un rol por ID.

        Args:
            role_id: ID del rol

        Returns:
            RoleResponse
        """
        role = await self._get_by_id_usecase.execute(role_id)
        return self._entity_to_response(role)

    async def get_all_roles(
        self, skip: int = 0, limit: int = 50
    ) -> list[RoleResponse]:
        """
        Obtiene todos los roles con paginación.

        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar

        Returns:
            Lista de RoleResponse
        """
        roles = await self._get_all_usecase.execute(skip=skip, limit=limit)
        return [self._entity_to_response(role) for role in roles]

    async def update_role(
        self, role_id: UUID, request: RoleUpdateRequest
    ) -> RoleResponse:
        """
        Actualiza un rol.

        Args:
            role_id: ID del rol
            request: Datos a actualizar

        Returns:
            RoleResponse con el rol actualizado
        """
        role = await self._update_usecase.execute(
            role_id=role_id,
            name=request.name,
            description=request.description,
            priority=request.priority,
            permissions=request.permissions,
        )

        return self._entity_to_response(role)

    async def delete_role(self, role_id: UUID) -> None:
        """
        Elimina un rol.

        Args:
            role_id: ID del rol
        """
        await self._delete_usecase.execute(role_id)

    def _entity_to_response(self, role) -> RoleResponse:
        """
        Convierte entidad Role a RoleResponse.

        Args:
            role: Entidad Role del dominio

        Returns:
            RoleResponse
        """
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            priority=role.priority,
            permissions=role.permissions,
            created_at=role.created_at,
            last_updated=role.last_updated,
        )
