"""
Role Routes - API Endpoints
Endpoints REST para gestión de roles
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from ...core.dependencies import (
    get_create_role_usecase,
    get_current_active_user,
    get_delete_role_usecase,
    get_get_all_roles_usecase,
    get_get_role_by_id_usecase,
    get_update_role_usecase,
)
from ...domain.entities.user import User
from ...domain.usecases.roles import (
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetAllRolesUseCase,
    GetRoleByIdUseCase,
    UpdateRoleUseCase,
)
from ...schemas.role_schemas import (
    RoleCreateRequest,
    RoleResponse,
    RolesListResponse,
    RoleUpdateRequest,
)
from ..mappers import RoleMapper
from ..utils import handle_domain_exceptions

# Router con prefijo /role
router = APIRouter(
    prefix="/role",
    tags=["Roles"],
    responses={
        404: {"description": "Rol no encontrado"},
        400: {"description": "Request inválido"},
        401: {"description": "No autenticado"},
        403: {"description": "Sin permisos"},
        500: {"description": "Error interno del servidor"},
    },
)


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear rol",
    description="""
    Crea un nuevo rol en el sistema.

    **Validaciones**:
    - Nombre debe ser único
    - Priority por defecto: "Invitado"

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def create_role(
    request: RoleCreateRequest,
    create_usecase: Annotated[CreateRoleUseCase, Depends(get_create_role_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> RoleResponse:
    """Crea un nuevo rol."""
    params = RoleMapper.create_request_to_params(request)
    role = await create_usecase.execute(**params)
    return RoleMapper.to_response(role)


@router.get(
    "",
    response_model=RolesListResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar roles",
    description="""
    Obtiene una lista de roles con paginación.

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def get_all_roles(
    current_user: Annotated[User, Depends(get_current_active_user)],
    get_all_usecase: Annotated[GetAllRolesUseCase, Depends(get_get_all_roles_usecase)],
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
) -> RolesListResponse:
    """Lista roles con paginación."""
    roles = await get_all_usecase.execute(skip=skip, limit=limit)
    # TODO: Agregar método count() al repositorio para obtener total
    total = len(roles)
    return RolesListResponse(
        total=total,
        roles=[RoleMapper.to_response(role) for role in roles],
        page=skip // limit + 1,
        page_size=limit,
    )


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener rol por ID",
    description="""
    Obtiene un rol específico por su ID.

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def get_role(
    role_id: UUID,
    get_by_id_usecase: Annotated[
        GetRoleByIdUseCase, Depends(get_get_role_by_id_usecase)
    ],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> RoleResponse:
    """Obtiene un rol por ID."""
    role = await get_by_id_usecase.execute(role_id)
    return RoleMapper.to_response(role)


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar rol",
    description="""
    Actualiza un rol existente.

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def update_role(
    role_id: UUID,
    request: RoleUpdateRequest,
    update_usecase: Annotated[UpdateRoleUseCase, Depends(get_update_role_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> RoleResponse:
    """Actualiza un rol."""
    params = RoleMapper.update_request_to_params(request)
    role = await update_usecase.execute(role_id=role_id, **params)
    return RoleMapper.to_response(role)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar rol",
    description="""
    Elimina un rol del sistema.

    **Permisos**: Requiere autenticación
    """,
)
async def delete_role(
    role_id: UUID,
    delete_usecase: Annotated[DeleteRoleUseCase, Depends(get_delete_role_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    """Elimina un rol."""
    from ...core.exceptions import NotFoundException

    try:
        await delete_usecase.execute(role_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
