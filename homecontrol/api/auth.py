from flask import Blueprint, request

from homecontrol.aircon.exceptions import ACConnectionError, ACInvalidStateError
from homecontrol.aircon.manager import ACManager
from homecontrol.aircon.structs import ACState
from homecontrol.api.authentication.structs import User
from homecontrol.api.authentication.user_manager import UserManager
from homecontrol.api.config import APIConfig
from homecontrol.api.database.client import APIDatabaseClient
from homecontrol.api.helpers import (
    authenticated,
    authenticated_user,
    check_required_params,
    get_user_manager,
    response,
    response_message,
)
from homecontrol.exceptions import DeviceNotRegisteredError
from homecontrol.helpers import ResponseStatus, dataclass_from_dict

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
        return response_message(
            "ERROR: Invalid username or password", ResponseStatus.UNAUTHORIZED
        )
    else:
        # Return an access token
        return response(
            {"access_token": user_manager.generate_access_token(user)},
            ResponseStatus.OK,
        )


@auth_api.route("/login/check", methods=["GET"])
@authenticated_user
def login_check(user: User):
    return response({"client_id": user.uuid}, ResponseStatus.OK)
