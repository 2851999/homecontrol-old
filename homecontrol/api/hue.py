from flask import Blueprint, request

from homecontrol.api.authentication.helpers import authenticated
from homecontrol.api.exceptions import APIError
from homecontrol.api.helpers import apply_filters, response
from homecontrol.helpers import ResponseStatus
from homecontrol.hue.api.exceptions import HueAPIError
from homecontrol.hue.grouped_light import GroupedLightState
from homecontrol.hue.light import LightState
from homecontrol.hue.manager import HueManager

hue_api = Blueprint("hue_api", __name__)

# ACManager
device_manager = HueManager()


@hue_api.errorhandler(HueAPIError)
def handle_hue_api_error(err: HueAPIError):
    """
    Handle any errors from the Hue API
    """
    raise APIError(str(err), ResponseStatus.BAD_REQUEST)


@hue_api.route("/hue/<bridge_name>/rooms", methods=["GET"])
@authenticated
def get_rooms(bridge_name):
    """
    Returns a dictionary of rooms a bridge has access to
    """
    bridge = device_manager.get_bridge(bridge_name)
    with bridge.start_session() as conn:
        try:
            rooms = conn.room.get_rooms()
            rooms = apply_filters(rooms)

            return response(rooms, ResponseStatus.OK)
        except HueAPIError as err:
            raise APIError(str(err), ResponseStatus.BAD_REQUEST)


@hue_api.route("/hue/<bridge_name>/light/<light_id>", methods=["GET"])
@authenticated
def get_light_state(bridge_name, light_id):
    """
    Returns the current state of a group of lights
    """
    bridge = device_manager.get_bridge(bridge_name)
    with bridge.start_session() as conn:
        return response(conn.light.get_state(light_id).to_dict(), ResponseStatus.OK)


@hue_api.route("/hue/<bridge_name>/light/<light_id>", methods=["PUT"])
@authenticated
def set_light_state(bridge_name, light_id):
    """
    Updates the state of a of a light
    """
    payload = request.get_json()
    bridge = device_manager.get_bridge(bridge_name)
    state = LightState.from_dict(payload)
    with bridge.start_session() as conn:
        conn.light.set_state(light_id, state)

        return response("Success", ResponseStatus.OK)


@hue_api.route("/hue/<bridge_name>/grouped_lights/<group_id>", methods=["GET"])
@authenticated
def get_grouped_light_state(bridge_name, group_id):
    """
    Returns the current state of a group of lights
    """
    bridge = device_manager.get_bridge(bridge_name)
    with bridge.start_session() as conn:
        return response(
            conn.grouped_light.get_state(group_id).to_dict(), ResponseStatus.OK
        )


@hue_api.route("/hue/<bridge_name>/grouped_lights/<group_id>", methods=["PUT"])
@authenticated
def set_grouped_light_state(bridge_name, group_id):
    """
    Updates the state of a group of lights
    """
    payload = request.get_json()
    bridge = device_manager.get_bridge(bridge_name)
    state = GroupedLightState.from_dict(payload)
    with bridge.start_session() as conn:
        conn.grouped_light.set_state(group_id, state)

        return response("Success", ResponseStatus.OK)


@hue_api.route("/hue/<bridge_name>/scenes", methods=["GET"])
@authenticated
def get_scenes(bridge_name):
    """
    Returns a list of scenes a bridge has access to
    """

    bridge = device_manager.get_bridge(bridge_name)
    with bridge.start_session() as conn:
        scenes = conn.scene.get_scenes()
        scenes = apply_filters(scenes)

        return response(scenes, ResponseStatus.OK)


@hue_api.route("/hue/<bridge_name>/scenes/<scene_id>", methods=["PUT"])
@authenticated
def recall_scene(bridge_name, scene_id):
    """
    Recalls a scene
    """
    bridge = device_manager.get_bridge(bridge_name)
    with bridge.start_session() as conn:
        conn.scene.recall_scene(scene_id)

        return response("Success", ResponseStatus.OK)
