from uuid import uuid4

from homecontrol.aircon.aircon import ACDevice
from homecontrol.aircon.manager import ACManager
from homecontrol.api.database.client import APIDatabaseClient
from homecontrol.api.exceptions import APIError
from homecontrol.exceptions import DeviceNotRegisteredError
from homecontrol.helpers import ResponseStatus


def save_state(database_client: APIDatabaseClient, name: str, device: ACDevice) -> str:
    """Saves the current state of an AC device to the database

    Args:
        device (ACDevice): The air conditioning unit to the save the state
                              of

    Returns:
        str: state_id of the added state
    """

    state_id = str(uuid4())
    current_state = device.get_state()

    with database_client.connect() as conn:
        conn.aircon.add_state(uuid=state_id, name=name, state=current_state)
    return state_id


def recall_state(database_client: APIDatabaseClient, state_id: str, device: ACDevice):
    """Recalls and assigns a saved AC state for a device

    Args:
        state_id (str): ID of the saved state
        device (ACDevice): Device to recall the state to

    """

    with database_client.connect() as conn:
        state = conn.aircon.find_state_by_id(state_id)

    device.set_state(state)
