"""
Alert Use Cases Dependencies
Dependencias para inyectar use cases de alertas
"""

from typing import Annotated

from fastapi import Depends

from app.domain.repositories.alert_repository import AlertRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.usecases.alerts import (
    CreateAlertUseCase,
    DeleteAlertUseCase,
    GetAlertByIdUseCase,
    GetPendingAlertsUseCase,
    GetScheduledAlertsUseCase,
    GetTodayAlertsUseCase,
    GetUpcomingAlertsUseCase,
    ListAlertsUseCase,
    MarkAlertAsCompletedUseCase,
    MarkAlertAsReadUseCase,
    UpdateAlertUseCase,
)

from .repositories import get_alert_repository, get_user_repository


def get_create_alert_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> CreateAlertUseCase:
    """Dependency para CreateAlertUseCase."""
    return CreateAlertUseCase(
        alert_repository=alert_repository, user_repository=user_repository
    )


def get_get_alert_by_id_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> GetAlertByIdUseCase:
    """Dependency para GetAlertByIdUseCase."""
    return GetAlertByIdUseCase(alert_repository=alert_repository)


def get_list_alerts_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> ListAlertsUseCase:
    """Dependency para ListAlertsUseCase."""
    return ListAlertsUseCase(alert_repository=alert_repository)


def get_update_alert_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> UpdateAlertUseCase:
    """Dependency para UpdateAlertUseCase."""
    return UpdateAlertUseCase(alert_repository=alert_repository)


def get_delete_alert_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> DeleteAlertUseCase:
    """Dependency para DeleteAlertUseCase."""
    return DeleteAlertUseCase(alert_repository=alert_repository)


def get_mark_alert_as_read_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> MarkAlertAsReadUseCase:
    """Dependency para MarkAlertAsReadUseCase."""
    return MarkAlertAsReadUseCase(alert_repository=alert_repository)


def get_mark_alert_as_completed_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> MarkAlertAsCompletedUseCase:
    """Dependency para MarkAlertAsCompletedUseCase."""
    return MarkAlertAsCompletedUseCase(alert_repository=alert_repository)


def get_get_pending_alerts_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> GetPendingAlertsUseCase:
    """Dependency para GetPendingAlertsUseCase."""
    return GetPendingAlertsUseCase(alert_repository=alert_repository)


def get_get_scheduled_alerts_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> GetScheduledAlertsUseCase:
    """Dependency para GetScheduledAlertsUseCase."""
    return GetScheduledAlertsUseCase(alert_repository=alert_repository)


def get_get_today_alerts_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> GetTodayAlertsUseCase:
    """Dependency para GetTodayAlertsUseCase."""
    return GetTodayAlertsUseCase(alert_repository=alert_repository)


def get_get_upcoming_alerts_usecase(
    alert_repository: Annotated[AlertRepository, Depends(get_alert_repository)],
) -> GetUpcomingAlertsUseCase:
    """Dependency para GetUpcomingAlertsUseCase."""
    return GetUpcomingAlertsUseCase(alert_repository=alert_repository)
