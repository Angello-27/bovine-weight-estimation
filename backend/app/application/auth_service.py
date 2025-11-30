"""
Auth Service - Business Logic (Refactorizado para Clean Architecture)
Orquesta casos de uso de autenticación
"""

from datetime import timedelta

from jose import (  # type: ignore  # No hay stubs oficiales para python-jose
    JWTError,
    jwt,
)
from passlib.context import CryptContext

from ..api.mappers import AuthMapper
from ..core.config import settings
from ..core.exceptions import AuthenticationException
from ..data.repositories.role_repository_impl import RoleRepositoryImpl
from ..data.repositories.user_repository_impl import UserRepositoryImpl
from ..domain.repositories.role_repository import RoleRepository
from ..domain.repositories.user_repository import UserRepository
from ..domain.usecases.auth import (
    AuthenticateUserUseCase,
    GetUserByTokenUseCase,
)
from ..schemas.auth_schemas import LoginRequest, LoginResponse, TokenData

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Servicio de autenticación y autorización (refactorizado).

    Single Responsibility: Orquestar casos de uso de autenticación y manejar JWT.
    Ahora usa Clean Architecture con Use Cases.
    """

    def __init__(
        self,
        user_repository: UserRepository | None = None,
        role_repository: RoleRepository | None = None,
    ):
        """
        Inicializa el servicio.

        Args:
            user_repository: Repositorio de usuarios (inyección de dependencia)
            role_repository: Repositorio de roles (inyección de dependencia)
        """
        self._user_repository = user_repository or UserRepositoryImpl()
        self._role_repository = role_repository or RoleRepositoryImpl()

        # Inicializar use cases
        self._authenticate_usecase = AuthenticateUserUseCase(
            user_repository=self._user_repository,
            role_repository=self._role_repository,
            password_verifier=self.verify_password,
        )
        self._get_user_by_token_usecase = GetUserByTokenUseCase(
            user_repository=self._user_repository
        )

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica una contraseña contra su hash.

        Args:
            plain_password: Contraseña en texto plano
            hashed_password: Contraseña hasheada

        Returns:
            True si la contraseña es correcta
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Genera hash de una contraseña.

        Args:
            password: Contraseña en texto plano

        Returns:
            Hash de la contraseña
        """
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Crea un token JWT.

        Args:
            data: Datos a incluir en el token
            expires_delta: Tiempo de expiración (opcional)

        Returns:
            Token JWT como string
        """
        from datetime import datetime

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_access_token(token: str) -> TokenData:
        """
        Decodifica y valida un token JWT.

        Args:
            token: Token JWT

        Returns:
            TokenData con información del usuario

        Raises:
            AuthenticationException: Si el token es inválido
        """
        from uuid import UUID

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            sub = payload.get("sub")
            user_id: UUID | None = None
            if sub:
                try:
                    user_id = UUID(sub)
                except (ValueError, TypeError):
                    raise AuthenticationException(
                        "Token inválido: ID de usuario inválido"
                    )
            username: str | None = payload.get("username")
            if user_id is None or username is None:
                raise AuthenticationException("Token inválido: datos faltantes")
            return TokenData(user_id=user_id, username=username)
        except JWTError as e:
            raise AuthenticationException(f"Token inválido: {str(e)}")

    async def authenticate_user(self, login_data: LoginRequest) -> LoginResponse:
        """
        Autentica un usuario y retorna token JWT.

        Args:
            login_data: Credenciales de login

        Returns:
            LoginResponse con token y datos del usuario

        Raises:
            AuthenticationException: Si las credenciales son inválidas
        """
        # Usar use case para autenticar
        user, role = await self._authenticate_usecase.execute(
            username=login_data.username,
            password=login_data.password,
        )

        # Crear token JWT
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires,
        )

        # Usar mapper para convertir a LoginResponse
        return AuthMapper.to_login_response(user, role, access_token)

    async def get_user_from_token(self, token: str):
        """
        Obtiene un usuario desde un token JWT.

        Args:
            token: Token JWT

        Returns:
            User entity del dominio

        Raises:
            AuthenticationException: Si el token es inválido o el usuario no existe
        """
        # Decodificar token
        token_data = self.decode_access_token(token)

        if token_data.user_id is None:
            raise AuthenticationException("Token inválido: ID de usuario faltante")

        # Usar use case para obtener usuario
        return await self._get_user_by_token_usecase.execute(token_data.user_id)
