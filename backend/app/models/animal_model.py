"""
Animal Model - Beanie ODM
Modelo de persistencia para animales bovinos en MongoDB
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field

from ..core.constants import BreedType, AgeCategory


class AnimalModel(Document):
    """
    Modelo de animal bovino para MongoDB.

    Implementa patrón Active Record con Beanie ODM.
    Single Responsibility: Persistencia de datos de animales.
    """

    # ID único del animal
    id: UUID = Field(default_factory=uuid4, alias="_id")

    # Datos básicos (obligatorios)
    ear_tag: Indexed(str, unique=True) = Field(
        ..., description="Número de caravana/arete (único)"
    )
    breed: Indexed(BreedType) = Field(..., description="Raza del animal (una de las 7)")
    birth_date: datetime = Field(..., description="Fecha de nacimiento")
    gender: Indexed(str) = Field(..., description="Género: male o female")

    # Datos opcionales
    name: Optional[str] = Field(None, description="Nombre del animal")
    color: Optional[str] = Field(None, description="Color del pelaje")
    birth_weight_kg: Optional[float] = Field(
        None, description="Peso al nacer en kg", ge=0, le=100
    )
    mother_id: Optional[UUID] = Field(None, description="ID de la madre")
    father_id: Optional[UUID] = Field(None, description="ID del padre")
    observations: Optional[str] = Field(None, description="Observaciones adicionales")
    photo_url: Optional[str] = Field(None, description="URL de foto del animal")

    # Estado
    status: Indexed(str) = Field(
        default="active", description="Estado: active/inactive/sold/deceased"
    )

    # Metadata
    farm_id: UUID = Field(..., description="ID de la hacienda")
    registration_date: datetime = Field(
        default_factory=datetime.utcnow, description="Fecha de registro en el sistema"
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Última actualización"
    )

    # Sincronización (US-005)
    device_id: Optional[str] = Field(
        None, description="ID del dispositivo que creó el registro"
    )
    synced_at: Optional[datetime] = Field(
        None, description="Timestamp de última sincronización"
    )

    class Settings:
        """Configuración de Beanie."""

        name = "animals"  # Nombre de la colección en MongoDB
        use_state_management = True
        validate_on_save = True

        # Índices para optimizar queries
        indexes = [
            "ear_tag",  # UNIQUE - búsqueda por caravana
            "breed",  # Filtro por raza
            "status",  # Filtro por estado
            "farm_id",  # Filtro por hacienda
            "registration_date",  # Ordenamiento cronológico
            [("ear_tag", 1), ("farm_id", 1)],  # Índice compuesto para búsqueda
        ]

    def calculate_age_months(self) -> int:
        """
        Calcula edad actual del animal en meses.

        Returns:
            Edad en meses
        """
        now = datetime.utcnow()
        return (now.year - self.birth_date.year) * 12 + (
            now.month - self.birth_date.month
        )

    def calculate_age_category(self) -> AgeCategory:
        """
        Calcula categoría de edad automáticamente.

        Returns:
            AgeCategory correspondiente según edad
        """
        return AgeCategory.from_age_months(self.calculate_age_months())

    def update_timestamp(self) -> None:
        """Actualiza timestamp de last_updated."""
        self.last_updated = datetime.utcnow()

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "_id": "550e8400-e29b-41d4-a716-446655440000",
                "ear_tag": "HG-BRA-001",
                "breed": "brahman",
                "birth_date": "2023-01-15T00:00:00Z",
                "gender": "female",
                "name": "Luna",
                "status": "active",
                "farm_id": "farm-001",
            }
        }

