from homecontrol.api.structs import APIInfo
from homecontrol.client.helpers import check_response
from homecontrol.client.session import APISession
from homecontrol.helpers import dataclass_from_dict


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
        check_response(
            response, "An error occurred obtaining info from the homecontrol API"
        )
        return dataclass_from_dict(APIInfo, response.json())
