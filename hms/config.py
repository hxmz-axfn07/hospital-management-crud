"""Configuration helpers for database access."""

from dataclasses import dataclass
import getpass
import os


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    user: str
    password: str
    database: str = "city_hospital"


def load_config() -> DatabaseConfig:
    """Load database credentials from env vars or interactive prompts."""
    user = os.getenv("HMS_DB_USER") or input("Enter your MySQL username: ").strip()
    password = os.getenv("HMS_DB_PASSWORD") or getpass.getpass(
        "Enter your MySQL password: "
    )
    host = os.getenv("HMS_DB_HOST", "localhost")
    database = os.getenv("HMS_DB_NAME", "city_hospital")
    return DatabaseConfig(host=host, user=user, password=password, database=database)
