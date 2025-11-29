"""
Domain Constants - Reglas de Negocio
Constantes del dominio (NO MODIFICAR sin autorización Bruno Brito Macedo)

Estas constantes representan reglas de negocio puras:
- Razas bovinas válidas (7 exactas)
- Categorías de edad (4 exactas)
- Métricas del sistema (objetivos críticos)
- Información de Hacienda Gamelera
"""

from .age_categories import AGE_CATEGORY_RANGES, AgeCategory
from .breeds import BREED_DISPLAY_NAMES, BREED_MODEL_FILENAMES, BreedType
from .hacienda import HaciendaConstants
from .metrics import CaptureConstants, SystemMetrics, WeightConstants

__all__ = [
    "BreedType",
    "BREED_DISPLAY_NAMES",
    "BREED_MODEL_FILENAMES",
    "AgeCategory",
    "AGE_CATEGORY_RANGES",
    "SystemMetrics",
    "CaptureConstants",
    "WeightConstants",
    "HaciendaConstants",
]
