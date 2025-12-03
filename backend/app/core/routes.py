"""
Routes Configuration
Configuración y registro de todas las rutas de la API
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import (
    alert_router,
    animals_router,
    auth_router,
    dashboard_router,
    farm_router,
    ml_router,
    reports_router,
    resources_router,
    role_router,
    sync_router,
    user_router,
    weighings_router,
)


def setup_routes(app: FastAPI) -> None:
    """
    Registra todas las rutas de la API en la aplicación FastAPI.

    Args:
        app: Instancia de FastAPI
    """
    # Montar archivos estáticos para servir imágenes
    # Obtener el directorio base del proyecto (subir 2 niveles desde este archivo)
    # backend/app/core/routes.py -> backend/uploads
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent
    uploads_dir = project_root / "uploads"

    # Crear directorio si no existe
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # Montar directorio de uploads como archivos estáticos
    app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

    # Include Routers (separados por dominio)
    app.include_router(auth_router)  # Autenticación y autorización
    app.include_router(user_router)  # Gestión de usuarios
    app.include_router(role_router)  # Gestión de roles
    app.include_router(farm_router)  # Gestión de fincas
    app.include_router(animals_router)  # US-003: Registro de Animales
    app.include_router(weighings_router)  # US-002/US-004: Estimación y Historial
    app.include_router(ml_router)  # US-002: Inferencia ML (Core del proyecto)
    app.include_router(sync_router)  # US-005: Sincronización Offline
    app.include_router(alert_router)  # Alertas y cronograma
    app.include_router(reports_router)  # Reportes (PDF, CSV, Excel)
    app.include_router(resources_router)  # Recursos estáticos (imágenes)
    app.include_router(dashboard_router)  # Dashboard y estadísticas
