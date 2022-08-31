import json
from typing import Dict, List, Type


def kelvin_to_mirek(kelvin: int):
    """
    Converts kelvin to mirek
    """
    return int(1000000.0 / kelvin)


def mirek_to_kelvin(mirek: int):
    """
    Converts mirek to kelvin
    """
    return int(1000000.0 / mirek)


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
