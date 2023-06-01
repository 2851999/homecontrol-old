from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict


class Config:
    """
    Handles a config file
    """

    # Path to the config file this class manages
    _path: Path

    # Current loaded data of this config
    data: Dict

    def __init__(self, file_name: str) -> None:
        """
        Loads the config using the given file name assuming it is either
        in the current working directory or it is located in the general
        config dir (currently /etc/homecontrol) - First one found is used
        """
        self._path = Path(file_name)

        self.load()

    def save(self):
        """
        Saves the config
        """
        with open(self.get_filepath(), "w", encoding="utf-8") as config_file:
            json.dump(self.data, config_file)

    def load(self):
        """
        Load the config (if it exists)
        """
        if self.does_exist():
            with open(self.get_filepath(), encoding="utf-8") as config_file:
                self.data = json.load(config_file)
        else:
            self.data = {}

    def get_filepath(self) -> Path:
        """
        Returns the path to a config file - prefers ones in the current
        working directory
        """
        if self._path.exists():
            # Current working dir
            return self._path
        else:
            # TODO: Modify for other platforms
            return Path("/etc/homecontrol/") / self._path

    def does_exist(self) -> bool:
        """
        Returns whether a config file exists
        """
        return self.get_filepath().exists()
