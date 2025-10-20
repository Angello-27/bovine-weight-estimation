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
    CattleSyncItem,
    HealthCheckResponse,
    SyncItemResponse,
    WeightEstimationSyncBatchRequest,
    WeightEstimationSyncBatchResponse,
    WeightEstimationSyncItem,
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
    "CattleSyncItem",
    "CattleSyncBatchRequest",
    "CattleSyncBatchResponse",
    "WeightEstimationSyncItem",
    "WeightEstimationSyncBatchRequest",
    "WeightEstimationSyncBatchResponse",
    "SyncItemResponse",
    "HealthCheckResponse",
]

