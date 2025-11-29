"""
Models Module - Beanie ODM para MongoDB
Modelos de persistencia (Data Layer)
"""

from .alert_model import AlertModel
from .animal_model import AnimalModel
from .farm_model import FarmModel
from .role_model import RoleModel
from .user_model import UserModel
from .weight_estimation_model import WeightEstimationModel

__all__ = [
    "AlertModel",
    "AnimalModel",
    "FarmModel",
    "RoleModel",
    "UserModel",
    "WeightEstimationModel",
]
