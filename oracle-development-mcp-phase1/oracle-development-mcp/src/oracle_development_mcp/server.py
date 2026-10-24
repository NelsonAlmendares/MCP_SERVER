import logging
from mcp.server.fastmcp import FastMCP

from .config import Settings, validate_settings
from .diagnostics import service_status, simulated_invalid_objects

settings = Settings()
validate_settings(settings)
logging.basicConfig(level=settings.mcp_log_level.upper())

mcp = FastMCP(
    "Oracle Development MCP",
    host=settings.mcp_host,
    port=settings.mcp_port,
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def estado_servidor() -> dict:
    """Return the MCP service status. Does not connect to Oracle."""
    return service_status(settings)


@mcp.tool()
def listar_objetos_invalidos_demo(esquema: str) -> dict:
    """Return SIMULATED invalid Oracle objects for the configured environment.

    This tool does NOT query Oracle. Never treat the returned data as real.
    """
    return simulated_invalid_objects(esquema, settings.mcp_environment)


def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
