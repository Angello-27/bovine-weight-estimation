"""
Update Role Use Case - Domain Layer
Caso de uso para actualizar un rol
"""

from uuid import UUID

from ....core.exceptions import AlreadyExistsException, NotFoundException
from ...entities.role import Role
from ...repositories.role_repository import RoleRepository


class UpdateRoleUseCase:
    """
    Caso de uso para actualizar un rol.

    Single Responsibility: Validar y actualizar un rol en el dominio.
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
        role_id: UUID,
        name: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        permissions: list[str] | None = None,
    ) -> Role:
        """
        Ejecuta el caso de uso para actualizar un rol.

        Args:
            role_id: ID del rol
            name: Nuevo nombre (opcional)
            description: Nueva descripción (opcional)
            priority: Nueva prioridad (opcional)
            permissions: Nueva lista de permisos (opcional)

        Returns:
            Role actualizado

        Raises:
            NotFoundException: Si el rol no existe
            AlreadyExistsException: Si el nombre ya existe
        """
        # Obtener rol existente
        role = await self._role_repository.get_by_id(role_id)
        if role is None:
            raise NotFoundException(resource="Role", field="id", value=str(role_id))

        # Validar nombre único si se está actualizando
        if name is not None and name != role.name:
            existing = await self._role_repository.find_by_name(name)
            if existing is not None:
                raise AlreadyExistsException(resource="Role", field="name", value=name)
            role.name = name

        # Actualizar otros campos
        if description is not None:
            role.description = description
        if priority is not None:
            role.priority = priority
        if permissions is not None:
            role.permissions = permissions

        # Actualizar timestamp
        role.update_timestamp()

        # Guardar cambios
        return await self._role_repository.save(role)
