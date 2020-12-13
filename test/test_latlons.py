"""Test latlons output for grids."""

# 3rd Party
import pytest
import numpy as np


# filename is passed as an argument to samplegribfile fixture
# expected is a 2d list [[0, 0], [0, -1], [-1, 0], [-1, -1]]
@pytest.mark.parametrize(
    "filename, expected",
    [
        # gridType='rotated_ll'
        ("cl00010000_ecoclimap_rot.grib1", [
            [-8.840292, 31.874274],
            [32.845938, 32.675248],
            [-36.036376, 64.895728],
            [57.967172, 66.542672],
        ]),
        # gridType='regular_ll'
        ("gfs.grb", [
            [0.0, 90.0],
            [357.5, 90.0],
            [0.0, -90.0],
            [357.5, -90.0]
        ]),
        # gridType='lambert'
        ("eta.grb", [
            [-133.459, 12.19],
            [-65.091275,14.334642],
            [-152.855459, 54.535803],
            [-49.385097, 57.289403]
        ]),
        # gridType='polar_stereographic'
        ("ngm.grb", [
            [-133.443, 7.647],
            [-76.557281, 7.647150],
            [173.746409, 44.287971],
            [-23.74651083940669,44.288441]
        ]),
        # gridType='regular_gg'
        ("flux.grb", [
           [0.0, 88.54195],
           [358.125, 88.541950],
           [0.0, -88.54195],
           [358.125, -88.54195]
        ]),
        # gridType='reduced_gg'
        ("ecmwf_tigge.grb", [
           [0.0, 89.655964],
           [359.55, 89.655964],
           [0.0,-89.655964],
           [359.55, -89.655964]
        ]),
        # gridType='mercator'
        ("dspr.temp.bin", [
          [-68.027832, 16.977484],
          [-63.9843, 16.97748],
          [-68.02783299999994, 19.54449],
          [-63.9843, 19.54449]
        ]),
        # gridType='reduced_ll'
        ("reduced_latlon_surface.grib2", [
          [0.0, 90.0],
          [359.64, 90.0],
          [0.0, -90.0],
          [359.64, -90.0]
        ])
        # no coverage for gridType = 'rotated_gg', 'albers', 'space_view',
        # 'equatorial_azimuthal_equidistant','lambert_azimuthal_equal_area'
        # (no sample grib files that use those grids)
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
        ("gfs.grb", [37, 24], [60., -2.5]),
        ("eta.grb", [32, 31], [-114.320061, 39.636536]),
        ("ngm.grb", [22, 17], [-124.093697, 42.418053]),
        ("flux.grb", [47, 64], [120.0, -0.952367]),
        ("ecmwf_tigge.grb", [200, 266], [119.7, -0.224718]),
        ("dspr.temp.bin", [112, 113], [-66.676034, 18.2714926]),
        ("reduced_latlon_surface.grib2", [250, 334], [119.99976, 0.0])
    ])
def test_latlons_randpoint(samplegribfile, pt_ji, expected):
    """Test the resulting grid data."""
    lats, lons = samplegribfile.message(1).latlons()
    j, i = pt_ji
    assert np.allclose([lons[j, i], lats[j, i]], expected)
