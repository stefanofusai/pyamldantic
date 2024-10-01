# pyamldantic

Validate and serialize YAML config files with Pydantic, with support for environment variables.

## Installation

```bash
pip install pyamldantic
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
is-debug: true
```

`config.py`

```python
from pydantic import BaseModel, SecretStr
from pyamldantic import YAMLConfig

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

## Acknowledgments

This project was inspired by [envyaml](https://github.com/thesimj/envyaml).

## Contributing

Contributions are welcome! To get started, please refer to our [contribution guidelines](https://github.com/stefanofusai/pyamldantic/blob/main/CONTRIBUTING.md).

## Issues

If you encounter any problems while using this package, please open a new issue [here](https://github.com/stefanofusai/pyamldantic/issues).
