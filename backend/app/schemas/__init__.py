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
