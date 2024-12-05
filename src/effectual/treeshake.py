from pathlib import Path

from transformations import minifyFile


def cleanPackages(file: Path) -> None:
    stringFile: str = str(file)
    if (
        file.suffix in (".pyc", ".pyd", ".exe", ".typed")
        or "__pycache__" in stringFile
        or ".dist-info" in stringFile
        or ".lock" in stringFile
    ):
        try:
            file.unlink()
        except PermissionError:
            pass
    elif file.suffix == ".py":
        minifyFile(file)
