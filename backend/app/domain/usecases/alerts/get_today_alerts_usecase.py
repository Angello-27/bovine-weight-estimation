"""
Get Today Alerts Use Case - Domain Layer
Caso de uso para obtener alertas programadas para el día de hoy
"""

from uuid import UUID

from ...entities.alert import Alert
from ...repositories.alert_repository import AlertRepository


class GetTodayAlertsUseCase:
    """
    Caso de uso para obtener alertas programadas para el día de hoy.

    Single Responsibility: Obtener alertas del día actual.
    """

    def __init__(self, alert_repository: AlertRepository):
        """
        Inicializa el caso de uso.

        Args:
            alert_repository: Repositorio de alertas (inyección de dependencia)
        """
        self._alert_repository = alert_repository

    async def execute(
        self, user_id: UUID | None = None, farm_id: UUID | None = None
    ) -> list[Alert]:
        """
        Ejecuta el caso de uso para obtener alertas del día de hoy.

        Args:
            user_id: Filtrar por usuario (opcional)
            farm_id: Filtrar por finca (opcional)

        Returns:
            Lista de Alert del día actual
        """
        return await self._alert_repository.find_today(user_id=user_id, farm_id=farm_id)
