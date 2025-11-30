"""
Sync Dependencies - Core Layer
Dependencias para casos de uso de sincronización
"""

from typing import Annotated

from fastapi import Depends

from ...domain.repositories.animal_repository import AnimalRepository
from ...domain.repositories.weight_estimation_repository import (
    WeightEstimationRepository,
)
from ...domain.usecases.sync import (
    GetSyncHealthUseCase,
    SyncCattleBatchUseCase,
    SyncWeightEstimationsBatchUseCase,
)
from .repositories import (
    get_animal_repository,
    get_weight_estimation_repository,
)


def get_sync_cattle_batch_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> SyncCattleBatchUseCase:
    """Dependency para SyncCattleBatchUseCase."""
    return SyncCattleBatchUseCase(animal_repository=animal_repository)


def get_sync_weight_estimations_batch_usecase(
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
) -> SyncWeightEstimationsBatchUseCase:
    """Dependency para SyncWeightEstimationsBatchUseCase."""
    return SyncWeightEstimationsBatchUseCase(
        weight_estimation_repository=weight_estimation_repository
    )


def get_sync_health_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> GetSyncHealthUseCase:
    """Dependency para GetSyncHealthUseCase."""
    return GetSyncHealthUseCase(animal_repository=animal_repository)
