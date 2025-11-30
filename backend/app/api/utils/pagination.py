"""
Pagination Utils - Utilidades para paginación
Funciones helper para calcular y manejar paginación en endpoints
"""


def calculate_pagination(skip: int, limit: int) -> dict[str, int]:
    """
    Calcula información de paginación.

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
