"""pygrib context manager"""
__all__ = ["read"]

from typing import Iterator
from contextlib import contextmanager

from ._pygrib import open

@contextmanager
def read(file_path: str) -> Iterator[open]:
    """wraper for pygrib.open as a context manager"""

    grib_file = open(file_path)

    try:
        yield grib_file
    finally:
        grib_file.close()
