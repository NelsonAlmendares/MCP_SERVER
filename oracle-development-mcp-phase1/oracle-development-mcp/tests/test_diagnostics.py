import pytest
from oracle_development_mcp.config import Settings, validate_settings
from oracle_development_mcp.diagnostics import service_status, simulated_invalid_objects


def test_service_status_does_not_claim_oracle_connection():
    status = service_status(Settings(_env_file=None))
    assert status["oracle_connected"] is False
    assert status["read_only"] is True


def test_demo_is_explicitly_simulated():
    result = simulated_invalid_objects("dev", "DEV")
    assert result["source"] == "SIMULATED_DATA_NOT_ORACLE"


@pytest.mark.parametrize("schema", ["SYS", "PROD", "DEV; DROP TABLE X"])
def test_disallowed_schemas(schema):
    with pytest.raises(ValueError):
        simulated_invalid_objects(schema, "DEV")


def test_cross_environment_rejected():
    with pytest.raises(ValueError):
        simulated_invalid_objects("UAT", "DEV")


def test_public_bind_rejected():
    with pytest.raises(ValueError):
        validate_settings(Settings(_env_file=None, mcp_host="0.0.0.0"))
