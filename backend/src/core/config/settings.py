from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    STATIC_URL: str = "/static/"
    STATIC_DIR: Path = BASE_DIR / "static"
    DOCS_DIR: Path = STATIC_DIR / "docs"

    # ---------------- APP ----------------
    APP_ENV: str = Field(..., description="Environment mode (development/production)")
    APP_HOST: str = Field(..., description="Application host")
    APP_PORT: int = Field(..., description="Application port")
    APP_WORKERS: int = Field(..., description="Number of workers for the application")
    APP_SECRET_KEY: str = Field(..., description="Secret key for the application")
    APP_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    APP_ALLOWED_HOSTS: str = Field(..., description="Comma-separated allowed origins")
    APP_CONTAINER: str = Field(..., description="Container name")
    APP_NETWORK: str = Field(..., description="Network name")
    APP_LOG_PATH: Path = Field(..., description="Path to application log file")
    APP_LOG_LEVEL: str = Field(..., description="Log level for the application")
    APP_TIMEZONE: str = Field(..., description="timezone for the app")
    APP_LOG_VOLUME: str = Field(..., description="timezone for the app")
    APP_LANGUAGE_CODE: str = Field(..., description="language code for the app")
    APP_DATABASE_URL: str = Field(..., description="database url for the app")

    # ---------------- DATABASE ----------------
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_NAME: str = Field(..., description="Database name")
    DB_USER: str = Field(..., description="Database user")
    DB_PASSWORD: str = Field(..., description="Database password")
    DB_CONTAINER: str = Field(..., description="Database container name")
    DB_VOLUME: str = Field(..., description="Database volume")

    # ---------------- EMAIL ----------------
    SMTP_SERVER: str = Field(..., description="SMTP server")
    SMTP_PORT: int = Field(..., description="SMTP port")
    SMTP_USERNAME: str = Field(..., description="SMTP username")
    SMTP_PASSWORD: str = Field(..., description="SMTP password")
    SENDER_EMAIL: str = Field(..., description="Sender email")

    # ---------------- PGADMIN ----------------
    PGADMIN_DEFAULT_EMAIL: str = Field(..., description="PGAdmin default email")
    PGADMIN_DEFAULT_PASSWORD: str = Field(..., description="PGAdmin default password")
    PGADMIN_SERVER_PORT: int = Field(..., description="PGAdmin server port")
    PGADMIN_CONTAINER: str = Field(..., description="PGAdmin container")

    # ---------------- VAPID WEB PUSH ----------------
    VAPID_PUBLIC_KEY: str = Field(default="", description="VAPID public key for Web Push")
    VAPID_PRIVATE_KEY: str = Field(default="", description="VAPID private key for Web Push")
    VAPID_CLAIMS_EMAIL: str = Field(default="mailto:admin@example.com", description="VAPID contact email")


    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


def reload_settings() -> Settings:
    load_dotenv(override=True)
    return Settings()


settings = reload_settings()
