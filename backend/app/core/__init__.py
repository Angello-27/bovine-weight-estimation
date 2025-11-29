"""
Core Module
Configuración, constantes y utilidades core del sistema
"""

from .config import Settings, get_settings, settings
from .constants import (
    AGE_CATEGORY_RANGES,
    BREED_DISPLAY_NAMES,
    BREED_MODEL_FILENAMES,
    AgeCategory,
    BreedType,
    CaptureConstants,
    HaciendaConstants,
    SystemMetrics,
)
from .exceptions import (
    AlreadyExistsException,
    AuthenticationException,
    DatabaseException,
    DomainException,
    MLModelException,
    NotFoundException,
    SyncConflictException,
    ValidationException,
)

__all__ = [
    # Config
    "Settings",
    "get_settings",
    "settings",
    # Constants
    "BreedType",
    "BREED_DISPLAY_NAMES",
    "BREED_MODEL_FILENAMES",
    "AgeCategory",
    "AGE_CATEGORY_RANGES",
    "SystemMetrics",
    "CaptureConstants",
    "HaciendaConstants",
    # Exceptions
    "DomainException",
    "ValidationException",
    "NotFoundException",
    "AlreadyExistsException",
    "AuthenticationException",
    "DatabaseException",
    "MLModelException",
    "SyncConflictException",
]
