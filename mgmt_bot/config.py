import logging
import sys
from json import load
from json.decoder import JSONDecodeError
from pathlib import Path

config_json_path = Path("config.json")
log = logging.getLogger(__name__)


def _get_config() -> dict:
    log.debug("Using %s as config file", config_json_path)
    try:
        with config_json_path.open("r", encoding="utf-8") as config_file:
            config = load(config_file)
    except FileNotFoundError:
        log.critical("%s not found.", config_json_path)
        sys.exit(1)
    except JSONDecodeError:
        log.critical("Failed to parse %s", config_json_path)
        sys.exit(1)
    log.debug(config)
    return config


config = _get_config()

__all__ = ["config"]
