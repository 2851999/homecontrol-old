from flask import Blueprint, request

from homecontrol.api.authentication.structs import User
from homecontrol.api.helpers import authenticated_user, get_user_manager, response
from homecontrol.api.exceptions import APIError
from homecontrol.helpers import ResponseStatus

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


@auth_api.route("/login/check", methods=["GET"])
@authenticated_user
def login_check(user: User):
    return response(
        {"client_id": user.uuid, "user_group": user.group}, ResponseStatus.OK
    )
