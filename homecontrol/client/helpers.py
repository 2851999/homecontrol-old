import json
from typing import Dict, Optional


def get_url_search_params(filters: Optional[Dict]) -> str:
    """
    Returns url search parameters given the filters to put into it
    """
    if filters:
        return f"?filters={json.dumps(filters)}"
    return ""
