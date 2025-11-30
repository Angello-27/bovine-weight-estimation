"""
Get Upcoming Alerts Use Case - Domain Layer
Caso de uso para obtener alertas programadas para los próximos N días
"""

from uuid import UUID

from ...entities.alert import Alert
from ...repositories.alert_repository import AlertRepository


class GetUpcomingAlertsUseCase:
    """
    Caso de uso para obtener alertas programadas para los próximos N días.

    Single Responsibility: Obtener alertas próximas para calendario.
    """

    def __init__(self, alert_repository: AlertRepository):
        """
        Inicializa el caso de uso.

        Args:
            alert_repository: Repositorio de alertas (inyección de dependencia)
        """
        self._alert_repository = alert_repository

    async def execute(
        self,
        days_ahead: int = 7,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
    ) -> list[Alert]:
        """
        Ejecuta el caso de uso para obtener alertas próximas.

        Args:
            days_ahead: Número de días hacia adelante (default: 7)
            user_id: Filtrar por usuario (opcional)
            farm_id: Filtrar por finca (opcional)

        Returns:
            Lista de Alert próximas
        """
        return await self._alert_repository.find_upcoming(
            days_ahead=days_ahead, user_id=user_id, farm_id=farm_id
        )
