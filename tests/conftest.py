import os

import pytest
from pydantic import BaseModel
from pytest_mock import MockerFixture


@pytest.fixture
def schema(mocker: MockerFixture) -> type[BaseModel]:
    mocker.patch.dict(os.environ, {"DATABASE_URL": "foo"})

    class DatabaseSchema(BaseModel):
        host: str
        name: str
        password: str
        port: int
        user: str

    class Schema(BaseModel):
        database: DatabaseSchema
        debug: bool | None
        environment: str
        missing_key: str | None = None

    return Schema
