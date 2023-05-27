from functools import wraps
from typing import Any, Dict, List, Optional

from flask import current_app, jsonify, request
from homecontrol.api.authentication.user_manager import UserManager

from homecontrol.api.filters import Filters
from homecontrol.api.structs import APIAuthConfig
from homecontrol.helpers import ResponseStatus, SubscriptableClass


def response(data: Dict, code: int):
    """
    Helper function that returns a repsonse
    """
    return jsonify(data), code


def response_message(message: str, code: int):
    """
    Helper function that returns a response for a message
    """
    return response({"message": message}, code)


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


def get_auth_config() -> APIAuthConfig:
    return current_app.config["APIAuthConfig"]


def get_user_manager() -> UserManager:
    return current_app.config["UserManager"]


def authenticated(func):
    """
    Decorator function for adding authentication to an endpoint
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_config: APIAuthConfig = get_auth_config()
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


def authenticated_user(func):
    """
    Decorator function for adding user authentication to an endpoint
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = request.headers
        bearer_token = headers.get("Authorization")
        if not bearer_token:
            return response_message(
                "ERROR: Missing access token", ResponseStatus.UNAUTHORIZED
            )
        token = bearer_token.replace("Bearer ", "")
        user_manager = get_user_manager()
        try:
            user = user_manager.verify_access_token(token)
        except Exception as err:
            return response_message(
                f"ERROR: Unable to verify token \n\n{err}",
                ResponseStatus.UNAUTHORIZED,
            )
        return func(*args, user, **kwargs)

    # Rename the function name (fixes "AssertionError: View function
    # mapping is overwriting an existing endpoint function: wrapper")
    wrapper.__name__ = func.__name__
    return wrapper
