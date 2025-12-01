"""
Farm Use Cases Dependencies
Dependencias para inyectar use cases de fincas
"""

from typing import Annotated

from fastapi import Depends

from app.domain.repositories.farm_repository import FarmRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.usecases.farms import (
    CreateFarmUseCase,
    DeleteFarmUseCase,
    GetAllFarmsUseCase,
    GetFarmByIdUseCase,
    GetFarmsByCriteriaUseCase,
    UpdateFarmUseCase,
)

from .repositories import get_farm_repository, get_user_repository


def get_create_farm_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> CreateFarmUseCase:
    """Dependency para CreateFarmUseCase."""
    return CreateFarmUseCase(
        farm_repository=farm_repository, user_repository=user_repository
    )


def get_get_farm_by_id_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> GetFarmByIdUseCase:
    """Dependency para GetFarmByIdUseCase."""
    return GetFarmByIdUseCase(farm_repository=farm_repository)


def get_get_all_farms_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> GetAllFarmsUseCase:
    """Dependency para GetAllFarmsUseCase."""
    return GetAllFarmsUseCase(farm_repository=farm_repository)


def get_update_farm_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> UpdateFarmUseCase:
    """Dependency para UpdateFarmUseCase."""
    return UpdateFarmUseCase(farm_repository=farm_repository)


def get_delete_farm_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> DeleteFarmUseCase:
    """Dependency para DeleteFarmUseCase."""
    return DeleteFarmUseCase(farm_repository=farm_repository)


def get_get_farms_by_criteria_usecase(
    farm_repository: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> GetFarmsByCriteriaUseCase:
    """Dependency para GetFarmsByCriteriaUseCase."""
    return GetFarmsByCriteriaUseCase(farm_repository=farm_repository)
