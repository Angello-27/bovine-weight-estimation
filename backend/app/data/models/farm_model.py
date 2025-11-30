"""
Farm Model - Beanie ODM
Modelo de persistencia para fincas/haciendas en MongoDB
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field

from ...domain.entities.farm import Farm


class FarmModel(Document):
    """
    Modelo de finca/hacienda para MongoDB.

    Representa una finca ganadera (ej: Hacienda Gamelera).
    Implementa patrón Active Record con Beanie ODM.
    Single Responsibility: Persistencia de datos de fincas.
    """

    # ID único de la finca
    id: UUID = Field(default_factory=uuid4, alias="_id")  # type: ignore[assignment]

    # Datos básicos
    name: Indexed(str) = Field(  # type: ignore
        ...,
        description="Nombre de la finca (ej: Hacienda Gamelera)",
        min_length=1,
        max_length=200,
    )
    owner_id: Annotated[UUID, Indexed()] = Field(  # type: ignore
        ..., description="ID del propietario (UserModel)"
    )

    # Ubicación (GeoJSON Point)
    location: dict = Field(
        ...,
        description="GeoJSON Point: {type: 'Point', coordinates: [longitude, latitude]}",
    )

    # Capacidad y animales
    capacity: int = Field(..., description="Capacidad máxima de animales", ge=1)
    total_animals: int = Field(
        default=0, description="Total actual de animales registrados", ge=0
    )

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Fecha de creación"
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Última actualización"
    )

    class Settings:
        """Configuración de Beanie."""

        name = "farms"  # Nombre de la colección en MongoDB
        use_state_management = True
        validate_on_save = True

        # Índices para optimizar queries
        indexes = [
            "name",  # Búsqueda por nombre
            "owner_id",  # Filtro por propietario
            [("owner_id", 1), ("name", 1)],  # Índice compuesto
        ]

    def update_timestamp(self) -> None:
        """Actualiza timestamp de last_updated."""
        self.last_updated = datetime.utcnow()

    def increment_animal_count(self) -> None:
        """Incrementa el contador de animales."""
        if self.total_animals < self.capacity:
            self.total_animals += 1
            self.update_timestamp()

    def decrement_animal_count(self) -> None:
        """Decrementa el contador de animales."""
        if self.total_animals > 0:
            self.total_animals -= 1
            self.update_timestamp()

    def get_location_coordinates(self) -> tuple[float, float]:
        """
        Extrae coordenadas de location GeoJSON.

        Returns:
            Tupla (longitude, latitude)
        """
        coords = self.location.get("coordinates", [])
        if len(coords) >= 2:
            return (coords[0], coords[1])
        return (0.0, 0.0)

    @classmethod
    def from_entity(cls, farm: Farm) -> "FarmModel":
        """
        Crea un FarmModel desde una entidad Farm.

        Args:
            farm: Entidad Farm del dominio

        Returns:
            FarmModel para persistencia
        """
        return cls(
            id=farm.id,
            name=farm.name,
            owner_id=farm.owner_id,
            location=farm.get_location_dict(),
            capacity=farm.capacity,
            total_animals=farm.total_animals,
            created_at=farm.created_at,
            last_updated=farm.last_updated,
        )

    def to_entity(self) -> Farm:
        """
        Convierte FarmModel a entidad Farm.

        Returns:
            Farm entity del dominio
        """
        lon, lat = self.get_location_coordinates()
        return Farm(
            id=self.id,
            name=self.name,
            owner_id=self.owner_id,
            latitude=lat,
            longitude=lon,
            capacity=self.capacity,
            total_animals=self.total_animals,
            created_at=self.created_at,
            last_updated=self.last_updated,
        )

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "_id": "770e8400-e29b-41d4-a716-446655440000",
                "name": "Hacienda Gamelera",
                "owner_id": "550e8400-e29b-41d4-a716-446655440000",
                "location": {
                    "type": "Point",
                    "coordinates": [-60.797889, -15.859500],  # [lon, lat]
                },
                "capacity": 500,
                "total_animals": 0,
            }
        }
