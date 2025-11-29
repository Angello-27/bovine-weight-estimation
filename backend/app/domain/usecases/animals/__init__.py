"""
Animal Use Cases - Domain Layer
Casos de uso para gestión de animales
"""

from .create_animal_usecase import CreateAnimalUseCase
from .delete_animal_usecase import DeleteAnimalUseCase
from .get_animal_by_id_usecase import GetAnimalByIdUseCase
from .get_animals_by_farm_usecase import GetAnimalsByFarmUseCase
from .update_animal_usecase import UpdateAnimalUseCase

__all__ = [
    "CreateAnimalUseCase",
    "GetAnimalByIdUseCase",
    "GetAnimalsByFarmUseCase",
    "UpdateAnimalUseCase",
    "DeleteAnimalUseCase",
]
