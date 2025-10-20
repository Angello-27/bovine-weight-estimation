"""
Models Module - Beanie ODM para MongoDB
Modelos de persistencia (Data Layer)
"""

from .animal_model import AnimalModel
from .weight_estimation_model import WeightEstimationModel

__all__ = [
    "AnimalModel",
    "WeightEstimationModel",
]

