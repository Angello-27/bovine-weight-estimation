"""
Schemas Module - Pydantic DTOs
Data Transfer Objects para API Layer
"""

from .animal_schemas import (
    AnimalCreateRequest,
    AnimalResponse,
    AnimalsListResponse,
    AnimalUpdateRequest,
)
from .auth_schemas import (
    LoginRequest,
    LoginResponse,
    TokenData,
)
from .farm_schemas import (
    FarmCreateRequest,
    FarmResponse,
    FarmsListResponse,
    FarmUpdateRequest,
)
from .role_schemas import (
    RoleCreateRequest,
    RoleResponse,
    RolesListResponse,
    RoleUpdateRequest,
)
from .sync_schemas import (
    CattleSyncBatchRequest,
    CattleSyncBatchResponse,
    CattleSyncItemRequest,
    CattleSyncItemResponse,
    HealthCheckResponse,
    WeightEstimationSyncBatchRequest,
    WeightEstimationSyncBatchResponse,
    WeightEstimationSyncItemRequest,
    WeightEstimationSyncItemResponse,
)
from .user_schemas import (
    UserCreateRequest,
    UserResponse,
    UsersListResponse,
    UserUpdateRequest,
)
from .weighing_schemas import (
    WeighingCreateRequest,
    WeighingResponse,
    WeighingsListResponse,
)

__all__ = [
    # Animals
    "AnimalCreateRequest",
    "AnimalUpdateRequest",
    "AnimalResponse",
    "AnimalsListResponse",
    # Auth
    "LoginRequest",
    "LoginResponse",
    "TokenData",
    # Farms
    "FarmCreateRequest",
    "FarmUpdateRequest",
    "FarmResponse",
    "FarmsListResponse",
    # Roles
    "RoleCreateRequest",
    "RoleUpdateRequest",
    "RoleResponse",
    "RolesListResponse",
    # Users
    "UserCreateRequest",
    "UserUpdateRequest",
    "UserResponse",
    "UsersListResponse",
    # Weighings
    "WeighingCreateRequest",
    "WeighingResponse",
    "WeighingsListResponse",
    # Sync
    "CattleSyncItemRequest",
    "CattleSyncItemResponse",
    "CattleSyncBatchRequest",
    "CattleSyncBatchResponse",
    "WeightEstimationSyncItemRequest",
    "WeightEstimationSyncItemResponse",
    "WeightEstimationSyncBatchRequest",
    "WeightEstimationSyncBatchResponse",
    "HealthCheckResponse",
]
