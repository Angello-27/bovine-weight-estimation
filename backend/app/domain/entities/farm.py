"""
Farm Entity - Domain Layer
Entidad pura del dominio sin dependencias externas
"""

from datetime import datetime
from uuid import UUID, uuid4


class Farm:
    """
    Entidad Farm del dominio.

    Single Responsibility: Representar una finca/hacienda en el dominio.
    Sin dependencias de frameworks (Beanie, FastAPI, etc.)
    """

    def __init__(
        self,
        id: UUID | None = None,
        name: str = "",
        owner_id: UUID | None = None,
        latitude: float = 0.0,
        longitude: float = 0.0,
        capacity: int = 0,
        total_animals: int = 0,
        created_at: datetime | None = None,
        last_updated: datetime | None = None,
    ):
        """Inicializa entidad Farm."""
        self.id = id or uuid4()
        self.name = name
        self.owner_id = owner_id
        self.latitude = latitude
        self.longitude = longitude
        self.capacity = capacity
        self.total_animals = total_animals
        self.created_at = created_at or datetime.utcnow()
        self.last_updated = last_updated or datetime.utcnow()

    def get_location_dict(self) -> dict:
        """
        Convierte coordenadas a formato GeoJSON Point.

        Returns:
            Dict con formato GeoJSON Point
        """
        return {
            "type": "Point",
            "coordinates": [self.longitude, self.latitude],  # [lon, lat]
        }

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

    def update_timestamp(self) -> None:
        """Actualiza timestamp de last_updated."""
        self.last_updated = datetime.utcnow()

    def __eq__(self, other: object) -> bool:
        """Compara dos fincas por ID."""
        if not isinstance(other, Farm):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash basado en ID."""
        return hash(self.id)
