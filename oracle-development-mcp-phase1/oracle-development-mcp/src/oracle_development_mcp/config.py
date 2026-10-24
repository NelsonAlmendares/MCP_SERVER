from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mcp_host: str = "127.0.0.1"
    mcp_port: int = 8000
    mcp_log_level: str = "INFO"
    mcp_environment: Literal["DEV", "UAT"] = "DEV"


def validate_settings(settings: Settings) -> None:
    if not 1 <= settings.mcp_port <= 65535:
        raise ValueError("MCP_PORT must be between 1 and 65535")
    if settings.mcp_host not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError(
            "Phase 1 is loopback-only. Configure a secured reverse proxy "
            "and authentication before exposing the MCP endpoint."
        )
