"""
Sync Mapper - API Layer
Mapper para conversión entre DTOs (Schemas) y Entities (Domain)
"""

from datetime import datetime

from ...domain.entities.sync_result import (
    SyncBatchResult,
    SyncItemResult,
    SyncItemStatus,
)
from ...schemas.sync_schemas import (
    CattleSyncBatchResponse,
    CattleSyncItemResponse,
    HealthCheckResponse,
    SyncStatus,
    WeightEstimationSyncBatchResponse,
    WeightEstimationSyncItemResponse,
)


class SyncMapper:
    """
    Mapper para sincronización.

    Single Responsibility: Convertir entre DTOs y Entities.
    """

    @staticmethod
    def to_cattle_batch_response(
        result: SyncBatchResult,
    ) -> CattleSyncBatchResponse:
        """
        Convierte SyncBatchResult a CattleSyncBatchResponse.

        Args:
            result: Resultado de sincronización del dominio

        Returns:
            CattleSyncBatchResponse para API
        """
        return CattleSyncBatchResponse(
            success=result.success,
            total_items=result.total_items,
            synced_count=result.synced_count,
            failed_count=result.failed_count,
            conflict_count=result.conflict_count,
            results=[
                SyncMapper._to_cattle_item_response(item) for item in result.results
            ],
            message=result.message,
        )

    @staticmethod
    def to_weight_estimation_batch_response(
        result: SyncBatchResult,
    ) -> WeightEstimationSyncBatchResponse:
        """
        Convierte SyncBatchResult a WeightEstimationSyncBatchResponse.

        Args:
            result: Resultado de sincronización del dominio

        Returns:
            WeightEstimationSyncBatchResponse para API
        """
        return WeightEstimationSyncBatchResponse(
            success=result.success,
            total_items=result.total_items,
            synced_count=result.synced_count,
            failed_count=result.failed_count,
            conflict_count=result.conflict_count,
            results=[
                SyncMapper._to_weight_estimation_item_response(item)
                for item in result.results
            ],
            message=result.message,
        )

    @staticmethod
    def to_health_check_response(health_data: dict[str, str]) -> HealthCheckResponse:
        """
        Convierte dict de health a HealthCheckResponse.

        Args:
            health_data: Datos de salud del dominio

        Returns:
            HealthCheckResponse para API
        """
        return HealthCheckResponse(
            status=health_data["status"],
            database=health_data["database"],
            timestamp=datetime.fromisoformat(health_data["timestamp"]),
            version=health_data.get("version", "1.0.0"),
        )

    @staticmethod
    def _to_cattle_item_response(
        item: SyncItemResult,
    ) -> CattleSyncItemResponse:
        """Convierte SyncItemResult a CattleSyncItemResponse."""
        return CattleSyncItemResponse(
            id=item.id,
            status=SyncMapper._map_status(item.status),
            message=item.message,
            conflict_data=item.conflict_data,
            synced_at=item.synced_at,
        )

    @staticmethod
    def _to_weight_estimation_item_response(
        item: SyncItemResult,
    ) -> WeightEstimationSyncItemResponse:
        """Convierte SyncItemResult a WeightEstimationSyncItemResponse."""
        return WeightEstimationSyncItemResponse(
            id=item.id,
            status=SyncMapper._map_status(item.status),
            message=item.message,
            conflict_data=item.conflict_data,
            synced_at=item.synced_at,
        )

    @staticmethod
    def _map_status(status: SyncItemStatus) -> SyncStatus:
        """Mapea SyncItemStatus (Domain) a SyncStatus (Schema)."""
        mapping = {
            SyncItemStatus.PENDING: SyncStatus.PENDING,
            SyncItemStatus.SYNCING: SyncStatus.SYNCING,
            SyncItemStatus.SYNCED: SyncStatus.SYNCED,
            SyncItemStatus.ERROR: SyncStatus.ERROR,
            SyncItemStatus.CONFLICT: SyncStatus.CONFLICT,
        }
        return mapping.get(status, SyncStatus.ERROR)
