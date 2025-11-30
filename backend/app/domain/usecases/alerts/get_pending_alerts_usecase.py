"""
Get Pending Alerts Use Case - Domain Layer
Caso de uso para obtener alertas pendientes
"""

from uuid import UUID

from ...entities.alert import Alert
from ...repositories.alert_repository import AlertRepository


class GetPendingAlertsUseCase:
    """
    Caso de uso para obtener alertas pendientes.

    Single Responsibility: Obtener alertas pendientes para procesar.
    """

    def __init__(self, alert_repository: AlertRepository):
        """
        Inicializa el caso de uso.

        Args:
            alert_repository: Repositorio de alertas (inyección de dependencia)
        """
        self._alert_repository = alert_repository

    async def execute(self, user_id: UUID | None = None) -> list[Alert]:
        """
        Ejecuta el caso de uso para obtener alertas pendientes.

        Args:
            user_id: Filtrar por usuario (opcional)

        Returns:
            Lista de Alert pendientes
        """
        return await self._alert_repository.find_pending(user_id=user_id)
