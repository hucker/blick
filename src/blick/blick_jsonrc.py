"""
Allow the usage of an JSON file as an RC file.  
"""
import json
import pathlib

from .blick_exception import BlickException
from .blick_rc import BlickRC


class BlickJsonRC(BlickRC):
    """
    Loads configurations from JSON files. Extends BlickRC.
    """

    def __init__(self, cfg: str, section: str):
        section_data = self._load_config(cfg, section)

        self.expand_attributes(section_data)

    def _load_config(self, cfg: str, section: str) -> dict:
        """Loads and returns the requested section from a JSON file."""
        cfg_file = pathlib.Path(cfg)
        try:
            with cfg_file.open("rt", encoding="utf8") as j:
                config_data = json.load(j)
        except (FileNotFoundError, json.JSONDecodeError, AttributeError, PermissionError) as error:
            raise BlickException(f"JSON config {cfg} error: {error}") from error

        return config_data.get(section, {})
