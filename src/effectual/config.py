from typing import Any

import rtoml


def loadConfig(configPath: str) -> dict[Any, Any]:
    """Loads effectual config from a file

    Args:
        configPath (str): Path to the config file

    Raises:
        RuntimeError: Invalid TOML format
        RuntimeError: No configuration file found

    Returns:
        dict: _description_
    """
    try:
        with open(configPath, "r", encoding="utf-8") as file:
            configData: dict[Any, Any] = dict(rtoml.load(file))
            if configData is None:
                configData = {
                    "sourceDirectory": "./src/",
                    "outputDirectory": "./dist/",
                    "outputFileName": "bundle.pyz",
                    "minification": True,
                    "compressionLevel": 5,
                }
            else:
                configData = configData.get("tool").get("effectual")  # type: ignore

    except ValueError as e:
        raise RuntimeError(f"Invalid TOML in {configPath}: {e}")
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file {configPath} not found.")

    return configData
