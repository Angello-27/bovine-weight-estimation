"""
API Routes Module
Routers de FastAPI por dominio
"""

from .animals import router as animals_router
from .ml import router as ml_router
from .sync import router as sync_router
from .weighings import router as weighings_router

__all__ = [
    "animals_router",
    "weighings_router",
    "sync_router",
    "ml_router",
]
