import importlib
import os
import shutil
import zipfile
from pathlib import Path
from time import perf_counter
from typing import Any

import rtoml

from .colors import completeColor, fileColor, folderColor, tagColor
from .config import loadConfig
from .fileHash import getFilehash
from .minifier import minifyFile, minifyToString


def bundleFiles(
    sourceDirectory: Path,
    outputDirectory: Path,
    outputFileName: str,
    compressionLevel: int,
    minification: bool,
) -> None:
    """Bundles dependencies and scripts into a single .pyz archive

    Args:
        sourceDirectory (Path): Source directory which must contain a __main__.py script
        outputDirectory (Path): Output directory for the bundle
        outputFileName (str): Name of the output bundle
        compressionLevel (int): Compression level for the bundle from 0-9
        minification (bool): If the scripts should be minified
    """
    outputDirectory.mkdir(parents=True, exist_ok=True)
    outputPath: Path = outputDirectory / outputFileName

    if outputPath.exists():
        outputPath.unlink()

    with zipfile.ZipFile(
        outputPath,
        "w",
        compresslevel=compressionLevel,
        compression=zipfile.ZIP_DEFLATED,
    ) as bundler:
        cachePath: Path = Path("./.effectual_cache/cachedPackages")

        totalSize: int = int(0)
        for cachedFile in cachePath.rglob("*"):
            if cachedFile.is_dir() and not any(cachedFile.iterdir()):
                continue
            totalSize += cachedFile.stat().st_size
            arcName = cachedFile.relative_to(cachePath)
            bundler.write(cachedFile, arcname=arcName)

        print(f"{tagColor('bundling')}   || uv dependencies {folderColor(totalSize)}")

        for pyFile in sourceDirectory.rglob("*.py"):
            print(f"{tagColor('bundling')}   || {pyFile.name} {fileColor(pyFile)}")
            if minification:
                fileContents = minifyToString(pyFile)
                bundler.writestr(zinfo_or_arcname=pyFile.name, data=fileContents)
            else:
                bundler.write(pyFile, arcname=pyFile.name)

    print(f"{tagColor('OUTPUT')}     || {outputFileName} {fileColor(outputPath)}")


def dependencies(minify: bool) -> None:
    with open("./pyproject.toml", "r", encoding="utf-8") as file:
        packages: list[str] = dict(rtoml.load(file)).get("project").get("dependencies")  # type: ignore

    arguments: list[str] = ["--no-compile", "--quiet", "--no-binary=none", "--no-cache"]

    pathToInstallTo: str = "./.effectual_cache/cachedPackages"
    argumentString: str = " ".join(arguments)

    if Path(pathToInstallTo).exists():
        shutil.rmtree(pathToInstallTo)

    for key in packages:
        print(f"{tagColor('installing')} || {key}")
        os.system(f'uv pip install "{key}" {argumentString} --target {pathToInstallTo}')

    print(f"{tagColor('optimizing')} || {', '.join(packages)}")

    multiprocessing = importlib.import_module("multiprocessing")

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(optimizeDependencies, Path(pathToInstallTo).rglob("*"))


def optimizeDependencies(file: Path) -> None:
    stringFile:str = str(file)
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


def main() -> None:
    """Entrypoint

    Raises:
        RuntimeError: In the event there is no source directory
    """

    configData: dict[Any, Any] = loadConfig("./pyproject.toml")

    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))
    outputDirectory: Path = Path(configData.get("outputDirectory", "out/"))
    outputFileName: str = configData.get("outputFileName", "bundle.pyz")
    compressionLevel: int = max(
        0, min(9, configData.get("compressionLevel", 5))
    )  # Default level if not set
    global minification
    minification = configData.get("minification", True)

    if not sourceDirectory.is_dir():
        raise RuntimeError(
            f"Source directory {sourceDirectory} does not exist or is not a directory."
        )

    uvHashPath: Path = Path("./.effectual_cache/pyprojectHash.toml")
    currentHash: dict[str, dict[str, str]] = dict()

    startTime = perf_counter()

    Path("./.effectual_cache/").mkdir(parents=True, exist_ok=True)
    currentHash["hashes"] = dict()
    currentHash["hashes"]["pyproject"] = getFilehash(Path("./pyproject.toml"))
    currentHash["hashes"]["lock"] = getFilehash(Path("./uv.lock"))

    if uvHashPath.exists():
        with open(uvHashPath, "r") as file:
            lastHash: dict[Any, Any] = dict(rtoml.load(file)).get("hashes")
        if currentHash["hashes"] != lastHash:
            with open(uvHashPath, "w") as file:
                rtoml.dump(currentHash, file)
            dependencies(minify=minification)
    else:
        with open(uvHashPath, "x") as file:
            rtoml.dump(currentHash, file)
        dependencies(minify=minification)

    bundleFiles(
        sourceDirectory,
        outputDirectory,
        outputFileName,
        compressionLevel,
        minification,
    )
    endTime = perf_counter()

    print(completeColor(f"Completed in {endTime - startTime:.4f}s"))


if "__main__" in __name__:
    main()
