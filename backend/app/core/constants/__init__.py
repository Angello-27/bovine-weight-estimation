"""
Core Constants - Domain Constants
Constantes del dominio (NO MODIFICAR sin autorización Bruno Brito Macedo)
"""

from .age_categories import AGE_CATEGORY_RANGES, AgeCategory
from .breeds import BREED_DISPLAY_NAMES, BREED_MODEL_FILENAMES, BreedType
from .hacienda import HaciendaConstants
from .metrics import CaptureConstants, SystemMetrics

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
