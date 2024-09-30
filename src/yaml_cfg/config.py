import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError
from yaml.scanner import ScannerError

from .exceptions import (
    FileNotFoundError,
    InvalidYAMLError,
    MissingEnvironmentVariableError,
    SchemaValidationError,
)


class YAMLConfig:
    """A class to parse and represent a YAML configuration file."""

    # Public methods

    @classmethod
    def load(cls, path: str, *, schema: type[BaseModel]) -> BaseModel:
        """Create a Pydantic configuration object from a YAML file and a Pydantic schema.

        :param path: The path to the YAML file
        :type path: str
        :param schema: The Pydantic schema
        :type schema: type[BaseModel]
        :raises FileNotFoundError: If the config file is not found
        :raises InvalidYAMLError: If the config file is not a valid YAML file
        :raises SchemaValidationError: If the config file does not match the expected schema
        :return: A Pydantic configuration object
        :rtype: BaseModel
        """  # noqa: E501
        _path = Path(path)

        if not _path.exists():
            raise FileNotFoundError(path)

        with _path.open() as file:
            try:
                data = yaml.safe_load(file)

            except ScannerError as e:
                raise InvalidYAMLError(path, e) from None

        cls._normalize_keys(data)
        cls._set_env_vars(data)

        try:
            return schema(**data)

        except ValidationError as e:
            raise SchemaValidationError(path, e) from None

    # Private methods

    @classmethod
    def _normalize_keys(cls, data: dict[str, Any]) -> None:
        """Replace dashes in keys with underscores.

        :param data: The data to process
        :type data: dict[str, Any]
        """
        for k in list(data.keys()):
            new_key = k.replace("-", "_")

            if new_key != k:
                data[new_key] = data.pop(k)

            if isinstance(data[new_key], dict):
                cls._normalize_keys(data[new_key])

    @classmethod
    def _set_env_vars(cls, data: dict[str, Any]) -> None:
        """Replace environment variables with their values.

        :param data: The data to process
        :type data: dict[str, Any]
        :raises MissingEnvironmentVariableError: If an expected environment variable is missing
        """  # noqa: E501
        for k, v in data.items():
            match v:
                case str() if v.startswith("$"):
                    nullable = v.endswith("?")

                    try:
                        value = os.environ[v[1:-1] if nullable is True else v[1:]]

                    except KeyError:
                        if nullable is True:
                            value = None

                        else:
                            raise MissingEnvironmentVariableError(v) from None

                    data[k] = value

                case dict():
                    cls._set_env_vars(v)
