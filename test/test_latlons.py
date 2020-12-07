"""Test latlons output for grids."""

# 3rd Party
import pytest
import numpy as np


# filename is passed as an argument to samplegribfile fixture
# expected is a 2d list [[0, 0], [0, -1], [-1, 0], [-1, -1]]
@pytest.mark.parametrize(
    "filename, expected",
    [
        ("cl00010000_ecoclimap_rot.grib1", [
            [-8.840292, 31.874274],
            [32.845938, 32.675248],
            [-36.036376, 64.895728],
            [57.967172, 66.542672],
        ]),
        ("gfs.grb", [
            [0.0, 90.0],
            [357.5, 90.0],
            [0.0, -90.0],
            [357.5, -90.0]
        ])
    ])
def test_latlons_corners(samplegribfile, expected):
    """Test the resulting grid data."""
    lats, lons = samplegribfile.message(1).latlons()
    res = []
    for j in [0, -1]:
        for i in [0, -1]:
            res.append([lons[j, i], lats[j, i]])
    assert np.allclose(res, expected)


# filename is passed as an argument to samplegribfile fixture
# pt_ji is a list for a point to example
# expected is the lon, lat value at that point
@pytest.mark.parametrize(
    "filename, pt_ji, expected",
    [
        ("cl00010000_ecoclimap_rot.grib1", [20, 17], [-6.549827, 36.674752]),
        ("gfs.grb", [37, 24], [60., -2.5])
    ])
def test_latlons_randpoint(samplegribfile, pt_ji, expected):
    """Test the resulting grid data."""
    lats, lons = samplegribfile.message(1).latlons()
    j, i = pt_ji
    assert np.allclose([lons[j, i], lats[j, i]], expected)
