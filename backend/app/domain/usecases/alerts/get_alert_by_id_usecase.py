"""
Get Alert By ID Use Case - Domain Layer
Caso de uso para obtener una alerta por ID
"""

from uuid import UUID

from ....core.exceptions import NotFoundException
from ...entities.alert import Alert
from ...repositories.alert_repository import AlertRepository


class GetAlertByIdUseCase:
    """
    Caso de uso para obtener una alerta por ID.

    Single Responsibility: Obtener una alerta por ID.
    """

    def __init__(self, alert_repository: AlertRepository):
        """
        Inicializa el caso de uso.

        Args:
            alert_repository: Repositorio de alertas (inyección de dependencia)
        """
        self._alert_repository = alert_repository

    async def execute(self, alert_id: UUID) -> Alert:
        """
        Ejecuta el caso de uso para obtener una alerta por ID.

        Args:
            alert_id: ID de la alerta

        Returns:
            Alert encontrada

        Raises:
            NotFoundException: Si la alerta no existe
        """
        alert = await self._alert_repository.get_by_id(alert_id)
        if alert is None:
            raise NotFoundException(resource="Alert", field="id", value=str(alert_id))
        return alert
