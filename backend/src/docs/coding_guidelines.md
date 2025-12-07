# Coding Guidelines

- App name service singular. Try to put one word name, but if have multiple words, use camel case.
Example: `user_service`, `admin`

- Directory inside app should be plural.
Example: `models`, `schemas`, `routes`, `services`

- Every folder should have `__init__.py` file.

- Every `__init__.py` file should have its sub-folders imports.
Example:
```python
from . import models
from . import schemas
from . import routes
from . import services
```

- Use `snake_case` for file names in below format:
```
<name>_service.py
<name>_schemas.py
<name>_routes.py
<name>_services.py
```

- classes should be the same as the file name but in `PascalCase`
Example: `UserService`, `AdminService`

- Every Classes should be written in separate file.

- Every python file imports should be in the below order:
1. Standard library imports
2. Third party imports
3. Local application imports
Example:
```python
from datetime import datetime
from fastapi import APIRouter
from app.core.config import settings
```

- Write all the function in async way unless specified otherwise.

- Allowed folders to create in any apps:
    - `models`           # for database models
    - `schemas`          # for pydantic schemas which act as a validation and serializer
    - `routes`           # write your routes here
    - `services`         # all the business logic should be here
    - `tests`            # Place project related tests or integration tests
    - `utils`            # holds the utility functions
    - `dependencies`     # holds the dependencies
    - `base`             # holds the base classes
    - `exceptions`       # holds the custom exceptions
    - `tasks`            # holds the tasks
    - `handlers`         # holds the handlers
    - `seeders`          # holds the seeders
    - `static`           # holds the static files
    - `templates`        # holds the templates using jinja2
