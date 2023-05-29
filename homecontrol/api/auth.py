from flask import Blueprint, request

from homecontrol.api.authentication.structs import User
from homecontrol.api.exceptions import APIError
from homecontrol.api.helpers import authenticated_user, get_user_manager, response
from homecontrol.exceptions import ResourceNotFoundError
from homecontrol.helpers import ResponseStatus, object_to_dict

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/login", methods=["POST"])
def login():
    """
    Attempts user login
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user_manager = get_user_manager()
    user = user_manager.verify_login(username, password)

    if not user:
        raise APIError("Invalid username or password", ResponseStatus.UNAUTHORIZED)
    else:
        # Return an access token
        return response(
            # TODO: Put into a struct that can be parsed on the other end
            {"access_token": user_manager.generate_access_token(user)},
            ResponseStatus.OK,
        )


@auth_api.route("/login", methods=["GET"])
@authenticated_user
def login_check(user: User):
    """Returns information about the current user"""
    return response(object_to_dict(user), ResponseStatus.OK)


@auth_api.route("/auth/users", methods=["GET"])
@authenticated_user(require_admin=True)
def get_users(user: User):
    user_manager = get_user_manager()
    users = user_manager.get_users()
    return response(object_to_dict(users), ResponseStatus.OK)


@auth_api.route("/auth/user/<user_id>", methods=["GET"])
@authenticated_user(require_admin=True)
def get_user(user: User, user_id):
    user_manager = get_user_manager()
    try:
        user = user_manager.get_user(user_id)
    except ResourceNotFoundError:
        raise APIError(
            f"User with the id '{user_id}' was not found", ResponseStatus.NOT_FOUND
        )
    return response(object_to_dict(user), ResponseStatus.OK)
