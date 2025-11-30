"""
Alert Mapper - DTO ↔ Entity Conversion
Convierte entre Alert DTOs y Alert Entities
"""

from ...domain.entities.alert import Alert
from ...schemas.alert_schemas import (
    AlertCreateRequest,
    AlertResponse,
    AlertUpdateRequest,
)


class AlertMapper:
    """
    Mapper para convertir entre Alert DTOs y Entities.

    Single Responsibility: Conversión entre capas Presentation y Domain.
    """

    @staticmethod
    def to_response(alert: Alert) -> AlertResponse:
        """
        Convierte Alert Entity a AlertResponse DTO.

        Args:
            alert: Entidad Alert del dominio

        Returns:
            AlertResponse DTO

        Raises:
            ValueError: Si user_id es None
        """
        if alert.user_id is None:
            raise ValueError("Alert must have a user_id")

        from ...domain.entities.alert import AlertStatus, AlertType, RecurrenceType

        return AlertResponse(
            id=alert.id,
            user_id=alert.user_id,
            farm_id=alert.farm_id,
            type=(
                AlertType(alert.type.value)
                if isinstance(alert.type, AlertType)
                else AlertType(alert.type)
            ),
            title=alert.title,
            message=alert.message,
            status=(
                AlertStatus(alert.status.value)
                if isinstance(alert.status, AlertStatus)
                else AlertStatus(alert.status)
            ),
            scheduled_at=alert.scheduled_at,
            recurrence=(
                RecurrenceType(alert.recurrence.value)
                if isinstance(alert.recurrence, RecurrenceType)
                else RecurrenceType(alert.recurrence)
            ),
            recurrence_end=alert.recurrence_end,
            reminder_before_days=alert.reminder_before_days,
            related_entity_type=alert.related_entity_type,
            related_entity_id=alert.related_entity_id,
            filter_criteria=alert.filter_criteria,
            location=alert.location,
            created_at=alert.created_at,
            sent_at=alert.sent_at,
            read_at=alert.read_at,
            completed_at=alert.completed_at,
        )

    @staticmethod
    def create_request_to_params(
        request: AlertCreateRequest,
    ) -> dict:
        """
        Convierte AlertCreateRequest a parámetros para CreateAlertUseCase.

        Args:
            request: AlertCreateRequest DTO

        Returns:
            Dict con parámetros para use case
        """
        # Construir location si hay coordenadas
        location = None
        if request.latitude is not None and request.longitude is not None:
            location = {
                "type": "Point",
                "coordinates": [request.longitude, request.latitude],
            }

        return {
            "user_id": request.user_id,
            "farm_id": request.farm_id,
            "type": (
                request.type.value
                if hasattr(request.type, "value")
                else str(request.type)
            ),
            "title": request.title,
            "message": request.message,
            "scheduled_at": request.scheduled_at,
            "recurrence": (
                request.recurrence.value
                if hasattr(request.recurrence, "value")
                else str(request.recurrence)
            ),
            "recurrence_end": request.recurrence_end,
            "reminder_before_days": request.reminder_before_days,
            "related_entity_type": request.related_entity_type,
            "related_entity_id": request.related_entity_id,
            "filter_criteria": request.filter_criteria,
            "location": location,
        }

    @staticmethod
    def update_request_to_params(
        request: AlertUpdateRequest,
    ) -> dict:
        """
        Convierte AlertUpdateRequest a parámetros para UpdateAlertUseCase.

        Args:
            request: AlertUpdateRequest DTO

        Returns:
            Dict con parámetros para use case
        """
        params: dict = {}
        if request.title is not None:
            params["title"] = request.title
        if request.message is not None:
            params["message"] = request.message
        if request.status is not None:
            params["status"] = (
                request.status.value
                if hasattr(request.status, "value")
                else str(request.status)
            )
        if request.scheduled_at is not None:
            params["scheduled_at"] = request.scheduled_at
        if request.recurrence is not None:
            params["recurrence"] = (
                request.recurrence.value
                if hasattr(request.recurrence, "value")
                else str(request.recurrence)
            )
        if request.recurrence_end is not None:
            params["recurrence_end"] = request.recurrence_end
        if request.reminder_before_days is not None:
            params["reminder_before_days"] = request.reminder_before_days

        # Construir location si hay coordenadas
        if request.latitude is not None and request.longitude is not None:
            params["location"] = {
                "type": "Point",
                "coordinates": [request.longitude, request.latitude],
            }

        return params
