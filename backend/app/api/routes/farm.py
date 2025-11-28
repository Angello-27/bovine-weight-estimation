"""
Farm Routes - API Endpoints
Endpoints REST para gestión de fincas
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ...api.dependencies import get_current_active_user
from ...core.errors import AlreadyExistsException, NotFoundException
from ...models import FarmModel, UserModel
from ...schemas.farm_schemas import (
    FarmCreateRequest,
    FarmResponse,
    FarmsListResponse,
    FarmUpdateRequest,
)
from ...services import FarmService

# Router con prefijo /farm
router = APIRouter(
    prefix="/farm",
    tags=["Fincas"],
    responses={
        404: {"description": "Finca no encontrada"},
        400: {"description": "Request inválido"},
        401: {"description": "No autenticado"},
        403: {"description": "Sin permisos"},
        500: {"description": "Error interno del servidor"},
    },
)


# Dependency injection del servicio
def get_farm_service() -> FarmService:
    """Dependency para inyectar FarmService."""
    return FarmService()


@router.post(
    "",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear finca",
    description="""
    Crea una nueva finca en el sistema.

    **Validaciones**:
    - Nombre debe ser único por propietario
    - Owner ID debe existir
    - Coordenadas GPS válidas
    - Capacidad mínima: 1 animal

    **Permisos**: Requiere autenticación
    """,
)
async def create_farm(
    request: FarmCreateRequest,
    farm_service: Annotated[FarmService, Depends(get_farm_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> FarmResponse:
    """
    Endpoint para crear una finca.

    Args:
        request: Datos de la finca a crear
        farm_service: Servicio de fincas (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        FarmResponse con la finca creada

    Raises:
        HTTPException 400: Si el nombre ya existe para ese propietario
        HTTPException 404: Si el owner_id no existe
    """
    try:
        return await farm_service.create_farm(request)
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "",
    response_model=FarmsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar fincas",
    description="""
    Obtiene una lista de fincas con paginación.

    **Filtros**:
    - owner_id: Filtrar por propietario (opcional)

    **Permisos**: Requiere autenticación
    """,
)
async def get_all_farms(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    owner_id: UUID | None = Query(None, description="Filtrar por propietario"),
    farm_service: Annotated[FarmService, Depends(get_farm_service)] = None,
    current_user: Annotated[UserModel, Depends(get_current_active_user)] = None,
) -> FarmsListResponse:
    """
    Endpoint para listar fincas.

    Args:
        skip: Número de registros a saltar
        limit: Número máximo de registros
        owner_id: Filtrar por propietario (opcional)
        farm_service: Servicio de fincas (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        FarmsListResponse con lista de fincas
    """
    farms = await farm_service.get_all_farms(skip=skip, limit=limit, owner_id=owner_id)
    total = await FarmModel.find_all().count() if owner_id is None else await FarmModel.find(FarmModel.owner_id == owner_id).count()
    return FarmsListResponse(total=total, farms=farms, page=skip // limit + 1, page_size=limit)


@router.get(
    "/{farm_id}",
    response_model=FarmResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener finca por ID",
    description="""
    Obtiene una finca específica por su ID.

    **Permisos**: Requiere autenticación
    """,
)
async def get_farm(
    farm_id: UUID,
    farm_service: Annotated[FarmService, Depends(get_farm_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> FarmResponse:
    """
    Endpoint para obtener una finca por ID.

    Args:
        farm_id: ID de la finca
        farm_service: Servicio de fincas (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        FarmResponse con la finca

    Raises:
        HTTPException 404: Si la finca no existe
    """
    try:
        return await farm_service.get_farm_by_id(farm_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put(
    "/{farm_id}",
    response_model=FarmResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar finca",
    description="""
    Actualiza una finca existente.

    **Validaciones**:
    - Nombre debe ser único por propietario
    - Capacidad no puede ser menor que total_animals actual

    **Permisos**: Requiere autenticación
    """,
)
async def update_farm(
    farm_id: UUID,
    request: FarmUpdateRequest,
    farm_service: Annotated[FarmService, Depends(get_farm_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> FarmResponse:
    """
    Endpoint para actualizar una finca.

    Args:
        farm_id: ID de la finca
        request: Datos a actualizar
        farm_service: Servicio de fincas (inyectado)
        current_user: Usuario actual (inyectado)

    Returns:
        FarmResponse con la finca actualizada

    Raises:
        HTTPException 404: Si la finca no existe
        HTTPException 400: Si el nombre ya existe o capacidad inválida
    """
    try:
        return await farm_service.update_farm(farm_id, request)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (AlreadyExistsException, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete(
    "/{farm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar finca",
    description="""
    Elimina una finca del sistema.

    **Validaciones**:
    - La finca no debe tener animales registrados

    **Permisos**: Requiere autenticación
    """,
)
async def delete_farm(
    farm_id: UUID,
    farm_service: Annotated[FarmService, Depends(get_farm_service)],
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> None:
    """
    Endpoint para eliminar una finca.

    Args:
        farm_id: ID de la finca
        farm_service: Servicio de fincas (inyectado)
        current_user: Usuario actual (inyectado)

    Raises:
        HTTPException 404: Si la finca no existe
        HTTPException 400: Si la finca tiene animales registrados
    """
    try:
        await farm_service.delete_farm(farm_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

