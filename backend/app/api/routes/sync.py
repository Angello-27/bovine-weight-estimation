"""
Sync Routes - US-005: Sincronización Offline
FastAPI endpoints para sincronización bidireccional
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ...schemas.sync_schemas import (
    CattleSyncBatchRequest,
    CattleSyncBatchResponse,
    HealthCheckResponse,
    WeightEstimationSyncBatchRequest,
    WeightEstimationSyncBatchResponse,
)
from ...services.sync_service import SyncService

# Router con prefijo /api/v1/sync
router = APIRouter(
    prefix="/api/v1/sync",
    tags=["Sincronización"],
    responses={
        500: {"description": "Error interno del servidor"},
        400: {"description": "Request inválido"},
    },
)


# Dependency injection del servicio
# TODO: En producción, usar FastAPI Depends con singleton pattern
def get_sync_service() -> SyncService:
    """
    Dependency para inyectar SyncService.

    TODO: Implementar como singleton en producción para mantener estado
    Por ahora retorna nueva instancia (MVP/testing)
    """
    return SyncService()


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
async def sync_cattle_batch(
    request: CattleSyncBatchRequest,
    sync_service: Annotated[SyncService, Depends(get_sync_service)],
) -> CattleSyncBatchResponse:
    """
    Endpoint para sincronizar batch de ganado.

    Args:
        request: Batch de animales a sincronizar
        sync_service: Servicio de sincronización (inyectado)

    Returns:
        CattleSyncBatchResponse con resultados por item

    Raises:
        HTTPException 400: Si el request es inválido
        HTTPException 500: Si hay error interno
    """
    try:
        # Validar batch size
        if len(request.items) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch size máximo es 100 items. "
                f"Recibido: {len(request.items)}",
            )

        # Procesar sincronización
        return await sync_service.sync_cattle_batch(
            items=request.items,
            device_id=request.device_id,
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log error y retornar 500
        print(f"Error en sync_cattle_batch: {str(e)}")  # TODO: Usar logger
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar sincronización: {str(e)}",
        )


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
async def sync_weight_estimations_batch(
    request: WeightEstimationSyncBatchRequest,
    sync_service: Annotated[SyncService, Depends(get_sync_service)],
) -> WeightEstimationSyncBatchResponse:
    """
    Endpoint para sincronizar batch de estimaciones de peso.

    Args:
        request: Batch de estimaciones a sincronizar
        sync_service: Servicio de sincronización (inyectado)

    Returns:
        WeightEstimationSyncBatchResponse con resultados

    Raises:
        HTTPException 400: Si el request es inválido
        HTTPException 500: Si hay error interno
    """
    try:
        # Validar batch size
        if len(request.items) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch size máximo es 100 items. "
                f"Recibido: {len(request.items)}",
            )

        # Procesar sincronización
        return await sync_service.sync_weight_estimations_batch(
            items=request.items,
            device_id=request.device_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en sync_weight_estimations_batch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar sincronización: {str(e)}",
        )


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
async def sync_health_check(
    sync_service: Annotated[SyncService, Depends(get_sync_service)],
) -> HealthCheckResponse:
    """
    Health check del servicio de sincronización.

    Returns:
        HealthCheckResponse con estado del servicio
    """
    try:
        # TODO: En producción, verificar MongoDB connection
        return HealthCheckResponse(
            status="online",
            database="memory (MVP)",  # TODO: Cambiar a "connected" con MongoDB
        )
    except Exception as e:
        return HealthCheckResponse(
            status="error",
            database=f"error: {str(e)}",
        )


@router.get(
    "/stats",
    summary="Estadísticas de sincronización",
    description="Retorna estadísticas del servicio de sincronización (solo dev/testing)",
)
async def sync_stats(
    sync_service: Annotated[SyncService, Depends(get_sync_service)],
):
    """
    Endpoint de estadísticas para desarrollo/testing.

    WARNING: Deshabilitar en producción por seguridad
    """
    return {
        "cattle_count": sync_service.get_cattle_count(),
        "weight_estimation_count": sync_service.get_weight_estimation_count(),
        "storage": "memory (MVP)",
        "note": "Deshabilitar en producción",
    }
