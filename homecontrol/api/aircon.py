from flask import Blueprint, request
from homecontrol.aircon.structs import ACConnectionError

from homecontrol.api.helpers import (
    authenticated,
    check_required_params,
    response,
    response_message,
)
from homecontrol.aircon.manager import ACManager
from homecontrol.api.structs import ResponseStatus


aircon_api = Blueprint("aircon_api", __name__)

# ACManager
device_manager = ACManager()


@aircon_api.route("/ac/devices", methods=["GET"])
@authenticated
def list_devices():
    """
    Returns a list of device names
    """
    return response(device_manager.list_devices(), ResponseStatus.OK)


@aircon_api.route("/ac/devices/state", methods=["PUT"])
@authenticated
def register_device():
    """
    Returns a list of device names
    """
    data = request.get_json()
    if not check_required_params(data, ["name", "ip"]):
        return response_message("Must give a name and ip", ResponseStatus.BAD_REQUEST)

    try:
        device_manager.register_device(data["name"], data["ip"])
    except ACConnectionError as err:
        return response_message(str(err), ResponseStatus.BAD_REQUEST)

    return response(None, ResponseStatus.CREATED)
