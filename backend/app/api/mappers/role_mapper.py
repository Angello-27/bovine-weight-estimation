"""
Role Mapper - DTO ↔ Entity Conversion
Convierte entre Role DTOs y Role Entities
"""

from ...domain.entities.role import Role
from ...schemas.role_schemas import (
    RoleCreateRequest,
    RoleResponse,
    RoleUpdateRequest,
)


class RoleMapper:
    """
    Mapper para convertir entre Role DTOs y Entities.

    Single Responsibility: Conversión entre capas Presentation y Domain.
    """

    @staticmethod
    def to_response(role: Role) -> RoleResponse:
        """
        Convierte Role Entity a RoleResponse DTO.

        Args:
            role: Entidad Role del dominio

        Returns:
            RoleResponse DTO
        """
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            priority=role.priority,
            permissions=role.permissions,
            created_at=role.created_at,
            last_updated=role.last_updated,
        )

    @staticmethod
    def create_request_to_params(request: RoleCreateRequest) -> dict:
        """
        Convierte RoleCreateRequest a parámetros para CreateRoleUseCase.

        Args:
            request: RoleCreateRequest DTO

        Returns:
            Dict con parámetros para use case
        """
        return {
            "name": request.name,
            "description": request.description,
            "priority": request.priority,
            "permissions": request.permissions or [],
        }

    @staticmethod
    def update_request_to_params(request: RoleUpdateRequest) -> dict:
        """
        Convierte RoleUpdateRequest a parámetros para UpdateRoleUseCase.

        Args:
            request: RoleUpdateRequest DTO

        Returns:
            Dict con parámetros para use case
        """
        params: dict = {}
        if request.name is not None:
            params["name"] = request.name
        if request.description is not None:
            params["description"] = request.description
        if request.priority is not None:
            params["priority"] = request.priority
        if request.permissions is not None:
            params["permissions"] = request.permissions
        return params

