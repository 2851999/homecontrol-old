from typing import Dict
from flask import current_app, request, jsonify

from homecontrol.api.structs import APIAuthInfo


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
            return response_message("ERROR: Unauthorized", 401)
        return func()

    # Rename the function name (fixes "AssertionError: View function
    # mapping is overwriting an existing endpoint function: wrapper")
    wrapper.__name__ = func.__name__
    return wrapper
