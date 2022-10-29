"""Collection of miscellaneous minor tests."""

import os
from tempfile import NamedTemporaryFile

import numpy as np
import pygrib
import pytest


def test_internal_value_type_of_runtime_error():
    grbindx = pygrib.index("../sampledata/gfs.grb", "shortName")
    with pytest.raises(RuntimeError) as e:
        grbindx.write("nonexistent/path")
    assert type(e.value.args[0]) is str


@pytest.mark.parametrize(
    "data_fname,scanning_mode,expected_values",
    [
        (
            "scanning_mode.grib2",
            0b00000000,
            np.array([[0, 1], [2, 3], [4, 5]], dtype=float),
        ),
        (
            "scanning_mode.grib2",
            0b10000000,
            np.array([[0, 1], [2, 3], [4, 5]], dtype=float),
        ),
        (
            "scanning_mode.grib2",
            0b01000000,
            np.array([[0, 1], [2, 3], [4, 5]], dtype=float),
        ),
        (
            "scanning_mode.grib2",
            0b00100000,
            np.array([[0, 3], [1, 4], [2, 5]], dtype=float),
        ),
        (
            "scanning_mode.grib2",
            0b00010000,
            np.array([[0, 1], [3, 2], [4, 5]], dtype=float),
        ),
        (
            "scanning_mode.grib2",
            0b00110000,
            np.array([[0, 3], [4, 1], [2, 5]], dtype=float),
        ),
        (
            "scanning_mode_with_bitmap.grib2",
            0b00000000,
            np.array([[np.nan, 1], [2, 3], [4, 5]], dtype=float),
        ),
        (
            "scanning_mode_with_bitmap.grib2",
            0b10000000,
            np.array([[np.nan, 1], [2, 3], [4, 5]], dtype=float),
        ),
        (
            "scanning_mode_with_bitmap.grib2",
            0b01000000,
            np.array([[np.nan, 1], [2, 3], [4, 5]], dtype=float),
        ),
        (
            "scanning_mode_with_bitmap.grib2",
            0b00100000,
            np.array([[np.nan, 3], [1, 4], [2, 5]], dtype=float),
        ),
        (
            "scanning_mode_with_bitmap.grib2",
            0b00010000,
            np.array([[np.nan, 1], [3, 2], [4, 5]], dtype=float),
        ),
        (
            "scanning_mode_with_bitmap.grib2",
            0b00110000,
            np.array([[np.nan, 3], [4, 1], [2, 5]], dtype=float),
        ),
    ],
)
def test_scanning_mode(data_fname, scanning_mode, expected_values):
    template_path = f"../sampledata/{data_fname}"
    with open(template_path, "rb") as f:
        template = f.read()
    scanning_mode_index = 0x6C
    bytes_ = (
        template[:scanning_mode_index]
        + scanning_mode.to_bytes(1, "big")
        + template[scanning_mode_index + 1 :]
    )
    with NamedTemporaryFile(mode="wb", delete=False) as temp:
        temp.write(bytes_)

    grbs = pygrib.open(temp.name)
    actual = grbs[1].values
    np.testing.assert_array_equal(actual, expected_values)

    grbs.close()
    os.unlink(temp.name)
