"""
Base Strategy - Interfaz para estrategias de estimación de peso
Implementa Strategy Pattern siguiendo principios SOLID
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

from app.core.constants import BreedType


class BaseWeightEstimationStrategy(ABC):
    """
    Interfaz base para estrategias de estimación de peso.
    
    Single Responsibility: Definir contrato común para todas las estrategias
    Open/Closed: Permite agregar nuevas estrategias sin modificar código existente
    Liskov Substitution: Todas las estrategias son intercambiables
    """
    
    @abstractmethod
    def estimate_weight(self, image_bytes: bytes, breed: BreedType) -> Dict[str, Any]:
        """
        Estima peso usando la estrategia específica.
        
        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)
            breed: Raza del animal
            
        Returns:
            Dict con peso estimado, confianza, método y metadatos
            
        Raises:
            ValueError: Si no se puede estimar el peso
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Retorna nombre identificador de la estrategia.
        
        Returns:
            Nombre único de la estrategia
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica si la estrategia está disponible.
        
        Returns:
            True si la estrategia puede ejecutarse
        """
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Retorna metadatos de la estrategia.
        
        Returns:
            Dict con información adicional de la estrategia
        """
        return {
            "strategy_name": self.get_strategy_name(),
            "available": self.is_available(),
        }
