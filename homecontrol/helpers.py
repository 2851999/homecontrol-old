import json
from dataclasses import dataclass, fields
from typing import Dict, List, Type


def dataclass_from_dict(class_type: dataclass, dictionary: Dict):
    """
    Converts a dictionary of values into a particular dataclass type
    """
    field_set = {f.name for f in fields(class_type) if f.init}
    filtered_arg_dict = {k: v for k, v in dictionary.items() if k in field_set}
    return class_type(**filtered_arg_dict)


def dataclass_list_from_dict(class_type: dataclass, lst: List[Dict]):
    """
    Converts a list of dictionary of values into a list of a particular dataclass type
    """
    classes = []
    for dictionary in lst:
        classes.append(dataclass_from_dict(class_type, dictionary))
    return classes


def dicts_to_list(class_type: Type, list_of_dicts: List[Dict]):
    """
    Converts a list of dictionaries to a list of a certain object type
    """
    result = []
    for dictionary in list_of_dicts:
        result.append(class_type(dictionary))
    return result


def object_to_dict(obj):
    """
    Converts an object to a dictionary
    """
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


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
