"""
Role Routes - API Endpoints
Endpoints REST para gestión de roles
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ...api.dependencies import get_current_active_user
from ...core.errors import AlreadyExistsException, NotFoundException
from ...models import RoleModel, UserModel
from ...schemas.role_schemas import (
    RoleCreateRequest,
    RoleResponse,
    RolesListResponse,
    RoleUpdateRequest,
)
from ...services import RoleService

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


# Dependency injection del servicio
def get_role_service() -> RoleService:
    """Dependency para inyectar RoleService."""
    return RoleService()


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
async def create_role(
    request: RoleCreateRequest,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> RoleResponse:
    """
    Endpoint para crear un rol.

    Args:
        request: Datos del rol a crear
        role_service: Servicio de roles (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        RoleResponse con el rol creado

    Raises:
        HTTPException 400: Si el nombre del rol ya existe
    """
    try:
        return await role_service.create_role(request)
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


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
async def get_all_roles(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    role_service: Annotated[RoleService, Depends(get_role_service)] = None,
    current_user: Annotated[UserModel, Depends(get_current_active_user)] = None,
) -> RolesListResponse:
    """
    Endpoint para listar roles.

    Args:
        skip: Número de registros a saltar
        limit: Número máximo de registros
        role_service: Servicio de roles (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        RolesListResponse con lista de roles
    """
    roles = await role_service.get_all_roles(skip=skip, limit=limit)
    total = await RoleModel.find_all().count()
    return RolesListResponse(total=total, roles=roles, page=skip // limit + 1, page_size=limit)


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
async def get_role(
    role_id: UUID,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> RoleResponse:
    """
    Endpoint para obtener un rol por ID.

    Args:
        role_id: ID del rol
        role_service: Servicio de roles (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        RoleResponse con el rol

    Raises:
        HTTPException 404: Si el rol no existe
    """
    try:
        return await role_service.get_role_by_id(role_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


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
async def update_role(
    role_id: UUID,
    request: RoleUpdateRequest,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> RoleResponse:
    """
    Endpoint para actualizar un rol.

    Args:
        role_id: ID del rol
        request: Datos a actualizar
        role_service: Servicio de roles (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        RoleResponse con el rol actualizado

    Raises:
        HTTPException 404: Si el rol no existe
        HTTPException 400: Si el nombre ya existe
    """
    try:
        return await role_service.update_role(role_id, request)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


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
    role_service: Annotated[RoleService, Depends(get_role_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> None:
    """
    Endpoint para eliminar un rol.

    Args:
        role_id: ID del rol
        role_service: Servicio de roles (inyectado)
        current_user: Usuario actual (inyectado)

    Raises:
        HTTPException 404: Si el rol no existe
    """
    try:
        await role_service.delete_role(role_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

