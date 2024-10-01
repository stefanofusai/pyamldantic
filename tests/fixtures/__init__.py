from pydantic import BaseModel, SecretStr


class DatabaseSchema(BaseModel):  # noqa: D101
    host: str
    name: str
    password: SecretStr
    port: int
    user: str
    ssl: bool = False
    timeout: int | None = None


class Schema(BaseModel):  # noqa: D101
    database: DatabaseSchema
    environment: str
    is_debug: bool
