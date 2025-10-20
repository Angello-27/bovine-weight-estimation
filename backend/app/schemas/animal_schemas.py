"""
Animal Schemas - Pydantic DTOs
Request/Response models para API de animales
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ..core.constants import BreedType


class AnimalCreateRequest(BaseModel):
    """Request para crear un animal."""

    ear_tag: str = Field(..., description="Número de caravana (único)", min_length=1)
    breed: BreedType = Field(..., description="Raza del animal")
    birth_date: datetime = Field(..., description="Fecha de nacimiento")
    gender: str = Field(..., description="Género: male o female")

    # Opcionales
    name: Optional[str] = Field(None, description="Nombre del animal")
    color: Optional[str] = None
    birth_weight_kg: Optional[float] = Field(None, ge=0, le=100)
    mother_id: Optional[UUID] = None
    father_id: Optional[UUID] = None
    observations: Optional[str] = None
    photo_url: Optional[str] = None
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

    name: Optional[str] = None
    color: Optional[str] = None
    observations: Optional[str] = None
    status: Optional[str] = None
    photo_url: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        """Valida status."""
        if v is not None and v not in ["active", "inactive", "sold", "deceased"]:
            raise ValueError(
                "Status debe ser: active, inactive, sold o deceased"
            )
        return v


class AnimalResponse(BaseModel):
    """Response de un animal."""

    id: UUID
    ear_tag: str
    breed: BreedType
    birth_date: datetime
    gender: str
    name: Optional[str] = None
    color: Optional[str] = None
    birth_weight_kg: Optional[float] = None
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
    animals: List[AnimalResponse]
    page: int = 1
    page_size: int = 50

