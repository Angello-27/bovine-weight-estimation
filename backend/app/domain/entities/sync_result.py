"""
Sync Result Entity - Domain Layer
Entidad para resultados de sincronización
"""

from datetime import datetime
from enum import Enum
from typing import Any


class SyncItemStatus(str, Enum):
    """Estado de sincronización de un item."""

    PENDING = "pending"
    SYNCING = "syncing"
    SYNCED = "synced"
    ERROR = "error"
    CONFLICT = "conflict"


class SyncItemResult:
    """
    Resultado de sincronización de un item individual.

    Single Responsibility: Representar el resultado de sincronizar un item.
    """

    def __init__(
        self,
        id: str,
        status: SyncItemStatus,
        message: str | None = None,
        conflict_data: dict[str, Any] | None = None,
        synced_at: datetime | None = None,
    ):
        """Inicializa resultado de sincronización."""
        self.id = id
        self.status = status
        self.message = message
        self.conflict_data = conflict_data
        self.synced_at = synced_at or datetime.utcnow()


class SyncBatchResult:
    """
    Resultado de sincronización de un batch completo.

    Single Responsibility: Representar el resultado de sincronizar un batch.
    """

    def __init__(
        self,
        success: bool,
        total_items: int,
        synced_count: int,
        failed_count: int,
        conflict_count: int,
        results: list[SyncItemResult],
        message: str,
        sync_timestamp: datetime | None = None,
    ):
        """Inicializa resultado de batch."""
        self.success = success
        self.total_items = total_items
        self.synced_count = synced_count
        self.failed_count = failed_count
        self.conflict_count = conflict_count
        self.results = results
        self.message = message
        self.sync_timestamp = sync_timestamp or datetime.utcnow()
