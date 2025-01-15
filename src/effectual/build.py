import hashlib
import os
import shutil
import zipfile
from pathlib import Path
from time import perf_counter
from typing import Any

from .colors import completeColor, fileColor, folderColor, tagColor
from .config import dumpHashes, loadConfig, loadToml
from .transformations import minifyFile, minifyToString


def bundleFiles(
    sourceDirectory: Path = Path("./src/"),
    outputDirectory: Path = Path("./out"),
    outputFileName: str = "bundle.pyz",
    compressionLevel: int = 5,
    minification: bool = True,
    freshHash: bool = False,
) -> None:
    """Bundles dependencies and scripts into a single .pyz archive

    Args:
        sourceDirectory (Path): Source directory which must contain a __main__.py script
        outputDirectory (Path): Output directory for the bundle
        outputFileName (str): Name of the output bundle
        compressionLevel (int): Compression level for the bundle from 0-9
        minification (bool): If the scripts should be minified
        freshHash (bool): Is the pyproject hash different then previously?
    """
    outputDirectory.mkdir(parents=True, exist_ok=True)
    outputPath: Path = outputDirectory / outputFileName

    with zipfile.ZipFile(
        outputPath,
        "w",
        compresslevel=compressionLevel,
        compression=zipfile.ZIP_DEFLATED,
    ) as bundler:
        cachePath: Path = Path("./.effectual_cache/cachedPackages")
        if cachePath.exists():
            if Path.iterdir(cachePath):
                totalSize: int = sum(
                    cachedFile.stat().st_size
                    for cachedFile in cachePath.rglob("*")
                    if cachedFile.is_file()
                )
                print(
                    f"{tagColor('bundling')}   || uv dependencies {folderColor(totalSize)}"  # noqa: E501
                )
                for cachedFile in cachePath.rglob("*"):
                    if cachedFile.is_dir() and not any(cachedFile.iterdir()):
                        continue
                    stringCachedFile = str(cachedFile)
                    if (
                        cachedFile.suffix
                        in (".pyc", ".pyd", "pyi", ".exe", ".typed", ".so")
                        or "__pycache__" in stringCachedFile
                        or ".dist-info" in stringCachedFile
                        or ".lock" in stringCachedFile
                    ):
                        continue
                    else:
                        if cachedFile.suffix == ".py" and minification and freshHash:
                            minifyFile(cachedFile)
                        arcName: str = str(cachedFile.relative_to(cachePath))
                        bundler.write(cachedFile, arcname=arcName)

        for pyFile in sourceDirectory.rglob("*.py"):
            print(f"{tagColor('bundling')}   || {pyFile.name} {fileColor(pyFile)}")
            if minification:
                fileContents = minifyToString(pyFile)
                bundler.writestr(zinfo_or_arcname=pyFile.name, data=fileContents)
            else:
                bundler.write(pyFile, arcname=pyFile.name)

    print(f"{tagColor('OUTPUT')}     || {outputFileName} {fileColor(outputPath)}")


def dependencies() -> None:
    """Installs relevant dependencies"""
    packages: list[str] = (
        loadToml("./pyproject.toml").get("project").get("dependencies")
    )

    if len(packages) != 0:
        arguments: list[str] = ["--no-compile", "--quiet", "--no-binary=none"]

        pathToInstallTo: str = "./.effectual_cache/cachedPackages"
        argumentString: str = " ".join(arguments)

        if Path(pathToInstallTo).exists():
            shutil.rmtree(pathToInstallTo)

        for key in packages:
            print(f"{tagColor('installing')} || {key}")
            os.system(
                f'uv pip install "{key}" {argumentString} --target {pathToInstallTo}'
            )


def getHash(filePath: Path) -> str:
    """Creates an MD5 Hash from a file

    Args:
        filePath (Path): Path to the file

    Returns:
        str: String of the hash
    """
    with open(filePath, "rb") as file:
        fileHash = hashlib.md5(file.read()).hexdigest()
    return fileHash


def main() -> None:
    """Entrypoint

    Raises:
        RuntimeError: In the event there is no source directory
    """

    configData: dict[str, Any] = loadConfig("./pyproject.toml")

    sourceDirectory: Path = Path(configData.get("sourceDirectory", "src/"))
    outputDirectory: Path = Path(configData.get("outputDirectory", "out/"))
    outputFileName: str = configData.get("outputFileName", "bundle.pyz")
    compressionLevel: int = max(
        0, min(9, configData.get("compressionLevel", 5))
    )  # Default level if not set
    minification: bool = configData.get("minification", True)

    if not sourceDirectory.is_dir():
        raise RuntimeError(
            f"Source directory {sourceDirectory} does not exist or is not a directory."
        )

    uvHashPath: Path = Path("./.effectual_cache/pyprojectHash.toml")
    currentHash: dict[str, dict[str, str]] = dict()

    startTime = perf_counter()

    Path("./.effectual_cache/").mkdir(parents=True, exist_ok=True)
    currentHash["hashes"] = dict()
    currentHash["hashes"]["pyproject"] = getHash(Path("./pyproject.toml"))
    currentHash["hashes"]["lock"] = getHash(Path("./uv.lock"))

    freshHash: bool = True  # Whether or not to re-optimize deps

    if uvHashPath.exists():
        lastHash: dict[str, Any] = loadToml(uvHashPath).get("hashes")
        if currentHash["hashes"] != lastHash:
            with open(uvHashPath, "w") as file:
                dumpHashes(currentHash, file)
            dependencies()
        else:
            freshHash = False
    else:
        with open(uvHashPath, "x") as file:
            dumpHashes(currentHash, file)
        dependencies()

    bundleFiles(
        sourceDirectory,
        outputDirectory,
        outputFileName,
        compressionLevel,
        minification,
        freshHash,
    )
    endTime = perf_counter()

    print(completeColor(f"Completed in {endTime - startTime:.4f}s"))


if "__main__" == __name__:
    main()
