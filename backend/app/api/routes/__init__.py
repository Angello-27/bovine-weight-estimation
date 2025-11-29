"""
API Routes Module
Routers de FastAPI por dominio
"""

from .alert import alert_router
from .animals import router as animals_router
from .auth import router as auth_router
from .farm import router as farm_router
from .ml import router as ml_router
from .role import router as role_router
from .sync import router as sync_router
from .user import router as user_router
from .weighings import router as weighings_router

__all__ = [
    "alert_router",
    "animals_router",
    "weighings_router",
    "sync_router",
    "ml_router",
]
