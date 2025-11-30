"""
Models Module - ⚠️ LEGACY (coexistencia temporal)

NOTA: Este módulo es legacy y será eliminado después de migrar Alert y Weighing.

Modelos migrados a data/models/:
- AnimalModel → data/models/animal_model.py
- UserModel → data/models/user_model.py
- RoleModel → data/models/role_model.py
- FarmModel → data/models/farm_model.py

Modelos pendientes de migrar:
- AlertModel → Pendiente
- WeightEstimationModel → Pendiente
"""

# Re-exportar desde data/models para compatibilidad temporal
from ..data.models.animal_model import AnimalModel
from ..data.models.farm_model import FarmModel
from ..data.models.role_model import RoleModel
from ..data.models.user_model import UserModel

# Modelos aún no migrados (legacy)
from .alert_model import AlertModel
from .weight_estimation_model import WeightEstimationModel

__all__ = [
    # Modelos migrados (re-exportados desde data/models/)
    "AnimalModel",
    "FarmModel",
    "RoleModel",
    "UserModel",
    # Modelos legacy (pendientes de migrar)
    "AlertModel",
    "WeightEstimationModel",
]
