from io import BytesIO
from pathlib import Path
import os

import pygrib
import pytest

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../sampledata/flux.grb"
)

print_result_expected_for_messages = """
1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200
2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
""".lstrip()


def assert_print_result(grbs, capsys, expected):
    for grb in grbs:
        print(grb)
    captured = capsys.readouterr()
    assert captured.out == expected


def run_print_assertions(grbs, capsys):
    assert_print_result(grbs, capsys, print_result_expected_for_messages)
    assert_print_result(grbs, capsys, "")
    grbs.seek(0)
    assert_print_result(grbs, capsys, print_result_expected_for_messages)


def test_open_for_filename(capsys):
    grbs = pygrib.open(filename)
    assert type(grbs.name) == str
    run_print_assertions(grbs, capsys)
    grbs.close()


def test_open_for_path_object(capsys):
    path = Path(filename)
    grbs = pygrib.open(path)
    assert type(grbs.name) == str
    run_print_assertions(grbs, capsys)
    grbs.close()


def test_open_for_bufferedreader_object(capsys):
    f = open(filename, "rb")
    grbs = pygrib.open(f)
    assert type(grbs.name) == str
    run_print_assertions(grbs, capsys)
    grbs.close()
    f.close()


def test_open_for_bytesio_object(capsys):
    with open(filename, "rb") as f:
        buffer = f.read()
    f = BytesIO(buffer)

    with pytest.raises(TypeError) as e:
        pygrib.open(f)
    assert str(e.value) == "expected bytes, _io.BytesIO found"
