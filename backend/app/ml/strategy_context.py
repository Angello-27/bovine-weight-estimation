"""
Strategy Context - Contexto para selección automática de estrategias
Implementa Strategy Pattern con selección automática
"""

from typing import Dict, Any, List

from ...core.constants import BreedType
from .base_strategy import BaseWeightEstimationStrategy
from .hybrid_strategy import HybridWeightEstimationStrategy
from .ml_strategy import MLWeightEstimationStrategy


class WeightEstimationContext:
    """
    Contexto que maneja la selección automática de estrategias.
    
    Single Responsibility: Coordinar estrategias de estimación
    Open/Closed: Fácil agregar nuevas estrategias
    Dependency Inversion: Depende de abstracciones (BaseWeightEstimationStrategy)
    """
    
    def __init__(self):
        """Inicializa el contexto con estrategias disponibles."""
        self._strategies: List[BaseWeightEstimationStrategy] = [
            MLWeightEstimationStrategy(),  # Prioridad alta: ML entrenado
            HybridWeightEstimationStrategy(),  # Fallback: Híbrido
        ]
    
    def estimate_weight(self, image_bytes: bytes, breed: BreedType) -> Dict[str, Any]:
        """
        Estima peso usando la mejor estrategia disponible.
        
        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)
            breed: Raza del animal
            
        Returns:
            Dict con peso estimado, confianza, método y metadatos
            
        Raises:
            ValueError: Si ninguna estrategia está disponible
        """
        # Buscar primera estrategia disponible
        for strategy in self._strategies:
            if strategy.is_available():
                try:
                    result = strategy.estimate_weight(image_bytes, breed)
                    result['selected_strategy'] = strategy.get_strategy_name()
                    return result
                except Exception as e:
                    # Si falla, continuar con siguiente estrategia
                    print(f"⚠️ Estrategia {strategy.get_strategy_name()} falló: {e}")
                    continue
        
        # Si ninguna estrategia funcionó
        raise ValueError("Ninguna estrategia de estimación está disponible")
    
    def get_available_strategies(self) -> List[str]:
        """
        Obtiene lista de estrategias disponibles.
        
        Returns:
            Lista de nombres de estrategias disponibles
        """
        return [
            strategy.get_strategy_name() 
            for strategy in self._strategies 
            if strategy.is_available()
        ]
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """
        Obtiene información de todas las estrategias.
        
        Returns:
            Dict con información de estrategias
        """
        return {
            "total_strategies": len(self._strategies),
            "available_strategies": self.get_available_strategies(),
            "strategy_details": [
                strategy.get_metadata() 
                for strategy in self._strategies
            ]
        }
    
    def add_strategy(self, strategy: BaseWeightEstimationStrategy, priority: int = 0) -> None:
        """
        Agrega nueva estrategia con prioridad específica.
        
        Args:
            strategy: Nueva estrategia a agregar
            priority: Prioridad (0 = más alta, se inserta al inicio)
        """
        if priority == 0:
            self._strategies.insert(0, strategy)
        else:
            self._strategies.append(strategy)
    
    def get_hybrid_strategy(self) -> HybridWeightEstimationStrategy | None:
        """
        Obtiene la estrategia híbrida si está disponible.
        
        Returns:
            Instancia de HybridWeightEstimationStrategy o None
        """
        for strategy in self._strategies:
            if isinstance(strategy, HybridWeightEstimationStrategy):
                return strategy
        return None
