from homecontrol.api.database.exceptions import DatabaseError
from homecontrol.api.structs import RoomState
from homecontrol.database.mysql.connection import DatabaseConnection
from homecontrol.exceptions import ResourceNotFoundError


class Rooms:
    """Handles rooms in the database"""

    # Users table name
    TABLE_ROOM_STATES = "room_states"

    _connection: DatabaseConnection

    def __init__(self, connection: DatabaseConnection) -> None:
        self._connection = connection

    def create_table(self):
        """
        Creates the table required for storing users in the database
        """
        self._connection.create_table(
            self.TABLE_ROOM_STATES,
            [
                "uuid VARCHAR(255)",
                "name VARCHAR(255)",
                "icon VARCHAR(255)",
                "room_name VARCHAR(255)",
                "ac_device VARCHAR(255)",
                "ac_state_id VARCHAR(255)",
                "hue_scene_id VARCHAR(255)",
                "broadlink_device VARCHAR(255)",
                "broadlink_actions VARCHAR(255)",
            ],
        )

    def add_state(self, state: RoomState):
        """
        Adds an aircon state to the database
        """
        self._connection.insert_values(
            self.TABLE_ROOM_STATES,
            [
                (
                    state.state_id,
                    state.name,
                    state.icon,
                    state.room_name,
                    state.ac_device_name,
                    state.ac_state_id,
                    state.hue_scene_id,
                    state.broadlink_device_name,
                    ",".join(state.broadlink_actions),
                )
            ],
        )
        self._connection.commit()

    def find_state_by_id(self, state_id: str) -> RoomState:
        """
        Obtains an ACState object from the database given its ID

        Raises:
            ResourceNotFoundError: If the user with the given ID is not found
            DatabaseError: If for some reason more than one state has the given
                           ID
        """
        state_data = self._connection.select_values(
            self.TABLE_ROOM_STATES,
            [
                "name",
                "icon",
                "room_name",
                "ac_device_name",
                "ac_state_id",
                "hue_scene_id",
                "broadlink_device_name",
                "broadlink_actions",
            ],
            where=(f"uuid=%s", (state_id,)),
        )

        if len(state_data) == 0:
            raise ResourceNotFoundError(
                f"Room state with the UUID '{state_id}' could not be found in the database"
            )
        if len(state_data) > 1:
            raise DatabaseError(
                f"{len(state_data)} room states were found to have the UUID '{state_id}' in the database"
            )
        state_data = state_data[0]
        return RoomState(
            state_id=state_id,
            name=state_data[0],
            icon=state_data[1],
            room_name=state_data[2],
            ac_device_name=state_data[3],
            ac_state_id=state_data[4],
            hue_scene_id=state_data[5],
            broadlink_device_name=state_data[6],
            broadlink_actions=state_data[7].split(","),
        )
