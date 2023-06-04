# TODO: Move this into the authentication folder
from functools import wraps

from flask import request

from homecontrol.api.authentication.structs import UserGroup
from homecontrol.api.exceptions import APIError
from homecontrol.api.helpers import get_auth_config, get_user_manager
from homecontrol.api.structs import APIAuthConfig
from homecontrol.helpers import ResponseStatus


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
            raise APIError("Unauthorized", ResponseStatus.UNAUTHORIZED)
        return func()

    # Rename the function name (fixes "AssertionError: View function
    # mapping is overwriting an existing endpoint function: wrapper")
    wrapper.__name__ = func.__name__
    return wrapper


# TODO: Move this into the authentication folder
def authenticated_user(original_func=None, require_admin=False):
    def _authenticated_user(func):
        """
        Decorator function for adding user authentication to an endpoint
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            headers = request.headers
            bearer_token = headers.get("Authorization")
            if not bearer_token:
                raise APIError("Missing access token", ResponseStatus.UNAUTHORIZED)
            token = bearer_token.replace("Bearer ", "")
            user_manager = get_user_manager()
            try:
                user = user_manager.verify_access_token(token)
            except Exception as err:
                raise APIError(
                    f"Unable to verify token \n\n{err}",
                    ResponseStatus.UNAUTHORIZED,
                )
            if require_admin and user.group != UserGroup.admin:
                raise APIError("Invalid permissions", ResponseStatus.UNAUTHORIZED)
            return func(*args, user, **kwargs)

        # Rename the function name (fixes "AssertionError: View function
        # mapping is overwriting an existing endpoint function: wrapper")
        wrapper.__name__ = func.__name__
        return wrapper

    if original_func:
        return _authenticated_user(original_func)

    return _authenticated_user
