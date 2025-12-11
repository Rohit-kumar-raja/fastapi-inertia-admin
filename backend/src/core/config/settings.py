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

    # ---------------- REDIS ----------------
    REDIS_CONTAINER: str = Field(..., description="Redis container name")
    REDIS_PORT: int = Field(..., description="Redis port")
    REDIS_VOLUME: str = Field(..., description="Redis volume")
    REDIS_HOST: str = "redis"

    # ---------------- INFLUXDB ----------------
    INFLUX_CONTAINER: str = Field(..., description="InfluxDB container name")
    INFLUX_PORT: int = Field(..., description="InfluxDB exposed port")
    INFLUX_VOLUME_DATA: str = Field(..., description="InfluxDB data volume name")
    INFLUX_VOLUME_CONFIG: str = Field(..., description="InfluxDB config volume name")
    INFLUX_URL: str = "http://influxdb:8086"
    INFLUX_TOKEN: str = "tei-admin-token-rotate"
    INFLUX_ORG: str = "tei"
    INFLUX_BUCKET: str = "plc_raw"

    # ---------------- GRAFANA ----------------
    GRAFANA_CONTAINER: str = Field(..., description="Grafana container name")
    GRAFANA_PORT: int = Field(..., description="Grafana exposed port")
    GRAFANA_VOLUME: str = Field(..., description="Grafana data volume")
    GRAFANA_ADMIN_USER: str = Field(..., description="Grafana admin username")
    GRAFANA_ADMIN_PASSWORD: str = Field(..., description="Grafana admin password")

    model_config = {
        "env_file": "/home/raja/dev/project/own/conquer/backend/.env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


def reload_settings() -> Settings:
    load_dotenv(override=True)
    return Settings()


settings = reload_settings()
