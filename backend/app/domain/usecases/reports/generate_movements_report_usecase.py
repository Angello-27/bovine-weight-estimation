"""
Generate Movements Report Use Case
Caso de uso para generar reporte de movimientos (ventas, fallecimientos)
"""

from datetime import datetime
from uuid import UUID

from ...repositories.animal_repository import AnimalRepository


class GenerateMovementsReportUseCase:
    """
    Caso de uso para generar reporte de movimientos.

    Single Responsibility: Coordinar obtención de datos y generación de reporte.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales
        """
        self.animal_repository = animal_repository

    async def execute(
        self,
        farm_id: UUID,
        format: str = "pdf",
        movement_type: str | None = None,  # "sold", "deceased", o None (todos)
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> dict:
        """
        Ejecuta el caso de uso.

        Args:
            farm_id: ID de la finca
            format: Formato del reporte ("pdf", "csv")
            movement_type: Tipo de movimiento ("sold", "deceased", o None para todos)
            date_from: Fecha desde (opcional)
            date_to: Fecha hasta (opcional)

        Returns:
            Dict con datos preparados para generación del reporte
        """
        # Obtener animales según tipo de movimiento
        if movement_type:
            status_filter = movement_type
        else:
            # Obtener ambos tipos
            status_filter = None

        animals = await self.animal_repository.find_by_criteria(
            farm_id=farm_id,
            status=status_filter,
            limit=None,
        )

        # Filtrar por tipo de movimiento si no se especificó status
        if not movement_type:
            # Filtrar solo sold y deceased
            animals = [a for a in animals if a.status in ["sold", "deceased"]]
        else:
            animals = [a for a in animals if a.status == movement_type]

        # Filtrar por rango de fechas (usando last_updated como aproximación)
        if date_from or date_to:
            filtered_animals = []
            for animal in animals:
                update_date = animal.last_updated
                if date_from and update_date < date_from:
                    continue
                if date_to and update_date > date_to:
                    continue
                filtered_animals.append(animal)
            animals = filtered_animals

        # Agrupar por tipo
        sold_animals = [a for a in animals if a.status == "sold"]
        deceased_animals = [a for a in animals if a.status == "deceased"]

        report_data = {
            "movements": animals,
            "sold_animals": sold_animals,
            "deceased_animals": deceased_animals,
            "summary": {
                "total_movements": len(animals),
                "total_sold": len(sold_animals),
                "total_deceased": len(deceased_animals),
            },
            "filters": {
                "farm_id": str(farm_id),
                "movement_type": movement_type,
                "date_from": date_from.isoformat() if date_from else None,
                "date_to": date_to.isoformat() if date_to else None,
            },
            "generated_at": datetime.utcnow(),
            "format": format,
        }

        return report_data
