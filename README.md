# pyamldantic

Validate and serialize YAML config files with Pydantic, with support for environment variables.

This package uses [uv](https://docs.astral.sh/uv/) for project management. To get started, ensure that **uv** is installed on your machine and updated to the `0.5.6` version. Detailed installation instructions for **uv** can be found [here](https://docs.astral.sh/uv/getting-started/installation/).

## Installation

```bash
uv add pyamldantic
```

## Usage

`config.yaml`

```yaml
database:
  host: $DATABASE_HOST
  name: $DATABASE_NAME
  password: $DATABASE_PASSWORD
  port: $DATABASE_PORT
  user: $DATABASE_USER
  timeout: $DATABASE_TIMEOUT?
environment: development
is_debug: true
```

`config.py`

```python
from pyamldantic import YAMLConfig
from pydantic import BaseModel, SecretStr

class DatabaseSchema(BaseModel):
    host: str
    name: str
    password: SecretStr
    port: int
    user: str
    ssl: bool = False
    timeout: int | None = None

class Schema(BaseModel):
    database: DatabaseSchema
    environment: str
    is_debug: bool

config = YAMLConfig.load("config.yaml", schema=Schema)
```

`main.py`

```python
from .config import config

if __name__ == "__main__":
    print(f"Initializing {config.environment} environment...")
    ...
```

## Development

```bash
uv sync --group=development
uv run pre-commit install --install-hooks
uv run pre-commit install --hook-type=commit-msg
```

## Testing

```bash
uv sync --group=testing
uv run pytest
```

## Acknowledgments

This project was inspired by [envyaml](https://github.com/thesimj/envyaml).

## Contributing

Contributions are welcome! To get started, please refer to our [contribution guidelines](https://github.com/stefanofusai/pyamldantic/blob/main/CONTRIBUTING.md).

## Issues

If you encounter any problems while using this package, please open a new issue [here](https://github.com/stefanofusai/pyamldantic/issues).
