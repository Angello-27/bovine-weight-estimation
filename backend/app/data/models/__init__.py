"""
Data Models - Beanie ODM Documents
Modelos de persistencia para MongoDB
"""

from .animal_model import AnimalModel
from .farm_model import FarmModel
from .role_model import RoleModel
from .user_model import UserModel

__all__ = ["AnimalModel", "FarmModel", "RoleModel", "UserModel"]
