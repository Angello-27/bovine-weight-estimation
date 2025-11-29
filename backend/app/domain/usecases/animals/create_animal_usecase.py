"""
Create Animal Use Case - Domain Layer
Caso de uso para crear un animal
"""

from datetime import datetime
from uuid import UUID

from ....core.exceptions import AlreadyExistsException
from ...entities.animal import Animal
from ...repositories.animal_repository import AnimalRepository


class CreateAnimalUseCase:
    """
    Caso de uso para crear un animal.

    Single Responsibility: Validar y crear un animal en el dominio.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales (inyección de dependencia)
        """
        self._animal_repository = animal_repository

    async def execute(
        self,
        ear_tag: str,
        breed: str,
        birth_date: str | datetime,
        gender: str,
        farm_id: UUID,
        name: str | None = None,
        color: str | None = None,
        birth_weight_kg: float | None = None,
        mother_id: str | None = None,
        father_id: str | None = None,
        observations: str | None = None,
        photo_url: str | None = None,
    ) -> Animal:
        """
        Ejecuta el caso de uso para crear un animal.

        Args:
            ear_tag: Número de caravana
            breed: Raza del animal
            birth_date: Fecha de nacimiento (datetime o string ISO)
            gender: Género (male/female)
            farm_id: ID de la hacienda
            name: Nombre del animal (opcional)
            color: Color del pelaje (opcional)
            birth_weight_kg: Peso al nacer (opcional)
            mother_id: ID de la madre (opcional)
            father_id: ID del padre (opcional)
            observations: Observaciones (opcional)
            photo_url: URL de foto (opcional)

        Returns:
            Animal creado

        Raises:
            AlreadyExistsException: Si la caravana ya existe
        """
        # Validar que la caravana no exista
        existing = await self._animal_repository.find_by_ear_tag(ear_tag, farm_id)

        if existing is not None:
            raise AlreadyExistsException(
                resource="Animal", field="ear_tag", value=ear_tag
            )

        # Convertir birth_date si es string
        if isinstance(birth_date, str):
            birth_date = datetime.fromisoformat(birth_date.replace("Z", "+00:00"))

        # Crear entidad Animal
        animal = Animal(
            ear_tag=ear_tag,
            breed=breed,
            birth_date=birth_date,
            gender=gender,
            name=name,
            color=color,
            birth_weight_kg=birth_weight_kg,
            mother_id=mother_id,
            father_id=father_id,
            observations=observations,
            photo_url=photo_url,
            farm_id=farm_id,
            status="active",
        )

        # Guardar usando el repositorio
        return await self._animal_repository.save(animal)
