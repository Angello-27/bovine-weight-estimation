"""
Animal Entity - Domain Layer
Entidad pura del dominio sin dependencias externas
"""

from datetime import datetime
from uuid import UUID, uuid4

from ..shared.constants import AgeCategory


class Animal:
    """
    Entidad Animal del dominio.

    Single Responsibility: Representar un animal bovino en el dominio.
    Sin dependencias de frameworks (Beanie, FastAPI, etc.)
    """

    def __init__(
        self,
        id: UUID | None = None,
        ear_tag: str = "",
        breed: str = "",
        birth_date: datetime | None = None,
        gender: str = "",
        name: str | None = None,
        color: str | None = None,
        birth_weight_kg: float | None = None,
        mother_id: str | None = None,
        father_id: str | None = None,
        observations: str | None = None,
        photo_url: str | None = None,
        status: str = "active",
        farm_id: UUID | None = None,
        registration_date: datetime | None = None,
        last_updated: datetime | None = None,
        device_id: str | None = None,
        synced_at: datetime | None = None,
    ):
        """Inicializa entidad Animal."""
        self.id = id or uuid4()
        self.ear_tag = ear_tag
        self.breed = breed
        self.birth_date = birth_date or datetime.utcnow()
        self.gender = gender
        self.name = name
        self.color = color
        self.birth_weight_kg = birth_weight_kg
        self.mother_id = mother_id
        self.father_id = father_id
        self.observations = observations
        self.photo_url = photo_url
        self.status = status
        self.farm_id = farm_id
        self.registration_date = registration_date or datetime.utcnow()
        self.last_updated = last_updated or datetime.utcnow()
        self.device_id = device_id
        self.synced_at = synced_at

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

    def __eq__(self, other: object) -> bool:
        """Compara dos animales por ID."""
        if not isinstance(other, Animal):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash basado en ID."""
        return hash(self.id)
