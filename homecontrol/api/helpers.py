from typing import Any, Dict, List, Optional

from flask import current_app, jsonify, request

from homecontrol.api.authentication.user_manager import UserManager
from homecontrol.api.database.client import APIDatabaseClient
from homecontrol.api.filters import Filters
from homecontrol.api.structs import APIAuthConfig
from homecontrol.helpers import SubscriptableClass


def response(data: Dict, code: int):
    """
    Helper function that returns a response
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


def get_database_client() -> APIDatabaseClient:
    return current_app.config["APIDatabaseClient"]
