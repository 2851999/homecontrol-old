from typing import Any, Dict, List
from flask import current_app, request, jsonify

from homecontrol.api.structs import APIAuthInfo, ResponseStatus


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


def authenticated(func):
    """
    Decorator function for adding authentication to an endpoint
    """

    def wrapper():
        auth_config: APIAuthInfo = current_app.config["APIAuthInfo"]
        if auth_config.required:
            headers = request.headers
            auth_key = headers.get("X-Api-Key")
            if auth_key == auth_config.key:
                return func()
            return response_message("ERROR: Unauthorized", ResponseStatus.UNAUTHORIZED)
        return func()

    # Rename the function name (fixes "AssertionError: View function
    # mapping is overwriting an existing endpoint function: wrapper")
    wrapper.__name__ = func.__name__
    return wrapper
