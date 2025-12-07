from inertia import (
    Inertia,
    inertia_dependency_factory,
    InertiaConfig,
)
from typing import Annotated
from fastapi.templating import Jinja2Templates
import os
from fastapi import Depends
from .settings import settings
from pathlib import Path


template_dir = os.path.join(settings.BASE_DIR, "templates")
templates = Jinja2Templates(directory=template_dir)

manifest_json = (
    Path(settings.BASE_DIR).resolve().parent.parent  # equivalent of "../.."
    / "webapp"
    / "dist"
    / "manifest.json"
)




inertia_config = InertiaConfig(
    templates=templates,
    manifest_json_path=manifest_json,
    environment="development",
    use_flash_messages=True,
    use_flash_errors=True,
    entrypoint_filename="main.ts",
    assets_prefix="/src",
    version="2.0",
)
InertiaDep = Annotated[Inertia, Depends(inertia_dependency_factory(inertia_config))]
