from fastapi import APIRouter, Depends

from .permission_router import permission_router
from .role_router import role_router
from .user_router import user_router
from .user_auth_router import auth_router
from ...dependencies.auth_dependency import web_auth

security_router = APIRouter(prefix="/admin")
security_router.include_router(permission_router, dependencies=[Depends(web_auth)])
security_router.include_router(role_router, dependencies=[Depends(web_auth)])
security_router.include_router(user_router, dependencies=[Depends(web_auth)])
security_router.include_router(auth_router)
