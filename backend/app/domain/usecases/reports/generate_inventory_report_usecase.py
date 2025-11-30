"""
Generate Inventory Report Use Case
Caso de uso para generar reporte de inventario de animales
"""

from datetime import datetime
from uuid import UUID

from ...repositories.animal_repository import AnimalRepository


class GenerateInventoryReportUseCase:
    """
    Caso de uso para generar reporte de inventario.

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
        status: str | None = None,
        breed: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> dict:
        """
        Ejecuta el caso de uso.

        Args:
            farm_id: ID de la finca
            format: Formato del reporte ("pdf", "csv", "excel")
            status: Filtro por estado (opcional)
            breed: Filtro por raza (opcional)
            date_from: Fecha desde para filtrar por registro (opcional)
            date_to: Fecha hasta para filtrar por registro (opcional)

        Returns:
            Dict con datos preparados para generación del reporte
        """
        # Obtener animales según filtros
        animals = await self.animal_repository.find_by_criteria(
            farm_id=farm_id,
            breed=breed,
            status=status,
            limit=None,  # Todos los que cumplan criterios
        )

        # Filtrar por rango de fechas si se especifica
        if date_from or date_to:
            filtered_animals = []
            for animal in animals:
                reg_date = animal.registration_date
                if date_from and reg_date < date_from:
                    continue
                if date_to and reg_date > date_to:
                    continue
                filtered_animals.append(animal)
            animals = filtered_animals

        # Calcular estadísticas
        animals_by_breed = {}
        animals_by_status = {}
        for animal in animals:
            # Por raza
            breed_key = animal.breed
            animals_by_breed[breed_key] = animals_by_breed.get(breed_key, 0) + 1

            # Por estado
            status_key = animal.status
            animals_by_status[status_key] = animals_by_status.get(status_key, 0) + 1

        report_data = {
            "animals": animals,
            "total_animals": len(animals),
            "statistics": {
                "by_breed": animals_by_breed,
                "by_status": animals_by_status,
            },
            "filters": {
                "farm_id": str(farm_id),
                "status": status,
                "breed": breed,
                "date_from": date_from.isoformat() if date_from else None,
                "date_to": date_to.isoformat() if date_to else None,
            },
            "generated_at": datetime.utcnow(),
            "format": format,
        }

        return report_data
