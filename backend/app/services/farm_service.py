"""
Farm Service - Business Logic
Lógica de negocio para gestión de fincas
"""

from uuid import UUID

from ..core.errors import AlreadyExistsException, NotFoundException
from ..models import FarmModel, UserModel
from ..schemas.farm_schemas import (
    FarmCreateRequest,
    FarmResponse,
    FarmUpdateRequest,
)


class FarmService:
    """
    Servicio de gestión de fincas.

    Single Responsibility: Business logic de fincas.
    """

    async def create_farm(self, request: FarmCreateRequest) -> FarmResponse:
        """
        Crea una nueva finca.

        Args:
            request: Datos de la finca a crear

        Returns:
            FarmResponse con la finca creada

        Raises:
            NotFoundException: Si el owner_id no existe
            AlreadyExistsException: Si ya existe una finca con ese nombre para ese propietario
        """
        # Validar que el propietario exista
        owner = await UserModel.get(request.owner_id)
        if owner is None:
            raise NotFoundException(
                resource="User", field="id", value=str(request.owner_id)
            )

        # Validar que no exista otra finca con el mismo nombre para el mismo propietario
        existing = await FarmModel.find_one(
            FarmModel.name == request.name,
            FarmModel.owner_id == request.owner_id,
        )
        if existing is not None:
            raise AlreadyExistsException(
                resource="Farm", field="name", value=request.name
            )

        # Crear finca con GeoJSON Point
        location = {
            "type": "Point",
            "coordinates": [request.longitude, request.latitude],  # [lon, lat]
        }

        farm = FarmModel(
            name=request.name,
            owner_id=request.owner_id,
            location=location,
            capacity=request.capacity,
        )
        await farm.insert()

        lon, lat = farm.get_location_coordinates()
        return FarmResponse(
            id=farm.id,
            name=farm.name,
            owner_id=farm.owner_id,
            latitude=lat,
            longitude=lon,
            capacity=farm.capacity,
            total_animals=farm.total_animals,
            created_at=farm.created_at,
            last_updated=farm.last_updated,
        )

    async def get_farm_by_id(self, farm_id: UUID) -> FarmResponse:
        """
        Obtiene una finca por ID.

        Args:
            farm_id: ID de la finca

        Returns:
            FarmResponse con la finca

        Raises:
            NotFoundException: Si la finca no existe
        """
        farm = await FarmModel.get(farm_id)
        if farm is None:
            raise NotFoundException(resource="Farm", field="id", value=str(farm_id))

        lon, lat = farm.get_location_coordinates()
        return FarmResponse(
            id=farm.id,
            name=farm.name,
            owner_id=farm.owner_id,
            latitude=lat,
            longitude=lon,
            capacity=farm.capacity,
            total_animals=farm.total_animals,
            created_at=farm.created_at,
            last_updated=farm.last_updated,
        )

    async def get_all_farms(
        self, skip: int = 0, limit: int = 50, owner_id: UUID | None = None
    ) -> list[FarmResponse]:
        """
        Obtiene todas las fincas con paginación.

        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            owner_id: Filtrar por propietario (opcional)

        Returns:
            Lista de FarmResponse
        """
        if owner_id:
            farms = (
                await FarmModel.find(FarmModel.owner_id == owner_id)
                .skip(skip)
                .limit(limit)
                .to_list()
            )
        else:
            farms = await FarmModel.find_all().skip(skip).limit(limit).to_list()

        return [
            FarmResponse(
                id=farm.id,
                name=farm.name,
                owner_id=farm.owner_id,
                latitude=farm.get_location_coordinates()[1],
                longitude=farm.get_location_coordinates()[0],
                capacity=farm.capacity,
                total_animals=farm.total_animals,
                created_at=farm.created_at,
                last_updated=farm.last_updated,
            )
            for farm in farms
        ]

    async def update_farm(
        self, farm_id: UUID, request: FarmUpdateRequest
    ) -> FarmResponse:
        """
        Actualiza una finca.

        Args:
            farm_id: ID de la finca
            request: Datos a actualizar

        Returns:
            FarmResponse con la finca actualizada

        Raises:
            NotFoundException: Si la finca no existe
            AlreadyExistsException: Si el nombre ya existe para ese propietario
        """
        farm = await FarmModel.get(farm_id)
        if farm is None:
            raise NotFoundException(resource="Farm", field="id", value=str(farm_id))

        # Validar nombre único si se está actualizando
        if request.name is not None and request.name != farm.name:
            existing = await FarmModel.find_one(
                FarmModel.name == request.name,
                FarmModel.owner_id == farm.owner_id,
            )
            if existing is not None:
                raise AlreadyExistsException(
                    resource="Farm", field="name", value=request.name
                )
            farm.name = request.name

        # Actualizar ubicación si se proporciona
        if request.latitude is not None and request.longitude is not None:
            farm.location = {
                "type": "Point",
                "coordinates": [request.longitude, request.latitude],
            }

        # Actualizar capacidad si se proporciona
        if request.capacity is not None:
            if request.capacity < farm.total_animals:
                raise ValueError(
                    f"La capacidad ({request.capacity}) no puede ser menor que el total de animales actual ({farm.total_animals})"
                )
            farm.capacity = request.capacity

        farm.update_timestamp()
        await farm.save()

        lon, lat = farm.get_location_coordinates()
        return FarmResponse(
            id=farm.id,
            name=farm.name,
            owner_id=farm.owner_id,
            latitude=lat,
            longitude=lon,
            capacity=farm.capacity,
            total_animals=farm.total_animals,
            created_at=farm.created_at,
            last_updated=farm.last_updated,
        )

    async def delete_farm(self, farm_id: UUID) -> None:
        """
        Elimina una finca.

        Args:
            farm_id: ID de la finca

        Raises:
            NotFoundException: Si la finca no existe
            ValueError: Si la finca tiene animales registrados
        """
        farm = await FarmModel.get(farm_id)
        if farm is None:
            raise NotFoundException(resource="Farm", field="id", value=str(farm_id))

        if farm.total_animals > 0:
            raise ValueError(
                f"No se puede eliminar la finca '{farm.name}' porque tiene {farm.total_animals} animales registrados"
            )

        await farm.delete()

