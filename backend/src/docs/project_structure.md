# Project Structure
```
i-tips-backend/                   # Root directory
├── .env.example                  # Environment variables example
├── .gitignore                    # Git ignore file
├── .vscode/                      # VSCode settings
├── docker-compose.yaml           # Docker compose file
├── Dockerfile                    # Dockerfile
├── pyproject.toml                # It holds the dependencies and can be installed using uv
├── README.md                     # Project documentation
├── src/                          # Source code
│   ├── alembic.ini               # It is used to manage the migrations
│   ├── apps/                     # Place for all apps here
│   │   └── admin/                # Admin app example
│   │       ├── models/           # database models
│   │       ├── routes/           # write your routes here
│   │       ├── schemas/          # for pydantic schemas which act as a validation and serializer
│   │       └── services/         # all the business logic should be here
│   ├── core/                     # Project related stuff
│   │   ├── config/               # holds the config for the project like database, redis, etc.
│   │   ├── middlewares/          # custom middlewares
│   │   └── security/             # all the security related stuff like  RBAC, etc.
│   ├── main.py                   # Main file of the project from where the app starts
│   ├── manage.py                 # CLI commands
│   ├── migrations/               # holds the migrations
│   ├── static/                   # holds the static files
│   └── tests/                    # Place project related tests or integration tests
└── uv.lock                       # dependency lock file
```