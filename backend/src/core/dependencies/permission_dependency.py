from typing import List
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .auth_dependency import api_auth, web_auth
from .db_dependency import get_db
from ..security.services.user_service import UserService


def require_permission(*permissions: str):
    """
    FastAPI dependency factory that checks if the current user has the required permission(s).

    Usage:
        @router.get("/users", dependencies=[Depends(require_permission("admin.user.read"))])
        async def list_users():
            ...

    SuperAdmin bypass: Users with is_superuser=True bypass all permission checks.
    """

    async def _check_permission(
        request: Request,
        session: AsyncSession = Depends(get_db),
    ):
        # Extract user info from request state (set by web_auth/api_auth middleware)
        user = getattr(request.state, "user", None)
        if user is None:
            # Try to extract from web_auth or api_auth
            try:
                token = request.cookies.get("access_token")
                if token:
                    from ..security.utils.auth import decode_token
                    payload = decode_token(token)
                    if payload:
                        user = {
                            "id": payload.get("id") or payload.get("sub"),
                            "username": payload.get("sub") or payload.get("username"),
                            "is_superuser": payload.get("is_superuser", False),
                        }
                else:
                    # Try Bearer token from Authorization header
                    auth_header = request.headers.get("Authorization", "")
                    if auth_header.startswith("Bearer "):
                        from ..security.utils.auth import decode_token
                        payload = decode_token(auth_header[7:])
                        if payload:
                            user = {
                                "id": payload.get("id") or payload.get("sub"),
                                "username": payload.get("sub") or payload.get("username"),
                                "is_superuser": payload.get("is_superuser", False),
                            }
            except Exception:
                pass

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )

        # SuperAdmin bypass — superusers can access everything
        if user.get("is_superuser", False):
            return user

        # Load user permissions
        user_id = user.get("id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user",
            )

        user_permissions = await UserService.get_user_permissions(user_id, session)

        # Check all required permissions
        missing = [p for p in permissions if p not in user_permissions]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {', '.join(missing)}",
            )

        return user

    return _check_permission
