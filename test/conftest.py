"""Useful for testing."""
# stdlib
import os

# 3rd Party Import
import pytest

# Local
import pygrib


@pytest.fixture()
def samplegribfile(filename):
    """Open a grib file from the sampledata folder."""
    sampledir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../sampledata"
    )
    print(os.path.join(sampledir, filename))
    return pygrib.open(os.path.join(sampledir, filename))
