"""
JWT Utilities
Utilidades para creación y decodificación de tokens JWT
"""

from datetime import datetime, timedelta
from uuid import UUID

from jose import (  # type: ignore  # No hay stubs oficiales para python-jose
    JWTError,
    jwt,
)

from ...schemas.auth_schemas import TokenData
from ..config import settings
from ..exceptions import AuthenticationException


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
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


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
                raise AuthenticationException("Token inválido: ID de usuario inválido")
        username: str | None = payload.get("username")
        if user_id is None or username is None:
            raise AuthenticationException("Token inválido: datos faltantes")
        return TokenData(user_id=user_id, username=username)
    except JWTError as e:
        raise AuthenticationException(f"Token inválido: {str(e)}")
