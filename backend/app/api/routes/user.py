"""
User Routes - API Endpoints
Endpoints REST para gestión de usuarios
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ...core.dependencies import (
    get_create_user_usecase,
    get_current_active_user,
    get_delete_user_usecase,
    get_get_all_users_usecase,
    get_get_user_by_id_usecase,
    get_get_users_by_criteria_usecase,
    get_update_user_usecase,
)
from ...core.utils.password import get_password_hash
from ...domain.entities.user import User
from ...domain.usecases.users import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    GetUsersByCriteriaUseCase,
    UpdateUserUseCase,
)
from ...schemas.user_schemas import (
    UserCreateRequest,
    UserResponse,
    UsersListResponse,
    UserUpdateRequest,
)
from ..mappers import UserMapper
from ..utils import handle_domain_exceptions

# Router con prefijo /api/v1/users
router = APIRouter(
    prefix="/api/v1/users",
    tags=["Usuarios"],
    responses={
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Request inválido"},
        401: {"description": "No autenticado"},
        403: {"description": "Sin permisos"},
        500: {"description": "Error interno del servidor"},
    },
)


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
@handle_domain_exceptions
async def create_user(
    request: UserCreateRequest,
    create_usecase: Annotated[CreateUserUseCase, Depends(get_create_user_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """Crea un nuevo usuario."""
    # Hash de contraseña
    hashed_password = get_password_hash(request.password)

    # Convertir request a parámetros y ejecutar use case
    params = UserMapper.create_request_to_params(request, hashed_password)
    user = await create_usecase.execute(**params)

    # Convertir entity a response
    return UserMapper.to_response(user)


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
@handle_domain_exceptions
async def get_all_users(
    current_user: Annotated[User, Depends(get_current_active_user)],
    get_all_usecase: Annotated[GetAllUsersUseCase, Depends(get_get_all_users_usecase)],
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
) -> UsersListResponse:
    """Lista usuarios con paginación."""
    users = await get_all_usecase.execute(skip=skip, limit=limit)
    # TODO: Agregar método count() al repositorio para obtener total
    total = len(users)
    return UsersListResponse(
        total=total,
        users=[UserMapper.to_response(user) for user in users],
        page=skip // limit + 1,
        page_size=limit,
    )


@router.get(
    "/by-criteria",
    response_model=UsersListResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar usuarios por criterios",
    description="""
    Busca usuarios aplicando filtros específicos.

    **Filtros disponibles**:
    - `role_id` (UUID, opcional): Filtrar por ID de rol
    - `is_active` (bool, opcional): Filtrar por estado activo/inactivo
    - `farm_id` (UUID, opcional): Filtrar por ID de finca asignada

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def get_users_by_criteria(
    current_user: Annotated[User, Depends(get_current_active_user)],
    get_by_criteria_usecase: Annotated[
        GetUsersByCriteriaUseCase, Depends(get_get_users_by_criteria_usecase)
    ],
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    role_id: UUID | None = Query(None, description="Filtrar por ID de rol"),
    is_active: bool | None = Query(None, description="Filtrar por estado activo"),
    farm_id: UUID | None = Query(None, description="Filtrar por ID de finca"),
) -> UsersListResponse:
    """Busca usuarios por criterios de filtrado."""
    filters: dict[str, Any] = {}
    if role_id is not None:
        filters["role_id"] = role_id
    if is_active is not None:
        filters["is_active"] = is_active
    if farm_id is not None:
        filters["farm_id"] = farm_id

    users, total = await get_by_criteria_usecase.execute(
        filters=filters, skip=skip, limit=limit
    )
    return UsersListResponse(
        total=total,
        users=[UserMapper.to_response(user) for user in users],
        page=skip // limit + 1,
        page_size=limit,
    )


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
@handle_domain_exceptions
async def get_user(
    user_id: UUID,
    get_by_id_usecase: Annotated[
        GetUserByIdUseCase, Depends(get_get_user_by_id_usecase)
    ],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """Obtiene un usuario por ID."""
    user = await get_by_id_usecase.execute(user_id)
    return UserMapper.to_response(user)


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
@handle_domain_exceptions
async def update_user(
    user_id: UUID,
    request: UserUpdateRequest,
    update_usecase: Annotated[UpdateUserUseCase, Depends(get_update_user_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """Actualiza un usuario."""
    # Hash de contraseña si se proporciona
    hashed_password = None
    if request.password is not None:
        hashed_password = get_password_hash(request.password)

    # Convertir request a parámetros y ejecutar use case
    params = UserMapper.update_request_to_params(request, hashed_password)
    user = await update_usecase.execute(user_id=user_id, **params)

    # Convertir entity a response
    return UserMapper.to_response(user)


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
    delete_usecase: Annotated[DeleteUserUseCase, Depends(get_delete_user_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    """Elimina un usuario."""
    from ...core.exceptions import NotFoundException

    try:
        await delete_usecase.execute(user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
