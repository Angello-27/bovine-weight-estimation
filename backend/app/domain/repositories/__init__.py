"""
Domain Repository Interfaces - Clean Architecture
Interfaces (ABC) para repositorios del dominio
"""

from .animal_repository import AnimalRepository
from .farm_repository import FarmRepository
from .role_repository import RoleRepository
from .user_repository import UserRepository

__all__ = [
    "AnimalRepository",
    "FarmRepository",
    "RoleRepository",
    "UserRepository",
]
