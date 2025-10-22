"""
Weight Estimation Strategies Package
Paquete de estrategias para estimación de peso bovino

Clean Architecture: Implementa Strategy Pattern para diferentes métodos de estimación
"""

from .base_strategy import BaseWeightEstimationStrategy
from .morphometric_strategy import MorphometricWeightEstimationStrategy
from .deep_learning_strategy import DeepLearningWeightEstimationStrategy

__all__ = [
    "BaseWeightEstimationStrategy",
    "MorphometricWeightEstimationStrategy",
    "DeepLearningWeightEstimationStrategy",
]
