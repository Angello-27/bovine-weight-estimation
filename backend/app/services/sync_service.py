"""
Sync Service - US-005: Sincronización Offline
Lógica de negocio para sincronización bidireccional con last-write-wins
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from ..models import AnimalModel, WeightEstimationModel
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
                        conflict_data=None,
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
        try:
            animal_id = UUID(item.id)
        except ValueError:
            return CattleSyncItemResponse(
                id=item.id,
                status=SyncStatus.ERROR,
                message="ID inválido (no es UUID válido)",
                conflict_data=None,
            )

        # Buscar animal existente en MongoDB
        existing = await AnimalModel.get(animal_id)

        # Caso 1: No existe en backend → CREATE
        if existing is None:
            await self._create_cattle(item, device_id)
            return CattleSyncItemResponse(
                id=item.id,
                status=SyncStatus.SYNCED,
                message="Animal creado exitosamente",
                conflict_data=None,
            )

        # Caso 2: Existe → Aplicar last-write-wins
        existing_timestamp = existing.last_updated
        incoming_timestamp = item.last_updated

        # Comparar timestamps UTC
        if incoming_timestamp > existing_timestamp:
            # Mobile tiene versión más reciente → Actualizar backend
            await self._update_cattle(item, existing, device_id)
            return CattleSyncItemResponse(
                id=item.id,
                status=SyncStatus.SYNCED,
                message="Animal actualizado (mobile más reciente)",
                conflict_data=None,
            )
        if incoming_timestamp < existing_timestamp:
            # Backend tiene versión más reciente → Retornar conflicto informativo
            # El mobile deberá actualizar su copia local
            return CattleSyncItemResponse(
                id=item.id,
                status=SyncStatus.CONFLICT,
                message="Backend tiene versión más reciente",
                conflict_data=self._animal_to_dict(
                    existing
                ),  # Retornar datos del backend
            )
        # Timestamps iguales → Ya está sincronizado
        return CattleSyncItemResponse(
            id=item.id,
            status=SyncStatus.SYNCED,
            message="Ya sincronizado (timestamps iguales)",
            conflict_data=None,
        )

    async def _create_cattle(self, item: CattleSyncItemRequest, device_id: str) -> None:
        """
        Crea un nuevo animal en MongoDB.

        Nota: farm_id se obtiene del primer animal existente o se usa el default.
        En producción, debería venir en el request.
        """
        # Obtener farm_id del primer animal existente o usar default
        # TODO: En producción, farm_id debería venir en el request
        first_animal = await AnimalModel.find_one()
        farm_id = (
            first_animal.farm_id
            if first_animal
            else UUID("550e8400-e29b-41d4-a716-446655440000")
        )

        animal = AnimalModel(
            id=UUID(item.id),
            ear_tag=item.ear_tag,
            breed=item.breed,
            birth_date=item.birth_date,
            gender=item.gender,
            name=item.name,
            color=item.color,
            birth_weight_kg=item.birth_weight,
            mother_id=item.mother_id,
            father_id=item.father_id,
            observations=item.observations,
            photo_url=item.photo_path,
            status=item.status,
            farm_id=farm_id,
            registration_date=item.registration_date,
            last_updated=item.last_updated,
            device_id=device_id,
            synced_at=datetime.utcnow(),
        )
        await animal.insert()

    async def _update_cattle(
        self,
        item: CattleSyncItemRequest,
        existing: AnimalModel,
        device_id: str,
    ) -> None:
        """Actualiza un animal existente en MongoDB."""
        existing.ear_tag = item.ear_tag
        existing.breed = item.breed
        existing.birth_date = item.birth_date
        existing.gender = item.gender
        existing.name = item.name
        existing.color = item.color
        existing.birth_weight_kg = item.birth_weight
        existing.mother_id = item.mother_id
        existing.father_id = item.father_id
        existing.observations = item.observations
        existing.photo_url = item.photo_path
        existing.status = item.status
        existing.last_updated = item.last_updated
        existing.device_id = device_id
        existing.synced_at = datetime.utcnow()
        await existing.save()

    def _animal_to_dict(self, animal: AnimalModel) -> dict[str, Any]:
        """Convierte AnimalModel a dict para conflict_data."""
        return {
            "id": str(animal.id),
            "ear_tag": animal.ear_tag,
            "breed": animal.breed,
            "birth_date": animal.birth_date.isoformat(),
            "gender": animal.gender,
            "name": animal.name,
            "color": animal.color,
            "birth_weight_kg": animal.birth_weight_kg,
            "mother_id": animal.mother_id,
            "father_id": animal.father_id,
            "status": animal.status,
            "last_updated": animal.last_updated.isoformat(),
        }

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
        try:
            estimation_id = UUID(item.id)
        except ValueError:
            return WeightEstimationSyncItemResponse(
                id=item.id,
                status=SyncStatus.ERROR,
                message="ID inválido (no es UUID válido)",
                conflict_data=None,
            )

        # Buscar estimación existente en MongoDB
        existing = await WeightEstimationModel.get(estimation_id)

        # Caso 1: No existe → CREATE
        if existing is None:
            await self._create_weight_estimation(item, device_id)
            return WeightEstimationSyncItemResponse(
                id=item.id,
                status=SyncStatus.SYNCED,
                message="Estimación creada exitosamente",
                conflict_data=None,
            )

        # Caso 2: Ya existe → Comparar timestamps
        existing_timestamp = existing.timestamp
        incoming_timestamp = item.timestamp

        if incoming_timestamp > existing_timestamp:
            # Mobile más reciente → Actualizar
            await self._update_weight_estimation(item, existing, device_id)
            return WeightEstimationSyncItemResponse(
                id=item.id,
                status=SyncStatus.SYNCED,
                message="Estimación actualizada (mobile más reciente)",
                conflict_data=None,
            )
        if incoming_timestamp < existing_timestamp:
            # Backend más reciente → Conflicto
            return WeightEstimationSyncItemResponse(
                id=item.id,
                status=SyncStatus.CONFLICT,
                message="Backend tiene versión más reciente",
                conflict_data=self._weighing_to_dict(existing),
            )

        # Timestamps iguales → Ya sincronizado
        return WeightEstimationSyncItemResponse(
            id=item.id,
            status=SyncStatus.SYNCED,
            message="Estimación ya existente",
            conflict_data=None,
        )

    async def _create_weight_estimation(
        self, item: WeightEstimationSyncItemRequest, device_id: str
    ) -> None:
        """Crea una nueva estimación en MongoDB."""
        animal_id = UUID(item.cattle_id) if item.cattle_id else None

        weighing = WeightEstimationModel(
            id=UUID(item.id),
            animal_id=str(animal_id) if animal_id else None,
            breed=item.breed,
            estimated_weight_kg=item.estimated_weight,
            confidence=item.confidence_score,
            method=item.method,
            model_version=item.model_version,
            processing_time_ms=item.processing_time_ms,
            frame_image_path=item.frame_image_path,
            latitude=item.gps_latitude,
            longitude=item.gps_longitude,
            timestamp=item.timestamp,
            device_id=device_id,
            synced_at=datetime.utcnow(),
        )
        await weighing.insert()

    async def _update_weight_estimation(
        self,
        item: WeightEstimationSyncItemRequest,
        existing: WeightEstimationModel,
        device_id: str,
    ) -> None:
        """Actualiza una estimación existente en MongoDB."""
        existing.animal_id = str(UUID(item.cattle_id)) if item.cattle_id else None
        existing.breed = item.breed
        existing.estimated_weight_kg = item.estimated_weight
        existing.confidence = item.confidence_score
        existing.method = item.method
        existing.model_version = item.model_version
        existing.processing_time_ms = item.processing_time_ms
        existing.frame_image_path = item.frame_image_path
        existing.latitude = item.gps_latitude
        existing.longitude = item.gps_longitude
        existing.timestamp = item.timestamp
        existing.device_id = device_id
        existing.synced_at = datetime.utcnow()
        await existing.save()

    def _weighing_to_dict(self, weighing: WeightEstimationModel) -> dict[str, Any]:
        """Convierte WeightEstimationModel a dict para conflict_data."""
        return {
            "id": str(weighing.id),
            "animal_id": weighing.animal_id,
            "breed": weighing.breed,
            "estimated_weight_kg": weighing.estimated_weight_kg,
            "confidence": weighing.confidence,
            "method": weighing.method,
            "model_version": weighing.model_version,
            "timestamp": weighing.timestamp.isoformat(),
        }

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

    async def get_cattle_count(self) -> int:
        """Retorna el conteo de animales almacenados en MongoDB"""
        return await AnimalModel.count()

    async def get_weight_estimation_count(self) -> int:
        """Retorna el conteo de estimaciones almacenadas en MongoDB"""
        return await WeightEstimationModel.count()
