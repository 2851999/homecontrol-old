from homecontrol.aircon.structs import ACFanSpeed, ACMode, ACState, ACSwingMode
from homecontrol.api.database.exceptions import DatabaseError
from homecontrol.database.mysql.connection import DatabaseConnection
from homecontrol.exceptions import ResourceNotFoundError


class Aircon:
    """Handles air conditioning in the database"""

    # Users table name
    TABLE_AIRCON_STATES = "aircon_states"

    _connection: DatabaseConnection

    def __init__(self, connection: DatabaseConnection) -> None:
        self._connection = connection

    def create_table(self):
        """
        Creates the table required for storing users in the database
        """
        self._connection.create_table(
            self.TABLE_AIRCON_STATES,
            [
                "uuid VARCHAR(255)",
                "name VARCHAR(255)",
                "power TINYINT",
                "prompt_tone TINYINT",
                "target TINYINT",
                "mode TINYINT",
                "fan TINYINT",
                "swing TINYINT",
                "eco TINYINT",
                "turbo TINYINT",
                "farenheit TINYINT",
            ],
        )

    def add_state(self, uuid: str, name: str, state: ACState):
        """
        Adds an aircon state to the database
        """
        self._connection.insert_values(
            self.TABLE_AIRCON_STATES,
            [
                (
                    uuid,
                    name,
                    state.power,
                    state.prompt_tone,
                    state.target,
                    int(state.mode),
                    int(state.fan),
                    int(state.swing),
                    state.eco,
                    state.turbo,
                    state.fahrenheit,
                )
            ],
        )
        self._connection.commit()

    def find_state_by_id(self, state_id: str) -> ACState:
        """
        Obtains an ACState object from the database given its ID

        Raises:
            ResourceNotFoundError: If the user with the given ID is not found
            DatabaseError: If for some reason more than one state has the given
                           ID
        """
        state_data = self._connection.select_values(
            self.TABLE_AIRCON_STATES,
            [
                "power",
                "prompt_tone",
                "target",
                "mode",
                "fan",
                "swing",
                "eco",
                "turbo",
                "farenheit",
            ],
            where=(f"uuid=%s", (state_id,)),
        )

        if len(state_data) == 0:
            raise ResourceNotFoundError(
                f"Aircon state with the UUID '{state_id}' could not be found in the database"
            )
        if len(state_data) > 1:
            raise DatabaseError(
                f"{len(state_data)} aircon states were found to have the UUID '{state_id}' in the database"
            )
        state_data = state_data[0]
        return ACState(
            power=bool(state_data[0]),
            prompt_tone=bool(state_data[1]),
            target=int(state_data[2]),
            mode=ACMode(state_data[3]),
            fan=ACFanSpeed(state_data[4]),
            swing=ACSwingMode(state_data[5]),
            eco=bool(state_data[6]),
            turbo=bool(state_data[7]),
            fahrenheit=bool(state_data[8]),
            # These aren't needed
            indoor=0,
            outdoor=0,
        )
