from ..config.inertia import inertia_config
from inertia import (
    Inertia,
    inertia_dependency_factory,
)
from typing import Annotated
from fastapi import Depends

InertiaDep = Annotated[Inertia, Depends(inertia_dependency_factory(inertia_config))]
