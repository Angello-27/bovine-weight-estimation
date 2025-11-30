"""
Alert Routes - API Endpoints
Endpoints REST para gestión de alertas y cronograma
"""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from ...application.alert_service import AlertService
from ...core.exceptions import NotFoundException
from ...schemas.alert_schemas import (
    AlertCreateRequest,
    AlertResponse,
    AlertsListResponse,
    AlertUpdateRequest,
)

# Crear router
alert_router = APIRouter(prefix="/alerts", tags=["Alerts"])

# Instancia del servicio
alert_service = AlertService()


@alert_router.post("", response_model=AlertResponse, status_code=201)
async def create_alert(request: AlertCreateRequest):
    """
    Crea una nueva alerta o evento programado.

    **Ejemplos de uso**:
    - Alerta automática de pérdida de peso
    - Evento programado: Sesión de pesaje masivo
    - Recordatorio recurrente: Vacunación trimestral
    """
    try:
        return await alert_service.create_alert(request)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear alerta: {str(e)}")


@alert_router.get("", response_model=AlertsListResponse)
async def list_alerts(
    user_id: UUID | None = Query(None, description="Filtrar por usuario"),
    farm_id: UUID | None = Query(None, description="Filtrar por finca"),
    type: str | None = Query(None, description="Filtrar por tipo"),
    status: str | None = Query(None, description="Filtrar por estado"),
    scheduled_from: datetime | None = Query(None, description="Filtrar desde fecha"),
    scheduled_to: datetime | None = Query(None, description="Filtrar hasta fecha"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamaño de página"),
):
    """
    Lista alertas con filtros opcionales.

    **Filtros disponibles**:
    - `user_id`: Alertas de un usuario específico
    - `farm_id`: Alertas de una finca específica
    - `type`: Tipo de alerta (weight_loss, scheduled_weighing, etc.)
    - `status`: Estado (pending, sent, read, completed, cancelled)
    - `scheduled_from` / `scheduled_to`: Rango de fechas programadas
    """
    try:
        alerts, total = await alert_service.list_alerts(
            user_id=user_id,
            farm_id=farm_id,
            type=type,
            status=status,
            scheduled_from=scheduled_from,
            scheduled_to=scheduled_to,
            page=page,
            page_size=page_size,
        )

        return AlertsListResponse(
            total=total,
            alerts=alerts,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al listar alertas: {str(e)}"
        )


@alert_router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: UUID):
    """
    Obtiene una alerta por ID.
    """
    try:
        return await alert_service.get_alert(alert_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener alerta: {str(e)}"
        )


@alert_router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(alert_id: UUID, request: AlertUpdateRequest):
    """
    Actualiza una alerta.
    """
    try:
        return await alert_service.update_alert(alert_id, request)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar alerta: {str(e)}"
        )


@alert_router.delete("/{alert_id}", status_code=204)
async def delete_alert(alert_id: UUID):
    """
    Elimina una alerta.
    """
    try:
        await alert_service.delete_alert(alert_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar alerta: {str(e)}"
        )


@alert_router.post("/{alert_id}/read", response_model=AlertResponse)
async def mark_alert_as_read(alert_id: UUID):
    """
    Marca una alerta como leída.
    """
    try:
        return await alert_service.mark_as_read(alert_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al marcar alerta como leída: {str(e)}"
        )


@alert_router.post("/{alert_id}/complete", response_model=AlertResponse)
async def mark_alert_as_completed(alert_id: UUID):
    """
    Marca un evento programado como completado.
    """
    try:
        return await alert_service.mark_as_completed(alert_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al marcar evento como completado: {str(e)}"
        )


@alert_router.get("/pending/list", response_model=list[AlertResponse])
async def get_pending_alerts(
    user_id: UUID | None = Query(None, description="Filtrar por usuario")
):
    """
    Obtiene alertas pendientes (para procesar por cron job).

    **Uso**: Endpoint interno para procesar alertas programadas.
    """
    try:
        return await alert_service.get_pending_alerts(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener alertas pendientes: {str(e)}"
        )


@alert_router.get("/scheduled/list", response_model=list[AlertResponse])
async def get_scheduled_alerts(
    from_date: datetime = Query(..., description="Fecha desde"),
    to_date: datetime = Query(..., description="Fecha hasta"),
):
    """
    Obtiene alertas programadas en un rango de fechas.

    **Uso**: Para calendario/vista de cronograma.
    """
    try:
        return await alert_service.get_scheduled_alerts(from_date, to_date)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener alertas programadas: {str(e)}"
        )


@alert_router.get("/today", response_model=list[AlertResponse])
async def get_today_alerts(
    user_id: UUID | None = Query(None, description="Filtrar por usuario"),
    farm_id: UUID | None = Query(None, description="Filtrar por finca"),
):
    """
    Obtiene alertas programadas para el día de hoy.

    **Uso**: Para que el móvil consulte las alertas del día actual.
    Ideal para revisar diariamente qué alertas están programadas.

    **Ejemplo**:
    - Alerta de pesaje masivo programada para hoy a las 8:00 AM
    - Recordatorio de vacunación programado para hoy a las 14:00 PM
    """
    try:
        return await alert_service.get_today_alerts(user_id=user_id, farm_id=farm_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener alertas de hoy: {str(e)}"
        )


@alert_router.get("/upcoming", response_model=list[AlertResponse])
async def get_upcoming_alerts(
    days_ahead: int = Query(
        7, ge=1, le=30, description="Días hacia adelante (default: 7)"
    ),
    user_id: UUID | None = Query(None, description="Filtrar por usuario"),
    farm_id: UUID | None = Query(None, description="Filtrar por finca"),
):
    """
    Obtiene alertas programadas para los próximos N días.

    **Uso**: Para que el móvil consulte alertas próximas (próxima semana, etc.).
    Útil para mostrar un calendario o vista de próximos eventos.

    **Parámetros**:
    - `days_ahead`: Número de días hacia adelante (1-30, default: 7)
    - `user_id`: Filtrar por usuario específico
    - `farm_id`: Filtrar por finca específica

    **Ejemplo**:
    - `GET /api/v1/alerts/upcoming?days_ahead=7` → Próximos 7 días
    - `GET /api/v1/alerts/upcoming?days_ahead=30&farm_id=...` → Próximo mes de una finca
    """
    try:
        return await alert_service.get_upcoming_alerts(
            days_ahead=days_ahead, user_id=user_id, farm_id=farm_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener alertas próximas: {str(e)}"
        )
