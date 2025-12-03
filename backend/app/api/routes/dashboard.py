"""
Dashboard Routes - API Endpoints
Endpoints REST para estadísticas del dashboard
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from ...core.dependencies import get_current_active_user
from ...core.dependencies.dashboard import get_get_dashboard_stats_usecase
from ...domain.entities.user import User
from ...domain.usecases.dashboard import GetDashboardStatsUseCase
from ...schemas.dashboard_schemas import DashboardStatsResponse
from ..utils import handle_domain_exceptions

# Router con prefijo /api/v1/dashboard
router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"],
    responses={
        401: {"description": "No autenticado"},
        403: {"description": "Sin permisos"},
        500: {"description": "Error interno del servidor"},
    },
)


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener estadísticas del dashboard",
    description="""
    Obtiene estadísticas agregadas del dashboard para la finca del usuario autenticado.

    **Estadísticas incluidas**:
    - totalCattle: Total de animales en la finca
    - averageWeight: Peso promedio (kg) de las estimaciones más recientes
    - totalBreeds: Número de razas diferentes
    - totalEstimations: Total de estimaciones de peso

    **Permisos**: Requiere autenticación
    """,
)
@handle_domain_exceptions
async def get_dashboard_stats(
    current_user: Annotated[User, Depends(get_current_active_user)],
    get_stats_usecase: Annotated[
        GetDashboardStatsUseCase, Depends(get_get_dashboard_stats_usecase)
    ],
) -> DashboardStatsResponse:
    """
    Endpoint para obtener estadísticas del dashboard.

    Args:
        current_user: Usuario autenticado (inyectado)
        get_stats_usecase: Caso de uso para obtener estadísticas (inyectado)

    Returns:
        DashboardStatsResponse con estadísticas del dashboard

    Raises:
        HTTPException 401: Si el usuario no está autenticado
        HTTPException 400: Si el usuario no tiene farm_id asignado
    """
    # Verificar que el usuario tenga farm_id
    if not current_user.farm_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no tiene una finca asignada",
        )

    # Obtener estadísticas usando el use case
    stats = await get_stats_usecase.execute(farm_id=current_user.farm_id)

    return DashboardStatsResponse(**stats)
