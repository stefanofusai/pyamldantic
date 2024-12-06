class InvalidYAMLError(Exception):
    """Raised when the config file is not a valid YAML file."""

    def __init__(self, path: str, e: Exception) -> None:  # noqa: D107
        super().__init__(f"{path} is not a valid YAML file: {e}")


class MissingEnvironmentVariableError(Exception):
    """Raised when an expected environment variable is missing."""

    def __init__(self, var: str) -> None:  # noqa: D107
        super().__init__(f"missing expected environment variable: `{var}`")


class SchemaValidationError(Exception):
    """Raised when the config file does not match the expected schema."""

    def __init__(self, path: str, e: Exception) -> None:  # noqa: D107
        super().__init__(f"{path} does not match the expected schema: {e}")
