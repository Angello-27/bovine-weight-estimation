"""
Reports Use Cases Dependencies
Dependencias para inyectar use cases de reportes
"""

from typing import Annotated

from fastapi import Depends

from app.domain.repositories.animal_repository import AnimalRepository
from app.domain.repositories.weight_estimation_repository import (
    WeightEstimationRepository,
)
from app.domain.usecases.reports import (
    GenerateGrowthReportUseCase,
    GenerateInventoryReportUseCase,
    GenerateMovementsReportUseCase,
    GenerateTraceabilityReportUseCase,
)

from .repositories import (
    get_animal_repository,
    get_weight_estimation_repository,
)


def get_generate_traceability_report_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
) -> GenerateTraceabilityReportUseCase:
    """Dependency para GenerateTraceabilityReportUseCase."""
    return GenerateTraceabilityReportUseCase(
        animal_repository=animal_repository,
        weight_estimation_repository=weight_estimation_repository,
    )


def get_generate_inventory_report_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> GenerateInventoryReportUseCase:
    """Dependency para GenerateInventoryReportUseCase."""
    return GenerateInventoryReportUseCase(animal_repository=animal_repository)


def get_generate_movements_report_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> GenerateMovementsReportUseCase:
    """Dependency para GenerateMovementsReportUseCase."""
    return GenerateMovementsReportUseCase(animal_repository=animal_repository)


def get_generate_growth_report_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
) -> GenerateGrowthReportUseCase:
    """Dependency para GenerateGrowthReportUseCase."""
    return GenerateGrowthReportUseCase(
        animal_repository=animal_repository,
        weight_estimation_repository=weight_estimation_repository,
    )
