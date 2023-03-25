from flask import Blueprint, request

from homecontrol.aircon.exceptions import ACConnectionError, ACInvalidStateError
from homecontrol.aircon.structs import ACState

from homecontrol.api.helpers import (
    authenticated,
    check_required_params,
    response,
    response_message,
)
from homecontrol.aircon.manager import ACManager
from homecontrol.exceptions import DeviceNotRegisteredError
from homecontrol.helpers import dataclass_from_dict, ResponseStatus


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


@aircon_api.route("/ac/devices/register", methods=["PUT"])
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


@aircon_api.route("/ac/devices/<name>", methods=["GET"])
@authenticated
def get_device(name):
    """
    Returns the current status of a device given its name
    """
    try:
        device = device_manager.get_device(name)
        try:
            return response(device.get_state().__dict__, ResponseStatus.OK)
        except ACConnectionError as err:
            return response_message(str(err), ResponseStatus.BAD_REQUEST)
    except DeviceNotRegisteredError as err:
        return response_message(str(err), ResponseStatus.BAD_REQUEST)


@aircon_api.route("/ac/devices/<name>", methods=["PUT"])
@authenticated
def set_device(name):
    """
    Assigns the state of a device and returns it
    """

    try:
        device = device_manager.get_device(name)

        # Should have a full new state in the data given
        new_state = dataclass_from_dict(ACState, request.get_json())

        try:
            device.set_state(new_state)
            return response(device.get_state().__dict__, ResponseStatus.OK)
        except (ACConnectionError, ACInvalidStateError) as err:
            return response_message(str(err), ResponseStatus.BAD_REQUEST)
    except DeviceNotRegisteredError as err:
        return response_message(str(err), ResponseStatus.BAD_REQUEST)
