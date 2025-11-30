"""
Alert Repository Interface - Domain Layer
Contrato para persistencia de alertas (Dependency Inversion)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from uuid import UUID

from ..entities.alert import Alert


class AlertRepository(ABC):
    """
    Interfaz para repositorio de alertas.

    Dependency Inversion: Domain define el contrato, Data lo implementa.
    """

    @abstractmethod
    async def save(self, alert: Alert) -> Alert:
        """
        Guarda o actualiza una alerta.

        Args:
            alert: Entidad Alert a persistir

        Returns:
            Alert guardado con ID asignado
        """
        pass

    @abstractmethod
    async def get_by_id(self, alert_id: UUID) -> Alert | None:
        """
        Obtiene una alerta por ID.

        Args:
            alert_id: ID de la alerta

        Returns:
            Alert si existe, None si no existe
        """
        pass

    @abstractmethod
    async def find(
        self,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
        type: str | None = None,
        status: str | None = None,
        scheduled_from: datetime | None = None,
        scheduled_to: datetime | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Alert]:
        """
        Busca alertas con filtros opcionales.

        Args:
            user_id: Filtrar por usuario
            farm_id: Filtrar por finca
            type: Filtrar por tipo
            status: Filtrar por estado
            scheduled_from: Filtrar desde fecha
            scheduled_to: Filtrar hasta fecha
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de Alert
        """
        pass

    @abstractmethod
    async def count(
        self,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
        type: str | None = None,
        status: str | None = None,
        scheduled_from: datetime | None = None,
        scheduled_to: datetime | None = None,
    ) -> int:
        """
        Cuenta alertas con filtros opcionales.

        Args:
            user_id: Filtrar por usuario
            farm_id: Filtrar por finca
            type: Filtrar por tipo
            status: Filtrar por estado
            scheduled_from: Filtrar desde fecha
            scheduled_to: Filtrar hasta fecha

        Returns:
            Número total de alertas que coinciden con los filtros
        """
        pass

    @abstractmethod
    async def delete(self, alert_id: UUID) -> bool:
        """
        Elimina una alerta.

        Args:
            alert_id: ID de la alerta

        Returns:
            True si se eliminó exitosamente
        """
        pass

    @abstractmethod
    async def find_pending(self, user_id: UUID | None = None) -> list[Alert]:
        """
        Busca alertas pendientes.

        Args:
            user_id: Filtrar por usuario (opcional)

        Returns:
            Lista de Alert pendientes
        """
        pass

    @abstractmethod
    async def find_scheduled(
        self, from_date: datetime, to_date: datetime
    ) -> list[Alert]:
        """
        Busca alertas programadas en un rango de fechas.

        Args:
            from_date: Fecha desde
            to_date: Fecha hasta

        Returns:
            Lista de Alert programadas
        """
        pass

    @abstractmethod
    async def find_today(
        self, user_id: UUID | None = None, farm_id: UUID | None = None
    ) -> list[Alert]:
        """
        Busca alertas programadas para el día de hoy.

        Args:
            user_id: Filtrar por usuario (opcional)
            farm_id: Filtrar por finca (opcional)

        Returns:
            Lista de Alert del día actual
        """
        pass

    @abstractmethod
    async def find_upcoming(
        self,
        days_ahead: int,
        user_id: UUID | None = None,
        farm_id: UUID | None = None,
    ) -> list[Alert]:
        """
        Busca alertas programadas para los próximos N días.

        Args:
            days_ahead: Número de días hacia adelante
            user_id: Filtrar por usuario (opcional)
            farm_id: Filtrar por finca (opcional)

        Returns:
            Lista de Alert próximas
        """
        pass
