"""
User Routes - API Endpoints
Endpoints REST para gestión de usuarios
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ...api.dependencies import get_current_active_user
from ...core.errors import AlreadyExistsException, NotFoundException
from ...models import UserModel
from ...schemas.user_schemas import (
    UserCreateRequest,
    UserResponse,
    UsersListResponse,
    UserUpdateRequest,
)
from ...services import UserService

# Router con prefijo /user
router = APIRouter(
    prefix="/user",
    tags=["Usuarios"],
    responses={
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Request inválido"},
        401: {"description": "No autenticado"},
        403: {"description": "Sin permisos"},
        500: {"description": "Error interno del servidor"},
    },
)


# Dependency injection del servicio
def get_user_service() -> UserService:
    """Dependency para inyectar UserService."""
    return UserService()


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="""
    Crea un nuevo usuario en el sistema.

    **Validaciones**:
    - Username debe ser único
    - Email debe ser único
    - Password mínimo 6 caracteres
    - Role ID debe existir

    **Permisos**: Requiere autenticación
    """,
)
async def create_user(
    request: UserCreateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Endpoint para crear un usuario.

    Args:
        request: Datos del usuario a crear
        user_service: Servicio de usuarios (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        UserResponse con el usuario creado

    Raises:
        HTTPException 400: Si el usuario o email ya existe
        HTTPException 404: Si el rol no existe
    """
    try:
        return await user_service.create_user(request)
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "",
    response_model=UsersListResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="""
    Obtiene una lista de usuarios con paginación.

    **Permisos**: Requiere autenticación
    """,
)
async def get_all_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    user_service: Annotated[UserService, Depends(get_user_service)] = None,
    current_user: Annotated[UserModel, Depends(get_current_active_user)] = None,
) -> UsersListResponse:
    """
    Endpoint para listar usuarios.

    Args:
        skip: Número de registros a saltar
        limit: Número máximo de registros
        user_service: Servicio de usuarios (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        UsersListResponse con lista de usuarios
    """
    users = await user_service.get_all_users(skip=skip, limit=limit)
    total = await UserModel.find_all().count()
    return UsersListResponse(total=total, users=users, page=skip // limit + 1, page_size=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="""
    Obtiene un usuario específico por su ID.

    **Permisos**: Requiere autenticación
    """,
)
async def get_user(
    user_id: UUID,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Endpoint para obtener un usuario por ID.

    Args:
        user_id: ID del usuario
        user_service: Servicio de usuarios (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        UserResponse con el usuario

    Raises:
        HTTPException 404: Si el usuario no existe
    """
    try:
        return await user_service.get_user_by_id(user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario",
    description="""
    Actualiza un usuario existente.

    **Permisos**: Requiere autenticación
    """,
)
async def update_user(
    user_id: UUID,
    request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Endpoint para actualizar un usuario.

    Args:
        user_id: ID del usuario
        request: Datos a actualizar
        user_service: Servicio de usuarios (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        UserResponse con el usuario actualizado

    Raises:
        HTTPException 404: Si el usuario no existe
        HTTPException 400: Si el email ya existe
    """
    try:
        return await user_service.update_user(user_id, request)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="""
    Elimina un usuario del sistema.

    **Permisos**: Requiere autenticación
    """,
)
async def delete_user(
    user_id: UUID,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> None:
    """
    Endpoint para eliminar un usuario.

    Args:
        user_id: ID del usuario
        user_service: Servicio de usuarios (inyectado)
        current_user: Usuario actual (inyectado)

    Raises:
        HTTPException 404: Si el usuario no existe
    """
    try:
        await user_service.delete_user(user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

