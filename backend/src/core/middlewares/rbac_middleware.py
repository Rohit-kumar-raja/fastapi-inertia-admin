"""
RBAC Middleware — Checks permissions on every authenticated request.

This middleware intercepts all requests to protected routes and verifies
that the authenticated user has a permission matching the route's name.
SuperAdmin users (is_superuser=True) bypass all permission checks.

How it works:
1. Skips unauthenticated routes (login, static files, docs, etc.)
2. Extracts the JWT token from cookies or Authorization header
3. SuperAdmin check — if is_superuser, allow immediately
4. Matches the request to a FastAPI route and gets its name (e.g. 'admin.role.read')
5. Checks if the user has that permission in their role assignments
6. Returns 403 if the user lacks the required permission
"""

import jwt
from jwt.exceptions import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.routing import APIRoute

from ..config.settings import settings


# Paths that should never be permission-checked
SKIP_PATHS = {
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
}

# Path prefixes that should never be permission-checked
SKIP_PREFIXES = (
    "/admin/login",
    "/admin/notifications",
    "/admin/settings/profile",
    "/admin/settings/password",
    "/static",
    "/assets",
    "/api/v1/login",
    "/_inertia",
)

# Route names that should bypass permission checks (public routes)
SKIP_ROUTE_NAMES = {
    "user.login",
    "user.login.post",
}


class RBACMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces RBAC permissions on every request.
    Maps each request to its FastAPI route name and checks
    if the authenticated user has that permission.
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Skip paths that don't need permission checking
        if path in SKIP_PATHS or any(path.startswith(prefix) for prefix in SKIP_PREFIXES):
            return await call_next(request)

        # Skip non-API requests (GET requests for Inertia pages are handled by web_auth)
        # Only enforce RBAC on API mutation endpoints and admin API endpoints
        if request.method == "GET":
            # Allow GET requests through — read access is controlled at route level
            return await call_next(request)

        # Try to extract JWT token
        token = None
        token = request.cookies.get("access_token")
        if not token:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]

        if not token:
            # No token — let the auth dependency handle 401
            return await call_next(request)

        # Decode token
        try:
            payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[settings.APP_ALGORITHM])
        except InvalidTokenError:
            return await call_next(request)

        # SuperAdmin bypass — allow all requests
        if payload.get("is_superuser", False):
            # Store user in request state for downstream use
            request.state.user = {
                "id": payload.get("id"),
                "username": payload.get("sub"),
                "is_superuser": True,
            }
            return await call_next(request)

        # Find the matching route and its name
        route_name = None
        for route in request.app.routes:
            if isinstance(route, APIRoute):
                match, _ = route.matches(request.scope)
                if match.value == 2:  # FULL match
                    route_name = route.name
                    break

        if not route_name:
            # No named route found — allow through
            return await call_next(request)

        if route_name in SKIP_ROUTE_NAMES:
            return await call_next(request)

        # Check user permissions
        user_id = payload.get("id")
        if not user_id:
            return await call_next(request)

        # Store user in request state
        request.state.user = {
            "id": user_id,
            "username": payload.get("sub"),
            "is_superuser": False,
        }

        # Load user permissions and check
        from ..security.services.user_service import UserService
        from ..config.database import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            user_permissions = await UserService.get_user_permissions(user_id, session)

        if route_name not in user_permissions:
            return JSONResponse(
                status_code=403,
                content={
                    "message": f"Permission denied: '{route_name}' is required",
                    "detail": "You do not have permission to perform this action",
                },
            )

        return await call_next(request)
