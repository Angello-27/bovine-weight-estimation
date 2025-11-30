"""
Create Farm Use Case - Domain Layer
Caso de uso para crear una finca
"""

from ....core.exceptions import AlreadyExistsException, NotFoundException
from ...entities.farm import Farm
from ...repositories.farm_repository import FarmRepository
from ...repositories.user_repository import UserRepository


class CreateFarmUseCase:
    """
    Caso de uso para crear una finca.

    Single Responsibility: Validar y crear una finca en el dominio.
    """

    def __init__(
        self,
        farm_repository: FarmRepository,
        user_repository: UserRepository,
    ):
        """
        Inicializa el caso de uso.

        Args:
            farm_repository: Repositorio de fincas
            user_repository: Repositorio de usuarios
        """
        self._farm_repository = farm_repository
        self._user_repository = user_repository

    async def execute(
        self,
        name: str,
        owner_id,
        latitude: float,
        longitude: float,
        capacity: int,
    ) -> Farm:
        """
        Ejecuta el caso de uso para crear una finca.

        Args:
            name: Nombre de la finca
            owner_id: ID del propietario
            latitude: Latitud GPS
            longitude: Longitud GPS
            capacity: Capacidad máxima de animales

        Returns:
            Farm creada

        Raises:
            NotFoundException: Si el propietario no existe
            AlreadyExistsException: Si ya existe una finca con ese nombre para ese propietario
        """
        # Validar que el propietario exista
        owner = await self._user_repository.get_by_id(owner_id)
        if owner is None:
            raise NotFoundException(resource="User", field="id", value=str(owner_id))

        # Validar que no exista otra finca con el mismo nombre para el mismo propietario
        existing = await self._farm_repository.find_by_name_and_owner(name, owner_id)
        if existing is not None:
            raise AlreadyExistsException(resource="Farm", field="name", value=name)

        # Crear entidad Farm
        farm = Farm(
            name=name,
            owner_id=owner_id,
            latitude=latitude,
            longitude=longitude,
            capacity=capacity,
            total_animals=0,
        )

        # Guardar usando el repositorio
        return await self._farm_repository.save(farm)
