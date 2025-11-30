"""
API Utils - Utilidades para routes
Funciones helper y utilidades comunes para endpoints
"""

from .exception_handlers import handle_domain_exceptions
from .pagination import calculate_pagination, calculate_skip

__all__ = [
    "handle_domain_exceptions",
    "calculate_pagination",
    "calculate_skip",
]
