from functools import wraps
from typing import Any, Dict, List, Optional
from flask import current_app, request, jsonify
from homecontrol.api.filters import Filters

from homecontrol.api.structs import APIAuthInfo
from homecontrol.helpers import ResponseStatus, SubscriptableClass


def response(data: Dict, code: int):
    """
    Helper function that returns a reponse
    """
    return jsonify(data), code


def response_message(message: str, code: int):
    """
    Helper function that returns a response for a messsage
    """
    return response({"messsage": message}, code)


def check_required_params(data: Dict[str, Any], params: List[str]):
    """
    Returns whether all the params are found as keys in the data
    """
    return all(param in data for param in params)


def get_filters() -> Optional[Filters]:
    """
    Attempts to get filters from request arguments, returns None if not found
    """
    filters_json = request.args.get("filters", None)
    if filters_json:
        return Filters(filters_json)
    return None


def apply_filters(items: List[SubscriptableClass]) -> List[SubscriptableClass]:
    """
    Obtains filters from request arguments and applies them to a list of items (if there are any)
    """
    filters = get_filters()
    if filters:
        return filters.apply(items)
    return items


def authenticated(func):
    """
    Decorator function for adding authentication to an endpoint
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_config: APIAuthInfo = current_app.config["APIAuthInfo"]
        if auth_config.required:
            headers = request.headers
            auth_key = headers.get("X-Api-Key")
            if auth_key == auth_config.key:
                return func(*args, **kwargs)
            return response_message("ERROR: Unauthorized", ResponseStatus.UNAUTHORIZED)
        return func()

    # Rename the function name (fixes "AssertionError: View function
    # mapping is overwriting an existing endpoint function: wrapper")
    wrapper.__name__ = func.__name__
    return wrapper
