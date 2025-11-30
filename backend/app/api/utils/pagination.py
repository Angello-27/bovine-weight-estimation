"""
Pagination Utils - Utilidades para paginación
Funciones helper para calcular y manejar paginación en endpoints
"""


def calculate_skip(page: int, page_size: int) -> int:
    """
    Calcula el número de registros a saltar (skip) desde page y page_size.

    Args:
        page: Número de página (empieza en 1)
        page_size: Tamaño de página

    Returns:
        Número de registros a saltar

    Example:
        ```python
        skip = calculate_skip(page=2, page_size=20)
        # Returns: 20 (salta los primeros 20 registros)
        ```
    """
    return (page - 1) * page_size if page > 0 and page_size > 0 else 0


def calculate_pagination(skip: int, limit: int) -> dict[str, int]:
    """
    Calcula información de paginación desde skip y limit.

    Args:
        skip: Número de registros a saltar
        limit: Tamaño de página

    Returns:
        Dict con page, page_size

    Example:
        ```python
        pagination = calculate_pagination(skip=10, limit=20)
        # Returns: {"page": 1, "page_size": 20}
        ```
    """
    return {
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
    }
