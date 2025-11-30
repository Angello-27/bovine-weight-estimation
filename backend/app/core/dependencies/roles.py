"""
Role Use Cases Dependencies
Dependencias para inyectar use cases de roles
"""

from typing import Annotated

from fastapi import Depends

from app.domain.repositories.role_repository import RoleRepository
from app.domain.usecases.roles import (
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetAllRolesUseCase,
    GetRoleByIdUseCase,
    UpdateRoleUseCase,
)

from .repositories import get_role_repository


def get_create_role_usecase(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> CreateRoleUseCase:
    """Dependency para CreateRoleUseCase."""
    return CreateRoleUseCase(role_repository=role_repository)


def get_get_role_by_id_usecase(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> GetRoleByIdUseCase:
    """Dependency para GetRoleByIdUseCase."""
    return GetRoleByIdUseCase(role_repository=role_repository)


def get_get_all_roles_usecase(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> GetAllRolesUseCase:
    """Dependency para GetAllRolesUseCase."""
    return GetAllRolesUseCase(role_repository=role_repository)


def get_update_role_usecase(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> UpdateRoleUseCase:
    """Dependency para UpdateRoleUseCase."""
    return UpdateRoleUseCase(role_repository=role_repository)


def get_delete_role_usecase(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> DeleteRoleUseCase:
    """Dependency para DeleteRoleUseCase."""
    return DeleteRoleUseCase(role_repository=role_repository)
