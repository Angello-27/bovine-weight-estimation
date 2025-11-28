"""
User Schemas - Pydantic DTOs
Request/Response models para API de usuarios
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    """Request para crear un usuario."""

    username: str = Field(..., description="Nombre de usuario", min_length=3, max_length=50)
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña", min_length=6)
    role_id: UUID = Field(..., description="ID del rol asignado")
    farm_id: UUID | None = Field(None, description="ID de la finca principal del usuario")


class UserUpdateRequest(BaseModel):
    """Request para actualizar un usuario."""

    email: EmailStr | None = None
    password: str | None = Field(None, description="Nueva contraseña", min_length=6)
    role_id: UUID | None = None
    farm_id: UUID | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    """Response de un usuario."""

    id: UUID
    username: str
    email: str
    role_id: UUID
    farm_id: UUID | None = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    last_updated: datetime
    last_login: datetime | None = None

    class Config:
        from_attributes = True


class UsersListResponse(BaseModel):
    """Response de lista de usuarios."""

    total: int
    users: list[UserResponse]
    page: int = 1
    page_size: int = 50

