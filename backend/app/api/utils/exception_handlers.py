"""
Exception Handlers - Manejo de excepciones para routes
Decorators y funciones para convertir excepciones del dominio a HTTP
"""

from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from fastapi import HTTPException, status

from app.core.exceptions import (
    AlreadyExistsException,
    MLModelException,
    NotFoundException,
    ValidationException,
)

T = TypeVar("T")


def handle_domain_exceptions(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[T]]:
    """
    Decorator para manejar excepciones del dominio y convertirlas a HTTP.

    Convierte:
    - NotFoundException → HTTP 404
    - AlreadyExistsException → HTTP 400
    - ValidationException → HTTP 400
    - MLModelException → HTTP 500
    - ValueError → HTTP 400

    Args:
        func: Función async del endpoint

    Returns:
        Función decorada con manejo de excepciones

    Example:
        ```python
        @handle_domain_exceptions
        async def create_user(...):
            # Si lanza NotFoundException → HTTP 404 automáticamente
            # Si lanza AlreadyExistsException → HTTP 400 automáticamente
            return result
        ```
    """

    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)
        except NotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except AlreadyExistsException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except ValidationException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except MLModelException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en modelo ML: {e.message}",
            )
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return wrapper
