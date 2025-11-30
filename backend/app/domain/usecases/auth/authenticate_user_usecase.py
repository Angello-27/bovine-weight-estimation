"""
Authenticate User Use Case - Domain Layer
Caso de uso para autenticar un usuario
"""

from collections.abc import Callable

from ....core.exceptions import AuthenticationException, NotFoundException
from ...entities.role import Role
from ...entities.user import User
from ...repositories.role_repository import RoleRepository
from ...repositories.user_repository import UserRepository


class AuthenticateUserUseCase:
    """
    Caso de uso para autenticar un usuario.

    Single Responsibility: Validar credenciales y autenticar usuario.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        password_verifier: Callable[[str, str], bool],
    ):
        """
        Inicializa el caso de uso.

        Args:
            user_repository: Repositorio de usuarios
            role_repository: Repositorio de roles
            password_verifier: Función para verificar contraseña (verify_password)
        """
        self._user_repository = user_repository
        self._role_repository = role_repository
        self._password_verifier = password_verifier

    async def execute(
        self,
        username: str,
        password: str,
    ) -> tuple[User, Role]:
        """
        Ejecuta el caso de uso para autenticar un usuario.

        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano

        Returns:
            Tupla (User, Role) del usuario autenticado

        Raises:
            AuthenticationException: Si las credenciales son inválidas
            NotFoundException: Si el rol no existe
        """
        # Buscar usuario por username
        user = await self._user_repository.find_by_username(username)
        if user is None:
            raise AuthenticationException("Usuario o contraseña incorrectos")

        # Verificar contraseña
        if not self._password_verifier(password, user.hashed_password):
            raise AuthenticationException("Usuario o contraseña incorrectos")

        # Verificar que el usuario esté activo
        if not user.is_active:
            raise AuthenticationException("Usuario inactivo")

        # Obtener rol del usuario
        if user.role_id is None:
            raise NotFoundException(resource="User", field="role_id", value="None")
        role = await self._role_repository.get_by_id(user.role_id)
        if role is None:
            raise NotFoundException(
                resource="Role", field="id", value=str(user.role_id)
            )

        # Actualizar último login
        user.update_last_login()
        await self._user_repository.save(user)

        return user, role
