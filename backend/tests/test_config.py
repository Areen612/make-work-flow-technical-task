import pytest

from config import ConfigurationError, Settings


def test_settings_accept_valid_values() -> None:
    settings = Settings(
        database_url="postgresql+psycopg://localhost/make_work_flow",
        frontend_origin="http://localhost:5173/",
    )

    assert settings.database_url == (
        "postgresql+psycopg://localhost/make_work_flow"
    )
    assert settings.frontend_origin == "http://localhost:5173"


def test_settings_reject_invalid_database_url() -> None:
    with pytest.raises(ConfigurationError, match="DATABASE_URL"):
        Settings(
            database_url="not a database URL",
            frontend_origin="http://localhost:5173",
        )


@pytest.mark.parametrize(
    "frontend_origin",
    [
        "localhost:5173",
        "ftp://localhost:5173",
        "http://localhost:5173/application",
        "http://localhost:99999",
    ],
)
def test_settings_reject_invalid_frontend_origin(
    frontend_origin: str,
) -> None:
    with pytest.raises(ConfigurationError, match="FRONTEND_ORIGIN"):
        Settings(
            database_url="sqlite://",
            frontend_origin=frontend_origin,
        )
