"""
Domain Repository Interfaces - Clean Architecture
Interfaces (ABC) para repositorios del dominio
"""

from .animal_repository import AnimalRepository
from .role_repository import RoleRepository
from .user_repository import UserRepository

__all__ = ["AnimalRepository", "RoleRepository", "UserRepository"]
