"""
Farm Routes - API Endpoints
Endpoints REST para gestión de fincas
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from ...core.dependencies import (
    get_create_farm_usecase,
    get_current_active_user,
    get_delete_farm_usecase,
    get_get_all_farms_usecase,
    get_get_farm_by_id_usecase,
    get_get_farms_by_criteria_usecase,
    get_update_farm_usecase,
)
from ...domain.entities.user import User
from ...domain.usecases.farms import (
    CreateFarmUseCase,
    DeleteFarmUseCase,
    GetAllFarmsUseCase,
    GetFarmByIdUseCase,
    GetFarmsByCriteriaUseCase,
    UpdateFarmUseCase,
)
from ...schemas.farm_schemas import (
    FarmCreateRequest,
    FarmResponse,
    FarmsListResponse,
    FarmUpdateRequest,
)
from ..mappers import FarmMapper
from ..utils import handle_domain_exceptions

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
@handle_domain_exceptions
async def create_farm(
    request: FarmCreateRequest,
    create_usecase: Annotated[CreateFarmUseCase, Depends(get_create_farm_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> FarmResponse:
    """Crea una nueva finca."""
    params = FarmMapper.create_request_to_params(request)
    farm = await create_usecase.execute(**params)
    return FarmMapper.to_response(farm)


@router.get(
    "",
    response_model=FarmsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar fincas",
    description="""
    Obtiene una lista de fincas con paginación.

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def get_all_farms(
    current_user: Annotated[User, Depends(get_current_active_user)],
    get_all_usecase: Annotated[GetAllFarmsUseCase, Depends(get_get_all_farms_usecase)],
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
) -> FarmsListResponse:
    """Lista fincas con paginación."""
    farms = await get_all_usecase.execute(skip=skip, limit=limit)
    # TODO: Agregar método count() al repositorio para obtener total
    total = len(farms)
    return FarmsListResponse(
        total=total,
        farms=[FarmMapper.to_response(farm) for farm in farms],
        page=skip // limit + 1,
        page_size=limit,
    )


@router.get(
    "/by-criteria",
    response_model=FarmsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar fincas por criterios",
    description="""
    Busca fincas aplicando filtros específicos.

    **Filtros disponibles**:
    - `owner_id` (UUID, opcional): Filtrar por propietario

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def get_farms_by_criteria(
    current_user: Annotated[User, Depends(get_current_active_user)],
    get_by_criteria_usecase: Annotated[
        GetFarmsByCriteriaUseCase, Depends(get_get_farms_by_criteria_usecase)
    ],
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    owner_id: UUID | None = Query(None, description="Filtrar por propietario"),
) -> FarmsListResponse:
    """Busca fincas por criterios de filtrado."""
    from typing import Any

    filters: dict[str, Any] = {}
    if owner_id is not None:
        filters["owner_id"] = owner_id

    farms, total = await get_by_criteria_usecase.execute(
        filters=filters, skip=skip, limit=limit
    )
    return FarmsListResponse(
        total=total,
        farms=[FarmMapper.to_response(farm) for farm in farms],
        page=skip // limit + 1,
        page_size=limit,
    )


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
@handle_domain_exceptions
async def get_farm(
    farm_id: UUID,
    get_by_id_usecase: Annotated[
        GetFarmByIdUseCase, Depends(get_get_farm_by_id_usecase)
    ],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> FarmResponse:
    """Obtiene una finca por ID."""
    farm = await get_by_id_usecase.execute(farm_id)
    return FarmMapper.to_response(farm)


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
@handle_domain_exceptions
async def update_farm(
    farm_id: UUID,
    request: FarmUpdateRequest,
    update_usecase: Annotated[UpdateFarmUseCase, Depends(get_update_farm_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> FarmResponse:
    """Actualiza una finca."""
    params = FarmMapper.update_request_to_params(request)
    farm = await update_usecase.execute(farm_id=farm_id, **params)
    return FarmMapper.to_response(farm)


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
    delete_usecase: Annotated[DeleteFarmUseCase, Depends(get_delete_farm_usecase)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    """Elimina una finca."""
    from fastapi import HTTPException

    from ...core.exceptions import NotFoundException, ValidationException

    try:
        await delete_usecase.execute(farm_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
