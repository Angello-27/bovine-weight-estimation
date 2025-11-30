"""
Create Alert Use Case - Domain Layer
Caso de uso para crear una alerta
"""

from datetime import datetime
from uuid import UUID

from ....core.exceptions import NotFoundException, ValidationException
from ...entities.alert import Alert
from ...repositories.alert_repository import AlertRepository
from ...repositories.user_repository import UserRepository


class CreateAlertUseCase:
    """
    Caso de uso para crear una alerta.

    Single Responsibility: Validar y crear una alerta en el dominio.
    """

    def __init__(
        self,
        alert_repository: AlertRepository,
        user_repository: UserRepository,
    ):
        """
        Inicializa el caso de uso.

        Args:
            alert_repository: Repositorio de alertas (inyección de dependencia)
            user_repository: Repositorio de usuarios (inyección de dependencia)
        """
        self._alert_repository = alert_repository
        self._user_repository = user_repository

    async def execute(
        self,
        user_id: UUID,
        farm_id: UUID | None,
        type: str,
        title: str,
        message: str,
        scheduled_at: datetime | None = None,
        recurrence: str = "none",
        recurrence_end: datetime | None = None,
        reminder_before_days: list[int] | None = None,
        related_entity_type: str | None = None,
        related_entity_id: UUID | None = None,
        filter_criteria: dict | None = None,
        location: dict | None = None,
    ) -> Alert:
        """
        Ejecuta el caso de uso para crear una alerta.

        Args:
            user_id: ID del usuario
            farm_id: ID de la finca (opcional)
            type: Tipo de alerta
            title: Título de la alerta
            message: Mensaje de la alerta
            scheduled_at: Fecha/hora programada (opcional)
            recurrence: Tipo de recurrencia
            recurrence_end: Fecha de fin de recurrencia (opcional)
            reminder_before_days: Días antes para recordatorios (opcional)
            related_entity_type: Tipo de entidad relacionada (opcional)
            related_entity_id: ID de entidad relacionada (opcional)
            filter_criteria: Criterios de filtro (opcional)
            location: Ubicación GeoJSON (opcional)

        Returns:
            Alert creada

        Raises:
            NotFoundException: Si el usuario no existe
            ValidationException: Si los datos son inválidos
        """
        # Validar que el usuario exista
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(resource="User", field="id", value=str(user_id))

        # Crear entidad Alert
        alert = Alert(
            user_id=user_id,
            farm_id=farm_id,
            type=type,
            title=title,
            message=message,
            scheduled_at=scheduled_at,
            recurrence=recurrence,
            recurrence_end=recurrence_end,
            reminder_before_days=reminder_before_days or [],
            related_entity_type=related_entity_type,
            related_entity_id=related_entity_id,
            filter_criteria=filter_criteria,
            location=location,
        )

        # Guardar usando el repositorio
        return await self._alert_repository.save(alert)
