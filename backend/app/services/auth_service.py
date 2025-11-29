"""
Auth Service - Business Logic
Lógica de negocio para autenticación y autorización
"""

from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from ..core.config import settings
from ..core.exceptions import AuthenticationException, NotFoundException
from ..models import RoleModel, UserModel
from ..schemas.auth_schemas import LoginRequest, LoginResponse, TokenData

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Servicio de autenticación y autorización.

    Single Responsibility: Business logic de autenticación.
    Maneja JWT tokens y verificación de contraseñas.
    """

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
        # Buscar usuario por username
        user = await UserModel.find_one(UserModel.username == login_data.username)

        if user is None:
            raise AuthenticationException("Usuario o contraseña incorrectos")

        # Verificar contraseña
        if not self.verify_password(login_data.password, user.hashed_password):
            raise AuthenticationException("Usuario o contraseña incorrectos")

        # Verificar que el usuario esté activo
        if not user.is_active:
            raise AuthenticationException("Usuario inactivo")

        # Obtener rol del usuario
        role = await RoleModel.find_one(RoleModel.id == user.role_id)
        if role is None:
            raise NotFoundException(
                resource="Role", field="id", value=str(user.role_id)
            )

        # Actualizar último login
        user.update_last_login()
        await user.save()

        # Crear token JWT
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires,
        )

        return LoginResponse(
            id=user.id,
            username=user.username,
            role=role.name,
            role_id=role.id,
            access_token=access_token,
            token_type="bearer",
        )
