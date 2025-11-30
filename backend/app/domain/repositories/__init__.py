"""
Domain Repository Interfaces - Clean Architecture
Interfaces (ABC) para repositorios del dominio
"""

from .alert_repository import AlertRepository
from .animal_repository import AnimalRepository
from .farm_repository import FarmRepository
from .role_repository import RoleRepository
from .user_repository import UserRepository

__all__ = [
    "AlertRepository",
    "AnimalRepository",
    "FarmRepository",
    "RoleRepository",
    "UserRepository",
]
