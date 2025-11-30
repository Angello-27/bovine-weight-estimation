"""
Models Module - Beanie ODM para MongoDB
Modelos de persistencia (Data Layer)

NOTA: UserModel y RoleModel se movieron a data/models/.
Se mantienen aquí para compatibilidad temporal.
"""

# Re-exportar desde data/models para compatibilidad
from ..data.models.animal_model import AnimalModel
from ..data.models.role_model import RoleModel
from ..data.models.user_model import UserModel
from .alert_model import AlertModel
from .farm_model import FarmModel
from .weight_estimation_model import WeightEstimationModel

__all__ = [
    "AlertModel",
    "AnimalModel",
    "FarmModel",
    "RoleModel",
    "UserModel",
    "WeightEstimationModel",
]
