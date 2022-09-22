from typing import Any
from pydantic import BaseSettings, PostgresDsn, validator, EmailStr


class Settings(BaseSettings):
    API_URL: str = "/api/v1"

    DEFAULT_LANG_CODE: str = "EN"

    # JWT
    JWT_SECRET_KEY: str  # TODO: Change to secrets
    JWT_ALG: str = "HS256"
    JWT_EXP: int = 1440  # JWT token expiry in minutes. Default is 1440.

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str  # TODO: Change to secrets
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Initial user
    INITIAL_EMAIL: EmailStr
    INITIAL_PASSWORD: str
    INITIAL_USER_ROLE: str

    # Sentence Embedding
    SENT_EMB_MODEL: str
    SENT_EMB_MODEL_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()
