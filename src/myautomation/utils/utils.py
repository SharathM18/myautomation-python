import hashlib
import tempfile
import uuid
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import pendulum


def get_uuid() -> str:
    """
    Generate a random UUID4.

    Usage:
        get_uuid()
        -> '116a0d88-ee35-4ab8-9c38-9fffe9674a92'
    """
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """
    Generate a timestamp.

    Usage:
        get_timestamp()
        -> '20260524_204010'
    """
    return pendulum.now().format("YYYYMMDD_HHmmss")


def md5_hash(file_path: Path) -> str:
    """
    Calculate the MD5 hash of a file.

    Usage:
        md5_hash(Path("file.txt"))
        -> 'd41d8cd98f00b204e9800998ecf8427e'
    """
    hash_md5 = hashlib.md5()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


@contextmanager
def get_temp_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory and automatically remove it
    when the context manager exits.

    Usage:
        with get_temp_dir() as tmp_dir:
            # logic goes here
            ...
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists.

    Usage:
        ensure_directory(Path("./outs"))
        ensure_directory(Path("./outs/logs/pipeline"))
    """
    path.mkdir(parents=True, exist_ok=True)
