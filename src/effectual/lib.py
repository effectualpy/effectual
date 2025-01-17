from hashlib import md5
from pathlib import Path


def getHash(filePath: Path) -> str:
    """Creates an MD5 Hash from a file

    Args:
        filePath (Path): Path to the file

    Returns:
        str: String of the hash
    """
    with open(filePath, "rb") as file:
        fileHash = md5(file.read()).hexdigest()
    return fileHash
