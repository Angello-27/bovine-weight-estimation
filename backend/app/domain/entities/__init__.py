"""
Domain Entities - Entidades puras del dominio
Sin dependencias de frameworks o infraestructura
"""

from .alert import Alert, AlertStatus, AlertType, RecurrenceType
from .animal import Animal
from .farm import Farm
from .role import Role
from .user import User

__all__ = [
    "Alert",
    "AlertStatus",
    "AlertType",
    "Animal",
    "Farm",
    "RecurrenceType",
    "Role",
    "User",
]
