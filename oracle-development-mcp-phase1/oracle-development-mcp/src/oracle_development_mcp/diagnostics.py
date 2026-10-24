from datetime import datetime, timezone
from .config import Settings


def service_status(settings: Settings) -> dict:
    return {
        "service": "oracle-development-mcp",
        "status": "ok",
        "phase": 1,
        "environment": settings.mcp_environment,
        "oracle_connected": False,
        "read_only": True,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def simulated_invalid_objects(environment: str, configured_environment: str) -> dict:
    environment = environment.strip().upper()
    if environment not in ("DEV", "UAT"):
        raise ValueError("Only DEV and UAT are allowed")
    if environment != configured_environment:
        raise ValueError("Cross-environment access is disabled")
    return {
        "environment": environment,
        "source": "SIMULATED_DATA_NOT_ORACLE",
        "items": [
            {"object_name": "GESTION_CLIENTES", "object_type": "PACKAGE BODY", "status": "INVALID"}
        ],
    }
