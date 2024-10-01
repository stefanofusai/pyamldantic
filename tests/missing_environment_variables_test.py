import pytest

from src.yaml_cfg import YAMLConfig
from src.yaml_cfg.exceptions import MissingEnvironmentVariableError

from .fixtures import Schema


def test_schema_validation_error() -> None:
    with pytest.raises(MissingEnvironmentVariableError):
        YAMLConfig.load("tests/fixtures/config.yaml", schema=Schema)
