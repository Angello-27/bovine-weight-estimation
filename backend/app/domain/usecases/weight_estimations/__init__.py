"""
Weight Estimations Use Cases
Casos de uso para estimaciones de peso
"""

from .create_weight_estimation_usecase import CreateWeightEstimationUseCase
from .delete_weight_estimation_usecase import DeleteWeightEstimationUseCase
from .estimate_weight_from_image_usecase import EstimateWeightFromImageUseCase
from .get_all_weight_estimations_usecase import GetAllWeightEstimationsUseCase
from .get_weight_estimation_by_id_usecase import GetWeightEstimationByIdUseCase
from .get_weight_estimations_by_animal_id_usecase import (
    GetWeightEstimationsByAnimalIdUseCase,
)
from .get_weight_estimations_by_criteria_usecase import (
    GetWeightEstimationsByCriteriaUseCase,
)

__all__ = [
    "CreateWeightEstimationUseCase",
    "DeleteWeightEstimationUseCase",
    "EstimateWeightFromImageUseCase",
    "GetWeightEstimationByIdUseCase",
    "GetWeightEstimationsByAnimalIdUseCase",
    "GetWeightEstimationsByCriteriaUseCase",
    "GetAllWeightEstimationsUseCase",
]
