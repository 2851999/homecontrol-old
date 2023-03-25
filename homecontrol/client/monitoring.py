from datetime import datetime
from typing import List, Optional
from homecontrol.api.monitoring import TempDataPoint
from homecontrol.client.exceptions import APIError
from homecontrol.helpers import (
    ResponseStatus,
    dataclass_list_from_dict,
)
from homecontrol.client.session import APISession


class Monitoring:
    """
    Handles monitoring endpoints
    """

    _session: APISession

    def __init__(self, session: APISession) -> None:
        self._session = session

    def get_temps(
        self,
        device_name: str,
        count: Optional[int] = None,
        step: Optional[int] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[TempDataPoint]:
        """
        Returns a list of scenes
        """
        response = self._session.get(
            "/monitoring/temps",
            params={
                "device_name": device_name,
                "count": count,
                "step": step,
                "start": start,
                "end": end,
            },
        )
        if response.status_code != ResponseStatus.OK:
            raise APIError(
                f"An error occurred obtaining temperatures for the device '{device_name}'"
            )
        return dataclass_list_from_dict(TempDataPoint, response.json())
