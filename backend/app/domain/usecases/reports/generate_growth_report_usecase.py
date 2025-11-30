"""
Generate Growth Report Use Case
Caso de uso para generar reporte de crecimiento (GDP, evolución de peso)
"""

from uuid import UUID

from ...repositories.animal_repository import AnimalRepository
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class GenerateGrowthReportUseCase:
    """
    Caso de uso para generar reporte de crecimiento.

    Single Responsibility: Coordinar obtención de datos y generación de reporte.
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
        self.animal_repository = animal_repository
        self.weight_estimation_repository = weight_estimation_repository

    async def execute(
        self,
        animal_id: UUID | None = None,
        farm_id: UUID | None = None,
        format: str = "pdf",
    ) -> dict:
        """
        Ejecuta el caso de uso.

        Args:
            animal_id: ID del animal (opcional, si se especifica reporte individual)
            farm_id: ID de la finca (opcional, si se especifica reporte grupal)
            format: Formato del reporte ("pdf", "csv", "excel")

        Returns:
            Dict con datos preparados para generación del reporte

        Raises:
            NotFoundException: Si se especifica animal_id y no existe
        """
        if animal_id:
            # Reporte individual
            animal = await self.animal_repository.get_by_id(animal_id)
            if animal is None:
                raise NotFoundException(
                    resource="Animal", field="id", value=str(animal_id)
                )

            # Obtener estimaciones
            weight_estimations = (
                await self.weight_estimation_repository.find_by_animal_id(
                    str(animal_id), skip=0, limit=1000
                )
            )

            # Calcular GDP si hay al menos 2 estimaciones
            gdp = None
            if len(weight_estimations) >= 2:
                first = weight_estimations[-1]  # Más antigua
                last = weight_estimations[0]  # Más reciente
                days_diff = (last.timestamp - first.timestamp).days
                if days_diff > 0:
                    weight_diff = last.estimated_weight_kg - first.estimated_weight_kg
                    gdp = weight_diff / days_diff

            report_data = {
                "type": "individual",
                "animal": animal,
                "weight_estimations": weight_estimations,
                "growth_metrics": {
                    "gdp": round(gdp, 2) if gdp else None,
                    "total_measurements": len(weight_estimations),
                    "first_weight": (
                        weight_estimations[-1].estimated_weight_kg
                        if weight_estimations
                        else None
                    ),
                    "current_weight": (
                        weight_estimations[0].estimated_weight_kg
                        if weight_estimations
                        else None
                    ),
                    "weight_gain": (
                        weight_estimations[0].estimated_weight_kg
                        - weight_estimations[-1].estimated_weight_kg
                        if len(weight_estimations) >= 2
                        else None
                    ),
                },
                "format": format,
            }
        else:
            # Reporte grupal por finca
            if farm_id is None:
                raise ValueError("Debe especificar animal_id o farm_id")

            animals = await self.animal_repository.get_by_farm(
                farm_id=farm_id, skip=0, limit=1000
            )

            # Obtener estimaciones para cada animal y calcular métricas
            animals_growth = []
            for animal in animals:
                estimations = await self.weight_estimation_repository.find_by_animal_id(
                    str(animal.id), skip=0, limit=1000
                )

                if len(estimations) >= 2:
                    first = estimations[-1]
                    last = estimations[0]
                    days_diff = (last.timestamp - first.timestamp).days
                    gdp = None
                    if days_diff > 0:
                        weight_diff = (
                            last.estimated_weight_kg - first.estimated_weight_kg
                        )
                        gdp = weight_diff / days_diff

                    animals_growth.append(
                        {
                            "animal": animal,
                            "gdp": round(gdp, 2) if gdp else None,
                            "measurements_count": len(estimations),
                            "current_weight": last.estimated_weight_kg,
                        }
                    )

            report_data = {
                "type": "group",
                "farm_id": str(farm_id),
                "animals": animals_growth,
                "summary": {
                    "total_animals": len(animals_growth),
                    "average_gdp": (
                        sum(a["gdp"] for a in animals_growth if a["gdp"] is not None)
                        / len([a for a in animals_growth if a["gdp"] is not None])
                        if animals_growth
                        else None
                    ),
                },
                "format": format,
            }

        return report_data
