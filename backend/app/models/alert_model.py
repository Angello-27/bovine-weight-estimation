"""
Alert Model - Beanie ODM
Modelo de persistencia para alertas y notificaciones con soporte para cronograma
"""

from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


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


class AlertModel(Document):
    """
    Modelo de alertas y notificaciones con soporte para cronograma.

    Single Responsibility: Persistencia de alertas y eventos programados.
    """

    # ID único
    id: UUID = Field(default_factory=uuid4, alias="_id")  # type: ignore

    # Usuario y finca
    user_id: Indexed(UUID) = Field(..., description="ID del usuario")  # type: ignore
    farm_id: UUID | None = Field(None, description="ID de la finca (opcional)")  # type: ignore

    # Tipo y contenido
    type: AlertType = Field(..., description="Tipo de alerta")
    title: str = Field(
        ..., description="Título de la alerta", min_length=1, max_length=200
    )
    message: str = Field(
        ..., description="Mensaje de la alerta", min_length=1, max_length=1000
    )
    status: AlertStatus = Field(
        default=AlertStatus.PENDING, description="Estado de la alerta"
    )

    # Cronograma (nuevo)
    scheduled_at: datetime | None = Field(
        None, description="Fecha/hora programada para la alerta o evento"
    )
    recurrence: RecurrenceType = Field(
        default=RecurrenceType.NONE, description="Tipo de recurrencia"
    )
    recurrence_end: datetime | None = Field(
        None, description="Fecha de fin de recurrencia"
    )
    reminder_before_days: list[int] = Field(
        default_factory=list,
        description="Días antes del evento para enviar recordatorios (ej: [7, 1])",
    )

    # Relaciones (nuevo)
    related_entity_type: str | None = Field(
        None, description="Tipo de entidad relacionada: 'animal', 'farm', 'session'"
    )
    related_entity_id: UUID | None = Field(
        None, description="ID de la entidad relacionada"
    )

    # Criterios de filtro para hatos/grupos (nuevo)
    filter_criteria: dict | None = Field(
        None,
        description=(
            "Criterios para filtrar animales en alertas de hatos: "
            "{'breed': 'nelore', 'age_category': 'terneros', 'gender': 'female', 'count': 50}"
        ),
    )

    # Ubicación (para rutas)
    location: dict | None = Field(
        None, description="GeoJSON Point para eventos con ubicación"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: datetime | None = None
    read_at: datetime | None = None
    completed_at: datetime | None = None

    class Settings:
        """Configuración de Beanie."""

        name = "alerts"  # Nombre de la colección en MongoDB
        use_state_management = True
        validate_on_save = True

        # Índices para optimizar queries
        indexes = [
            "user_id",
            "status",
            "type",
            "scheduled_at",  # Para consultas de cronograma
            "farm_id",
            [("user_id", 1), ("status", 1)],  # Índice compuesto
            [("scheduled_at", 1), ("status", 1)],  # Para procesar alertas programadas
        ]

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

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "_id": "770e8400-e29b-41d4-a716-446655440000",
                "user_id": "440e8400-e29b-41d4-a716-446655440000",
                "farm_id": "550e8400-e29b-41d4-a716-446655440000",
                "type": "scheduled_weighing",
                "title": "Sesión de Pesaje Masivo - Potrero Norte",
                "message": "Pesar 50 animales del potrero norte",
                "status": "pending",
                "scheduled_at": "2024-12-20T08:00:00Z",
                "recurrence": "none",
                "reminder_before_days": [7, 1],
                "related_entity_type": "session",
                "location": {
                    "type": "Point",
                    "coordinates": [-60.797889, -15.859500],
                },
            }
        }
