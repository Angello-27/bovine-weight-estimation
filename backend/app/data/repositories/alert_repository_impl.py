"""
Alert Repository Implementation - Data Layer
Implementación del repositorio de alertas usando Beanie ODM
"""

from datetime import datetime
from typing import Any, cast
from uuid import UUID

from ...domain.entities.alert import Alert
from ...domain.repositories.alert_repository import AlertRepository
from ..models.alert_model import AlertModel


class AlertRepositoryImpl(AlertRepository):
    """
    Implementación del repositorio de alertas usando Beanie ODM.

    Single Responsibility: Persistencia de alertas en MongoDB.
    """

    def _to_entity(self, model: AlertModel) -> Alert:
        """
        Convierte AlertModel (Data) a Alert (Domain Entity).

        Args:
            model: Modelo de Beanie

        Returns:
            Entidad Alert del dominio
        """
        return Alert(
            id=model.id,
            user_id=model.user_id,
            farm_id=model.farm_id,
            type=model.type,
            title=model.title,
            message=model.message,
            status=model.status,
            scheduled_at=model.scheduled_at,
            recurrence=model.recurrence,
            recurrence_end=model.recurrence_end,
            reminder_before_days=model.reminder_before_days,
            related_entity_type=model.related_entity_type,
            related_entity_id=model.related_entity_id,
            filter_criteria=model.filter_criteria,
            location=model.location,
            created_at=model.created_at,
            sent_at=model.sent_at,
            read_at=model.read_at,
            completed_at=model.completed_at,
        )

    def _to_model(self, entity: Alert) -> AlertModel:
        """
        Convierte Alert (Domain Entity) a AlertModel (Data).

        Args:
            entity: Entidad Alert del dominio

        Returns:
            Modelo de Beanie
        """
        return AlertModel(
            id=entity.id,
            user_id=entity.user_id,
            farm_id=entity.farm_id,
            type=entity.type,
            title=entity.title,
            message=entity.message,
            status=entity.status,
            scheduled_at=entity.scheduled_at,
            recurrence=entity.recurrence,
            recurrence_end=entity.recurrence_end,
            reminder_before_days=entity.reminder_before_days,
            related_entity_type=entity.related_entity_type,
            related_entity_id=entity.related_entity_id,
            filter_criteria=entity.filter_criteria,
            location=entity.location,
            created_at=entity.created_at,
            sent_at=entity.sent_at,
            read_at=entity.read_at,
            completed_at=entity.completed_at,
        )

    async def save(self, alert: Alert) -> Alert:
        """Guarda o actualiza una alerta."""
        model = self._to_model(alert)
        await model.save()
        return self._to_entity(model)

    async def get_by_id(self, alert_id: UUID) -> Alert | None:
        """Obtiene una alerta por ID."""
        model = await AlertModel.get(alert_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def find(
        self,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
        type: str | None = None,
        status: str | None = None,
        scheduled_from: datetime | None = None,
        scheduled_to: datetime | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Alert]:
        """Busca alertas con filtros opcionales."""
        query: dict[str, Any] = {}

        if user_id:
            query["user_id"] = user_id
        if farm_id:
            query["farm_id"] = farm_id
        if type:
            query["type"] = cast(Any, type)
        if status:
            query["status"] = cast(Any, status)

        alerts_query = AlertModel.find(query)

        if scheduled_from:
            alerts_query = alerts_query.find(AlertModel.scheduled_at >= scheduled_from)  # type: ignore
        if scheduled_to:
            alerts_query = alerts_query.find(AlertModel.scheduled_at <= scheduled_to)  # type: ignore

        alerts = (
            await alerts_query.sort(-AlertModel.created_at)
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        return [self._to_entity(alert) for alert in alerts]

    async def count(
        self,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
        type: str | None = None,
        status: str | None = None,
        scheduled_from: datetime | None = None,
        scheduled_to: datetime | None = None,
    ) -> int:
        """Cuenta alertas con filtros opcionales."""
        query: dict[str, Any] = {}

        if user_id:
            query["user_id"] = user_id
        if farm_id:
            query["farm_id"] = farm_id
        if type:
            query["type"] = cast(Any, type)
        if status:
            query["status"] = cast(Any, status)

        alerts_query = AlertModel.find(query)

        if scheduled_from:
            alerts_query = alerts_query.find(AlertModel.scheduled_at >= scheduled_from)  # type: ignore
        if scheduled_to:
            alerts_query = alerts_query.find(AlertModel.scheduled_at <= scheduled_to)  # type: ignore

        return await alerts_query.count()

    async def delete(self, alert_id: UUID) -> bool:
        """Elimina una alerta."""
        alert = await AlertModel.get(alert_id)
        if alert is None:
            return False
        await alert.delete()
        return True

    async def find_pending(self, user_id: UUID | None = None) -> list[Alert]:
        """Busca alertas pendientes."""
        query: dict[str, Any] = {"status": "pending"}
        if user_id:
            query["user_id"] = user_id

        alerts = await AlertModel.find(query).sort(AlertModel.scheduled_at).to_list()
        return [self._to_entity(alert) for alert in alerts]

    async def find_scheduled(
        self, from_date: datetime, to_date: datetime
    ) -> list[Alert]:
        """Busca alertas programadas en un rango de fechas."""
        alerts = (
            await AlertModel.find(
                AlertModel.scheduled_at >= from_date,  # type: ignore
                AlertModel.scheduled_at <= to_date,  # type: ignore
                AlertModel.status != "cancelled",  # type: ignore
            )
            .sort(AlertModel.scheduled_at)
            .to_list()
        )
        return [self._to_entity(alert) for alert in alerts]

    async def find_today(
        self, user_id: UUID | None = None, farm_id: UUID | None = None
    ) -> list[Alert]:
        """Busca alertas programadas para el día de hoy."""
        now = datetime.utcnow()
        start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)

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
        return [self._to_entity(alert) for alert in alerts]

    async def find_upcoming(
        self,
        days_ahead: int,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
    ) -> list[Alert]:
        """Busca alertas programadas para los próximos N días."""
        from datetime import timedelta

        now = datetime.utcnow()
        start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0)
        end_date = start_of_today + timedelta(days=days_ahead)

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
        return [self._to_entity(alert) for alert in alerts]
