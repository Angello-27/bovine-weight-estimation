"""
Weight Estimations Dependencies - Core Layer
Dependencias para casos de uso de estimaciones de peso
"""

from typing import Annotated

from fastapi import Depends

from ...domain.repositories.animal_repository import AnimalRepository
from ...domain.repositories.weight_estimation_repository import (
    WeightEstimationRepository,
)
from ...domain.usecases.weight_estimations import (
    CreateWeightEstimationUseCase,
    EstimateWeightFromImageUseCase,
    GetAllWeightEstimationsUseCase,
    GetWeightEstimationByIdUseCase,
    GetWeightEstimationsByAnimalIdUseCase,
)
from .repositories import (
    get_animal_repository,
    get_weight_estimation_repository,
)


def get_create_weight_estimation_usecase(
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> CreateWeightEstimationUseCase:
    """Dependency para CreateWeightEstimationUseCase."""
    return CreateWeightEstimationUseCase(
        weight_estimation_repository=weight_estimation_repository,
        animal_repository=animal_repository,
    )


def get_weight_estimation_by_id_usecase(
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
) -> GetWeightEstimationByIdUseCase:
    """Dependency para GetWeightEstimationByIdUseCase."""
    return GetWeightEstimationByIdUseCase(
        weight_estimation_repository=weight_estimation_repository
    )


def get_weight_estimations_by_animal_id_usecase(
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
) -> GetWeightEstimationsByAnimalIdUseCase:
    """Dependency para GetWeightEstimationsByAnimalIdUseCase."""
    return GetWeightEstimationsByAnimalIdUseCase(
        weight_estimation_repository=weight_estimation_repository
    )


def get_all_weight_estimations_usecase(
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
) -> GetAllWeightEstimationsUseCase:
    """Dependency para GetAllWeightEstimationsUseCase."""
    return GetAllWeightEstimationsUseCase(
        weight_estimation_repository=weight_estimation_repository
    )


def get_estimate_weight_from_image_usecase(
    weight_estimation_repository: Annotated[
        WeightEstimationRepository, Depends(get_weight_estimation_repository)
    ],
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> EstimateWeightFromImageUseCase:
    """Dependency para EstimateWeightFromImageUseCase."""
    return EstimateWeightFromImageUseCase(
        weight_estimation_repository=weight_estimation_repository,
        animal_repository=animal_repository,
    )
