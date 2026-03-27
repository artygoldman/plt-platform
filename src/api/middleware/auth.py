"""FastAPI auth middleware: extracts and validates JWT from Authorization header."""

import logging
from typing import Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.services.auth import verify_token

logger = logging.getLogger(__name__)

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, str]:
    """Dependency that extracts and validates JWT token from Authorization header.

    This function is used as a FastAPI dependency in protected routes to ensure
    the request includes a valid JWT token. Automatically extracts the token from
    the Authorization: Bearer <token> header.

    Args:
        credentials: HTTPAuthorizationCredentials from FastAPI security scheme,
                    automatically extracted from the Authorization header.

    Returns:
        Dictionary with decoded token data: {"user_id": str}

    Raises:
        HTTPException: 403 Forbidden if token is invalid, expired, or malformed.
                      401 Unauthorized if Authorization header is missing (handled by HTTPBearer)

    Example:
        @router.get("/api/v1/profile")
        async def get_profile(current_user = Depends(get_current_user)):
            user_id = current_user["user_id"]
            # fetch user data
            return user_data
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            logger.warning("Token payload missing user_id")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token: missing user_id",
            )

        logger.debug(f"User authenticated: {user_id}")
        return payload

    except ValueError as e:
        logger.warning(f"Token validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token",
        )
    except Exception as e:
        logger.error(f"Unexpected error validating token: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token validation failed",
        )
