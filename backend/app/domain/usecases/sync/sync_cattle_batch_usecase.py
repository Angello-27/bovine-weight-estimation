"""
Sync Cattle Batch Use Case - Domain Layer
Caso de uso para sincronizar batch de animales con estrategia last-write-wins
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from ...entities.animal import Animal
from ...entities.sync_result import SyncBatchResult, SyncItemResult, SyncItemStatus
from ...repositories.animal_repository import AnimalRepository


class SyncCattleBatchUseCase:
    """
    Caso de uso para sincronizar batch de animales.

    Single Responsibility: Sincronizar animales con estrategia last-write-wins.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales (inyección de dependencia)
        """
        self._animal_repository = animal_repository

    async def execute(
        self,
        items: list[dict[str, Any]],
        device_id: str,
    ) -> SyncBatchResult:
        """
        Ejecuta la sincronización de batch de animales.

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
                result = await self._sync_cattle_item(item_data, device_id)
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

    async def _sync_cattle_item(
        self,
        item_data: dict[str, Any],
        device_id: str,
    ) -> SyncItemResult:
        """
        Sincroniza un item individual con last-write-wins.

        Lógica:
        1. Si no existe en backend → CREATE
        2. Si existe → Comparar timestamps UTC
        3. El más reciente prevalece (last-write-wins)
        """
        try:
            animal_id = UUID(item_data["id"])
        except (ValueError, KeyError):
            return SyncItemResult(
                id=item_data.get("id", "unknown"),
                status=SyncItemStatus.ERROR,
                message="ID inválido (no es UUID válido)",
            )

        # Buscar animal existente
        existing = await self._animal_repository.get_by_id(animal_id)

        # Caso 1: No existe → CREATE
        if existing is None:
            animal = await self._create_animal_from_item(item_data, device_id)
            await self._animal_repository.save(animal)
            return SyncItemResult(
                id=item_data["id"],
                status=SyncItemStatus.SYNCED,
                message="Animal creado exitosamente",
            )

        # Caso 2: Existe → Aplicar last-write-wins
        existing_timestamp = existing.last_updated
        incoming_timestamp = datetime.fromisoformat(
            item_data["last_updated"].replace("Z", "+00:00")
        )

        if incoming_timestamp > existing_timestamp:
            # Mobile más reciente → Actualizar backend
            updated_animal = await self._update_animal_from_item(
                existing, item_data, device_id
            )
            await self._animal_repository.save(updated_animal)
            return SyncItemResult(
                id=item_data["id"],
                status=SyncItemStatus.SYNCED,
                message="Animal actualizado (mobile más reciente)",
            )

        if incoming_timestamp < existing_timestamp:
            # Backend más reciente → Conflicto
            return SyncItemResult(
                id=item_data["id"],
                status=SyncItemStatus.CONFLICT,
                message="Backend tiene versión más reciente",
                conflict_data=self._animal_to_dict(existing),
            )

        # Timestamps iguales → Ya sincronizado
        return SyncItemResult(
            id=item_data["id"],
            status=SyncItemStatus.SYNCED,
            message="Ya sincronizado (timestamps iguales)",
        )

    async def _create_animal_from_item(
        self, item_data: dict[str, Any], device_id: str
    ) -> Animal:
        """Crea entidad Animal desde item de sincronización."""
        # Obtener farm_id (por ahora usar default o del item si viene)
        # TODO: En producción, farm_id debería venir en el request
        farm_id = (
            UUID(item_data.get("farm_id"))
            if item_data.get("farm_id")
            else UUID("550e8400-e29b-41d4-a716-446655440000")
        )

        return Animal(
            id=UUID(item_data["id"]),
            ear_tag=item_data["ear_tag"],
            breed=item_data["breed"],
            birth_date=datetime.fromisoformat(
                item_data["birth_date"].replace("Z", "+00:00")
            ),
            gender=item_data["gender"],
            name=item_data.get("name"),
            color=item_data.get("color"),
            birth_weight_kg=item_data.get("birth_weight"),
            mother_id=item_data.get("mother_id"),
            father_id=item_data.get("father_id"),
            observations=item_data.get("observations"),
            photo_url=item_data.get("photo_path"),
            status=item_data.get("status", "active"),
            farm_id=farm_id,
            registration_date=datetime.fromisoformat(
                item_data["registration_date"].replace("Z", "+00:00")
            ),
            last_updated=datetime.fromisoformat(
                item_data["last_updated"].replace("Z", "+00:00")
            ),
            device_id=device_id,
            synced_at=datetime.utcnow(),
        )

    async def _update_animal_from_item(
        self, existing: Animal, item_data: dict[str, Any], device_id: str
    ) -> Animal:
        """Actualiza entidad Animal desde item de sincronización."""
        existing.ear_tag = item_data["ear_tag"]
        existing.breed = item_data["breed"]
        existing.birth_date = datetime.fromisoformat(
            item_data["birth_date"].replace("Z", "+00:00")
        )
        existing.gender = item_data["gender"]
        existing.name = item_data.get("name")
        existing.color = item_data.get("color")
        existing.birth_weight_kg = item_data.get("birth_weight")
        existing.mother_id = item_data.get("mother_id")
        existing.father_id = item_data.get("father_id")
        existing.observations = item_data.get("observations")
        existing.photo_url = item_data.get("photo_path")
        existing.status = item_data.get("status", "active")
        existing.last_updated = datetime.fromisoformat(
            item_data["last_updated"].replace("Z", "+00:00")
        )
        existing.device_id = device_id
        existing.synced_at = datetime.utcnow()
        return existing

    def _animal_to_dict(self, animal: Animal) -> dict[str, Any]:
        """Convierte Animal a dict para conflict_data."""
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
