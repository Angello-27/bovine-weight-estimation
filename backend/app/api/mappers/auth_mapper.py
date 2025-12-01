"""
Auth Mapper - DTO ↔ Entity Conversion
Convierte entre Auth DTOs y Domain Entities
"""

from ...domain.entities.role import Role
from ...domain.entities.user import User
from ...schemas.auth_schemas import LoginResponse


class AuthMapper:
    """
    Mapper para convertir entre Auth DTOs y Entities.

    Single Responsibility: Conversión entre capas Presentation y Domain para autenticación.
    """

    @staticmethod
    def to_login_response(user: User, role: Role, access_token: str) -> LoginResponse:
        """
        Convierte User + Role + access_token a LoginResponse DTO.

        Args:
            user: Entidad User del dominio
            role: Entidad Role del dominio
            access_token: Token JWT generado

        Returns:
            LoginResponse DTO

        Raises:
            ValueError: Si user.id o role.id son None
        """
        if user.id is None:
            raise ValueError("User must have an id")
        if role.id is None:
            raise ValueError("Role must have an id")

        return LoginResponse(
            id=user.id,
            username=user.username,
            role=role.name,
            role_priority=role.priority,  # Incluir priority del rol
            role_id=role.id,
            farm_id=user.farm_id,  # Incluir farm_id del usuario
            access_token=access_token,
            token_type="bearer",
        )
