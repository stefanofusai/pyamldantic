import os
from pathlib import Path
from typing import Any, Self

import yaml
from pydantic import BaseModel, ValidationError
from yaml.scanner import ScannerError

from .exceptions import (
    FileNotFoundError,
    InvalidYAMLError,
    MissingEnvironmentVariableError,
    SchemaValidationError,
)


class YAMLConfig(BaseModel):
    """A class to represent and parse a configuration file.

    :raises FileNotFoundError: If the config file is not found
    :raises InvalidYAMLError: If the config file is not a valid YAML file
    :raises MissingEnvironmentVariableError: If an expected environment variable is missing
    :raises SchemaValidationError: If the config file does not match the expected schema
    :return: A YAMLConfig object
    :rtype: YAMLConfig
    """  # noqa: E501

    # Public methods

    @classmethod
    def from_yaml(cls, path: str) -> Self:
        """Create a configuration object from a YAML file.

        :param path: The path to the YAML file
        :type path: str
        :raises FileNotFoundError: If the config file is not found
        :raises InvalidYAMLError: If the config file is not a valid YAML file
        :raises SchemaValidationError: If the config file does not match the expected schema
        :return: A YAMLConfig object
        :rtype: Self
        """  # noqa: E501
        _path = Path(path)

        if not _path.exists():
            raise FileNotFoundError(path)

        with _path.open() as file:
            try:
                data = yaml.safe_load(file)

            except ScannerError as e:
                raise InvalidYAMLError(path, e) from None

        cls._replace_dashes_in_keys(data)
        cls._replace_env_vars(data)

        try:
            return cls(**data)

        except ValidationError as e:
            raise SchemaValidationError(path, e) from None

    # Private methods

    @staticmethod
    def _replace_dashes_in_keys(data: dict[str, Any]) -> None:
        """Replace dashes in keys with underscores.

        :param data: The data to process
        :type data: dict[str, Any]
        """
        for k in list(data.keys()):
            new_key = k.replace("-", "_")

            if new_key != k:
                data[new_key] = data.pop(k)

            if isinstance(data[new_key], dict):
                YAMLConfig._replace_dashes_in_keys(data[new_key])

    @staticmethod
    def _replace_env_vars(data: dict[str, Any]) -> None:
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
                    YAMLConfig._replace_env_vars(v)
