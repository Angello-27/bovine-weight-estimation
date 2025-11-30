"""
Generate Traceability Report Use Case
Caso de uso para generar reporte de trazabilidad individual de un animal
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...repositories.animal_repository import AnimalRepository
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class GenerateTraceabilityReportUseCase:
    """
    Caso de uso para generar reporte de trazabilidad individual.

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

    async def execute(self, animal_id: UUID, format: str = "pdf") -> dict:
        """
        Ejecuta el caso de uso.

        Args:
            animal_id: ID del animal
            format: Formato del reporte ("pdf", "csv", "excel")

        Returns:
            Dict con:
            {
                "animal": Animal,
                "weight_estimations": list[WeightEstimation],
                "lineage": dict (padre, madre, descendientes),
                "timeline": list[dict] (eventos),
                "format": str,
                "data": dict  # Datos preparados para generación
            }

        Raises:
            NotFoundException: Si el animal no existe
        """
        # 1. Obtener animal
        animal = await self.animal_repository.get_by_id(animal_id)
        if animal is None:
            raise NotFoundException(resource="Animal", field="id", value=str(animal_id))

        # 2. Obtener estimaciones de peso
        weight_estimations = await self.weight_estimation_repository.find_by_animal_id(
            str(animal_id), skip=0, limit=1000
        )

        # 3. Obtener linaje
        mother = None
        if animal.mother_id:
            mother = await self.animal_repository.get_by_id(UUID(animal.mother_id))

        father = None
        if animal.father_id:
            father = await self.animal_repository.get_by_id(UUID(animal.father_id))

        descendants = await self.animal_repository.find_descendants(
            animal_id, parent_role="both"
        )

        # 4. Preparar datos para el reporte
        report_data = {
            "animal": animal,
            "weight_estimations": weight_estimations,
            "lineage": {
                "mother": mother,
                "father": father,
                "descendants": descendants,
            },
            "summary": {
                "total_weight_estimations": len(weight_estimations),
                "current_weight": (
                    weight_estimations[0].estimated_weight_kg
                    if weight_estimations
                    else None
                ),
                "first_weight": (
                    weight_estimations[-1].estimated_weight_kg
                    if weight_estimations
                    else None
                ),
                "age_months": animal.calculate_age_months(),
            },
            "format": format,
        }

        return report_data
