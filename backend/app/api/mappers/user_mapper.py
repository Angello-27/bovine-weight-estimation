"""
User Mapper - DTO ↔ Entity Conversion
Convierte entre User DTOs y User Entities
"""

from uuid import UUID

from ...domain.entities.user import User
from ...schemas.user_schemas import (
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)


class UserMapper:
    """
    Mapper para convertir entre User DTOs y Entities.

    Single Responsibility: Conversión entre capas Presentation y Domain.
    """

    @staticmethod
    def to_response(user: User) -> UserResponse:
        """
        Convierte User Entity a UserResponse DTO.

        Args:
            user: Entidad User del dominio

        Returns:
            UserResponse DTO
        """
        if user.role_id is None:
            raise ValueError("User must have a role_id")
        role_id: UUID = user.role_id  # Type assertion after None check
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role_id=role_id,
            farm_id=user.farm_id,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            last_updated=user.last_updated,
            last_login=user.last_login,
        )

    @staticmethod
    def create_request_to_params(
        request: UserCreateRequest, hashed_password: str
    ) -> dict:
        """
        Convierte UserCreateRequest a parámetros para CreateUserUseCase.

        Args:
            request: UserCreateRequest DTO
            hashed_password: Contraseña hasheada

        Returns:
            Dict con parámetros para use case
        """
        return {
            "username": request.username,
            "email": request.email,
            "hashed_password": hashed_password,
            "role_id": request.role_id,
            "farm_id": request.farm_id,
        }

    @staticmethod
    def update_request_to_params(
        request: UserUpdateRequest, hashed_password: str | None = None
    ) -> dict:
        """
        Convierte UserUpdateRequest a parámetros para UpdateUserUseCase.

        Args:
            request: UserUpdateRequest DTO
            hashed_password: Contraseña hasheada (opcional)

        Returns:
            Dict con parámetros para use case
        """
        params: dict = {}
        if request.email is not None:
            params["email"] = request.email
        if hashed_password is not None:
            params["hashed_password"] = hashed_password
        if request.role_id is not None:
            params["role_id"] = request.role_id
        if request.farm_id is not None:
            params["farm_id"] = request.farm_id
        if request.is_active is not None:
            params["is_active"] = request.is_active
        return params
