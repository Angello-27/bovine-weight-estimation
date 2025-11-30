"""
List Alerts Use Case - Domain Layer
Caso de uso para listar alertas con filtros
"""

from datetime import datetime
from uuid import UUID

from ...entities.alert import Alert
from ...repositories.alert_repository import AlertRepository


class ListAlertsUseCase:
    """
    Caso de uso para listar alertas con filtros.

    Single Responsibility: Listar alertas con filtros y paginación.
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
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
        type: str | None = None,
        status: str | None = None,
        scheduled_from: datetime | None = None,
        scheduled_to: datetime | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[Alert], int]:
        """
        Ejecuta el caso de uso para listar alertas.

        Args:
            user_id: Filtrar por usuario
            farm_id: Filtrar por finca
            type: Filtrar por tipo
            status: Filtrar por estado
            scheduled_from: Filtrar desde fecha
            scheduled_to: Filtrar hasta fecha
            page: Número de página
            page_size: Tamaño de página

        Returns:
            Tupla (lista de Alert, total)
        """
        skip = (page - 1) * page_size
        alerts = await self._alert_repository.find(
            user_id=user_id,
            farm_id=farm_id,
            type=type,
            status=status,
            scheduled_from=scheduled_from,
            scheduled_to=scheduled_to,
            skip=skip,
            limit=page_size,
        )
        total = await self._alert_repository.count(
            user_id=user_id,
            farm_id=farm_id,
            type=type,
            status=status,
            scheduled_from=scheduled_from,
            scheduled_to=scheduled_to,
        )
        return alerts, total
