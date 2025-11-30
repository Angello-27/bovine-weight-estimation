"""
Update User Use Case - Domain Layer
Caso de uso para actualizar un usuario
"""

from uuid import UUID

from ....core.exceptions import AlreadyExistsException, NotFoundException
from ...entities.user import User
from ...repositories.role_repository import RoleRepository
from ...repositories.user_repository import UserRepository


class UpdateUserUseCase:
    """
    Caso de uso para actualizar un usuario.

    Single Responsibility: Validar y actualizar un usuario en el dominio.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ):
        """
        Inicializa el caso de uso.

        Args:
            user_repository: Repositorio de usuarios
            role_repository: Repositorio de roles
        """
        self._user_repository = user_repository
        self._role_repository = role_repository

    async def execute(
        self,
        user_id: UUID,
        email: str | None = None,
        hashed_password: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        role_id: UUID | None = None,
        farm_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> User:
        """
        Ejecuta el caso de uso para actualizar un usuario.

        Args:
            user_id: ID del usuario
            email: Nuevo email (opcional)
            hashed_password: Nueva contraseña hasheada (opcional)
            first_name: Nuevo nombre (opcional)
            last_name: Nuevo apellido (opcional)
            role_id: Nuevo ID de rol (opcional)
            farm_id: Nuevo ID de finca (opcional)
            is_active: Nuevo estado activo (opcional)

        Returns:
            User actualizado

        Raises:
            NotFoundException: Si el usuario o rol no existe
            AlreadyExistsException: Si el email ya existe
        """
        # Obtener usuario existente
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(resource="User", field="id", value=str(user_id))

        # Validar email único si se está actualizando
        if email is not None and email != user.email:
            existing_email = await self._user_repository.find_by_email(email)
            if existing_email is not None:
                raise AlreadyExistsException(
                    resource="User", field="email", value=email
                )
            user.email = email

        # Actualizar contraseña si se proporciona
        if hashed_password is not None:
            user.hashed_password = hashed_password

        # Actualizar nombre si se proporciona
        if first_name is not None:
            user.first_name = first_name

        # Actualizar apellido si se proporciona
        if last_name is not None:
            user.last_name = last_name

        # Actualizar rol si se proporciona
        if role_id is not None:
            role = await self._role_repository.get_by_id(role_id)
            if role is None:
                raise NotFoundException(resource="Role", field="id", value=str(role_id))
            user.role_id = role_id

        # Actualizar finca si se proporciona
        if farm_id is not None:
            user.farm_id = farm_id

        # Actualizar estado activo si se proporciona
        if is_active is not None:
            user.is_active = is_active

        # Actualizar timestamp
        user.update_timestamp()

        # Guardar cambios
        return await self._user_repository.save(user)
