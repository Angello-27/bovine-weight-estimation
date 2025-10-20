"""
Custom Exceptions
Excepciones personalizadas del dominio
"""


class DomainException(Exception):
    """Excepción base del dominio."""

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code or "DOMAIN_ERROR"
        super().__init__(self.message)


class ValidationException(DomainException):
    """Excepción de validación de datos."""

    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class NotFoundException(DomainException):
    """Excepción cuando un recurso no se encuentra."""

    def __init__(self, resource: str, identifier: str):
        message = f"{resource} con ID '{identifier}' no encontrado"
        super().__init__(message, code="NOT_FOUND")
        self.resource = resource
        self.identifier = identifier


class AlreadyExistsException(DomainException):
    """Excepción cuando un recurso ya existe."""

    def __init__(self, resource: str, field: str, value: str):
        message = f"{resource} con {field}='{value}' ya existe"
        super().__init__(message, code="ALREADY_EXISTS")
        self.resource = resource
        self.field = field
        self.value = value


class DatabaseException(DomainException):
    """Excepción de base de datos."""

    def __init__(self, message: str, original_error: Exception | None = None):
        super().__init__(message, code="DATABASE_ERROR")
        self.original_error = original_error


class MLModelException(DomainException):
    """Excepción relacionada con modelos ML."""

    def __init__(self, message: str):
        super().__init__(message, code="ML_MODEL_ERROR")


class SyncConflictException(DomainException):
    """Excepción de conflicto en sincronización."""

    def __init__(
        self, resource: str, item_id: str, server_timestamp: str, client_timestamp: str
    ):
        message = (
            f"Conflicto de sincronización en {resource} ID '{item_id}': "
            f"Server={server_timestamp}, Client={client_timestamp}"
        )
        super().__init__(message, code="SYNC_CONFLICT")
        self.resource = resource
        self.item_id = item_id
        self.server_timestamp = server_timestamp
        self.client_timestamp = client_timestamp
