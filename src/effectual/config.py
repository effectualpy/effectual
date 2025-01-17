from io import TextIOWrapper
from pathlib import Path
from typing import Any

import rtoml


def loadToml(tomlFile: str | Path) -> dict[str, Any]:
    """Loads a toml file from a specific path to a dictionary

    Args:
        pathToToml (str): Path of a toml file

    Raises:
        RuntimeError: Toml file is incorrectly configured
        RuntimeError: Toml file is can't be located

    Returns:
        dict[Any, Any]: Dictionary of toml file contents
    """
    try:
        with open(tomlFile, "r", encoding="utf-8") as file:
            return dict(rtoml.load(file))
    except ValueError as e:
        raise RuntimeError(f"Invalid TOML in {tomlFile}: {e}")
    except FileNotFoundError:
        raise RuntimeError(f"TOML file {tomlFile} not found.")


def loadConfig(configPath: str = "./pyproject.toml") -> dict[Any, Any]:
    """Loads effectual config from a file

    Args:
        configPath (str): Path to the config file

    Returns:
        dict: Dictionary containing effectual config
    """
    configData: dict[str, Any] = loadToml(configPath)
    try:
        configData = configData["tool"]["effectual"]
    except KeyError:
        configData = {
            "sourceDirectory": "./src/",
            "outputDirectory": "./dist/",
            "outputFileName": "bundle.pyz",
            "minification": True,
            "compressionLevel": 5,
        }

    return configData


def dumpHashes(hashesToDump: dict[str, dict[str, str]], file: TextIOWrapper) -> None:
    """Dumps hashes in a specific format to a toml file

    Args:
        hashesToDump (dict[str, dict[str, str]]): Dictionary of hashes to dump as toml
        file (_type_): File object
    """
    rtoml.dump(hashesToDump, file, pretty=False)
