from flask import Blueprint, request

from homecontrol.api.aircon import device_manager as ac_device_manager
from homecontrol.api.hue import device_manager as hue_device_manager
from homecontrol.api.helpers import (
    authenticated,
    response,
    response_message,
)
from homecontrol.api.structs import Room
from homecontrol.helpers import ResponseStatus, object_to_dict


home_api = Blueprint("home_api", __name__)


@home_api.route("/home/rooms", methods=["GET"])
@authenticated
def get_rooms():
    """
    Returns the current status of a device given its name
    """
    args = request.args

    # Get the bridge name
    bridge_name = args.get("bridge_name")

    if bridge_name is None:
        return response_message(
            "bridge_name must be given for this request", ResponseStatus.BAD_REQUEST
        )

    hue_bridge = hue_device_manager.get_bridge(bridge_name)
    ac_devices = ac_device_manager.list_devices()

    hue_rooms = None
    with hue_bridge.start_session() as conn:
        hue_rooms = conn.room.get_rooms()

    rooms_dict = {}

    for hue_room in hue_rooms:
        room = Room(name=hue_room.name, hue_room_id=hue_room.identifier)
        rooms_dict[hue_room.name] = room

    for ac_device_name in ac_devices:
        room = rooms_dict.get(ac_device_name)
        if room is None:
            room = Room(
                name=ac_device_name,
            )
        room.ac_device_name = ac_device_name
        rooms_dict[ac_device_name] = room

    rooms = list(rooms_dict.values())

    return response(object_to_dict(rooms), ResponseStatus.OK)
