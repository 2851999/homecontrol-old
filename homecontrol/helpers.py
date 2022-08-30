from dataclasses import dataclass, fields
from typing import Dict


def dataclass_from_dict(class_type: dataclass, dictionary: Dict):
    """
    Converts a dictionary of values into a particular dataclass type
    """
    field_set = {f.name for f in fields(class_type) if f.init}
    filtered_arg_dict = {k: v for k, v in dictionary.items() if k in field_set}
    return class_type(**filtered_arg_dict)


class ResponseStatus:
    """
    Various response codes
    """

    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404


class SubscriptableClass:
    """
    Useful for making classes subscriptable
    """

    def __getitem__(self, item):
        return getattr(self, item)
