"""
Sync Weight Estimations Batch Use Case - Domain Layer
Caso de uso para sincronizar batch de estimaciones de peso con estrategia last-write-wins
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from ...entities.sync_result import SyncBatchResult, SyncItemResult, SyncItemStatus
from ...entities.weight_estimation import WeightEstimation
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class SyncWeightEstimationsBatchUseCase:
    """
    Caso de uso para sincronizar batch de estimaciones de peso.

    Single Responsibility: Sincronizar estimaciones con estrategia last-write-wins.
    """

    def __init__(self, weight_estimation_repository: WeightEstimationRepository):
        """
        Inicializa el caso de uso.

        Args:
            weight_estimation_repository: Repositorio de estimaciones (inyección de dependencia)
        """
        self._weight_estimation_repository = weight_estimation_repository

    async def execute(
        self,
        items: list[dict[str, Any]],
        device_id: str,
    ) -> SyncBatchResult:
        """
        Ejecuta la sincronización de batch de estimaciones.

        Args:
            items: Lista de items a sincronizar (max 100)
            device_id: ID del dispositivo móvil

        Returns:
            SyncBatchResult con resultados por item
        """
        results: list[SyncItemResult] = []
        synced_count = 0
        failed_count = 0
        conflict_count = 0

        for item_data in items:
            try:
                result = await self._sync_weight_estimation_item(item_data, device_id)
                results.append(result)

                if result.status == SyncItemStatus.SYNCED:
                    synced_count += 1
                elif result.status == SyncItemStatus.CONFLICT:
                    conflict_count += 1
                else:
                    failed_count += 1

            except Exception as e:
                results.append(
                    SyncItemResult(
                        id=item_data.get("id", "unknown"),
                        status=SyncItemStatus.ERROR,
                        message=f"Error al sincronizar: {str(e)}",
                    )
                )
                failed_count += 1

        success = failed_count == 0
        total_items = len(items)

        return SyncBatchResult(
            success=success,
            total_items=total_items,
            synced_count=synced_count,
            failed_count=failed_count,
            conflict_count=conflict_count,
            results=results,
            message=self._generate_sync_message(
                synced_count, failed_count, conflict_count, total_items
            ),
        )

    async def _sync_weight_estimation_item(
        self,
        item_data: dict[str, Any],
        device_id: str,
    ) -> SyncItemResult:
        """
        Sincroniza una estimación individual con last-write-wins.

        Nota: Las estimaciones típicamente son inmutables (solo CREATE),
        pero se mantiene lógica completa por consistencia.
        """
        try:
            estimation_id = UUID(item_data["id"])
        except (ValueError, KeyError):
            return SyncItemResult(
                id=item_data.get("id", "unknown"),
                status=SyncItemStatus.ERROR,
                message="ID inválido (no es UUID válido)",
            )

        # Buscar estimación existente
        existing = await self._weight_estimation_repository.find_by_id(estimation_id)

        # Caso 1: No existe → CREATE
        if existing is None:
            estimation = self._create_estimation_from_item(item_data, device_id)
            await self._weight_estimation_repository.create(estimation)
            return SyncItemResult(
                id=item_data["id"],
                status=SyncItemStatus.SYNCED,
                message="Estimación creada exitosamente",
            )

        # Caso 2: Ya existe → Comparar timestamps
        existing_timestamp = existing.timestamp
        incoming_timestamp = datetime.fromisoformat(
            item_data["timestamp"].replace("Z", "+00:00")
        )

        if incoming_timestamp > existing_timestamp:
            # Mobile más reciente → Actualizar
            updated_estimation = self._update_estimation_from_item(
                existing, item_data, device_id
            )
            await self._weight_estimation_repository.update(updated_estimation)
            return SyncItemResult(
                id=item_data["id"],
                status=SyncItemStatus.SYNCED,
                message="Estimación actualizada (mobile más reciente)",
            )

        if incoming_timestamp < existing_timestamp:
            # Backend más reciente → Conflicto
            return SyncItemResult(
                id=item_data["id"],
                status=SyncItemStatus.CONFLICT,
                message="Backend tiene versión más reciente",
                conflict_data=self._estimation_to_dict(existing),
            )

        # Timestamps iguales → Ya sincronizado
        return SyncItemResult(
            id=item_data["id"],
            status=SyncItemStatus.SYNCED,
            message="Estimación ya existente",
        )

    def _create_estimation_from_item(
        self, item_data: dict[str, Any], device_id: str
    ) -> WeightEstimation:
        """Crea entidad WeightEstimation desde item de sincronización."""
        animal_id = UUID(item_data["cattle_id"]) if item_data.get("cattle_id") else None

        return WeightEstimation(
            id=UUID(item_data["id"]),
            animal_id=str(animal_id) if animal_id else None,
            breed=item_data["breed"],
            estimated_weight_kg=item_data["estimated_weight"],
            confidence=item_data["confidence_score"],
            method=item_data.get("method", "tflite"),
            model_version=item_data.get("model_version", "1.0.0"),
            processing_time_ms=item_data["processing_time_ms"],
            frame_image_path=item_data["frame_image_path"],
            latitude=item_data.get("gps_latitude"),
            longitude=item_data.get("gps_longitude"),
            timestamp=datetime.fromisoformat(
                item_data["timestamp"].replace("Z", "+00:00")
            ),
            device_id=device_id,
            synced_at=datetime.utcnow(),
        )

    def _update_estimation_from_item(
        self,
        existing: WeightEstimation,
        item_data: dict[str, Any],
        device_id: str,
    ) -> WeightEstimation:
        """Actualiza entidad WeightEstimation desde item de sincronización."""
        existing.animal_id = (
            str(UUID(item_data["cattle_id"])) if item_data.get("cattle_id") else None
        )
        existing.breed = item_data["breed"]
        existing.estimated_weight_kg = item_data["estimated_weight"]
        existing.confidence = item_data["confidence_score"]
        existing.method = item_data.get("method", "tflite")
        existing.ml_model_version = item_data.get("ml_model_version", "1.0.0")
        existing.processing_time_ms = item_data["processing_time_ms"]
        existing.frame_image_path = item_data["frame_image_path"]
        existing.latitude = item_data.get("gps_latitude")
        existing.longitude = item_data.get("gps_longitude")
        existing.timestamp = datetime.fromisoformat(
            item_data["timestamp"].replace("Z", "+00:00")
        )
        existing.device_id = device_id
        existing.synced_at = datetime.utcnow()
        return existing

    def _estimation_to_dict(self, estimation: WeightEstimation) -> dict[str, Any]:
        """Convierte WeightEstimation a dict para conflict_data."""
        return {
            "id": str(estimation.id),
            "animal_id": estimation.animal_id,
            "breed": estimation.breed,
            "estimated_weight_kg": estimation.estimated_weight_kg,
            "confidence": estimation.confidence,
            "method": estimation.method,
            "ml_model_version": estimation.ml_model_version,
            "timestamp": estimation.timestamp.isoformat(),
        }

    def _generate_sync_message(
        self,
        synced: int,
        failed: int,
        conflicts: int,
        total: int,
    ) -> str:
        """Genera mensaje de resumen de sincronización."""
        if failed == 0 and conflicts == 0:
            return f"✓ {synced} de {total} items sincronizados exitosamente"
        if failed > 0 and conflicts == 0:
            return f"⚠ {synced} sincronizados, {failed} errores de {total} items"
        if conflicts > 0:
            return (
                f"⚠ {synced} sincronizados, {conflicts} conflictos, "
                f"{failed} errores de {total} items"
            )
        return f"Sincronización completada: {synced}/{total}"
