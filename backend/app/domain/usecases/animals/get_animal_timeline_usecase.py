"""
Get Animal Timeline Use Case
Caso de uso para obtener timeline completo de eventos de un animal
"""

from datetime import datetime
from uuid import UUID

from ....core.exceptions import NotFoundException
from ...repositories.animal_repository import AnimalRepository
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class GetAnimalTimelineUseCase:
    """
    Caso de uso para obtener timeline completo de eventos de un animal.

    Single Responsibility: Construir timeline con todos los eventos del animal.
    """

    def __init__(
        self,
        animal_repository: AnimalRepository,
        weight_estimation_repository: WeightEstimationRepository,
    ):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales
            weight_estimation_repository: Repositorio de estimaciones de peso
        """
        self.animal_repository = animal_repository
        self.weight_estimation_repository = weight_estimation_repository

    async def execute(self, animal_id: UUID) -> dict:
        """
        Ejecuta el caso de uso.

        Args:
            animal_id: ID del animal

        Returns:
            Dict con timeline completo:
            {
                "animal": Animal,
                "events": list[dict]  # Eventos ordenados por fecha
            }

        Raises:
            NotFoundException: Si el animal no existe
        """
        # 1. Obtener animal
        animal = await self.animal_repository.get_by_id(animal_id)
        if animal is None:
            raise NotFoundException(resource="Animal", field="id", value=str(animal_id))

        # 2. Obtener todas las estimaciones de peso del animal
        weight_estimations = await self.weight_estimation_repository.find_by_animal_id(
            str(animal_id), skip=0, limit=1000
        )

        # 3. Construir lista de eventos
        events = []

        # Evento de registro
        events.append(
            {
                "type": "registration",
                "timestamp": animal.registration_date,
                "description": "Animal registrado en el sistema",
                "data": {
                    "ear_tag": animal.ear_tag,
                    "farm_id": str(animal.farm_id),
                },
            }
        )

        # Evento de nacimiento
        events.append(
            {
                "type": "birth",
                "timestamp": animal.birth_date,
                "description": "Nacimiento del animal",
                "data": {
                    "breed": animal.breed,
                    "gender": animal.gender,
                    "birth_weight_kg": animal.birth_weight_kg,
                },
            }
        )

        # Eventos de estimaciones de peso
        for estimation in weight_estimations:
            events.append(
                {
                    "type": "weight_estimation",
                    "timestamp": estimation.timestamp,
                    "description": f"Estimación de peso: {estimation.estimated_weight_kg} kg",
                    "data": {
                        "estimated_weight_kg": estimation.estimated_weight_kg,
                        "confidence": estimation.confidence,
                        "method": estimation.method,
                        "ml_model_version": estimation.ml_model_version,
                        "gps_latitude": None,  # TODO: agregar GPS a WeightEstimation cuando esté disponible
                        "gps_longitude": None,
                        "frame_image_path": estimation.frame_image_path,
                        "processing_time_ms": estimation.processing_time_ms,
                    },
                }
            )

        # Evento de última actualización (si es diferente de registro)
        if animal.last_updated != animal.registration_date:
            events.append(
                {
                    "type": "update",
                    "timestamp": animal.last_updated,
                    "description": "Última actualización de datos",
                    "data": {},
                }
            )

        # Cambios de estado (si el estado cambió de active)
        if animal.status != "active":
            # Buscar cuándo cambió el estado (aproximación: usar last_updated)
            events.append(
                {
                    "type": "status_change",
                    "timestamp": animal.last_updated,
                    "description": f"Estado cambiado a: {animal.status}",
                    "data": {
                        "status": animal.status,
                    },
                }
            )

        # 4. Ordenar eventos por timestamp
        # Función helper para extraer timestamp como float (comparable)
        def get_timestamp_key(event: dict) -> float:
            """Extrae timestamp de un evento y lo convierte a float para comparación."""
            ts = event["timestamp"]
            if isinstance(ts, datetime):
                return ts.timestamp()
            # Fallback (no debería pasar, pero para seguridad)
            return 0.0

        events.sort(key=get_timestamp_key, reverse=False)

        return {
            "animal": animal,
            "events": events,
            "total_events": len(events),
            "weight_estimations_count": len(weight_estimations),
        }
