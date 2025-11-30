"""
Mappers - DTO ↔ Entity Conversion
Mappers para convertir entre DTOs (Presentation) y Entities (Domain)
"""

from .animal_mapper import AnimalMapper
from .auth_mapper import AuthMapper
from .farm_mapper import FarmMapper
from .role_mapper import RoleMapper
from .user_mapper import UserMapper

__all__ = [
    "AnimalMapper",
    "AuthMapper",
    "FarmMapper",
    "RoleMapper",
    "UserMapper",
]
