from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from ..config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def api_auth(token: str = Depends(oauth2_scheme)):
    """Extract user info from JWT token without querying the database."""
    try:


        payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[settings.APP_ALGORITHM])
        user_id = payload.get("sub")
        username = payload.get("username")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

        return {"id": user_id, "username": username}  # Return user info from token instead of DB

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def web_auth(request: Request):
    """Extract user info from JWT token without querying the database."""
    try:
        token = request.cookies.get("access_token")
        payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[settings.APP_ALGORITHM])
        user_id = payload.get("sub")
        username = payload.get("username")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

        return {"id": user_id, "username": username}  # Return user info from token instead of DB

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")
