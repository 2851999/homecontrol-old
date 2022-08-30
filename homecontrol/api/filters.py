from abc import ABC, abstractmethod
from ast import Str
import json
from typing import Dict, List, Type

from homecontrol.helpers import SubscriptableClass


class Filter(ABC):
    """
    Base class for filters
    """

    # Param the filter acts on
    param: str

    # Value this filter looks for
    value: str

    def __init__(self, param: Str, value: str) -> None:
        self.param = param
        self.value = value

    @abstractmethod
    def apply(self, items: List[SubscriptableClass]):
        """
        Applies this filter to a list of items
        """


class EqualsFilter(Filter):
    """
    Equality filter
    """

    def __init__(self, param: str, value: str) -> None:
        super().__init__(param, value)

    def apply(self, items: List[SubscriptableClass]):
        """
        Applies this filter to a list of items and returns the result
        """
        return [item for item in items if item[self.param] == self.value]


class Filters:
    """
    For handling a group of filters
    """

    # List of all possible filters
    FILTERS: Dict[str, Type[Filter]] = {"eq": EqualsFilter}

    _filters: List[Filter]

    def __init__(self, filters_json: str):
        """
        Loads a set of filters from JSON from a query URL

        Expects a format e.g. {"room[eq]": "room_id", "name[eq]": "room_name"}

        :param filters: JSON representing the filters from the URL
        """
        self._filters = []

        filters = json.loads(filters_json)

        for key, value in filters.items():
            if "[" not in key or "]" not in key:
                raise ValueError(f"No operator found in key '{key}'")
            split = key.split("[")
            param = split[0]
            operator = split[1][:-1]

            if operator not in Filters.FILTERS:
                raise ValueError(f"No filter found with the operator '{operator}'")
            self._filters.append(Filters.FILTERS[operator](param=param, value=value))

    def apply(self, items: List[SubscriptableClass]) -> List[SubscriptableClass]:
        """
        Applies the filters to a list of items and returns the result
        """
        for fil in self._filters:
            items = fil.apply(items)
        return items
