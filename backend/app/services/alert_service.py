"""
Alert Service - Business Logic
Lógica de negocio para gestión de alertas y cronograma
"""

from datetime import datetime
from typing import Any, cast
from uuid import UUID

from ..core.exceptions import NotFoundException
from ..data.models.user_model import UserModel
from ..models import AlertModel  # TODO: Migrar a data/models/
from ..schemas.alert_schemas import (
    AlertCreateRequest,
    AlertResponse,
    AlertUpdateRequest,
)


class AlertService:
    """
    Servicio de gestión de alertas.

    Single Responsibility: Business logic de alertas y cronograma.
    """

    async def create_alert(self, request: AlertCreateRequest) -> AlertResponse:
        """
        Crea una nueva alerta.

        Args:
            request: Datos de la alerta a crear

        Returns:
            AlertResponse con la alerta creada

        Raises:
            NotFoundException: Si el user_id no existe
        """
        # Validar que el usuario exista
        user = await UserModel.get(request.user_id)
        if user is None:
            raise NotFoundException(
                resource="User", field="id", value=str(request.user_id)
            )

        # Construir location si hay coordenadas
        location = None
        if request.latitude is not None and request.longitude is not None:
            location = {
                "type": "Point",
                "coordinates": [request.longitude, request.latitude],
            }

        # Crear alerta
        alert = AlertModel(
            user_id=request.user_id,
            farm_id=request.farm_id,
            type=request.type,
            title=request.title,
            message=request.message,
            scheduled_at=request.scheduled_at,
            recurrence=request.recurrence,
            recurrence_end=request.recurrence_end,
            reminder_before_days=request.reminder_before_days,
            related_entity_type=request.related_entity_type,
            related_entity_id=request.related_entity_id,
            location=location,
        )

        await alert.insert()

        return AlertResponse.model_validate(alert)

    async def get_alert(self, alert_id: UUID) -> AlertResponse:
        """
        Obtiene una alerta por ID.

        Args:
            alert_id: ID de la alerta

        Returns:
            AlertResponse con la alerta

        Raises:
            NotFoundException: Si la alerta no existe
        """
        alert = await AlertModel.get(alert_id)
        if alert is None:
            raise NotFoundException(resource="Alert", field="id", value=str(alert_id))

        return AlertResponse.model_validate(alert)

    async def list_alerts(
        self,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
        type: str | None = None,
        status: str | None = None,
        scheduled_from: datetime | None = None,
        scheduled_to: datetime | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[AlertResponse], int]:
        """
        Lista alertas con filtros.

        Args:
            user_id: Filtrar por usuario
            farm_id: Filtrar por finca
            type: Filtrar por tipo
            status: Filtrar por estado
            scheduled_from: Filtrar desde fecha
            scheduled_to: Filtrar hasta fecha
            page: Número de página
            page_size: Tamaño de página

        Returns:
            Tupla (lista de alertas, total)
        """
        # Construir query
        # Usar Any para permitir valores de diferentes tipos (UUID, str, enum)
        query: dict[str, Any] = {}

        if user_id:
            query["user_id"] = user_id
        if farm_id:
            query["farm_id"] = farm_id
        if type:
            # type y status son strings desde la API, pero el modelo espera enums
            # Beanie los convertirá automáticamente al hacer la query
            query["type"] = cast(Any, type)
        if status:
            query["status"] = cast(Any, status)

        # Query base
        alerts_query = AlertModel.find(query)

        # Filtros de fecha programada
        if scheduled_from:
            alerts_query = alerts_query.find(AlertModel.scheduled_at >= scheduled_from)  # type: ignore
        if scheduled_to:
            alerts_query = alerts_query.find(AlertModel.scheduled_at <= scheduled_to)  # type: ignore

        # Contar total
        total = await alerts_query.count()

        # Paginación
        skip = (page - 1) * page_size
        alerts = (
            await alerts_query.sort(-AlertModel.created_at)
            .skip(skip)
            .limit(page_size)
            .to_list()
        )

        return [AlertResponse.model_validate(alert) for alert in alerts], total

    async def update_alert(
        self, alert_id: UUID, request: AlertUpdateRequest
    ) -> AlertResponse:
        """
        Actualiza una alerta.

        Args:
            alert_id: ID de la alerta
            request: Datos a actualizar

        Returns:
            AlertResponse con la alerta actualizada

        Raises:
            NotFoundException: Si la alerta no existe
        """
        alert = await AlertModel.get(alert_id)
        if alert is None:
            raise NotFoundException(resource="Alert", field="id", value=str(alert_id))

        # Actualizar campos
        if request.title is not None:
            alert.title = request.title
        if request.message is not None:
            alert.message = request.message
        if request.status is not None:
            alert.status = request.status
        if request.scheduled_at is not None:
            alert.scheduled_at = request.scheduled_at
        if request.recurrence is not None:
            alert.recurrence = request.recurrence
        if request.recurrence_end is not None:
            alert.recurrence_end = request.recurrence_end
        if request.reminder_before_days is not None:
            alert.reminder_before_days = request.reminder_before_days

        # Actualizar location si hay coordenadas
        if request.latitude is not None and request.longitude is not None:
            alert.location = {
                "type": "Point",
                "coordinates": [request.longitude, request.latitude],
            }

        await alert.save()

        return AlertResponse.model_validate(alert)

    async def delete_alert(self, alert_id: UUID) -> None:
        """
        Elimina una alerta.

        Args:
            alert_id: ID de la alerta

        Raises:
            NotFoundException: Si la alerta no existe
        """
        alert = await AlertModel.get(alert_id)
        if alert is None:
            raise NotFoundException(resource="Alert", field="id", value=str(alert_id))

        await alert.delete()

    async def mark_as_read(self, alert_id: UUID) -> AlertResponse:
        """
        Marca una alerta como leída.

        Args:
            alert_id: ID de la alerta

        Returns:
            AlertResponse con la alerta actualizada

        Raises:
            NotFoundException: Si la alerta no existe
        """
        alert = await AlertModel.get(alert_id)
        if alert is None:
            raise NotFoundException(resource="Alert", field="id", value=str(alert_id))

        alert.mark_as_read()
        await alert.save()

        return AlertResponse.model_validate(alert)

    async def mark_as_completed(self, alert_id: UUID) -> AlertResponse:
        """
        Marca un evento como completado.

        Args:
            alert_id: ID de la alerta

        Returns:
            AlertResponse con la alerta actualizada

        Raises:
            NotFoundException: Si la alerta no existe
        """
        alert = await AlertModel.get(alert_id)
        if alert is None:
            raise NotFoundException(resource="Alert", field="id", value=str(alert_id))

        alert.mark_as_completed()
        await alert.save()

        return AlertResponse.model_validate(alert)

    async def get_pending_alerts(
        self, user_id: UUID | None = None
    ) -> list[AlertResponse]:
        """
        Obtiene alertas pendientes (para procesar).

        Args:
            user_id: Filtrar por usuario (opcional)

        Returns:
            Lista de alertas pendientes
        """
        query: dict[str, Any] = {"status": "pending"}
        if user_id:
            query["user_id"] = user_id

        alerts = await AlertModel.find(query).sort(AlertModel.scheduled_at).to_list()

        return [AlertResponse.model_validate(alert) for alert in alerts]

    async def get_scheduled_alerts(
        self, from_date: datetime, to_date: datetime
    ) -> list[AlertResponse]:
        """
        Obtiene alertas programadas en un rango de fechas.

        Args:
            from_date: Fecha desde
            to_date: Fecha hasta

        Returns:
            Lista de alertas programadas
        """
        alerts = (
            await AlertModel.find(
                AlertModel.scheduled_at >= from_date,
                AlertModel.scheduled_at <= to_date,
                AlertModel.status != "cancelled",
            )
            .sort(AlertModel.scheduled_at)
            .to_list()
        )

        return [AlertResponse.model_validate(alert) for alert in alerts]

    async def get_today_alerts(
        self, user_id: UUID | None = None, farm_id: UUID | None = None
    ) -> list[AlertResponse]:
        """
        Obtiene alertas programadas para el día de hoy.

        Args:
            user_id: Filtrar por usuario (opcional)
            farm_id: Filtrar por finca (opcional)

        Returns:
            Lista de alertas del día actual
        """
        now = datetime.utcnow()
        start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)

        # Construir query con condiciones de Beanie
        query_conditions = [
            AlertModel.scheduled_at >= start_of_day,  # type: ignore
            AlertModel.scheduled_at <= end_of_day,  # type: ignore
            AlertModel.status != "cancelled",  # type: ignore
        ]

        if user_id:
            query_conditions.append(AlertModel.user_id == user_id)  # type: ignore
        if farm_id:
            query_conditions.append(AlertModel.farm_id == farm_id)  # type: ignore

        alerts = (
            await AlertModel.find(*query_conditions)
            .sort(AlertModel.scheduled_at)
            .to_list()
        )

        return [AlertResponse.model_validate(alert) for alert in alerts]

    async def get_upcoming_alerts(
        self,
        days_ahead: int = 7,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
    ) -> list[AlertResponse]:
        """
        Obtiene alertas programadas para los próximos N días.

        Args:
            days_ahead: Número de días hacia adelante (default: 7)
            user_id: Filtrar por usuario (opcional)
            farm_id: Filtrar por finca (opcional)

        Returns:
            Lista de alertas próximas
        """
        from datetime import timedelta

        now = datetime.utcnow()
        start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0)
        end_date = start_of_today + timedelta(days=days_ahead)

        # Construir query con condiciones de Beanie
        query_conditions = [
            AlertModel.scheduled_at >= start_of_today,  # type: ignore
            AlertModel.scheduled_at <= end_date,  # type: ignore
            AlertModel.status != "cancelled",  # type: ignore
        ]

        if user_id:
            query_conditions.append(AlertModel.user_id == user_id)  # type: ignore
        if farm_id:
            query_conditions.append(AlertModel.farm_id == farm_id)  # type: ignore

        alerts = (
            await AlertModel.find(*query_conditions)
            .sort(AlertModel.scheduled_at)
            .to_list()
        )

        return [AlertResponse.model_validate(alert) for alert in alerts]
