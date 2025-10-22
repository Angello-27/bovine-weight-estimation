"""
ML Strategies - Patrón Strategy para diferentes métodos de estimación
Implementa Strategy Pattern para estimación de peso bovino
"""

from .base_strategy import BaseWeightEstimationStrategy
from .hybrid_strategy import HybridWeightEstimationStrategy
from .ml_strategy import MLWeightEstimationStrategy

__all__ = [
    "BaseWeightEstimationStrategy",
    "HybridWeightEstimationStrategy", 
    "MLWeightEstimationStrategy",
]
