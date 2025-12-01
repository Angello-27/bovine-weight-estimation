"""
Auth Schemas - Pydantic DTOs
Request/Response models para autenticación
"""

from uuid import UUID

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Request para iniciar sesión."""

    username: str = Field(..., description="Nombre de usuario", min_length=3)
    password: str = Field(..., description="Contraseña", min_length=1)


class LoginResponse(BaseModel):
    """Response después de iniciar sesión exitosamente."""

    id: UUID
    username: str
    role: str  # Nombre del rol
    role_priority: str  # Prioridad del rol (Invitado, Usuario, Administrador)
    role_id: UUID
    farm_id: UUID | None = None  # ID de la finca principal del usuario
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """Datos del token JWT."""

    user_id: UUID | None = None
    username: str | None = None
