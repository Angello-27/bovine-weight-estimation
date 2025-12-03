"""
Dashboard Use Cases Dependencies
Dependencias para inyectar use cases de dashboard
"""

from typing import Annotated

from fastapi import Depends

from app.domain.repositories.animal_repository import AnimalRepository
from app.domain.repositories.weight_estimation_repository import (
    WeightEstimationRepository,
)
from app.domain.usecases.dashboard import GetDashboardStatsUseCase

from .repositories import (
    get_animal_repository,
    get_weight_estimation_repository,
)


def get_get_dashboard_stats_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
) -> GetDashboardStatsUseCase:
    """Dependency para GetDashboardStatsUseCase."""
    return GetDashboardStatsUseCase(
        animal_repository=animal_repository,
        weight_estimation_repository=weight_estimation_repository,
    )
