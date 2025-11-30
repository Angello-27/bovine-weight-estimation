"""
Sync Routes - US-005: Sincronización Offline
FastAPI endpoints para sincronización bidireccional
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ...core.dependencies import (
    get_sync_cattle_batch_usecase,
    get_sync_health_usecase,
    get_sync_weight_estimations_batch_usecase,
)
from ...domain.usecases.sync import (
    GetSyncHealthUseCase,
    SyncCattleBatchUseCase,
    SyncWeightEstimationsBatchUseCase,
)
from ...schemas.sync_schemas import (
    CattleSyncBatchRequest,
    CattleSyncBatchResponse,
    HealthCheckResponse,
    WeightEstimationSyncBatchRequest,
    WeightEstimationSyncBatchResponse,
)
from ..mappers.sync_mapper import SyncMapper
from ..utils.exception_handlers import handle_domain_exceptions

# Router con prefijo /api/v1/sync
router = APIRouter(
    prefix="/api/v1/sync",
    tags=["Sincronización"],
    responses={
        500: {"description": "Error interno del servidor"},
        400: {"description": "Request inválido"},
    },
)


@router.post(
    "/cattle",
    response_model=CattleSyncBatchResponse,
    status_code=status.HTTP_200_OK,
    summary="Sincronizar ganado (batch)",
    description="""
    Sincroniza un batch de hasta 100 animales desde el dispositivo móvil.

    **Estrategia last-write-wins**:
    - Compara timestamps UTC de mobile vs backend
    - El dato más reciente prevalece automáticamente
    - Retorna conflictos para que mobile actualice su copia local si es necesario

    **Casos de uso**:
    - CREATE: Animal no existe en backend
    - UPDATE: Animal existe, mobile tiene versión más reciente
    - CONFLICT: Animal existe, backend tiene versión más reciente (retorna datos)

    **Performance**:
    - Batch size máximo: 100 items
    - Timeout recomendado: 30 segundos
    - Para >100 animales, enviar múltiples batches
    """,
    response_description="Resultado de sincronización por cada item",
)
@handle_domain_exceptions
async def sync_cattle_batch(
    sync_usecase: Annotated[
        SyncCattleBatchUseCase, Depends(get_sync_cattle_batch_usecase)
    ],
    request: CattleSyncBatchRequest,
) -> CattleSyncBatchResponse:
    """
    Endpoint para sincronizar batch de ganado.

    Args:
        request: Batch de animales a sincronizar
        sync_usecase: Caso de uso de sincronización (inyectado)

    Returns:
        CattleSyncBatchResponse con resultados por item

    Raises:
        HTTPException 400: Si el request es inválido
        HTTPException 500: Si hay error interno
    """
    # Validar batch size
    if len(request.items) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch size máximo es 100 items. " f"Recibido: {len(request.items)}",
        )

    # Convertir items a dict para el use case
    items_dict = [item.model_dump() for item in request.items]

    # Ejecutar caso de uso
    result = await sync_usecase.execute(
        items=items_dict,
        device_id=request.device_id,
    )

    # Convertir resultado a response usando mapper
    return SyncMapper.to_cattle_batch_response(result)


@router.post(
    "/weight-estimations",
    response_model=WeightEstimationSyncBatchResponse,
    status_code=status.HTTP_200_OK,
    summary="Sincronizar estimaciones de peso (batch)",
    description="""
    Sincroniza un batch de hasta 100 estimaciones de peso desde mobile.

    **Características**:
    - Estimaciones son típicamente inmutables (solo CREATE)
    - Si ya existe, se marca como ya sincronizado
    - Batch processing para optimizar red en zonas rurales

    **Performance**:
    - Batch size máximo: 100 items
    - Timeout recomendado: 30 segundos
    - Compresión automática para payloads >1KB
    """,
    response_description="Resultado de sincronización por cada estimación",
)
@handle_domain_exceptions
async def sync_weight_estimations_batch(
    sync_usecase: Annotated[
        SyncWeightEstimationsBatchUseCase,
        Depends(get_sync_weight_estimations_batch_usecase),
    ],
    request: WeightEstimationSyncBatchRequest,
) -> WeightEstimationSyncBatchResponse:
    """
    Endpoint para sincronizar batch de estimaciones de peso.

    Args:
        request: Batch de estimaciones a sincronizar
        sync_usecase: Caso de uso de sincronización (inyectado)

    Returns:
        WeightEstimationSyncBatchResponse con resultados

    Raises:
        HTTPException 400: Si el request es inválido
        HTTPException 500: Si hay error interno
    """
    # Validar batch size
    if len(request.items) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch size máximo es 100 items. " f"Recibido: {len(request.items)}",
        )

    # Convertir items a dict para el use case
    items_dict = [item.model_dump() for item in request.items]

    # Ejecutar caso de uso
    result = await sync_usecase.execute(
        items=items_dict,
        device_id=request.device_id,
    )

    # Convertir resultado a response usando mapper
    return SyncMapper.to_weight_estimation_batch_response(result)


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check de sincronización",
    description="""
    Verifica que el servicio de sincronización está online y operativo.

    **Uso móvil**:
    - Llamar antes de sync para verificar conectividad
    - Timeout corto (2-3 segundos) para detectar offline rápido
    - Usar para mostrar indicador de conexión en UI
    """,
)
@handle_domain_exceptions
async def sync_health_check(
    health_usecase: Annotated[GetSyncHealthUseCase, Depends(get_sync_health_usecase)],
) -> HealthCheckResponse:
    """
    Health check del servicio de sincronización.

    Returns:
        HealthCheckResponse con estado del servicio
    """
    health_data = await health_usecase.execute()
    return SyncMapper.to_health_check_response(health_data)


@router.get(
    "/stats",
    summary="Estadísticas de sincronización",
    description="Retorna estadísticas del servicio de sincronización (solo dev/testing)",
)
@handle_domain_exceptions
async def sync_stats():
    """
    Endpoint de estadísticas para desarrollo/testing.

    WARNING: Deshabilitar en producción por seguridad
    """
    from ...core.dependencies.repositories import (
        get_animal_repository,
        get_weight_estimation_repository,
    )

    animal_repo = get_animal_repository()
    weight_repo = get_weight_estimation_repository()

    cattle_count = await animal_repo.count()
    weight_count = await weight_repo.count()

    return {
        "cattle_count": cattle_count,
        "weight_estimation_count": weight_count,
        "storage": "MongoDB",
        "note": "Deshabilitar en producción",
    }
