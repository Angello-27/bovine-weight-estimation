"""
Update Farm Use Case - Domain Layer
Caso de uso para actualizar una finca
"""

from uuid import UUID

from ....core.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException,
)
from ...entities.farm import Farm
from ...repositories.farm_repository import FarmRepository


class UpdateFarmUseCase:
    """
    Caso de uso para actualizar una finca.

    Single Responsibility: Validar y actualizar una finca en el dominio.
    """

    def __init__(self, farm_repository: FarmRepository):
        """
        Inicializa el caso de uso.

        Args:
            farm_repository: Repositorio de fincas
        """
        self._farm_repository = farm_repository

    async def execute(
        self,
        farm_id: UUID,
        name: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        capacity: int | None = None,
    ) -> Farm:
        """
        Ejecuta el caso de uso para actualizar una finca.

        Args:
            farm_id: ID de la finca
            name: Nuevo nombre (opcional)
            latitude: Nueva latitud (opcional)
            longitude: Nueva longitud (opcional)
            capacity: Nueva capacidad (opcional)

        Returns:
            Farm actualizada

        Raises:
            NotFoundException: Si la finca no existe
            AlreadyExistsException: Si el nombre ya existe para ese propietario
            ValidationException: Si la capacidad es menor que total_animals
        """
        # Obtener finca existente
        farm = await self._farm_repository.get_by_id(farm_id)
        if farm is None:
            raise NotFoundException(resource="Farm", field="id", value=str(farm_id))

        # Validar nombre único si se está actualizando
        if name is not None and name != farm.name:
            owner_id = farm.owner_id
            if owner_id is None:
                raise ValidationException(
                    "No se puede actualizar el nombre de una finca sin propietario"
                )
            existing = await self._farm_repository.find_by_name_and_owner(
                name, owner_id
            )
            if existing is not None:
                raise AlreadyExistsException(resource="Farm", field="name", value=name)
            farm.name = name

        # Actualizar ubicación si se proporciona
        if latitude is not None and longitude is not None:
            farm.latitude = latitude
            farm.longitude = longitude

        # Actualizar capacidad si se proporciona
        if capacity is not None:
            if capacity < farm.total_animals:
                raise ValidationException(
                    f"La capacidad ({capacity}) no puede ser menor que el total de animales actual ({farm.total_animals})"
                )
            farm.capacity = capacity

        # Actualizar timestamp
        farm.update_timestamp()

        # Guardar cambios
        return await self._farm_repository.save(farm)
