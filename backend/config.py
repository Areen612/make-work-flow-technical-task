import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ROOT_ENV_FILE = PROJECT_ROOT / ".env"
BACKEND_ENV_FILE = Path(__file__).with_name(".env")


class ConfigurationError(RuntimeError):
    """Raised when required application configuration is missing or invalid."""


def _required_environment_variable(name: str, setup_hint: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise ConfigurationError(f"{name} is not set. {setup_hint}")

    return value.strip()


def _validate_database_url(value: str) -> str:
    try:
        make_url(value)
    except ArgumentError as exc:
        raise ConfigurationError(
            "DATABASE_URL must be a valid SQLAlchemy database URL."
        ) from exc

    return value


def _validate_frontend_origin(value: str) -> str:
    parsed = urlsplit(value)

    try:
        port_is_valid = parsed.port is None or 0 < parsed.port <= 65535
    except ValueError:
        port_is_valid = False

    if (
        parsed.scheme not in {"http", "https"}
        or parsed.hostname is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
        or not port_is_valid
    ):
        raise ConfigurationError(
            "FRONTEND_ORIGIN must contain only an http(s) scheme, host, "
            "and optional port."
        )

    # CORS origins do not include a trailing slash.
    return value.rstrip("/")


@dataclass(frozen=True)
class Settings:
    database_url: str
    frontend_origin: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "database_url",
            _validate_database_url(self.database_url),
        )
        object.__setattr__(
            self,
            "frontend_origin",
            _validate_frontend_origin(self.frontend_origin),
        )


def load_settings() -> Settings:
    """Load shared and backend-specific environment settings."""
    # load_dotenv does not replace exported shell variables by default.
    load_dotenv(ROOT_ENV_FILE)
    load_dotenv(BACKEND_ENV_FILE)

    return Settings(
        database_url=_required_environment_variable(
            "DATABASE_URL",
            "Copy backend/.env.example to backend/.env.",
        ),
        frontend_origin=_required_environment_variable(
            "FRONTEND_ORIGIN",
            "Copy .env.example to .env.",
        ),
    )


settings = load_settings()
