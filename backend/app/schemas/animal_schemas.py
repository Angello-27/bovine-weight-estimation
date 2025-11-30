"""
Animal Schemas - Pydantic DTOs
Request/Response models para API de animales
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ..domain.shared.constants import BreedType


class AnimalCreateRequest(BaseModel):
    """Request para crear un animal."""

    ear_tag: str = Field(..., description="Número de caravana (único)", min_length=1)
    breed: BreedType = Field(..., description="Raza del animal")
    birth_date: datetime = Field(..., description="Fecha de nacimiento")
    gender: str = Field(..., description="Género: male o female")

    # Opcionales
    name: str | None = Field(None, description="Nombre del animal")
    color: str | None = None
    birth_weight_kg: float | None = Field(None, ge=0, le=100)
    mother_id: UUID | None = None
    father_id: UUID | None = None
    observations: str | None = None
    photo_url: str | None = None
    farm_id: UUID = Field(..., description="ID de la hacienda")

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        """Valida género."""
        if v not in ["male", "female"]:
            raise ValueError("Gender debe ser 'male' o 'female'")
        return v

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: datetime) -> datetime:
        """Valida que la fecha de nacimiento sea válida."""
        if v > datetime.utcnow():
            raise ValueError("Fecha de nacimiento no puede ser futura")
        return v


class AnimalUpdateRequest(BaseModel):
    """Request para actualizar un animal."""

    name: str | None = None
    color: str | None = None
    observations: str | None = None
    status: str | None = None
    photo_url: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        """Valida status."""
        if v is not None and v not in ["active", "inactive", "sold", "deceased"]:
            raise ValueError("Status debe ser: active, inactive, sold o deceased")
        return v


class AnimalResponse(BaseModel):
    """Response de un animal."""

    id: UUID
    ear_tag: str
    breed: BreedType
    birth_date: datetime
    gender: str
    name: str | None = None
    color: str | None = None
    birth_weight_kg: float | None = None
    status: str
    farm_id: UUID
    registration_date: datetime
    last_updated: datetime

    # Campos calculados
    age_months: int
    age_category: str

    class Config:
        from_attributes = True


class AnimalsListResponse(BaseModel):
    """Response de lista de animales."""

    total: int
    animals: list[AnimalResponse]
    page: int = 1
    page_size: int = 50


# ===== Trazabilidad Schemas =====


class AnimalLineageResponse(BaseModel):
    """Response de linaje de un animal."""

    animal: AnimalResponse
    mother: AnimalResponse | None = None
    father: AnimalResponse | None = None
    descendants: list[AnimalResponse] = Field(default_factory=list)
    descendants_count: int = 0

    class Config:
        from_attributes = True


class TimelineEventData(BaseModel):
    """Datos adicionales de un evento del timeline."""

    ear_tag: str | None = None
    farm_id: str | None = None
    breed: str | None = None
    gender: str | None = None
    birth_weight_kg: float | None = None
    estimated_weight_kg: float | None = None
    confidence: float | None = None
    method: str | None = None
    ml_model_version: str | None = None
    gps_latitude: float | None = None
    gps_longitude: float | None = None
    frame_image_path: str | None = None
    processing_time_ms: int | None = None
    status: str | None = None


class TimelineEvent(BaseModel):
    """Evento individual del timeline."""

    type: str = Field(
        ...,
        description="Tipo de evento: registration, birth, weight_estimation, update, status_change",
    )
    timestamp: datetime
    description: str
    data: TimelineEventData = Field(default_factory=TimelineEventData)

    class Config:
        from_attributes = True


class AnimalTimelineResponse(BaseModel):
    """Response del timeline completo de un animal."""

    animal: AnimalResponse
    events: list[TimelineEvent]
    total_events: int
    weight_estimations_count: int

    class Config:
        from_attributes = True
