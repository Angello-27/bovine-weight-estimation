"""
Repository Dependencies
Dependencias para inyectar repositorios
"""

from app.data.repositories.alert_repository_impl import AlertRepositoryImpl
from app.data.repositories.animal_repository_impl import AnimalRepositoryImpl
from app.data.repositories.farm_repository_impl import FarmRepositoryImpl
from app.data.repositories.role_repository_impl import RoleRepositoryImpl
from app.data.repositories.user_repository_impl import UserRepositoryImpl
from app.data.repositories.weight_estimation_repository_impl import (
    WeightEstimationRepositoryImpl,
)
from app.domain.repositories.alert_repository import AlertRepository
from app.domain.repositories.animal_repository import AnimalRepository
from app.domain.repositories.farm_repository import FarmRepository
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.weight_estimation_repository import (
    WeightEstimationRepository,
)


def get_user_repository() -> UserRepository:
    """Dependency para obtener UserRepository."""
    return UserRepositoryImpl()


def get_role_repository() -> RoleRepository:
    """Dependency para obtener RoleRepository."""
    return RoleRepositoryImpl()


def get_farm_repository() -> FarmRepository:
    """Dependency para obtener FarmRepository."""
    return FarmRepositoryImpl()


def get_animal_repository() -> AnimalRepository:
    """Dependency para obtener AnimalRepository."""
    return AnimalRepositoryImpl()


def get_alert_repository() -> AlertRepository:
    """Dependency para obtener AlertRepository."""
    return AlertRepositoryImpl()


def get_weight_estimation_repository() -> WeightEstimationRepository:
    """Dependency para obtener WeightEstimationRepository."""
    return WeightEstimationRepositoryImpl()
