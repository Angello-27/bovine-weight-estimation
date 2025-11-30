"""
Domain Entities - Entidades puras del dominio
Sin dependencias de frameworks o infraestructura
"""

from .animal import Animal
from .farm import Farm
from .role import Role
from .user import User

__all__ = ["Animal", "Farm", "Role", "User"]
