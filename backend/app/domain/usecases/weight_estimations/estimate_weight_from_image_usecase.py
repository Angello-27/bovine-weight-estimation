"""
Estimate Weight From Image Use Case - Domain Layer
Caso de uso para estimar peso desde imagen usando ML
"""

from uuid import UUID

from ....core.utils.ml_inference import estimate_weight_from_image
from ...entities.weight_estimation import WeightEstimation
from ...repositories.animal_repository import AnimalRepository
from ...repositories.weight_estimation_repository import WeightEstimationRepository
from ...shared.constants import BreedType


class EstimateWeightFromImageUseCase:
    """
    Caso de uso para estimar peso desde imagen y guardar la estimación.

    Single Responsibility: Coordinar inferencia ML y persistencia de estimación.
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
        image_bytes: bytes,
        breed: BreedType,
        animal_id: UUID | None = None,
        device_id: str | None = None,
        frame_image_path: str | None = None,
    ) -> WeightEstimation:
        """
        Ejecuta el caso de uso para estimar peso desde imagen.

        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)
            breed: Raza del animal
            animal_id: ID del animal (opcional)
            device_id: ID del dispositivo (opcional)
            frame_image_path: Path donde se guardará la imagen (opcional)

        Returns:
            WeightEstimation guardada

        Raises:
            ValidationException: Si datos son inválidos
            NotFoundException: Si el animal_id existe pero el animal no se encuentra
            MLModelException: Si hay error en ML
        """
        # Validar que el animal existe (si se proporciona)
        if animal_id and self._animal_repository:
            animal = await self._animal_repository.get_by_id(animal_id)
            if animal is None:
                from ....core.exceptions import NotFoundException

                raise NotFoundException(
                    resource="Animal", field="id", value=str(animal_id)
                )

        # Estimar peso usando util ML
        estimation = await estimate_weight_from_image(
            image_bytes=image_bytes,
            breed=breed,
            animal_id=str(animal_id) if animal_id else None,
            device_id=device_id,
            frame_image_path=frame_image_path,
        )

        # Guardar estimación usando el repositorio
        return await self._weight_estimation_repository.create(estimation)
