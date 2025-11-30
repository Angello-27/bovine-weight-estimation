"""
Role Model - Beanie ODM
Modelo de persistencia para roles en MongoDB
"""

from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


class RoleModel(Document):
    """
    Modelo de rol para MongoDB.

    Implementa patrón Active Record con Beanie ODM.
    Single Responsibility: Persistencia de datos de roles.
    """

    # ID único del rol
    id: UUID = Field(default_factory=uuid4, alias="_id")

    # Datos del rol
    name: Indexed(str, unique=True) = Field(
        ..., description="Nombre del rol (único)", min_length=1, max_length=50
    )
    description: str | None = Field(
        None, description="Descripción del rol", max_length=500
    )
    priority: str = Field(
        default="Invitado",
        description="Prioridad del rol: Invitado, Usuario, Administrador, etc.",
    )

    # Permisos (puede expandirse en el futuro)
    permissions: list[str] = Field(
        default_factory=list, description="Lista de permisos del rol"
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

        name = "roles"  # Nombre de la colección en MongoDB
        use_state_management = True
        validate_on_save = True

        # Índices para optimizar queries
        indexes = [
            "name",  # UNIQUE - búsqueda por nombre
            "priority",  # Filtro por prioridad
        ]

    def update_timestamp(self) -> None:
        """Actualiza timestamp de last_updated."""
        self.last_updated = datetime.utcnow()

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "_id": "660e8400-e29b-41d4-a716-446655440000",
                "name": "Administrador",
                "description": "Rol con acceso completo al sistema",
                "priority": "Administrador",
                "permissions": ["read", "write", "delete", "admin"],
            }
        }

