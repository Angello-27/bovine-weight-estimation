"""
Get Users By Criteria Use Case - Domain Layer
Caso de uso para obtener usuarios por criterios de filtrado
"""

from uuid import UUID

from ...entities.user import User
from ...repositories.user_repository import UserRepository


class GetUsersByCriteriaUseCase:
    """
    Caso de uso para obtener usuarios por criterios de filtrado.

    Single Responsibility: Listar usuarios del dominio con filtros específicos.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso.

        Args:
            user_repository: Repositorio de usuarios
        """
        self._user_repository = user_repository

    async def execute(
        self, filters: dict, skip: int = 0, limit: int = 50
    ) -> tuple[list[User], int]:
        """
        Ejecuta el caso de uso para obtener usuarios por criterios.

        Args:
            filters: Diccionario con criterios de filtrado
                     Ejemplos:
                     - {"role_id": UUID(...)}: Filtrar por rol
                     - {"is_active": True}: Filtrar por estado activo
                     - {"role_id": UUID(...), "is_active": True}: Combinar filtros
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Tupla con (lista de User que coinciden con los criterios, total de registros)
        """
        users = await self._user_repository.find_by_criteria(
            filters=filters, skip=skip, limit=limit
        )
        total = await self._user_repository.count_by_criteria(filters=filters)
        return users, total
