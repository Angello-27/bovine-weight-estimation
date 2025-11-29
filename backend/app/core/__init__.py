"""
Core Module
Configuración, excepciones e infraestructura compartida del sistema

Clean Architecture: Core contiene solo infraestructura técnica.
Las constantes del dominio están en domain/shared/constants/
"""

from .config import Settings, get_settings, settings
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
