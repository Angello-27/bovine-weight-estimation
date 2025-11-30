"""
Auth Dependencies
Dependencias para autenticación y autorización
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthenticationException
from app.core.utils.jwt import decode_access_token
from app.core.utils.password import verify_password
from app.domain.entities.user import User
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.usecases.auth import AuthenticateUserUseCase, GetUserByTokenUseCase

from .repositories import get_role_repository, get_user_repository

# Security scheme para JWT Bearer tokens
security = HTTPBearer()


def get_authenticate_user_usecase(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> AuthenticateUserUseCase:
    """Dependency para AuthenticateUserUseCase."""
    return AuthenticateUserUseCase(
        user_repository=user_repository,
        role_repository=role_repository,
        password_verifier=verify_password,
    )


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
        # Decodificar token usando utilidad JWT
        token_data = decode_access_token(credentials.credentials)

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
