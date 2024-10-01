from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from src.yaml_cfg import YAMLConfig
from src.yaml_cfg.exceptions import SchemaValidationError

from .fixtures import Schema


def test_schema_validation_error(mocker: MockerFixture) -> None:
    mocker.patch.object(Path, "open", mocker.mock_open(read_data="key: value"))

    with pytest.raises(SchemaValidationError):
        YAMLConfig.load("tests/fixtures/config.yaml", schema=Schema)
