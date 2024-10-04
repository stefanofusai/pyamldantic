import pytest

from src.pyamldantic import YAMLConfig
from src.pyamldantic.exceptions import MissingEnvironmentVariableError

from .fixtures import Schema


def test_missing_environment_variable() -> None:
    with pytest.raises(MissingEnvironmentVariableError):
        YAMLConfig.load("tests/fixtures/config.yaml", schema=Schema)
