# from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# from ..utils import error_response
from ..utils.auth import decode_token, set_request_context

# from ..utils.auth import reset_request_context
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class Auth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(Auth, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        set_request_context(request)  # Set global request
        credentials: HTTPAuthorizationCredentials = await super(Auth, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            payload = decode_token(credentials.credentials)  # Assume this returns user data or None
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token.",
                )

            # Store the user payload in request state
            request.state.user = payload  # Attach user to request state

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )
