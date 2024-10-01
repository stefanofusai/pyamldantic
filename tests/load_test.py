import os

from pydantic import SecretStr
from pytest_mock import MockerFixture

from src.pyamldantic import YAMLConfig

from .fixtures import Schema


def test_load(mocker: MockerFixture) -> None:
    mocker.patch.dict(
        os.environ,
        {
            "DATABASE_HOST": "foo",
            "DATABASE_NAME": "bar",
            "DATABASE_PASSWORD": "baz",
            "DATABASE_PORT": "5432",
            "DATABASE_USER": "qux",
        },
    )

    config = YAMLConfig.load("tests/fixtures/config.yaml", schema=Schema)
    assert config.database.host == os.environ["DATABASE_HOST"]
    assert config.database.name == os.environ["DATABASE_NAME"]
    assert config.database.password == SecretStr(os.environ["DATABASE_PASSWORD"])
    assert config.database.port == int(os.environ["DATABASE_PORT"])
    assert config.database.user == os.environ["DATABASE_USER"]
    assert config.database.ssl is False
    assert config.database.timeout is None
    assert config.environment == "testing"
    assert config.is_debug
