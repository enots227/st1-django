"""Module contains common exceptions objects.

- WebError: Base error for St1 web apps. Should be treated as abstract class 
    i.e. do not raise this error.

- FriendlyError: An error where the message of the error can safely be presented
    to external clients for example 400 errors.

    Use Cases:
        - Customer Database Offline

    Examples:
        - The user's customer database is offline. Returns 503 Service Unavailable.

- GuardianError: An error where the message displayed to the users is always 
    "Access Denied". This error should represent an authentication (403) or 
    authorization error (401).

    Use Cases:
        - Access Violation
        - Invalid Request Authentication

    Examples:
        - The user attempted to access a resource that they are not allowed. 
            Returns a 401 Unauthorized.
        - The request could not be authenticated. Returns a 403 Forbidden.

- ValidationError:
    A friendly error detailing the problems with their request.

    Use Cases:
        - Invalid User Input

    Examples:
        - The "mids" field expected an array instead a string was provided. 
            Returns a 400 Bad Request.
"""
from typing import Any
from django.utils.translation import gettext


class WebError(Exception):
    """An exception intentionally implemented to prevent false data generation 
    and ensure confidentiality and integrity; occurs when logic did not got as 
    expected.
    """

    def __init__(self, 
        status_code: int,
        code: int,
        message: str,
        detail: Any = None,
        debug: str = None):
        """Initialize WebError.

        Args:
            status_code: The error status code returned to the user.
            message: The error message returned to the user.
            detail: The error detail returned to the user.
            debug: Text that only shows up in debug mode (displayed to user).

        """
        self.status_code: int = status_code
        self.code: int = code
        self.message: str = message
        self.detail: Any = detail
        self.debug: str = debug
        super().__init__(self.message)


class FriendlyError(WebError):
    """An exception that will be displayed to users."""

    def __init__(self,
        status_code: int,
        code: int,
        message: str,
        detail: Any = None,
        debug: str = None):
        """Initialize FriendlyError.

        Args:
            status_code: The error status code returned to the user.
            message: The error message returned to the user.
            detail: The error detail returned to the user.
            debug: Text that only shows up in debug mode (displayed to user).

        """
        super().__init__(status_code, code, message, detail, debug)


class GuardianError(WebError):
    """An exception that will NOT be displayed to users. The user will merely 
    see access denied.
    """

    def __init__(self,
        code: int,
        iss: str = "Unknown",
        sub: str = "Unknown",
        status_code: int = 403,
        debug: str = None):
        """Initialize GuardianError.

        Args:
            status_code: The error status code returned to the user.
            iss: The issuer of the request if any.
            sub: The subject of the request if any.
            debug: Text that only shows up in debug mode (displayed to user).

        """
        super().__init__(status_code, code, gettext('Access Denied'), debug=debug)
        self.iss = iss
        self.sub = sub


class ValidationError(FriendlyError):
    """An exception that will be displayed to users with validation errors."""

    def __init__(self, errors: Any, debug: str = None):
        """Initialize ValidationError.

        Args:
            errors: The validation errors.
            debug: Text that only shows up in debug mode (displayed to user).

        """
        super().__init__(400, 4000, gettext("Bad Input"), errors, debug)

