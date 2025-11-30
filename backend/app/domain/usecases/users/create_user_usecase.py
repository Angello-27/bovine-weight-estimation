"""
Create User Use Case - Domain Layer
Caso de uso para crear un usuario
"""

from uuid import UUID

from ....core.exceptions import AlreadyExistsException, NotFoundException
from ...entities.user import User
from ...repositories.role_repository import RoleRepository
from ...repositories.user_repository import UserRepository


class CreateUserUseCase:
    """
    Caso de uso para crear un usuario.

    Single Responsibility: Validar y crear un usuario en el dominio.
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
        username: str,
        email: str,
        hashed_password: str,
        role_id: UUID,
        farm_id: UUID | None = None,
    ) -> User:
        """
        Ejecuta el caso de uso para crear un usuario.

        Args:
            username: Nombre de usuario
            email: Email del usuario
            hashed_password: Contraseña hasheada
            role_id: ID del rol
            farm_id: ID de la finca (opcional)

        Returns:
            User creado

        Raises:
            AlreadyExistsException: Si el username o email ya existe
            NotFoundException: Si el rol no existe
        """
        # Validar que el username no exista
        existing_username = await self._user_repository.find_by_username(username)
        if existing_username is not None:
            raise AlreadyExistsException(
                resource="User", field="username", value=username
            )

        # Validar que el email no exista
        existing_email = await self._user_repository.find_by_email(email)
        if existing_email is not None:
            raise AlreadyExistsException(resource="User", field="email", value=email)

        # Validar que el rol exista
        role = await self._role_repository.get_by_id(role_id)
        if role is None:
            raise NotFoundException(resource="Role", field="id", value=str(role_id))

        # Crear entidad User
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role_id=role_id,
            farm_id=farm_id,
            is_active=True,
            is_superuser=False,
        )

        # Guardar usando el repositorio
        return await self._user_repository.save(user)
