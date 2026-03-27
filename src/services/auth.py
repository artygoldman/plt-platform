"""JWT authentication service: create/verify tokens, password hashing."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import get_settings

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Raises:
        ValueError: If password is empty
    """
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain text password against a hashed password.

    Args:
        plain: Plain text password
        hashed: Hashed password to verify against

    Returns:
        True if password matches, False otherwise
    """
    try:
        return pwd_context.verify(plain, hashed)
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False


def create_access_token(
    user_id: str, expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token for a user.

    Args:
        user_id: User ID to encode in token
        expires_delta: Optional custom expiration time delta. If None, uses default from settings.

    Returns:
        Encoded JWT token string

    Raises:
        ValueError: If user_id is empty
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")

    settings = get_settings()

    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.jwt_expiration_minutes)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"user_id": user_id, "exp": expire}

    try:
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.jwt_algorithm
        )
        logger.info(f"Created access token for user: {user_id}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating access token: {e}")
        raise


def verify_token(token: str) -> Dict[str, str]:
    """Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Dictionary containing decoded token data: {"user_id": str}

    Raises:
        JWTError: If token is invalid, expired, or tampered with
        ValueError: If token is empty or user_id is missing from payload
    """
    if not token:
        raise ValueError("Token cannot be empty")

    settings = get_settings()

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        user_id = payload.get("user_id")

        if not user_id:
            raise ValueError("user_id not found in token payload")

        logger.debug(f"Token verified successfully for user: {user_id}")
        return {"user_id": user_id}

    except JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {e}")
        raise
