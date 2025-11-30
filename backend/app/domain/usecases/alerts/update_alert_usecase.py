"""
Update Alert Use Case - Domain Layer
Caso de uso para actualizar una alerta
"""

from datetime import datetime
from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.alert import Alert
from ...repositories.alert_repository import AlertRepository


class UpdateAlertUseCase:
    """
    Caso de uso para actualizar una alerta.

    Single Responsibility: Actualizar una alerta existente.
    """

    def __init__(self, alert_repository: AlertRepository):
        """
        Inicializa el caso de uso.

        Args:
            alert_repository: Repositorio de alertas (inyección de dependencia)
        """
        self._alert_repository = alert_repository

    async def execute(
        self,
        alert_id: UUID,
        title: str | None = None,
        message: str | None = None,
        status: str | None = None,
        scheduled_at: datetime | None = None,
        recurrence: str | None = None,
        recurrence_end: datetime | None = None,
        reminder_before_days: list[int] | None = None,
        location: dict | None = None,
    ) -> Alert:
        """
        Ejecuta el caso de uso para actualizar una alerta.

        Args:
            alert_id: ID de la alerta
            title: Nuevo título (opcional)
            message: Nuevo mensaje (opcional)
            status: Nuevo estado (opcional)
            scheduled_at: Nueva fecha programada (opcional)
            recurrence: Nuevo tipo de recurrencia (opcional)
            recurrence_end: Nueva fecha de fin de recurrencia (opcional)
            reminder_before_days: Nuevos días de recordatorio (opcional)
            location: Nueva ubicación (opcional)

        Returns:
            Alert actualizada

        Raises:
            NotFoundException: Si la alerta no existe
        """
        alert = await self._alert_repository.get_by_id(alert_id)
        if alert is None:
            raise NotFoundException(resource="Alert", field="id", value=str(alert_id))

        # Actualizar campos si se proporcionan
        if title is not None:
            alert.title = title
        if message is not None:
            alert.message = message
        if status is not None:
            alert.status = status
        if scheduled_at is not None:
            alert.scheduled_at = scheduled_at
        if recurrence is not None:
            alert.recurrence = recurrence
        if recurrence_end is not None:
            alert.recurrence_end = recurrence_end
        if reminder_before_days is not None:
            alert.reminder_before_days = reminder_before_days
        if location is not None:
            alert.location = location

        return await self._alert_repository.save(alert)
