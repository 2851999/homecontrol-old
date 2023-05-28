import json
from typing import Dict, Optional

from requests import Response

from homecontrol.client.exceptions import APIClientError
from homecontrol.helpers import ResponseStatus


def get_url_search_params(filters: Optional[Dict]) -> str:
    """
    Returns url search parameters given the filters to put into it
    """
    if filters:
        return f"?filters={json.dumps(filters)}"
    return ""


def check_response(response: Response, error_message: str):
    """Checks whether a response is ok, and if not raises an APIClientError
    with any message in the response if applicable"""
    if response.status_code != ResponseStatus.OK:
        try:
            decoded_response = response.json()
            if "message" in decoded_response:
                api_error_message = decoded_response["message"]
                error_message += (
                    f"\n\nError message from homecontrol API: {api_error_message}"
                )
        except json.JSONDecodeError:
            pass
        raise APIClientError(error_message)
