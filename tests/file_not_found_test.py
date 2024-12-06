import pytest

from src.pyamldantic import YAMLConfig

from .fixtures import Schema


def test_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        YAMLConfig.load("tests/fixtures/foo.yaml", schema=Schema)
