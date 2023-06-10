from flask import Blueprint

from homecontrol.api.authentication.helpers import authenticated
from homecontrol.api.helpers import response
from homecontrol.broadlink.manager import BroadlinkManager
from homecontrol.helpers import ResponseStatus

broadlink_api = Blueprint("broadlink_api", __name__)

# Broadlink manager
broadlink_device_manager = BroadlinkManager()


@broadlink_api.route("/broadlink/<device_name>/ir/<command_name>", methods=["PUT"])
@authenticated
def run_command(device_name, command_name):
    """
    Returns a list of device names
    """
    broadlink_device_manager.playback_ir_command(device_name, command_name)
    return response(broadlink_device_manager.list_devices(), ResponseStatus.OK)
