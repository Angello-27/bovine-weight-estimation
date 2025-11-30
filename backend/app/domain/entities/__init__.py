"""
Domain Entities - Entidades puras del dominio
Sin dependencias de frameworks o infraestructura
"""

from .alert import Alert, AlertStatus, AlertType, RecurrenceType
from .animal import Animal
from .farm import Farm
from .role import Role
from .sync_result import SyncBatchResult, SyncItemResult, SyncItemStatus
from .user import User
from .weight_estimation import WeightEstimation

__all__ = [
    "Alert",
    "AlertStatus",
    "AlertType",
    "Animal",
    "Farm",
    "RecurrenceType",
    "Role",
    "SyncBatchResult",
    "SyncItemResult",
    "SyncItemStatus",
    "User",
    "WeightEstimation",
]
