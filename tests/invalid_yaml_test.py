from pathlib import Path

import pytest
from pydantic import BaseModel
from pytest_mock import MockerFixture

from src.yaml_cfg import YAMLConfig
from src.yaml_cfg.exceptions import InvalidYAMLError


def test_invalid_yaml_error(mocker: MockerFixture, schema: type[BaseModel]) -> None:
    mocker.patch.object(Path, "exists", autospec=True, return_value=True)
    mocker.patch.object(Path, "open", mocker.mock_open(read_data="key: value:"))

    with pytest.raises(InvalidYAMLError):
        YAMLConfig.load("config.yaml", schema=schema)
