"""
Weighings Routes - API Endpoints
Endpoints REST para estimaciones de peso
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from ...core.dependencies.weight_estimations import (
    get_all_weight_estimations_usecase,
    get_create_weight_estimation_usecase,
    get_get_weight_estimations_by_criteria_usecase,
    get_weight_estimation_by_id_usecase,
    get_weight_estimations_by_animal_id_usecase,
)
from ...domain.usecases.weight_estimations import (
    CreateWeightEstimationUseCase,
    GetAllWeightEstimationsUseCase,
    GetWeightEstimationByIdUseCase,
    GetWeightEstimationsByAnimalIdUseCase,
    GetWeightEstimationsByCriteriaUseCase,
)
from ...schemas.weighing_schemas import (
    WeighingCreateRequest,
    WeighingResponse,
    WeighingsListResponse,
)
from ..mappers import WeightEstimationMapper
from ..utils.exception_handlers import handle_domain_exceptions
from ..utils.pagination import calculate_skip

# Router con prefijo /api/v1/weighings
router = APIRouter(
    prefix="/api/v1/weighings",
    tags=["Weighings"],
    responses={
        404: {"description": "Pesaje no encontrado"},
        400: {"description": "Request inválido"},
        500: {"description": "Error interno del servidor"},
    },
)


@router.post(
    "",
    response_model=WeighingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear estimación de peso",
    description="""
    Crea una nueva estimación de peso.

    **Validaciones**:
    - Confidence ≥80% (mínimo aceptable)
    - Peso entre 0-1500 kg
    - Raza debe ser una de las 7 exactas
    - Animal debe existir (si se proporciona animal_id)

    **US-002**: Estimación de Peso por Raza con IA
    **US-004**: Historial de Pesajes
    """,
)
@handle_domain_exceptions
async def create_weighing(
    request: WeighingCreateRequest,
    create_usecase: Annotated[
        CreateWeightEstimationUseCase, Depends(get_create_weight_estimation_usecase)
    ],
) -> WeighingResponse:
    """Crea una nueva estimación de peso."""
    params = WeightEstimationMapper.create_request_to_params(request)
    estimation = await create_usecase.execute(**params)
    return WeightEstimationMapper.to_response(estimation)


@router.get(
    "/by-criteria",
    response_model=WeighingsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar estimaciones por criterios",
    description="""
    Busca estimaciones de peso aplicando filtros específicos.

    **Filtros disponibles**:
    - `animal_id` (UUID, opcional): Filtrar por animal
    - `breed` (string, opcional): Filtrar por raza

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def get_weighings_by_criteria(
    get_by_criteria_usecase: Annotated[
        GetWeightEstimationsByCriteriaUseCase,
        Depends(get_get_weight_estimations_by_criteria_usecase),
    ],
    animal_id: UUID | None = Query(None, description="Filtrar por animal"),
    breed: str | None = Query(None, description="Filtrar por raza"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamaño de página"),
) -> WeighingsListResponse:
    """Busca estimaciones por criterios de filtrado."""
    from typing import Any

    skip = calculate_skip(page=page, page_size=page_size)
    filters: dict[str, Any] = {}
    if animal_id is not None:
        filters["animal_id"] = animal_id
    if breed is not None:
        filters["breed"] = breed

    estimations, total = await get_by_criteria_usecase.execute(
        filters=filters, skip=skip, limit=page_size
    )

    weighings = [WeightEstimationMapper.to_response(e) for e in estimations]

    return WeighingsListResponse(
        total=total,
        weighings=weighings,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/animal/{animal_id}",
    response_model=WeighingsListResponse,
    summary="Historial de pesajes por animal",
    description="""
    Obtiene historial completo de pesajes de un animal.

    Ordenado por fecha descendente (más reciente primero).

    **US-004**: Historial de Pesajes con Gráficos
    """,
)
@handle_domain_exceptions
async def get_animal_weighings(
    get_by_animal_usecase: Annotated[
        GetWeightEstimationsByAnimalIdUseCase,
        Depends(get_weight_estimations_by_animal_id_usecase),
    ],
    animal_id: UUID,
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamaño de página"),
) -> WeighingsListResponse:
    """Obtiene historial de pesajes de un animal."""
    skip = calculate_skip(page=page, page_size=page_size)
    estimations = await get_by_animal_usecase.execute(
        animal_id=animal_id, skip=skip, limit=page_size
    )

    weighings = [WeightEstimationMapper.to_response(e) for e in estimations]

    return WeighingsListResponse(
        total=len(weighings),
        weighings=weighings,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{weighing_id}",
    response_model=WeighingResponse,
    summary="Obtener estimación por ID",
    description="Obtiene los datos de una estimación específica.",
)
@handle_domain_exceptions
async def get_weighing(
    weighing_id: UUID,
    get_by_id_usecase: Annotated[
        GetWeightEstimationByIdUseCase, Depends(get_weight_estimation_by_id_usecase)
    ],
) -> WeighingResponse:
    """Obtiene una estimación por ID."""
    estimation = await get_by_id_usecase.execute(weighing_id)
    return WeightEstimationMapper.to_response(estimation)


@router.get(
    "",
    response_model=WeighingsListResponse,
    summary="Listar todas las estimaciones",
    description="Lista todas las estimaciones con paginación (admin).",
)
@handle_domain_exceptions
async def list_weighings(
    get_all_usecase: Annotated[
        GetAllWeightEstimationsUseCase, Depends(get_all_weight_estimations_usecase)
    ],
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
) -> WeighingsListResponse:
    """Lista todas las estimaciones."""
    skip = calculate_skip(page=page, page_size=page_size)
    estimations = await get_all_usecase.execute(skip=skip, limit=page_size)

    weighings = [WeightEstimationMapper.to_response(e) for e in estimations]

    return WeighingsListResponse(
        total=len(weighings),
        weighings=weighings,
        page=page,
        page_size=page_size,
    )
