from homecontrol.api.database.aircon import Aircon
from homecontrol.api.database.rooms import Rooms
from homecontrol.api.database.users import Users
from homecontrol.database.mysql.connection import DatabaseConnection
from homecontrol.database.mysql.structs import DatabaseConnectionInfo


class APIDatabaseConnection(DatabaseConnection):
    """
    Handles a connection to the homecontrol database
    """

    users: Users
    aircon: Aircon
    rooms: Rooms

    def __init__(self, connection_info: DatabaseConnectionInfo) -> None:
        super().__init__(connection_info)

    def __enter__(self):
        super().__enter__()

        self.users = Users(self)
        self.aircon = Aircon(self)
        self.rooms = Rooms(self)
        return self

    def init_db(self):
        """
        Creates any necessary tables, for now just for Users
        """
        self.users.create_table()
        self.aircon.create_table()
        self.rooms.create_table()
