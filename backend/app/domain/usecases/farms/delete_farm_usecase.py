"""
Delete Farm Use Case - Domain Layer
Caso de uso para eliminar una finca
"""

from uuid import UUID

from ....core.exceptions import NotFoundException, ValidationException
from ...repositories.farm_repository import FarmRepository


class DeleteFarmUseCase:
    """
    Caso de uso para eliminar una finca.

    Single Responsibility: Eliminar una finca del dominio.
    """

    def __init__(self, farm_repository: FarmRepository):
        """
        Inicializa el caso de uso.

        Args:
            farm_repository: Repositorio de fincas
        """
        self._farm_repository = farm_repository

    async def execute(self, farm_id: UUID) -> None:
        """
        Ejecuta el caso de uso para eliminar una finca.

        Args:
            farm_id: ID de la finca

        Raises:
            NotFoundException: Si la finca no existe
            ValidationException: Si la finca tiene animales registrados
        """
        # Verificar que la finca existe
        farm = await self._farm_repository.get_by_id(farm_id)
        if farm is None:
            raise NotFoundException(resource="Farm", field="id", value=str(farm_id))

        # Validar que no tenga animales
        if farm.total_animals > 0:
            raise ValidationException(
                f"No se puede eliminar la finca '{farm.name}' porque tiene {farm.total_animals} animales registrados"
            )

        # Eliminar
        await self._farm_repository.delete(farm_id)
