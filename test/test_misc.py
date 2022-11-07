"""Collection of miscellaneous minor tests."""

import pygrib
import pytest


def test_internal_value_type_of_runtime_error():
    grbindx = pygrib.index("../sampledata/gfs.grb", "shortName")
    with pytest.raises(RuntimeError) as e:
        grbindx.write("nonexistent/path")
    assert type(e.value.args[0]) is str
