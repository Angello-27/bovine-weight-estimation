"""
Core Dependencies - Dependency Injection
Dependencias centralizadas para inyección en toda la aplicación

NOTA: Estas dependencias son específicas de FastAPI (Depends), pero se colocan
en core/ porque son infraestructura compartida que puede ser usada por
múltiples capas de presentación (API REST, GraphQL, etc.)
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application import AuthService
from app.core.exceptions import AuthenticationException
from app.data.repositories.animal_repository_impl import AnimalRepositoryImpl
from app.data.repositories.farm_repository_impl import FarmRepositoryImpl
from app.data.repositories.role_repository_impl import RoleRepositoryImpl
from app.data.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.entities.user import User
from app.domain.repositories.animal_repository import AnimalRepository
from app.domain.repositories.farm_repository import FarmRepository
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.usecases.animals import (
    CreateAnimalUseCase,
    DeleteAnimalUseCase,
    GetAnimalByIdUseCase,
    GetAnimalsByFarmUseCase,
    UpdateAnimalUseCase,
)
from app.domain.usecases.auth import GetUserByTokenUseCase
from app.domain.usecases.farms import (
    CreateFarmUseCase,
    DeleteFarmUseCase,
    GetAllFarmsUseCase,
    GetFarmByIdUseCase,
    UpdateFarmUseCase,
)
from app.domain.usecases.roles import (
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetAllRolesUseCase,
    GetRoleByIdUseCase,
    UpdateRoleUseCase,
)
from app.domain.usecases.users import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
)
from app.schemas.auth_schemas import TokenData

# Security scheme para JWT Bearer tokens
security = HTTPBearer()

# ==================== Repository Dependencies ====================


def get_user_repository() -> UserRepository:
    """Dependency para obtener UserRepository."""
    return UserRepositoryImpl()


def get_role_repository() -> RoleRepository:
    """Dependency para obtener RoleRepository."""
    return RoleRepositoryImpl()


def get_farm_repository() -> FarmRepository:
    """Dependency para obtener FarmRepository."""
    return FarmRepositoryImpl()


def get_animal_repository() -> AnimalRepository:
    """Dependency para obtener AnimalRepository."""
    return AnimalRepositoryImpl()


# ==================== Auth Dependencies ====================


def get_get_user_by_token_usecase(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetUserByTokenUseCase:
    """Dependency para GetUserByTokenUseCase."""
    return GetUserByTokenUseCase(user_repository=user_repository)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    get_user_by_token_usecase: Annotated[
        GetUserByTokenUseCase, Depends(get_get_user_by_token_usecase)
    ],
) -> User:
    """
    Dependency para obtener el usuario actual desde el token JWT.

    Args:
        credentials: Credenciales del header Authorization
        get_user_by_token_usecase: Caso de uso para obtener usuario por token

    Returns:
        User entity del dominio

    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    try:
        # Decodificar token usando AuthService (solo para decodificación)
        auth_service = AuthService()
        token_data: TokenData = auth_service.decode_access_token(
            credentials.credentials
        )

        if token_data.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Usar caso de uso directamente para obtener usuario
        return await get_user_by_token_usecase.execute(token_data.user_id)

    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error al validar token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency para obtener usuario activo.

    Args:
        current_user: Usuario actual

    Returns:
        User entity del dominio activo

    Raises:
        HTTPException 403: Si el usuario no está activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo"
        )
    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependency para obtener usuario superusuario.

    Args:
        current_user: Usuario actual

    Returns:
        User entity del dominio superusuario

    Raises:
        HTTPException 403: Si el usuario no es superusuario
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes",
        )
    return current_user


# ==================== User Use Cases ====================


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


# ==================== Role Use Cases ====================


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


# ==================== Farm Use Cases ====================


def get_create_farm_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> CreateFarmUseCase:
    """Dependency para CreateFarmUseCase."""
    return CreateFarmUseCase(
        farm_repository=farm_repository, user_repository=user_repository
    )


def get_get_farm_by_id_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> GetFarmByIdUseCase:
    """Dependency para GetFarmByIdUseCase."""
    return GetFarmByIdUseCase(farm_repository=farm_repository)


def get_get_all_farms_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> GetAllFarmsUseCase:
    """Dependency para GetAllFarmsUseCase."""
    return GetAllFarmsUseCase(farm_repository=farm_repository)


def get_update_farm_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> UpdateFarmUseCase:
    """Dependency para UpdateFarmUseCase."""
    return UpdateFarmUseCase(farm_repository=farm_repository)


def get_delete_farm_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> DeleteFarmUseCase:
    """Dependency para DeleteFarmUseCase."""
    return DeleteFarmUseCase(farm_repository=farm_repository)


# ==================== Animal Use Cases ====================


def get_create_animal_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> CreateAnimalUseCase:
    """Dependency para CreateAnimalUseCase."""
    return CreateAnimalUseCase(animal_repository=animal_repository)


def get_get_animal_by_id_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> GetAnimalByIdUseCase:
    """Dependency para GetAnimalByIdUseCase."""
    return GetAnimalByIdUseCase(animal_repository=animal_repository)


def get_get_animals_by_farm_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> GetAnimalsByFarmUseCase:
    """Dependency para GetAnimalsByFarmUseCase."""
    return GetAnimalsByFarmUseCase(animal_repository=animal_repository)


def get_update_animal_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> UpdateAnimalUseCase:
    """Dependency para UpdateAnimalUseCase."""
    return UpdateAnimalUseCase(animal_repository=animal_repository)


def get_delete_animal_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> DeleteAnimalUseCase:
    """Dependency para DeleteAnimalUseCase."""
    return DeleteAnimalUseCase(animal_repository=animal_repository)


__all__ = [
    # Repositories
    "get_user_repository",
    "get_role_repository",
    "get_farm_repository",
    "get_animal_repository",
    # Auth
    "get_get_user_by_token_usecase",
    "get_current_user",
    "get_current_active_user",
    "get_current_superuser",
    "security",
    # User Use Cases
    "get_create_user_usecase",
    "get_get_user_by_id_usecase",
    "get_get_all_users_usecase",
    "get_update_user_usecase",
    "get_delete_user_usecase",
    # Role Use Cases
    "get_create_role_usecase",
    "get_get_role_by_id_usecase",
    "get_get_all_roles_usecase",
    "get_update_role_usecase",
    "get_delete_role_usecase",
    # Farm Use Cases
    "get_create_farm_usecase",
    "get_get_farm_by_id_usecase",
    "get_get_all_farms_usecase",
    "get_update_farm_usecase",
    "get_delete_farm_usecase",
    # Animal Use Cases
    "get_create_animal_usecase",
    "get_get_animal_by_id_usecase",
    "get_get_animals_by_farm_usecase",
    "get_update_animal_usecase",
    "get_delete_animal_usecase",
]
