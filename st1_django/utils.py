"""Common view logic."""
import json
import asyncio
from json.decoder import JSONDecodeError
from typing import Any
from django.utils.decorators import classonlymethod
from django.views.generic import View
from django.utils.translation import gettext
from st1_django.errors import FriendlyError


# Async Helpers
class AsyncView(View):
    """Base Async View."""

    # noinspection PyMethodParameters,PyProtectedMember
    @classonlymethod
    def as_view(cls, **kwargs):
        """Handles converting the class into an async view function."""
        view = super().as_view(**kwargs)
        # noinspection PyUnresolvedReferences
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view


# JSON Helpers
def json_deserialize(raw: str) -> Any:
    """Deserialize JSON and if anything fails ensure that the middleware 
    understand how to handle it.

    NOTE: This should ONLY BE CALLED IN A VIEW function and not by the business 
        logic. If you are deserializing, JSON in the business logic use 
        json.loads(raw: str). If you use this in the business logic and it 
        errors, then the error middleware handle will receive a FriendlyError. 
        This will cause user to be presented with a status 400 stating their 
        input JSON is wrong, which in fact it is the business logic that isn't 
        working.

    Args:
        raw: The raw JSON string.

    Returns:
        The JSON string decoded.

    Raises:
        FriendlyError: Missing JSON.
        FriendlyError: Invalid JSON syntax.
    """
    if not raw:
        raise FriendlyError(
            status_code=400,
            code=1000,
            message=gettext("Missing JSON."),
        )

    try:
        return json.loads(raw)
    except JSONDecodeError as e:
        raise FriendlyError(
            status_code=400,
            code=1001,
            message=gettext("Invalid JSON syntax."),
            debug=str(e),
        )
