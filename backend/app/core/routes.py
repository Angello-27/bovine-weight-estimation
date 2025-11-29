"""
Routes Configuration
Configuración y registro de todas las rutas de la API
"""

from fastapi import FastAPI

from app.api.routes import (
    alert_router,
    animals_router,
    auth_router,
    farm_router,
    ml_router,
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
