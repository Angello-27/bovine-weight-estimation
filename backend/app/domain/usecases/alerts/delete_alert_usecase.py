"""
Delete Alert Use Case - Domain Layer
Caso de uso para eliminar una alerta
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...repositories.alert_repository import AlertRepository


class DeleteAlertUseCase:
    """
    Caso de uso para eliminar una alerta.

    Single Responsibility: Eliminar una alerta.
    """

    def __init__(self, alert_repository: AlertRepository):
        """
        Inicializa el caso de uso.

        Args:
            alert_repository: Repositorio de alertas (inyección de dependencia)
        """
        self._alert_repository = alert_repository

    async def execute(self, alert_id: UUID) -> None:
        """
        Ejecuta el caso de uso para eliminar una alerta.

        Args:
            alert_id: ID de la alerta

        Raises:
            NotFoundException: Si la alerta no existe
        """
        alert = await self._alert_repository.get_by_id(alert_id)
        if alert is None:
            raise NotFoundException(resource="Alert", field="id", value=str(alert_id))

        await self._alert_repository.delete(alert_id)
