from flask import Blueprint, request

from homecontrol.api.aircon.aircon import device_manager as ac_device_manager
from homecontrol.api.broadlink import broadlink_device_manager
from homecontrol.api.aircon.aircon import find_device
from homecontrol.api.authentication.helpers import authenticated
from homecontrol.api.exceptions import APIError
from homecontrol.api.helpers import get_database_client, response
from homecontrol.api.hue import device_manager as hue_device_manager
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
        raise APIError(
            "bridge_name must be given for this request", ResponseStatus.BAD_REQUEST
        )

    hue_bridge = hue_device_manager.get_bridge(bridge_name)
    ac_devices = ac_device_manager.list_devices()

    hue_rooms = None
    with hue_bridge.start_session() as conn:
        hue_rooms = conn.room.get_rooms()

    rooms_dict = {}

    for hue_room in hue_rooms:
        room = Room(
            name=hue_room.name,
            hue_room_id=hue_room.identifier,
            hue_light_group=hue_room.light_group,
            hue_lights=hue_room.lights,
        )
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


@home_api.route("/home/outdoor_temp", methods=["GET"])
@authenticated
def get_outdoor_temp():
    """
    Returns the current outdoor temp as measured by AC units (for now
    just selecting the result of the first unit)
    """

    ac_devices = ac_device_manager.list_devices()

    outdoor_temp = "N/A"

    if len(ac_devices) > 0:
        outdoor_temp = ac_device_manager.get_device(ac_devices[0]).get_state().outdoor

    return response(outdoor_temp, ResponseStatus.OK)


@home_api.route("/home/room/<name>/states", methods=["GET"])
@authenticated
def get_room_states(name: str):
    """
    Returns a list of room states for a given room
    """

    # Obtain the room states for the room
    database_client = get_database_client()
    with database_client.connect() as conn:
        room_states = conn.rooms.find_states_in_room(name)

    return response(object_to_dict(room_states), ResponseStatus.OK)


@home_api.route("/home/rooms/state/<state_id>", methods=["PUT"])
@authenticated
def recall_room_state(state_id: str):
    """
    Recalls a room state with a given ID
    """

    # Obtain the room and AC state
    database_client = get_database_client()
    ac_state = None
    with database_client.connect() as conn:
        room_state = conn.rooms.find_state_by_id(state_id)
        if room_state.ac_device_name and room_state.ac_state_id:
            ac_state = conn.aircon.find_state_by_id(room_state.ac_state_id)

    # Apply the AC state if required
    if ac_state:
        ac_device = find_device(room_state.ac_device_name)
        ac_device.set_state(ac_state)

    # Apply the Hue scene if required
    if room_state.hue_scene_id:
        hue_bridge = hue_device_manager.get_bridge("Home")
        with hue_bridge.start_session() as conn:
            conn.scene.recall_scene(room_state.hue_scene_id)

    # Apply the broadlink actions if required
    if room_state.broadlink_device_name and room_state.broadlink_actions:
        for action in room_state.broadlink_actions:
            broadlink_device_manager.playback_ir_command(
                room_state.broadlink_device_name, action
            )

    return response(object_to_dict(room_state), ResponseStatus.OK)
