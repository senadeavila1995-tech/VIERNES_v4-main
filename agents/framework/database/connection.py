import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


load_dotenv()


def _build_database_url() -> str:
    """
    Construye la URL de conexión.

    Soporta:
    - SQLite para tests/runtime aislado
    - MySQL para producción
    """

    driver = os.getenv(
        "DB_DRIVER",
        "mysql"
    )


    if driver == "sqlite":

        return os.getenv(
            "DB_URL",
            "sqlite:///./runtime_test.db"
        )


    user = os.getenv(
        "DB_USER",
        "root"
    )

    password = os.getenv(
        "DB_PASSWORD",
        ""
    )

    host = os.getenv(
        "DB_HOST",
        "localhost"
    )

    port = os.getenv(
        "DB_PORT",
        "3306"
    )

    database = os.getenv(
        "DB_NAME",
        "viernes_db"
    )


    return (
        f"mysql+pymysql://{user}:{password}"
        f"@{host}:{port}/{database}"
    )


DATABASE_URL = _build_database_url()


engine: Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
