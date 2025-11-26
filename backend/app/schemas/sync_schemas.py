"""
Sync Schemas - US-005: Sincronización Offline
Pydantic v2 schemas para sincronización bidireccional
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class SyncStatus(str, Enum):
    """Estado de sincronización"""

    PENDING = "pending"
    SYNCING = "syncing"
    SYNCED = "synced"
    ERROR = "error"
    CONFLICT = "conflict"


class SyncOperation(str, Enum):
    """Tipo de operación de sincronización"""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


# ===== Cattle Sync Schemas =====


class CattleSyncItemRequest(BaseModel):
    """Item de ganado a sincronizar desde mobile"""

    id: str = Field(..., description="UUID del animal")
    ear_tag: str = Field(..., min_length=1, max_length=50, description="Caravana única")
    name: str | None = Field(None, max_length=100, description="Nombre del animal")
    breed: str = Field(..., description="Raza del animal (7 razas válidas)")
    birth_date: datetime = Field(..., description="Fecha de nacimiento")
    gender: str = Field(..., description="Género: male/female")
    color: str | None = Field(None, max_length=50)
    birth_weight: float | None = Field(None, gt=0, lt=100)
    mother_id: str | None = None
    father_id: str | None = None
    observations: str | None = Field(None, max_length=1000)
    status: str = Field(
        default="active", description="Estado: active/sold/dead/inactive"
    )
    registration_date: datetime = Field(..., description="Fecha de registro")
    last_updated: datetime = Field(..., description="Última modificación UTC")
    photo_path: str | None = None
    operation: SyncOperation = Field(..., description="create/update/delete")

    @field_validator("breed")
    @classmethod
    def validate_breed(cls, v: str) -> str:
        valid_breeds = [
            "nelore",
            "brahman",
            "guzerat",
            "senepol",
            "girolando",
            "gyr_lechero",
            "sindi",
        ]
        if v.lower() not in valid_breeds:
            raise ValueError(f"Raza inválida. Válidas: {valid_breeds}")
        return v.lower()

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        if v.lower() not in ["male", "female"]:
            raise ValueError("Género debe ser 'male' o 'female'")
        return v.lower()


class CattleSyncBatchRequest(BaseModel):
    """Batch de animales a sincronizar"""

    items: list[CattleSyncItemRequest] = Field(
        ..., min_length=1, max_length=100, description="Máximo 100 items por batch"
    )
    device_id: str = Field(..., description="ID del dispositivo móvil")
    sync_timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp UTC de sincronización"
    )


class CattleSyncItemResponse(BaseModel):
    """Respuesta de sincronización por item"""

    id: str
    status: SyncStatus
    message: str | None = None
    conflict_data: dict[str, Any] | None = Field(
        None, description="Datos del servidor si hay conflicto"
    )
    synced_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp de sincronización"
    )


class CattleSyncBatchResponse(BaseModel):
    """Respuesta batch de sincronización de ganado"""

    success: bool
    total_items: int
    synced_count: int
    failed_count: int
    conflict_count: int
    results: list[CattleSyncItemResponse]
    sync_timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: str


# ===== Weight Estimation Sync Schemas =====


class WeightEstimationSyncItemRequest(BaseModel):
    """Item de estimación de peso a sincronizar"""

    id: str = Field(..., description="UUID de la estimación")
    cattle_id: str | None = Field(None, description="ID del animal (puede ser null)")
    breed: str = Field(..., description="Raza")
    estimated_weight: float = Field(
        ..., gt=0, lt=1500, description="Peso estimado en kg"
    )
    confidence_score: float = Field(..., ge=0, le=1, description="Confianza 0-1")
    frame_image_path: str = Field(..., description="Path del fotograma")
    timestamp: datetime = Field(..., description="Fecha/hora de la estimación")
    gps_latitude: float | None = Field(None, ge=-90, le=90)
    gps_longitude: float | None = Field(None, ge=-180, le=180)
    method: str = Field(default="tflite", description="Método de estimación")
    model_version: str = Field(default="1.0.0", description="Versión del modelo ML")
    processing_time_ms: int = Field(..., gt=0, description="Tiempo de procesamiento")
    operation: SyncOperation = Field(..., description="create/update/delete")

    @field_validator("breed")
    @classmethod
    def validate_breed(cls, v: str) -> str:
        valid_breeds = [
            "nelore",
            "brahman",
            "guzerat",
            "senepol",
            "girolando",
            "gyr_lechero",
            "sindi",
        ]
        if v.lower() not in valid_breeds:
            raise ValueError(f"Raza inválida. Válidas: {valid_breeds}")
        return v.lower()


class WeightEstimationSyncBatchRequest(BaseModel):
    """Batch de estimaciones a sincronizar"""

    items: list[WeightEstimationSyncItemRequest] = Field(
        ..., min_length=1, max_length=100, description="Máximo 100 items por batch"
    )
    device_id: str = Field(..., description="ID del dispositivo móvil")
    sync_timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp UTC de sincronización"
    )


class WeightEstimationSyncItemResponse(BaseModel):
    """Respuesta de sincronización por estimación"""

    id: str
    status: SyncStatus
    message: str | None = None
    conflict_data: dict[str, Any] | None = None
    synced_at: datetime = Field(default_factory=datetime.utcnow)


class WeightEstimationSyncBatchResponse(BaseModel):
    """Respuesta batch de sincronización de estimaciones"""

    success: bool
    total_items: int
    synced_count: int
    failed_count: int
    conflict_count: int
    results: list[WeightEstimationSyncItemResponse]
    sync_timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: str


# ===== Health Check Schema =====


class HealthCheckResponse(BaseModel):
    """Respuesta de health check"""

    status: str = Field(..., description="online/offline")
    database: str = Field(..., description="Estado de MongoDB")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
