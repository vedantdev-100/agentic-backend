from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    groq_api_key: str
    fastmcp_api_key: str
    alpha_vantage_api_key: str

    arith_python: str
    arith_main: str

    expense_mcp_url: str = ("https://provincial-plum-turtle.fastmcp.app/mcp")

    database_url: str = "chatbot.db"

    model_name: str = "openai/gpt-oss-20b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()