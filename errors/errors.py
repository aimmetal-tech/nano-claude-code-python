class ClaudeClientError(Exception):
    """Base class for exceptions in this module."""

    pass


class ValidationError(ClaudeClientError):
    """Exception raised for errors in the input."""

    pass
