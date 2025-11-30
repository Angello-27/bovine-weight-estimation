"""
Alert Entity - Domain Layer
Entidad pura del dominio sin dependencias externas
"""

from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4


class AlertType(str, Enum):
    """Tipos de alertas disponibles."""

    # Alertas automáticas
    WEIGHT_LOSS = "weight_loss"
    STAGNATION = "stagnation"
    SYSTEM = "system"

    # Alertas programadas (cronograma)
    SCHEDULED_WEIGHING = "scheduled_weighing"
    VETERINARY_TREATMENT = "veterinary_treatment"
    CALENDAR_EVENT = "calendar_event"
    ROUTE_PLANNING = "route_planning"
    REMINDER = "reminder"  # Genérico para recordatorios


class AlertStatus(str, Enum):
    """Estados de una alerta."""

    PENDING = "pending"  # Programada, aún no enviada
    SENT = "sent"  # Enviada al usuario
    READ = "read"  # Leída por el usuario
    CANCELLED = "cancelled"  # Cancelada
    COMPLETED = "completed"  # Evento completado


class RecurrenceType(str, Enum):
    """Tipos de recurrencia para alertas programadas."""

    NONE = "none"  # Una sola vez
    DAILY = "daily"  # Diario
    WEEKLY = "weekly"  # Semanal
    MONTHLY = "monthly"  # Mensual
    QUARTERLY = "quarterly"  # Trimestral
    YEARLY = "yearly"  # Anual
    CUSTOM = "custom"  # Personalizado


class Alert:
    """
    Entidad Alert del dominio.

    Single Responsibility: Representar una alerta o evento programado en el dominio.
    Sin dependencias de frameworks (Beanie, FastAPI, etc.)
    """

    def __init__(
        self,
        id: UUID | None = None,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
        type: AlertType | str = AlertType.SYSTEM,
        title: str = "",
        message: str = "",
        status: AlertStatus | str = AlertStatus.PENDING,
        scheduled_at: datetime | None = None,
        recurrence: RecurrenceType | str = RecurrenceType.NONE,
        recurrence_end: datetime | None = None,
        reminder_before_days: list[int] | None = None,
        related_entity_type: str | None = None,
        related_entity_id: UUID | None = None,
        filter_criteria: dict | None = None,
        location: dict | None = None,
        created_at: datetime | None = None,
        sent_at: datetime | None = None,
        read_at: datetime | None = None,
        completed_at: datetime | None = None,
    ):
        """Inicializa entidad Alert."""
        self.id = id or uuid4()
        self.user_id = user_id
        self.farm_id = farm_id
        self.type = type if isinstance(type, AlertType) else AlertType(type)
        self.title = title
        self.message = message
        self.status = status if isinstance(status, AlertStatus) else AlertStatus(status)
        self.scheduled_at = scheduled_at
        self.recurrence = (
            recurrence
            if isinstance(recurrence, RecurrenceType)
            else RecurrenceType(recurrence)
        )
        self.recurrence_end = recurrence_end
        self.reminder_before_days = reminder_before_days or []
        self.related_entity_type = related_entity_type
        self.related_entity_id = related_entity_id
        self.filter_criteria = filter_criteria
        self.location = location
        self.created_at = created_at or datetime.utcnow()
        self.sent_at = sent_at
        self.read_at = read_at
        self.completed_at = completed_at

    def is_scheduled(self) -> bool:
        """
        Verifica si la alerta está programada para el futuro.

        Returns:
            True si está programada y aún no ha pasado la fecha
        """
        if self.scheduled_at is None:
            return False
        return self.scheduled_at > datetime.utcnow()

    def should_send_reminder(self, days_before: int) -> bool:
        """
        Verifica si debe enviarse recordatorio X días antes.

        Args:
            days_before: Días antes del evento

        Returns:
            True si debe enviarse el recordatorio ahora
        """
        if not self.scheduled_at:
            return False

        days_until = (self.scheduled_at - datetime.utcnow()).days
        return days_until == days_before

    def mark_as_sent(self) -> None:
        """Marca la alerta como enviada."""
        self.status = AlertStatus.SENT
        self.sent_at = datetime.utcnow()

    def mark_as_read(self) -> None:
        """Marca la alerta como leída."""
        self.status = AlertStatus.READ
        self.read_at = datetime.utcnow()

    def mark_as_completed(self) -> None:
        """Marca el evento como completado."""
        self.status = AlertStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def cancel(self) -> None:
        """Cancela la alerta."""
        self.status = AlertStatus.CANCELLED

    def get_next_recurrence_date(self) -> datetime | None:
        """
        Calcula la próxima fecha de recurrencia.

        Returns:
            Próxima fecha o None si no hay recurrencia
        """
        if self.recurrence == RecurrenceType.NONE or not self.scheduled_at:
            return None

        if self.recurrence_end and datetime.utcnow() >= self.recurrence_end:
            return None

        now = datetime.utcnow()
        next_date = self.scheduled_at

        # Calcular siguiente fecha según tipo de recurrencia
        while next_date <= now:
            if self.recurrence == RecurrenceType.DAILY:
                next_date += timedelta(days=1)
            elif self.recurrence == RecurrenceType.WEEKLY:
                next_date += timedelta(weeks=1)
            elif self.recurrence == RecurrenceType.MONTHLY:
                next_date += timedelta(days=30)
            elif self.recurrence == RecurrenceType.QUARTERLY:
                next_date += timedelta(days=90)
            elif self.recurrence == RecurrenceType.YEARLY:
                next_date += timedelta(days=365)
            else:
                return None

            if self.recurrence_end and next_date > self.recurrence_end:
                return None

        return next_date

    def update_timestamp(self) -> None:
        """Actualiza timestamp de last_updated."""
        # Nota: Alert no tiene last_updated, pero mantenemos consistencia con otras entidades
        pass

    def __eq__(self, other: object) -> bool:
        """Compara dos alertas por ID."""
        if not isinstance(other, Alert):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash basado en ID."""
        return hash(self.id)
