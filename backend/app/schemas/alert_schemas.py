"""
Alert Schemas - Pydantic DTOs
Request/Response models para API de alertas
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ..domain.entities.alert import AlertStatus, AlertType, RecurrenceType


class AlertCreateRequest(BaseModel):
    """Request para crear una alerta."""

    user_id: UUID = Field(..., description="ID del usuario")
    farm_id: UUID | None = Field(None, description="ID de la finca (opcional)")
    type: AlertType = Field(..., description="Tipo de alerta")
    title: str = Field(
        ..., description="Título de la alerta", min_length=1, max_length=200
    )
    message: str = Field(
        ..., description="Mensaje de la alerta", min_length=1, max_length=1000
    )
    scheduled_at: datetime | None = Field(None, description="Fecha/hora programada")
    recurrence: RecurrenceType = Field(
        default=RecurrenceType.NONE, description="Tipo de recurrencia"
    )
    recurrence_end: datetime | None = Field(
        None, description="Fecha de fin de recurrencia"
    )
    reminder_before_days: list[int] = Field(
        default_factory=list, description="Días antes para recordatorios (ej: [7, 1])"
    )
    related_entity_type: str | None = Field(
        None, description="Tipo de entidad relacionada"
    )
    related_entity_id: UUID | None = Field(
        None, description="ID de la entidad relacionada"
    )
    filter_criteria: dict | None = Field(
        None,
        description=(
            "Criterios para filtrar animales en alertas de hatos: "
            "{'breed': 'nelore', 'age_category': 'terneros', 'gender': 'female', 'count': 50}"
        ),
    )
    latitude: float | None = Field(None, description="Latitud GPS", ge=-90, le=90)
    longitude: float | None = Field(None, description="Longitud GPS", ge=-180, le=180)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Valida que el título no esté vacío."""
        if not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v.strip()

    @field_validator("reminder_before_days")
    @classmethod
    def validate_reminder_days(cls, v: list[int]) -> list[int]:
        """Valida que los días de recordatorio sean positivos."""
        if any(day < 0 for day in v):
            raise ValueError("Los días de recordatorio deben ser positivos")
        return sorted(set(v), reverse=True)  # Ordenar y eliminar duplicados


class AlertUpdateRequest(BaseModel):
    """Request para actualizar una alerta."""

    title: str | None = Field(None, min_length=1, max_length=200)
    message: str | None = Field(None, min_length=1, max_length=1000)
    status: AlertStatus | None = None
    scheduled_at: datetime | None = None
    recurrence: RecurrenceType | None = None
    recurrence_end: datetime | None = None
    reminder_before_days: list[int] | None = None
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)


class AlertResponse(BaseModel):
    """Response de una alerta."""

    id: UUID
    user_id: UUID
    farm_id: UUID | None
    type: AlertType
    title: str
    message: str
    status: AlertStatus
    scheduled_at: datetime | None
    recurrence: RecurrenceType
    recurrence_end: datetime | None
    reminder_before_days: list[int]
    related_entity_type: str | None
    related_entity_id: UUID | None
    filter_criteria: dict | None
    location: dict | None
    created_at: datetime
    sent_at: datetime | None
    read_at: datetime | None
    completed_at: datetime | None

    class Config:
        from_attributes = True


class AlertsListResponse(BaseModel):
    """Response de lista de alertas."""

    total: int
    alerts: list[AlertResponse]
    page: int = 1
    page_size: int = 50


class AlertFilterParams(BaseModel):
    """Parámetros de filtro para listar alertas."""

    user_id: UUID | None = None
    farm_id: UUID | None = None
    type: AlertType | None = None
    status: AlertStatus | None = None
    scheduled_from: datetime | None = None
    scheduled_to: datetime | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=100)
