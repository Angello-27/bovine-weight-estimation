"""
Get Scheduled Alerts Use Case - Domain Layer
Caso de uso para obtener alertas programadas en un rango de fechas
"""

from datetime import datetime

from ...entities.alert import Alert
from ...repositories.alert_repository import AlertRepository


class GetScheduledAlertsUseCase:
    """
    Caso de uso para obtener alertas programadas en un rango de fechas.

    Single Responsibility: Obtener alertas programadas para calendario/cronograma.
    """

    def __init__(self, alert_repository: AlertRepository):
        """
        Inicializa el caso de uso.

        Args:
            alert_repository: Repositorio de alertas (inyección de dependencia)
        """
        self._alert_repository = alert_repository

    async def execute(self, from_date: datetime, to_date: datetime) -> list[Alert]:
        """
        Ejecuta el caso de uso para obtener alertas programadas.

        Args:
            from_date: Fecha desde
            to_date: Fecha hasta

        Returns:
            Lista de Alert programadas
        """
        return await self._alert_repository.find_scheduled(from_date, to_date)
