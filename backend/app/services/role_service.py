"""
Role Service - Business Logic
Lógica de negocio para gestión de roles
"""

from uuid import UUID

from ..core.exceptions import AlreadyExistsException, NotFoundException
from ..models import RoleModel
from ..schemas.role_schemas import (
    RoleCreateRequest,
    RoleResponse,
    RoleUpdateRequest,
)


class RoleService:
    """
    Servicio de gestión de roles.

    Single Responsibility: Business logic de roles.
    """

    async def create_role(self, request: RoleCreateRequest) -> RoleResponse:
        """
        Crea un nuevo rol.

        Args:
            request: Datos del rol a crear

        Returns:
            RoleResponse con el rol creado

        Raises:
            AlreadyExistsException: Si el nombre del rol ya existe
        """
        # Validar que el nombre no exista
        existing = await RoleModel.find_one(RoleModel.name == request.name)
        if existing is not None:
            raise AlreadyExistsException(
                resource="Role", field="name", value=request.name
            )

        # Crear rol
        role = RoleModel(
            name=request.name,
            description=request.description,
            priority=request.priority,
            permissions=request.permissions or [],
        )
        await role.insert()

        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            priority=role.priority,
            permissions=role.permissions,
            created_at=role.created_at,
            last_updated=role.last_updated,
        )

    async def get_role_by_id(self, role_id: UUID) -> RoleResponse:
        """
        Obtiene un rol por ID.

        Args:
            role_id: ID del rol

        Returns:
            RoleResponse con el rol

        Raises:
            NotFoundException: Si el rol no existe
        """
        role = await RoleModel.get(role_id)
        if role is None:
            raise NotFoundException(resource="Role", field="id", value=str(role_id))

        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            priority=role.priority,
            permissions=role.permissions,
            created_at=role.created_at,
            last_updated=role.last_updated,
        )

    async def get_all_roles(self, skip: int = 0, limit: int = 50) -> list[RoleResponse]:
        """
        Obtiene todos los roles con paginación.

        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar

        Returns:
            Lista de RoleResponse
        """
        roles = await RoleModel.find_all().skip(skip).limit(limit).to_list()
        return [
            RoleResponse(
                id=role.id,
                name=role.name,
                description=role.description,
                priority=role.priority,
                permissions=role.permissions,
                created_at=role.created_at,
                last_updated=role.last_updated,
            )
            for role in roles
        ]

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

        Raises:
            NotFoundException: Si el rol no existe
            AlreadyExistsException: Si el nombre ya existe
        """
        role = await RoleModel.get(role_id)
        if role is None:
            raise NotFoundException(resource="Role", field="id", value=str(role_id))

        # Validar nombre único si se está actualizando
        if request.name is not None and request.name != role.name:
            existing = await RoleModel.find_one(RoleModel.name == request.name)
            if existing is not None:
                raise AlreadyExistsException(
                    resource="Role", field="name", value=request.name
                )
            role.name = request.name

        # Actualizar otros campos
        if request.description is not None:
            role.description = request.description
        if request.priority is not None:
            role.priority = request.priority
        if request.permissions is not None:
            role.permissions = request.permissions

        role.update_timestamp()
        await role.save()

        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            priority=role.priority,
            permissions=role.permissions,
            created_at=role.created_at,
            last_updated=role.last_updated,
        )

    async def delete_role(self, role_id: UUID) -> None:
        """
        Elimina un rol.

        Args:
            role_id: ID del rol

        Raises:
            NotFoundException: Si el rol no existe
        """
        role = await RoleModel.get(role_id)
        if role is None:
            raise NotFoundException(resource="Role", field="id", value=str(role_id))

        await role.delete()
