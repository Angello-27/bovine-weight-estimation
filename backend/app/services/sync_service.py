"""
Sync Service - US-005: Sincronización Offline
Lógica de negocio para sincronización bidireccional con last-write-wins
"""

from typing import Any

from ..schemas.sync_schemas import (
    CattleSyncBatchResponse,
    CattleSyncItemRequest,
    CattleSyncItemResponse,
    SyncStatus,
    WeightEstimationSyncBatchResponse,
    WeightEstimationSyncItemRequest,
    WeightEstimationSyncItemResponse,
)


class SyncService:
    """
    Servicio de sincronización con estrategia last-write-wins.

    Single Responsibility: Sincronizar datos entre mobile y backend
    siguiendo estrategia de resolución de conflictos basada en timestamps UTC.

    Estrategia US-005:
    - Last-Write-Wins: El dato con timestamp UTC más reciente prevalece
    - No se requiere intervención manual del usuario
    - Conflictos se resuelven automáticamente
    """

    def __init__(self):
        """
        Inicializa el servicio de sincronización.

        TODO: En producción, inyectar MongoDB repository/client
        Para MVP/Sprint 2: Almacenamiento en memoria (dict)
        """
        # Almacenamiento temporal en memoria (MVP)
        # TODO: Reemplazar con MongoDB en producción
        self._cattle_storage: dict[str, dict[str, Any]] = {}
        self._weight_estimation_storage: dict[str, dict[str, Any]] = {}

    async def sync_cattle_batch(
        self,
        items: list[CattleSyncItemRequest],
        device_id: str,
    ) -> CattleSyncBatchResponse:
        """
        Sincroniza un batch de animales con estrategia last-write-wins.

        Args:
            items: Lista de items a sincronizar (max 100)
            device_id: ID del dispositivo móvil

        Returns:
            CattleSyncBatchResponse con resultados por item
        """
        results: list[CattleSyncItemResponse] = []
        synced_count = 0
        failed_count = 0
        conflict_count = 0

        for item in items:
            try:
                result = await self._sync_cattle_item(item, device_id)
                results.append(result)

                if result.status == SyncStatus.SYNCED:
                    synced_count += 1
                elif result.status == SyncStatus.CONFLICT:
                    conflict_count += 1
                else:
                    failed_count += 1

            except Exception as e:
                # Error al procesar item individual
                results.append(
                    CattleSyncItemResponse(
                        id=item.id,
                        status=SyncStatus.ERROR,
                        message=f"Error al sincronizar: {str(e)}",
                    )
                )
                failed_count += 1

        success = failed_count == 0
        total_items = len(items)

        return CattleSyncBatchResponse(
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

    async def _sync_cattle_item(
        self,
        item: CattleSyncItemRequest,
        device_id: str,
    ) -> CattleSyncItemResponse:
        """
        Sincroniza un item individual de ganado con last-write-wins.

        Lógica:
        1. Si no existe en backend → CREATE
        2. Si existe → Comparar timestamps UTC
        3. El más reciente prevalece (last-write-wins)
        4. Si hay conflicto, se retorna ambos datos para log
        """
        existing = self._cattle_storage.get(item.id)

        # Caso 1: No existe en backend → CREATE
        if existing is None:
            await self._create_cattle(item)
            return CattleSyncItemResponse(
                id=item.id,
                status=SyncStatus.SYNCED,
                message="Animal creado exitosamente",
            )

        # Caso 2: Existe → Aplicar last-write-wins
        existing_timestamp = existing.get("last_updated")
        incoming_timestamp = item.last_updated

        # Comparar timestamps UTC
        if incoming_timestamp > existing_timestamp:
            # Mobile tiene versión más reciente → Actualizar backend
            await self._update_cattle(item)
            return CattleSyncItemResponse(
                id=item.id,
                status=SyncStatus.SYNCED,
                message="Animal actualizado (mobile más reciente)",
            )
        if incoming_timestamp < existing_timestamp:
            # Backend tiene versión más reciente → Retornar conflicto informativo
            # El mobile deberá actualizar su copia local
            return CattleSyncItemResponse(
                id=item.id,
                status=SyncStatus.CONFLICT,
                message="Backend tiene versión más reciente",
                conflict_data=existing,  # Retornar datos del backend
            )
        # Timestamps iguales → Ya está sincronizado
        return CattleSyncItemResponse(
            id=item.id,
            status=SyncStatus.SYNCED,
            message="Ya sincronizado (timestamps iguales)",
        )

    async def _create_cattle(self, item: CattleSyncItemRequest) -> None:
        """Crea un nuevo animal en el backend"""
        self._cattle_storage[item.id] = item.model_dump()

    async def _update_cattle(self, item: CattleSyncItemRequest) -> None:
        """Actualiza un animal existente en el backend"""
        self._cattle_storage[item.id] = item.model_dump()

    async def sync_weight_estimations_batch(
        self,
        items: list[WeightEstimationSyncItemRequest],
        device_id: str,
    ) -> WeightEstimationSyncBatchResponse:
        """
        Sincroniza un batch de estimaciones de peso con last-write-wins.

        Args:
            items: Lista de estimaciones a sincronizar (max 100)
            device_id: ID del dispositivo móvil

        Returns:
            WeightEstimationSyncBatchResponse con resultados
        """
        results: list[WeightEstimationSyncItemResponse] = []
        synced_count = 0
        failed_count = 0
        conflict_count = 0

        for item in items:
            try:
                result = await self._sync_weight_estimation_item(item, device_id)
                results.append(result)

                if result.status == SyncStatus.SYNCED:
                    synced_count += 1
                elif result.status == SyncStatus.CONFLICT:
                    conflict_count += 1
                else:
                    failed_count += 1

            except Exception as e:
                results.append(
                    WeightEstimationSyncItemResponse(
                        id=item.id,
                        status=SyncStatus.ERROR,
                        message=f"Error al sincronizar: {str(e)}",
                    )
                )
                failed_count += 1

        success = failed_count == 0
        total_items = len(items)

        return WeightEstimationSyncBatchResponse(
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
        item: WeightEstimationSyncItemRequest,
        device_id: str,
    ) -> WeightEstimationSyncItemResponse:
        """
        Sincroniza una estimación individual con last-write-wins.

        Nota: Las estimaciones típicamente son inmutables (solo CREATE),
        pero se mantiene lógica completa por consistencia.
        """
        existing = self._weight_estimation_storage.get(item.id)

        # Caso 1: No existe → CREATE
        if existing is None:
            await self._create_weight_estimation(item)
            return WeightEstimationSyncItemResponse(
                id=item.id,
                status=SyncStatus.SYNCED,
                message="Estimación creada exitosamente",
            )

        # Caso 2: Ya existe → Retornar como ya sincronizado
        # (Las estimaciones no se modifican típicamente)
        return WeightEstimationSyncItemResponse(
            id=item.id,
            status=SyncStatus.SYNCED,
            message="Estimación ya existente",
        )

    async def _create_weight_estimation(
        self, item: WeightEstimationSyncItemRequest
    ) -> None:
        """Crea una nueva estimación en el backend"""
        self._weight_estimation_storage[item.id] = item.model_dump()

    def _generate_sync_message(
        self,
        synced: int,
        failed: int,
        conflicts: int,
        total: int,
    ) -> str:
        """Genera mensaje de resumen de sincronización"""
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

    # ===== Métodos de utilidad =====

    def get_cattle_count(self) -> int:
        """Retorna el conteo de animales almacenados"""
        return len(self._cattle_storage)

    def get_weight_estimation_count(self) -> int:
        """Retorna el conteo de estimaciones almacenadas"""
        return len(self._weight_estimation_storage)

    def clear_all_data(self) -> None:
        """
        Limpia todos los datos (solo para testing).

        WARNING: No usar en producción
        """
        self._cattle_storage.clear()
        self._weight_estimation_storage.clear()
