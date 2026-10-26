import os
import signal
import subprocess
import time
import zipfile
from pathlib import Path
from typing import Any

from watchfiles import watch

from .colors import completeColor, fileColor, tagColor
from .tomlHash import loadConfig


def bundle(sourceDirectory: Path, outputFile: Path) -> None:
    """Bundles scripts into a single .pyz archive

    Args:
        sourceDirectory (Path): Path to the original python scripts
    """
    startTime = time.perf_counter()

    with zipfile.ZipFile(outputFile, "w") as bundler:
        for pyFile in sourceDirectory.rglob("*.py"):
            # ^ TODO: if no new files added don't rerun this
            print(f"{tagColor('bundling')}   || {pyFile.name} {fileColor(pyFile)}")
            bundler.write(pyFile, arcname=pyFile.name)

    endTime = time.perf_counter()

    print(completeColor(f"Completed in {endTime - startTime:.4f}s"))


def main() -> None:
    """Super fast bundling for the 'efec dev' command"""
    configData: dict[Any, Any] = loadConfig("./pyproject.toml")
    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))
    outputFileName: Path = Path(configData.get("outputFileName", "bundle.pyz"))
    devBundlePath: Path = Path("./.effectual_cache/dev/")

    devBundlePath.mkdir(parents=True, exist_ok=True)
    outputFile: Path = devBundlePath / outputFileName

    bundle(sourceDirectory, outputFile)
    runCommand = subprocess.Popen(["uv", "run", outputFile], shell=True)

    pidSet: set[int] = set()
    pidSet.add(runCommand.pid)  # Adds PID of runCommand to the set

    for change in watch(sourceDirectory, debounce=600):
        # TODO: Also need to make sure this reloads on changes in
        # pyproject.toml and uv.lock (effects file behaviour)
        print(f"{tagColor('reloaded')}   || file change detected")
        for pid in pidSet.copy():  # Tries killing previous instance
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass
            pidSet.remove(pid)
        bundle(sourceDirectory, outputFile)
        runCommand = subprocess.Popen(["uv", "run", outputFile], shell=True)
        pidSet.add(runCommand.pid)


if __name__ == "__main__":
    main()
