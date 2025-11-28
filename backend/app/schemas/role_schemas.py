"""
Role Schemas - Pydantic DTOs
Request/Response models para API de roles
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RoleCreateRequest(BaseModel):
    """Request para crear un rol."""

    name: str = Field(..., description="Nombre del rol", min_length=1, max_length=50)
    description: str | None = Field(None, description="Descripción del rol", max_length=500)
    priority: str = Field(
        default="Invitado",
        description="Prioridad del rol: Invitado, Usuario, Administrador, etc.",
    )
    permissions: list[str] = Field(
        default_factory=list, description="Lista de permisos del rol"
    )


class RoleUpdateRequest(BaseModel):
    """Request para actualizar un rol."""

    name: str | None = Field(None, min_length=1, max_length=50)
    description: str | None = Field(None, max_length=500)
    priority: str | None = None
    permissions: list[str] | None = None


class RoleResponse(BaseModel):
    """Response de un rol."""

    id: UUID
    name: str
    description: str | None = None
    priority: str
    permissions: list[str]
    created_at: datetime
    last_updated: datetime

    class Config:
        from_attributes = True


class RolesListResponse(BaseModel):
    """Response de lista de roles."""

    total: int
    roles: list[RoleResponse]
    page: int = 1
    page_size: int = 50

