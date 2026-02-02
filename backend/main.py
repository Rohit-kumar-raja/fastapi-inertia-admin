import os
import asyncio

from pydantic import BaseModel, EmailStr

from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from inertia import (
    InertiaResponse,
    inertia_version_conflict_exception_handler,
    inertia_request_validation_exception_handler,
    InertiaVersionConflictException,
    lazy,
    defer,
)
from src.core.config.inertia import (
    inertia_config,
    InertiaDep,
)
from src.apps.admin.routes import admin_router
from src.core.security.routers import security_router


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
app.add_exception_handler(
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    RequestValidationError,
    inertia_request_validation_exception_handler,  # type: ignore[arg-type]
)


vue_dir = (
    os.path.join(os.path.dirname(__file__), "..", "webapp", "dist")
    if inertia_config.environment != "development"
    else os.path.join(os.path.dirname(__file__), "..", "webapp", "src")
)

app.mount("/src", StaticFiles(directory=vue_dir), name="src")
app.mount(
    "/assets", StaticFiles(directory=os.path.join(vue_dir, "assets")), name="assets"
)




class UserLogin(BaseModel):
    email: EmailStr
    password: str


@app.get("/login", response_model=None)
async def login_page(inertia: InertiaDep) -> InertiaResponse:
    return await inertia.render("Login")



app.include_router(admin_router)
app.include_router(security_router)
