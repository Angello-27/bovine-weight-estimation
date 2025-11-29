"""
API Dependencies
Dependencias para autenticación y autorización en FastAPI
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..core.exceptions import AuthenticationException
from ..models import UserModel
from ..schemas.auth_schemas import TokenData
from ..services import AuthService

# Security scheme para JWT Bearer tokens
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_service: Annotated[AuthService, Depends(lambda: AuthService())],
) -> UserModel:
    """
    Dependency para obtener el usuario actual desde el token JWT.

    Args:
        credentials: Credenciales del header Authorization
        auth_service: Servicio de autenticación

    Returns:
        UserModel del usuario autenticado

    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    try:
        # Decodificar token
        token_data: TokenData = auth_service.decode_access_token(
            credentials.credentials
        )

        # Buscar usuario
        if token_data.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await UserModel.get(token_data.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo",
            )

        return user

    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:
    """
    Dependency para obtener usuario activo.

    Args:
        current_user: Usuario actual

    Returns:
        UserModel del usuario activo

    Raises:
        HTTPException 403: Si el usuario no está activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo"
        )
    return current_user


async def get_current_superuser(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:
    """
    Dependency para obtener usuario superusuario.

    Args:
        current_user: Usuario actual

    Returns:
        UserModel del superusuario

    Raises:
        HTTPException 403: Si el usuario no es superusuario
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes",
        )
    return current_user
