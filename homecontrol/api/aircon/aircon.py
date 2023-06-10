from flask import Blueprint, request

from homecontrol.aircon.aircon import ACDevice
from homecontrol.aircon.exceptions import ACInvalidStateError
from homecontrol.aircon.manager import ACManager
from homecontrol.aircon.structs import ACState
from homecontrol.api.authentication.helpers import authenticated
from homecontrol.api.exceptions import APIError
from homecontrol.api.helpers import check_required_params, response
from homecontrol.exceptions import DeviceConnectionError, DeviceNotRegisteredError
from homecontrol.helpers import ResponseStatus, dataclass_from_dict

aircon_api = Blueprint("aircon_api", __name__)

# ACManager
device_manager = ACManager()


def find_device(name: str) -> ACDevice:
    """
    Returns a device or throws an appropriate error if not found
    """
    try:
        return device_manager.get_device(name)
    except DeviceNotRegisteredError as err:
        raise APIError(str(err), ResponseStatus.NOT_FOUND)


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
        raise APIError("Must give a name and ip", ResponseStatus.BAD_REQUEST)

    try:
        device_manager.register_device(data["name"], data["ip"])
    except DeviceConnectionError as err:
        raise APIError(str(err), ResponseStatus.BAD_REQUEST)

    return response(None, ResponseStatus.CREATED)


@aircon_api.route("/ac/devices/<name>", methods=["GET"])
@authenticated
def get_device(name):
    """
    Returns the current status of a device given its name
    """
    device = find_device(name)
    try:
        return response(device.get_state().__dict__, ResponseStatus.OK)
    except DeviceConnectionError as err:
        raise APIError(str(err), ResponseStatus.BAD_REQUEST)


@aircon_api.route("/ac/devices/<name>", methods=["PUT"])
@authenticated
def set_device(name):
    """
    Assigns the state of a device and returns it
    """
    device = find_device(name)

    # Should have a full new state in the data given
    new_state = dataclass_from_dict(ACState, request.get_json())

    try:
        device.set_state(new_state)
        return response(device.get_state().__dict__, ResponseStatus.OK)
    except (DeviceConnectionError, ACInvalidStateError) as err:
        raise APIError(str(err), ResponseStatus.BAD_REQUEST)
