import hashlib
from multiprocessing import Pool
from pathlib import Path


def getFilehash(filePath: Path) -> str:
    """Gets the file hash of a single python script

    Args:
        filePath (Path): Path to a file

    Returns:
        str: Hash of the file
    """
    with open(filePath, "rb") as file:
        fileHash = hashlib.sha1(file.read()).hexdigest()
    return fileHash


def getAllHashes(sourceDirectory: Path, fileExtension: str) -> set[str]:
    """Gets all hashes in directory

    Args:
        sourceDirectory (Path): Path to a folder containing files

    Returns:
        set[str]: Set containing paths and hashes
    """

    with Pool() as pool:
        hashList: set[str] = set(
            pool.map(getFilehash, sourceDirectory.glob(f"*.{fileExtension}"))
        )
    return hashList
