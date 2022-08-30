from typing import Dict, List, Type, get_args, get_origin, get_type_hints


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


class HueAPIObject:
    """
    Useful for creating class structures for the responses from
    the Hue API
    """

    def __init__(self, dictionary: Dict):
        types = get_type_hints(self)
        for key, value in dictionary.items():
            current_type = types[key]
            if get_origin(current_type) == list:
                list_type = get_args(current_type)[0]
                setattr(self, key, dicts_to_list(list_type, dictionary[key]))
            else:
                setattr(self, key, current_type(value))
