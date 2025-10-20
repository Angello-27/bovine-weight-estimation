"""
Core Constants - Domain Constants
Constantes del dominio (NO MODIFICAR sin autorización Bruno Brito Macedo)
"""

from .breeds import BreedType, BREED_DISPLAY_NAMES, BREED_MODEL_FILENAMES
from .age_categories import AgeCategory, AGE_CATEGORY_RANGES
from .metrics import SystemMetrics, CaptureConstants
from .hacienda import HaciendaConstants

__all__ = [
    "BreedType",
    "BREED_DISPLAY_NAMES",
    "BREED_MODEL_FILENAMES",
    "AgeCategory",
    "AGE_CATEGORY_RANGES",
    "SystemMetrics",
    "CaptureConstants",
    "HaciendaConstants",
]

