"""
Farm Schemas - Pydantic DTOs
Request/Response models para API de fincas
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class FarmCreateRequest(BaseModel):
    """Request para crear una finca."""

    name: str = Field(..., description="Nombre de la finca", min_length=1, max_length=200)
    owner_id: UUID = Field(..., description="ID del propietario")
    latitude: float = Field(..., description="Latitud GPS", ge=-90, le=90)
    longitude: float = Field(..., description="Longitud GPS", ge=-180, le=180)
    capacity: int = Field(..., description="Capacidad máxima de animales", ge=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Valida que el nombre no esté vacío."""
        if not v.strip():
            raise ValueError("El nombre de la finca no puede estar vacío")
        return v.strip()


class FarmUpdateRequest(BaseModel):
    """Request para actualizar una finca."""

    name: str | None = Field(None, min_length=1, max_length=200)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    capacity: int | None = Field(None, ge=1)


class FarmResponse(BaseModel):
    """Response de una finca."""

    id: UUID
    name: str
    owner_id: UUID
    latitude: float
    longitude: float
    capacity: int
    total_animals: int
    created_at: datetime
    last_updated: datetime

    class Config:
        from_attributes = True


class FarmsListResponse(BaseModel):
    """Response de lista de fincas."""

    total: int
    farms: list[FarmResponse]
    page: int = 1
    page_size: int = 50

