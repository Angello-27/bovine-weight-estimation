"""
Alert Routes - API Endpoints
Endpoints REST para gestión de alertas y cronograma
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from ...core.dependencies import (
    get_create_alert_usecase,
    get_delete_alert_usecase,
    get_get_alert_by_id_usecase,
    get_get_pending_alerts_usecase,
    get_get_scheduled_alerts_usecase,
    get_get_today_alerts_usecase,
    get_get_upcoming_alerts_usecase,
    get_list_alerts_usecase,
    get_mark_alert_as_completed_usecase,
    get_mark_alert_as_read_usecase,
    get_update_alert_usecase,
)
from ...domain.usecases.alerts import (
    CreateAlertUseCase,
    DeleteAlertUseCase,
    GetAlertByIdUseCase,
    GetPendingAlertsUseCase,
    GetScheduledAlertsUseCase,
    GetTodayAlertsUseCase,
    GetUpcomingAlertsUseCase,
    ListAlertsUseCase,
    MarkAlertAsCompletedUseCase,
    MarkAlertAsReadUseCase,
    UpdateAlertUseCase,
)
from ...schemas.alert_schemas import (
    AlertCreateRequest,
    AlertResponse,
    AlertsListResponse,
    AlertUpdateRequest,
)
from ..mappers import AlertMapper
from ..utils import handle_domain_exceptions

# Crear router
alert_router = APIRouter(prefix="/alerts", tags=["Alerts"])


@alert_router.post("", response_model=AlertResponse, status_code=201)
@handle_domain_exceptions
async def create_alert(
    request: AlertCreateRequest,
    create_usecase: Annotated[CreateAlertUseCase, Depends(get_create_alert_usecase)],
) -> AlertResponse:
    """
    Crea una nueva alerta o evento programado.

    **Ejemplos de uso**:
    - Alerta automática de pérdida de peso
    - Evento programado: Sesión de pesaje masivo
    - Recordatorio recurrente: Vacunación trimestral
    """
    params = AlertMapper.create_request_to_params(request)
    alert = await create_usecase.execute(**params)
    return AlertMapper.to_response(alert)


@alert_router.get("", response_model=AlertsListResponse)
@handle_domain_exceptions
async def list_alerts(
    user_id: UUID | None = Query(None, description="Filtrar por usuario"),
    farm_id: UUID | None = Query(None, description="Filtrar por finca"),
    type: str | None = Query(None, description="Filtrar por tipo"),
    status: str | None = Query(None, description="Filtrar por estado"),
    scheduled_from: datetime | None = Query(None, description="Filtrar desde fecha"),
    scheduled_to: datetime | None = Query(None, description="Filtrar hasta fecha"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamaño de página"),
    list_usecase: Annotated[
        ListAlertsUseCase, Depends(get_list_alerts_usecase)
    ] = Depends(get_list_alerts_usecase),
) -> AlertsListResponse:
    """
    Lista alertas con filtros opcionales.

    **Filtros disponibles**:
    - `user_id`: Alertas de un usuario específico
    - `farm_id`: Alertas de una finca específica
    - `type`: Tipo de alerta (weight_loss, scheduled_weighing, etc.)
    - `status`: Estado (pending, sent, read, completed, cancelled)
    - `scheduled_from` / `scheduled_to`: Rango de fechas programadas
    """
    alerts, total = await list_usecase.execute(
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
        alerts=[AlertMapper.to_response(alert) for alert in alerts],
        page=page,
        page_size=page_size,
    )


@alert_router.get("/{alert_id}", response_model=AlertResponse)
@handle_domain_exceptions
async def get_alert(
    alert_id: UUID,
    get_by_id_usecase: Annotated[
        GetAlertByIdUseCase, Depends(get_get_alert_by_id_usecase)
    ],
) -> AlertResponse:
    """Obtiene una alerta por ID."""
    alert = await get_by_id_usecase.execute(alert_id)
    return AlertMapper.to_response(alert)


@alert_router.put("/{alert_id}", response_model=AlertResponse)
@handle_domain_exceptions
async def update_alert(
    alert_id: UUID,
    request: AlertUpdateRequest,
    update_usecase: Annotated[UpdateAlertUseCase, Depends(get_update_alert_usecase)],
) -> AlertResponse:
    """Actualiza una alerta."""
    params = AlertMapper.update_request_to_params(request)
    alert = await update_usecase.execute(alert_id=alert_id, **params)
    return AlertMapper.to_response(alert)


@alert_router.delete("/{alert_id}", status_code=204)
@handle_domain_exceptions
async def delete_alert(
    alert_id: UUID,
    delete_usecase: Annotated[DeleteAlertUseCase, Depends(get_delete_alert_usecase)],
):
    """Elimina una alerta."""
    await delete_usecase.execute(alert_id)
    return


@alert_router.post("/{alert_id}/read", response_model=AlertResponse)
@handle_domain_exceptions
async def mark_alert_as_read(
    alert_id: UUID,
    mark_read_usecase: Annotated[
        MarkAlertAsReadUseCase, Depends(get_mark_alert_as_read_usecase)
    ],
) -> AlertResponse:
    """Marca una alerta como leída."""
    alert = await mark_read_usecase.execute(alert_id)
    return AlertMapper.to_response(alert)


@alert_router.post("/{alert_id}/complete", response_model=AlertResponse)
@handle_domain_exceptions
async def mark_alert_as_completed(
    alert_id: UUID,
    mark_completed_usecase: Annotated[
        MarkAlertAsCompletedUseCase,
        Depends(get_mark_alert_as_completed_usecase),
    ],
) -> AlertResponse:
    """Marca un evento programado como completado."""
    alert = await mark_completed_usecase.execute(alert_id)
    return AlertMapper.to_response(alert)


@alert_router.get("/pending/list", response_model=list[AlertResponse])
@handle_domain_exceptions
async def get_pending_alerts(
    user_id: UUID | None = Query(None, description="Filtrar por usuario"),
    get_pending_usecase: Annotated[
        GetPendingAlertsUseCase, Depends(get_get_pending_alerts_usecase)
    ] = Depends(get_get_pending_alerts_usecase),
) -> list[AlertResponse]:
    """
    Obtiene alertas pendientes (para procesar por cron job).

    **Uso**: Endpoint interno para procesar alertas programadas.
    """
    alerts = await get_pending_usecase.execute(user_id=user_id)
    return [AlertMapper.to_response(alert) for alert in alerts]


@alert_router.get("/scheduled/list", response_model=list[AlertResponse])
@handle_domain_exceptions
async def get_scheduled_alerts(
    from_date: datetime = Query(..., description="Fecha desde"),
    to_date: datetime = Query(..., description="Fecha hasta"),
    get_scheduled_usecase: Annotated[
        GetScheduledAlertsUseCase, Depends(get_get_scheduled_alerts_usecase)
    ] = Depends(get_get_scheduled_alerts_usecase),
) -> list[AlertResponse]:
    """
    Obtiene alertas programadas en un rango de fechas.

    **Uso**: Para calendario/vista de cronograma.
    """
    alerts = await get_scheduled_usecase.execute(from_date, to_date)
    return [AlertMapper.to_response(alert) for alert in alerts]


@alert_router.get("/today", response_model=list[AlertResponse])
@handle_domain_exceptions
async def get_today_alerts(
    user_id: UUID | None = Query(None, description="Filtrar por usuario"),
    farm_id: UUID | None = Query(None, description="Filtrar por finca"),
    get_today_usecase: Annotated[
        GetTodayAlertsUseCase, Depends(get_get_today_alerts_usecase)
    ] = Depends(get_get_today_alerts_usecase),
) -> list[AlertResponse]:
    """
    Obtiene alertas programadas para el día de hoy.

    **Uso**: Para que el móvil consulte las alertas del día actual.
    Ideal para revisar diariamente qué alertas están programadas.

    **Ejemplo**:
    - Alerta de pesaje masivo programada para hoy a las 8:00 AM
    - Recordatorio de vacunación programado para hoy a las 14:00 PM
    """
    alerts = await get_today_usecase.execute(user_id=user_id, farm_id=farm_id)
    return [AlertMapper.to_response(alert) for alert in alerts]


@alert_router.get("/upcoming", response_model=list[AlertResponse])
@handle_domain_exceptions
async def get_upcoming_alerts(
    days_ahead: int = Query(
        7, ge=1, le=30, description="Días hacia adelante (default: 7)"
    ),
    user_id: UUID | None = Query(None, description="Filtrar por usuario"),
    farm_id: UUID | None = Query(None, description="Filtrar por finca"),
    get_upcoming_usecase: Annotated[
        GetUpcomingAlertsUseCase, Depends(get_get_upcoming_alerts_usecase)
    ] = Depends(get_get_upcoming_alerts_usecase),
) -> list[AlertResponse]:
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
    alerts = await get_upcoming_usecase.execute(
        days_ahead=days_ahead, user_id=user_id, farm_id=farm_id
    )
    return [AlertMapper.to_response(alert) for alert in alerts]
