"""
User Entity - Domain Layer
Entidad pura del dominio sin dependencias externas
"""

from datetime import datetime
from uuid import UUID, uuid4


class User:
    """
    Entidad User del dominio.

    Single Responsibility: Representar un usuario en el dominio.
    Sin dependencias de frameworks (Beanie, FastAPI, etc.)
    """

    def __init__(
        self,
        id: UUID | None = None,
        username: str = "",
        email: str = "",
        hashed_password: str = "",
        first_name: str | None = None,
        last_name: str | None = None,
        role_id: UUID | None = None,
        farm_id: UUID | None = None,
        is_active: bool = True,
        is_superuser: bool = False,
        created_at: datetime | None = None,
        last_updated: datetime | None = None,
        last_login: datetime | None = None,
    ):
        """Inicializa entidad User."""
        self.id = id or uuid4()
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.first_name = first_name
        self.last_name = last_name
        self.role_id = role_id
        self.farm_id = farm_id
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.created_at = created_at or datetime.utcnow()
        self.last_updated = last_updated or datetime.utcnow()
        self.last_login = last_login

    def update_timestamp(self) -> None:
        """Actualiza timestamp de last_updated."""
        self.last_updated = datetime.utcnow()

    def update_last_login(self) -> None:
        """Actualiza timestamp de último login."""
        self.last_login = datetime.utcnow()

    def __eq__(self, other: object) -> bool:
        """Compara dos usuarios por ID."""
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash basado en ID."""
        return hash(self.id)
