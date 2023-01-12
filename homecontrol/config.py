import json
from os.path import expanduser, exists
from typing import Any, Dict


class Config:
    """
    Handles a config file
    """

    # Path to the config file this class manages
    _path: str

    # Current loaded data of this config
    data: Dict

    def __init__(self, path) -> None:
        """
        Constructor - loads the config from the given path, following the format
        ~/CONFIG_FILEPATH/path
        """
        self._path = path

        self.load()

    def save(self):
        """
        Saves the config
        """
        Config.save_to_json(self._path, self.data)

    def load(self):
        """
        Load the config (if it exists)
        """
        if Config.does_exist(self._path):
            self.data = Config.load_from_json(self._path)
        else:
            self.data = {}

    @staticmethod
    def get_filepath(path: str) -> str:
        """
        Returns the path to a config file - prefers ones in the current
        working directory
        """
        if exists(path):
            # Current working dir
            return path
        else:
            # TODO: Modify for other platforms
            return f"/etc/homecontrol/{path}"

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
