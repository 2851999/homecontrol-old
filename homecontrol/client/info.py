from typing import List
from homecontrol.api.structs import APIInfo, Room
from homecontrol.client.exceptions import APIError
from homecontrol.helpers import ResponseStatus, dataclass_from_dict
from homecontrol.client.session import APISession


class Info:
    """
    Handles info endpoints
    """

    _session: APISession

    def __init__(self, session: APISession) -> None:
        self._session = session

    def get_info(self) -> str:
        """
        Returns the info about the homecontrol API
        """
        response = self._session.get("/info")
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occurred obtaining info from the homecontrol API")
        return dataclass_from_dict(APIInfo, response.json())
