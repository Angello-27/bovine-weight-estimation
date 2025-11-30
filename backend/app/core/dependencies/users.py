"""
User Use Cases Dependencies
Dependencias para inyectar use cases de usuarios
"""

from typing import Annotated

from fastapi import Depends

from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.usecases.users import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
)

from .repositories import get_role_repository, get_user_repository


def get_create_user_usecase(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> CreateUserUseCase:
    """Dependency para CreateUserUseCase."""
    return CreateUserUseCase(
        user_repository=user_repository, role_repository=role_repository
    )


def get_get_user_by_id_usecase(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetUserByIdUseCase:
    """Dependency para GetUserByIdUseCase."""
    return GetUserByIdUseCase(user_repository=user_repository)


def get_get_all_users_usecase(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetAllUsersUseCase:
    """Dependency para GetAllUsersUseCase."""
    return GetAllUsersUseCase(user_repository=user_repository)


def get_update_user_usecase(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> UpdateUserUseCase:
    """Dependency para UpdateUserUseCase."""
    return UpdateUserUseCase(
        user_repository=user_repository, role_repository=role_repository
    )


def get_delete_user_usecase(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> DeleteUserUseCase:
    """Dependency para DeleteUserUseCase."""
    return DeleteUserUseCase(user_repository=user_repository)
