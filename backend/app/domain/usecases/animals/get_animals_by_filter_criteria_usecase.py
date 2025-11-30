"""
Get Animals By Filter Criteria Use Case - Domain Layer
Caso de uso para obtener animales filtrados por criterios
"""

from uuid import UUID

from ....core.exceptions import ValidationException
from ...entities.animal import Animal
from ...repositories.animal_repository import AnimalRepository
from ...shared.constants import AgeCategory, BreedType


class GetAnimalsByFilterCriteriaUseCase:
    """
    Caso de uso para obtener animales filtrados por criterios.

    Single Responsibility: Validar criterios y obtener animales filtrados.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales (inyección de dependencia)
        """
        self._animal_repository = animal_repository

    def _validate_filter_criteria(self, criteria: dict) -> None:
        """
        Valida que los criterios de filtrado sean válidos.

        Args:
            criteria: Diccionario con criterios de filtrado

        Raises:
            ValidationException: Si algún criterio es inválido
        """
        # Validar raza si está presente
        if "breed" in criteria and criteria["breed"]:
            breed = criteria["breed"]
            if not BreedType.is_valid(breed):
                valid_breeds = [b.value for b in BreedType]
                raise ValidationException(
                    f"Raza inválida: {breed}. Razas válidas: {', '.join(valid_breeds)}"
                )

        # Validar categoría de edad si está presente
        if "age_category" in criteria and criteria["age_category"]:
            age_category = criteria["age_category"]
            try:
                AgeCategory(age_category)
            except ValueError:
                valid_categories = [c.value for c in AgeCategory]
                raise ValidationException(
                    f"Categoría de edad inválida: {age_category}. "
                    f"Categorías válidas: {', '.join(valid_categories)}"
                )

        # Validar género si está presente
        if "gender" in criteria and criteria["gender"]:
            gender = criteria["gender"]
            if gender not in ["male", "female"]:
                raise ValidationException(
                    f"Género inválido: {gender}. Géneros válidos: male, female"
                )

        # Validar estado si está presente
        if "status" in criteria and criteria["status"]:
            status = criteria["status"]
            valid_statuses = ["active", "inactive", "sold", "dead"]
            if status not in valid_statuses:
                raise ValidationException(
                    f"Estado inválido: {status}. "
                    f"Estados válidos: {', '.join(valid_statuses)}"
                )

    async def execute(
        self,
        farm_id: UUID,
        filter_criteria: dict | None = None,
    ) -> list[Animal]:
        """
        Ejecuta el caso de uso para obtener animales filtrados.

        Args:
            farm_id: ID de la finca
            filter_criteria: Criterios de filtrado (opcional)
                Ejemplo: {
                    "breed": "nelore",
                    "age_category": "terneros",
                    "gender": "female",
                    "status": "active",
                    "count": 50  # Límite opcional
                }

        Returns:
            Lista de Animal que cumplen los criterios

        Raises:
            ValidationException: Si los criterios son inválidos
        """
        # Validar criterios si están presentes
        if filter_criteria:
            self._validate_filter_criteria(filter_criteria)

        # Extraer criterios individuales
        breed = filter_criteria.get("breed") if filter_criteria else None
        age_category = filter_criteria.get("age_category") if filter_criteria else None
        gender = filter_criteria.get("gender") if filter_criteria else None
        status = filter_criteria.get("status") if filter_criteria else None
        limit = filter_criteria.get("count") if filter_criteria else None

        # Obtener animales filtrados
        return await self._animal_repository.find_by_criteria(
            farm_id=farm_id,
            breed=breed,
            age_category=age_category,
            gender=gender,
            status=status,
            limit=limit,
        )
