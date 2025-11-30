"""
Application Services Module - Business Logic Layer
Lógica de negocio para módulos complejos (ML, Weighing)

Nota: Los CRUDs simples (User, Role, Farm, Animal, Alert, Sync) ya no usan Application Services,
sino que las routes inyectan directamente los Use Cases desde core.dependencies.

Servicios eliminados (migrados a Clean Architecture):
- AuthService → core/utils/jwt.py + core/utils/password.py + AuthenticateUserUseCase
- SyncService → domain/usecases/sync/ (SyncCattleBatchUseCase, SyncWeightEstimationsBatchUseCase)
"""

from .ml_service import MLService
from .weighing_service import WeighingService

__all__ = [
    "WeighingService",
    "MLService",
]
