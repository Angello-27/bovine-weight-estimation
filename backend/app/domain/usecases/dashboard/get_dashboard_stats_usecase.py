"""
Get Dashboard Stats Use Case - Domain Layer
Caso de uso para obtener estadísticas del dashboard
"""

from uuid import UUID

from ...repositories.animal_repository import AnimalRepository
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class GetDashboardStatsUseCase:
    """
    Caso de uso para obtener estadísticas del dashboard.

    Single Responsibility: Calcular estadísticas agregadas del sistema.
    """

    def __init__(
        self,
        animal_repository: AnimalRepository,
        weight_estimation_repository: WeightEstimationRepository,
    ):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales
            weight_estimation_repository: Repositorio de estimaciones de peso
        """
        self._animal_repository = animal_repository
        self._weight_estimation_repository = weight_estimation_repository

    async def execute(self, farm_id: UUID) -> dict:
        """
        Ejecuta el caso de uso para obtener estadísticas del dashboard.

        Args:
            farm_id: ID de la finca para filtrar estadísticas

        Returns:
            Diccionario con estadísticas:
            - totalCattle: Total de animales en la finca
            - averageWeight: Peso promedio (kg) de las estimaciones más recientes
            - totalBreeds: Número de razas diferentes
            - totalEstimations: Total de estimaciones de peso
        """
        # Obtener todos los animales de la finca
        animals = await self._animal_repository.find_by_criteria_dict(
            filters={"farm_id": farm_id}, skip=0, limit=10000
        )
        total_cattle = len(animals)

        # Obtener IDs de animales
        animal_ids = [str(animal.id) for animal in animals]

        # Contar razas únicas
        unique_breeds = {animal.breed for animal in animals if animal.breed}
        total_breeds = len(unique_breeds)

        # Obtener todas las estimaciones de los animales de la finca
        total_estimations = 0
        weights = []

        if animal_ids:
            # Convertir animal_ids a set para búsqueda rápida
            animal_ids_set = set(animal_ids)

            # Obtener todas las estimaciones (sin filtro, ya que el repositorio no soporta $in)
            # Luego filtrar en memoria por animal_id
            all_estimations = await self._weight_estimation_repository.find_all(
                skip=0, limit=100000
            )

            # Filtrar estimaciones por los animales de la finca
            farm_estimations = [
                est for est in all_estimations if str(est.animal_id) in animal_ids_set
            ]
            total_estimations = len(farm_estimations)

            # Agrupar por animal_id y obtener la más reciente de cada animal
            # (las estimaciones ya vienen ordenadas por timestamp DESC)
            latest_by_animal: dict[str, float] = {}
            for estimation in farm_estimations:
                animal_id_str = str(estimation.animal_id)
                weight = estimation.estimated_weight_kg
                if weight and weight > 0 and animal_id_str not in latest_by_animal:
                    latest_by_animal[animal_id_str] = weight

            weights = list(latest_by_animal.values())

        # Calcular peso promedio
        average_weight = sum(weights) / len(weights) if weights else 0.0

        return {
            "total_cattle": total_cattle,
            "average_weight": round(average_weight, 1),
            "total_breeds": total_breeds,
            "total_estimations": total_estimations,
        }
