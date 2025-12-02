"""
Weighing Schemas - Pydantic DTOs
Request/Response models para API de pesajes
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ..domain.shared.constants import BreedType, SystemMetrics


class WeighingCreateRequest(BaseModel):
    """Request para crear una estimación de peso."""

    animal_id: UUID | None = Field(None, description="ID del animal (opcional)")
    breed: BreedType = Field(..., description="Raza del animal")
    estimated_weight_kg: float = Field(
        ..., description="Peso estimado en kg", ge=0, le=1500
    )
    confidence: float = Field(..., description="Confidence score (0.0-1.0)", ge=0, le=1)
    processing_time_ms: int = Field(..., description="Tiempo de procesamiento en ms")
    frame_image_path: str = Field(..., description="Path del fotograma")

    # Opcionales
    method: str = Field(default="tflite", description="Método de estimación")
    ml_model_version: str = Field(default="1.0.0", description="Versión del modelo ML")
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    device_id: str | None = None

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Valida confidence."""
        if v < SystemMetrics.MIN_CONFIDENCE:
            raise ValueError(
                f"Confidence {v:.2%} < {SystemMetrics.MIN_CONFIDENCE:.0%} mínimo"
            )
        return v


class AnimalInfo(BaseModel):
    """Información básica del animal para incluir en la respuesta de estimación."""

    id: UUID
    name: str | None = None
    ear_tag: str | None = None

    class Config:
        from_attributes = True


class WeighingResponse(BaseModel):
    """Response de una estimación de peso."""

    id: UUID
    animal_id: UUID | None
    animal: AnimalInfo | None = None  # Información del animal si está disponible
    breed: BreedType
    estimated_weight_kg: float
    confidence: float
    confidence_level: str  # high/medium/low
    method: str
    ml_model_version: str
    processing_time_ms: int
    latitude: float | None
    longitude: float | None
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class WeighingsListResponse(BaseModel):
    """Response de lista de pesajes."""

    total: int
    weighings: list[WeighingResponse]
    page: int = 1
    page_size: int = 50
