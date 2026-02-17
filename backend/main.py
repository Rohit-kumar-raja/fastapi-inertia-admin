import os
import asyncio

from pydantic import BaseModel, EmailStr

from fastapi import FastAPI,  Request
from fastapi.responses import JSONResponse
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
    inertia_config
)
from src.core.dependencies.inertia_dependency import InertiaDep
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors: dict = {}
    for err in exc.errors():
        field = err["loc"][-1]
        message = err["msg"]

        if field not in errors:
            errors[field] = []
        errors[field].append(message)

    return JSONResponse(
        status_code=422,
        content={"errors": errors, "message": "Validation error", "success": False},
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
