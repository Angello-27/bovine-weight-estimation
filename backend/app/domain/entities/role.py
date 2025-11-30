"""
Role Entity - Domain Layer
Entidad pura del dominio sin dependencias externas
"""

from datetime import datetime
from uuid import UUID, uuid4


class Role:
    """
    Entidad Role del dominio.

    Single Responsibility: Representar un rol en el dominio.
    Sin dependencias de frameworks (Beanie, FastAPI, etc.)
    """

    def __init__(
        self,
        id: UUID | None = None,
        name: str = "",
        description: str | None = None,
        priority: str = "Invitado",
        permissions: list[str] | None = None,
        created_at: datetime | None = None,
        last_updated: datetime | None = None,
    ):
        """Inicializa entidad Role."""
        self.id = id or uuid4()
        self.name = name
        self.description = description
        self.priority = priority
        self.permissions = permissions or []
        self.created_at = created_at or datetime.utcnow()
        self.last_updated = last_updated or datetime.utcnow()

    def update_timestamp(self) -> None:
        """Actualiza timestamp de last_updated."""
        self.last_updated = datetime.utcnow()

    def __eq__(self, other: object) -> bool:
        """Compara dos roles por ID."""
        if not isinstance(other, Role):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash basado en ID."""
        return hash(self.id)
