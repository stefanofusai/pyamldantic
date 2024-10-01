import pytest

from src.yaml_cfg import YAMLConfig
from src.yaml_cfg.exceptions import FileNotFoundError

from .fixtures import Schema


def test_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        YAMLConfig.load("tests/fixtures/foo.yaml", schema=Schema)
