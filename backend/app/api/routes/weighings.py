"""
Weighings Routes - API Endpoints
Endpoints REST para estimaciones de peso
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ...core.exceptions import NotFoundException, ValidationException
from ...schemas.weighing_schemas import (
    WeighingCreateRequest,
    WeighingResponse,
    WeighingsListResponse,
)
from ...services import WeighingService

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


# Dependency injection del servicio
def get_weighing_service() -> WeighingService:
    """Dependency para inyectar WeighingService."""
    return WeighingService()


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
async def create_weighing(
    request: WeighingCreateRequest,
    service: Annotated[WeighingService, Depends(get_weighing_service)],
) -> WeighingResponse:
    """Crea una nueva estimación de peso."""
    try:
        return await service.create_weighing(request)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear estimación: {str(e)}",
        )


@router.get(
    "/{weighing_id}",
    response_model=WeighingResponse,
    summary="Obtener estimación por ID",
    description="Obtiene los datos de una estimación específica.",
)
async def get_weighing(
    weighing_id: UUID,
    service: Annotated[WeighingService, Depends(get_weighing_service)],
) -> WeighingResponse:
    """Obtiene una estimación por ID."""
    try:
        return await service.get_weighing(weighing_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estimación: {str(e)}",
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
async def get_animal_weighings(
    service: Annotated[WeighingService, Depends(get_weighing_service)],
    animal_id: UUID,
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamaño de página"),
) -> WeighingsListResponse:
    """Obtiene historial de pesajes de un animal."""
    try:
        skip = (page - 1) * page_size
        weighings = await service.get_weighings_by_animal(
            animal_id=animal_id,
            skip=skip,
            limit=page_size,
        )

        total = len(weighings)

        return WeighingsListResponse(
            total=total,
            weighings=weighings,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historial: {str(e)}",
        )


@router.get(
    "",
    response_model=WeighingsListResponse,
    summary="Listar todas las estimaciones",
    description="Lista todas las estimaciones con paginación (admin).",
)
async def list_weighings(
    service: Annotated[WeighingService, Depends(get_weighing_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
) -> WeighingsListResponse:
    """Lista todas las estimaciones."""
    try:
        skip = (page - 1) * page_size
        weighings = await service.get_all_weighings(skip=skip, limit=page_size)

        total = len(weighings)

        return WeighingsListResponse(
            total=total,
            weighings=weighings,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar estimaciones: {str(e)}",
        )
