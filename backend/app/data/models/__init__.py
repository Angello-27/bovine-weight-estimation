"""
Data Models - Beanie ODM Documents
Modelos de persistencia para MongoDB
"""

from .animal_model import AnimalModel
from .role_model import RoleModel
from .user_model import UserModel

__all__ = ["AnimalModel", "RoleModel", "UserModel"]
