"""
Auth Routes - API Endpoints
Endpoints REST para autenticación
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status

from ...core.config import settings
from ...core.dependencies import get_authenticate_user_usecase
from ...core.utils.jwt import create_access_token
from ...domain.usecases.auth import AuthenticateUserUseCase
from ...schemas.auth_schemas import LoginRequest, LoginResponse
from ..mappers import AuthMapper
from ..utils import handle_domain_exceptions

# Router con prefijo /auth
router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
    responses={
        401: {"description": "Credenciales inválidas"},
        400: {"description": "Request inválido"},
        500: {"description": "Error interno del servidor"},
    },
)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="""
    Autentica un usuario y retorna un token JWT.

    **Request**:
    - username: Nombre de usuario
    - password: Contraseña

    **Response**:
    - id: ID del usuario
    - username: Nombre de usuario
    - role: Nombre del rol
    - role_id: ID del rol
    - access_token: Token JWT para autenticación
    - token_type: Tipo de token (bearer)

    **Errores**:
    - 401: Credenciales inválidas
    - 400: Request inválido
    """,
)
@handle_domain_exceptions
async def login(
    login_data: LoginRequest,
    authenticate_usecase: Annotated[
        AuthenticateUserUseCase, Depends(get_authenticate_user_usecase)
    ] = Depends(get_authenticate_user_usecase),
) -> LoginResponse:
    """
    Endpoint para iniciar sesión.

    Args:
        login_data: Credenciales de login
        authenticate_usecase: Caso de uso de autenticación (inyectado)

    Returns:
        LoginResponse con token y datos del usuario

    Raises:
        HTTPException 401: Si las credenciales son inválidas
    """
    # Autenticar usuario usando el use case
    user, role = await authenticate_usecase.execute(
        username=login_data.username,
        password=login_data.password,
    )

    # Crear token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires,
    )

    # Usar mapper para convertir a LoginResponse
    return AuthMapper.to_login_response(user, role, access_token)
