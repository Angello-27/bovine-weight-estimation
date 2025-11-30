"""
Create Weight Estimation Use Case - Domain Layer
Caso de uso para crear una estimación de peso
"""

from datetime import datetime
from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.weight_estimation import WeightEstimation
from ...repositories.animal_repository import AnimalRepository
from ...repositories.weight_estimation_repository import WeightEstimationRepository


class CreateWeightEstimationUseCase:
    """
    Caso de uso para crear una estimación de peso.

    Single Responsibility: Validar y crear una estimación en el dominio.
    """

    def __init__(
        self,
        weight_estimation_repository: WeightEstimationRepository,
        animal_repository: AnimalRepository | None = None,
    ):
        """
        Inicializa el caso de uso.

        Args:
            weight_estimation_repository: Repositorio de estimaciones
            animal_repository: Repositorio de animales (opcional, para validar)
        """
        self._weight_estimation_repository = weight_estimation_repository
        self._animal_repository = animal_repository

    async def execute(
        self,
        animal_id: str | None,
        breed: str,
        estimated_weight_kg: float,
        confidence: float,
        method: str,
        model_version: str,
        processing_time_ms: int,
        frame_image_path: str,
        latitude: float | None = None,
        longitude: float | None = None,
        timestamp: datetime | None = None,
        device_id: str | None = None,
    ) -> WeightEstimation:
        """
        Ejecuta el caso de uso para crear una estimación.

        Args:
            animal_id: ID del animal (opcional)
            breed: Raza del animal
            estimated_weight_kg: Peso estimado en kg
            confidence: Confidence score (0.0-1.0)
            method: Método de estimación (tflite, web_upload, etc.)
            model_version: Versión del modelo
            processing_time_ms: Tiempo de procesamiento en ms
            frame_image_path: Path del fotograma
            latitude: Latitud GPS (opcional)
            longitude: Longitud GPS (opcional)
            timestamp: Timestamp de la estimación (opcional)
            device_id: ID del dispositivo (opcional)

        Returns:
            WeightEstimation creada

        Raises:
            NotFoundException: Si el animal_id existe pero el animal no se encuentra
        """
        # Validar que el animal existe (si se proporciona)
        if animal_id and self._animal_repository:
            try:
                animal = await self._animal_repository.get_by_id(UUID(animal_id))
                if animal is None:
                    raise NotFoundException(
                        resource="Animal", field="id", value=animal_id
                    )
            except ValueError:
                # Si UUID es inválido, no encontrado
                raise NotFoundException(
                    resource="Animal", field="id", value=animal_id
                )

        # Crear entidad WeightEstimation
        estimation = WeightEstimation(
            animal_id=animal_id,
            breed=breed,
            estimated_weight_kg=estimated_weight_kg,
            confidence=confidence,
            method=method,
            model_version=model_version,
            processing_time_ms=processing_time_ms,
            frame_image_path=frame_image_path,
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp,
            device_id=device_id,
        )

        # Guardar usando el repositorio
        return await self._weight_estimation_repository.create(estimation)

