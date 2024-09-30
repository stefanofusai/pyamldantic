import os

import pytest
from pydantic import BaseModel, SecretStr
from pytest_mock import MockerFixture


@pytest.fixture
def schema(mocker: MockerFixture) -> type[BaseModel]:
    mocker.patch.dict(
        os.environ,
        {
            "DATABASE_HOST": "foo",
            "DATABASE_NAME": "bar",
            "DATABASE_PASSWORD": "baz",
            "DATABASE_PORT": "qux",
            "DATABASE_USER": "quux",
        },
    )

    class DatabaseSchema(BaseModel):
        host: str
        name: str
        password: SecretStr
        port: int
        user: str
        schema: str | None = None
        ssl: bool = False
        timeout: int | None = None

    class Schema(BaseModel):
        database: DatabaseSchema
        debug: bool
        environment: str

    return Schema
