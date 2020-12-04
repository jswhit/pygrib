"""Test latlons output for grids."""

# 3rd Party
import pytest
import numpy as np


# filename is passed as an argument to samplegribfile fixture
@pytest.mark.parametrize(
    "filename, expected",
    [
        ("cl00010000_ecoclimap_rot.grib1", [-8.840292, 31.874274]),
        ("tigge.grb", [0., 90.])
    ])
def test_latlons(samplegribfile, expected):
    """Test the resulting grid data."""
    lats, lons = samplegribfile.message(1).latlons()
    assert np.allclose([lons[0, 0], lats[0, 0]], expected)
