"""
Services Module - Business Logic Layer
Lógica de negocio para módulos complejos (Auth, Sync, ML, Alert, Animal, Weighing)

Nota: Los CRUDs simples (User, Role, Farm) ya no usan Application Services,
sino que las routes inyectan directamente los Use Cases desde core.dependencies.
"""

from .alert_service import AlertService
from .animal_service import AnimalService
from .auth_service import AuthService
from .ml_service import MLService
from .sync_service import SyncService
from .weighing_service import WeighingService

__all__ = [
    "AlertService",
    "AnimalService",
    "AuthService",
    "WeighingService",
    "MLService",
    "SyncService",
]
