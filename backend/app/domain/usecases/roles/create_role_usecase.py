"""
Create Role Use Case - Domain Layer
Caso de uso para crear un rol
"""

from ....core.exceptions import AlreadyExistsException
from ...entities.role import Role
from ...repositories.role_repository import RoleRepository


class CreateRoleUseCase:
    """
    Caso de uso para crear un rol.

    Single Responsibility: Validar y crear un rol en el dominio.
    """

    def __init__(self, role_repository: RoleRepository):
        """
        Inicializa el caso de uso.

        Args:
            role_repository: Repositorio de roles
        """
        self._role_repository = role_repository

    async def execute(
        self,
        name: str,
        description: str | None = None,
        priority: str = "Invitado",
        permissions: list[str] | None = None,
    ) -> Role:
        """
        Ejecuta el caso de uso para crear un rol.

        Args:
            name: Nombre del rol
            description: Descripción del rol (opcional)
            priority: Prioridad del rol
            permissions: Lista de permisos (opcional)

        Returns:
            Role creado

        Raises:
            AlreadyExistsException: Si el nombre del rol ya existe
        """
        # Validar que el nombre no exista
        existing = await self._role_repository.find_by_name(name)
        if existing is not None:
            raise AlreadyExistsException(resource="Role", field="name", value=name)

        # Crear entidad Role
        role = Role(
            name=name,
            description=description,
            priority=priority,
            permissions=permissions or [],
        )

        # Guardar usando el repositorio
        return await self._role_repository.save(role)
