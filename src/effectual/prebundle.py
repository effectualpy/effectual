import os
from pathlib import Path

from .colors import errorColor, tagColor
from .tomlHash import loadToml


def preparePackages() -> None:
    """Installs relevant dependencies"""
    try:
        packages: list[str] = (
            loadToml("./pyproject.toml").get("project").get("dependencies")  # ty: ignore[unresolved-attribute]
        )

        if len(packages) != 0:
            arguments: list[str] = ["--no-compile", "--quiet", "--no-binary=none"]

            pathToInstallTo: str = "./.effectual_cache/cachedPackages"
            argumentString: str = " ".join(arguments)

            if Path(pathToInstallTo).exists():
                __import__("shutil").rmtree(pathToInstallTo)  # Lazy import

            for key in packages:
                print(f"{tagColor('installing')} || {key}")
                os.system(
                    f'uv pip install "{key}" {argumentString} --target {pathToInstallTo}'
                )
    except ConnectionError:
        print(errorColor("No internet connection"))
