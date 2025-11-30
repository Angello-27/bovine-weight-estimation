"""
User Model - Beanie ODM
Modelo de persistencia para usuarios en MongoDB
"""

from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class UserModel(Document):
    """
    Modelo de usuario para MongoDB.

    Implementa patrón Active Record con Beanie ODM.
    Single Responsibility: Persistencia de datos de usuarios.
    """

    # ID único del usuario
    id: UUID = Field(default_factory=uuid4, alias="_id")

    # Datos de autenticación
    username: Indexed(str, unique=True) = Field(
        ..., description="Nombre de usuario (único)", min_length=3, max_length=50
    )
    email: Indexed(EmailStr, unique=True) = Field(
        ..., description="Email del usuario (único)"
    )
    hashed_password: str = Field(..., description="Contraseña hasheada con bcrypt")

    # Relación con rol
    role_id: UUID = Field(..., description="ID del rol asignado al usuario")
    
    # Relación con finca (opcional - un usuario puede tener múltiples fincas)
    farm_id: UUID | None = Field(
        None, description="ID de la finca principal del usuario"
    )

    # Estado
    is_active: bool = Field(default=True, description="Usuario activo/inactivo")
    is_superuser: bool = Field(
        default=False, description="Usuario administrador del sistema"
    )

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Fecha de creación"
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Última actualización"
    )
    last_login: datetime | None = Field(
        None, description="Último inicio de sesión"
    )

    class Settings:
        """Configuración de Beanie."""

        name = "users"  # Nombre de la colección en MongoDB
        use_state_management = True
        validate_on_save = True

        # Índices para optimizar queries
        indexes = [
            "username",  # UNIQUE - búsqueda por username
            "email",  # UNIQUE - búsqueda por email
            "role_id",  # Filtro por rol
            "farm_id",  # Filtro por finca
            "is_active",  # Filtro por estado activo
        ]

    def update_timestamp(self) -> None:
        """Actualiza timestamp de last_updated."""
        self.last_updated = datetime.utcnow()

    def update_last_login(self) -> None:
        """Actualiza timestamp de último login."""
        self.last_login = datetime.utcnow()

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "_id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "juan_perez",
                "email": "juan@example.com",
                "role_id": "660e8400-e29b-41d4-a716-446655440000",
                "is_active": True,
                "is_superuser": False,
            }
        }

