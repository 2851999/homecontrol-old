import json
from os.path import expanduser, exists
from typing import Any, Dict


class Config:
    """
    Handles config files
    """

    CONFIG_FILEPATH: str = "/homecontrol"

    @staticmethod
    def get_filepath(path: str) -> str:
        """
        Returns the full path to a config file given its path in the config
        directory e.g. ~/CONFIG_FILEPATH/path
        """
        # Obtain the home directory
        home_path = expanduser("~")
        return f"{home_path}{Config.CONFIG_FILEPATH}/{path}"

    @staticmethod
    def load_from_json(path: str) -> Any:
        """
        Returns config from a json file located at ~/CONFIG_FILEPATH/path
        """
        file_path = Config.get_filepath(path)

        with open(file_path, encoding="utf-8") as config_file:
            return json.load(config_file)

    @staticmethod
    def save_to_json(path: str, data: Dict) -> Any:
        """
        Saves config to a json file located at ~/CONFIG_FILEPATH/path
        """

        # Obtain the home directory
        file_path = Config.get_filepath(path)

        with open(file_path, "w", encoding="utf-8") as config_file:
            json.dump(data, config_file)

    @staticmethod
    def does_exist(path: str) -> bool:
        """
        Returns whether a config file exists
        """
        return exists(Config.get_filepath(path))
