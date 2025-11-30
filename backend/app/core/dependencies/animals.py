"""
Animal Use Cases Dependencies
Dependencias para inyectar use cases de animales
"""

from typing import Annotated

from fastapi import Depends

from app.domain.repositories.animal_repository import AnimalRepository
from app.domain.usecases.animals import (
    CreateAnimalUseCase,
    DeleteAnimalUseCase,
    GetAnimalByIdUseCase,
    GetAnimalsByFarmUseCase,
    UpdateAnimalUseCase,
)

from .repositories import get_animal_repository


def get_create_animal_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> CreateAnimalUseCase:
    """Dependency para CreateAnimalUseCase."""
    return CreateAnimalUseCase(animal_repository=animal_repository)


def get_get_animal_by_id_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> GetAnimalByIdUseCase:
    """Dependency para GetAnimalByIdUseCase."""
    return GetAnimalByIdUseCase(animal_repository=animal_repository)


def get_get_animals_by_farm_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> GetAnimalsByFarmUseCase:
    """Dependency para GetAnimalsByFarmUseCase."""
    return GetAnimalsByFarmUseCase(animal_repository=animal_repository)


def get_update_animal_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> UpdateAnimalUseCase:
    """Dependency para UpdateAnimalUseCase."""
    return UpdateAnimalUseCase(animal_repository=animal_repository)


def get_delete_animal_usecase(
    animal_repository: Annotated[AnimalRepository, Depends(get_animal_repository)],
) -> DeleteAnimalUseCase:
    """Dependency para DeleteAnimalUseCase."""
    return DeleteAnimalUseCase(animal_repository=animal_repository)
