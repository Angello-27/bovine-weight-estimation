"""
Auth Routes - API Endpoints
Endpoints REST para autenticación
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ...application import AuthService
from ...core.exceptions import AuthenticationException
from ...schemas.auth_schemas import LoginRequest, LoginResponse

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


# Dependency injection del servicio
def get_auth_service() -> AuthService:
    """Dependency para inyectar AuthService."""
    return AuthService()


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
async def login(
    login_data: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResponse:
    """
    Endpoint para iniciar sesión.

    Args:
        login_data: Credenciales de login
        auth_service: Servicio de autenticación (inyectado)

    Returns:
        LoginResponse con token y datos del usuario

    Raises:
        HTTPException 401: Si las credenciales son inválidas
    """
    try:
        return await auth_service.authenticate_user(login_data)
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
