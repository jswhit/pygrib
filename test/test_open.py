from io import BytesIO, SEEK_CUR
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

print_result_expected_for_data_with_offset = """
1:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
2:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
3:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
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


@pytest.mark.xfail(reason="unimplemented")
def test_open_for_bytesio_object(capsys):
    with open(filename, "rb") as f:
        buffer = f.read()
    f = BytesIO(buffer)
    grbs = pygrib.open(f)
    assert type(grbs.name) == str
    run_print_assertions(grbs, capsys)
    grbs.close()
    f.close()


def test_open_for_textiowrapper_object():
    f = open(filename, "r")

    with pytest.raises(TypeError) as e:
        pygrib.open(f)
    assert str(e.value) == "expected bytes, _io.TextIOWrapper found"


INDICATOR = b"GRIB"


def read_indicator(f):
    assert f.read(len(INDICATOR)) == INDICATOR


def read_indicator_and_seek_to_starting_point(f):
    read_indicator(f)
    f.seek(-len(INDICATOR), SEEK_CUR)


def reread_end_section_using_raw_file_access(f):
    end_section_bytes = b"7777"
    f.seek(-len(end_section_bytes), SEEK_CUR)
    assert f.read(len(end_section_bytes)) == end_section_bytes


@pytest.mark.parametrize(
    "preprocess, print_result_expected, postprocess",
    [
        (read_indicator, print_result_expected_for_data_with_offset, None,),
        pytest.param(
            read_indicator_and_seek_to_starting_point,
            print_result_expected_for_messages,
            None,
            marks=pytest.mark.xfail(reason="bug"),
        ),
        (
            None,
            print_result_expected_for_messages,
            reread_end_section_using_raw_file_access,
        ),
        pytest.param(
            read_indicator_and_seek_to_starting_point,
            print_result_expected_for_messages,
            reread_end_section_using_raw_file_access,
            marks=pytest.mark.xfail(reason="bug"),
        ),
    ],
)
def test_open_for_bufferedreader_object_with_raw_file_reading(
    capsys, preprocess, print_result_expected, postprocess
):
    f = open(filename, "rb")

    if preprocess is not None:
        preprocess(f)

    grbs = pygrib.open(f)
    assert_print_result(grbs, capsys, print_result_expected)
    grbs.seek(0)
    assert_print_result(grbs, capsys, print_result_expected)
    grbs.close()

    if postprocess is not None:
        postprocess(f)
    f.close()


@pytest.mark.parametrize(
    "preprocess, print_result_expected, postprocess",
    [
        (read_indicator, print_result_expected_for_data_with_offset, None,),
        (
            read_indicator_and_seek_to_starting_point,
            print_result_expected_for_messages,
            None,
        ),
        (
            None,
            print_result_expected_for_messages,
            reread_end_section_using_raw_file_access,
        ),
        (
            read_indicator_and_seek_to_starting_point,
            print_result_expected_for_messages,
            reread_end_section_using_raw_file_access,
        ),
    ],
)
@pytest.mark.xfail(reason="unimplemented")
def test_open_for_bytesio_object_with_raw_file_reading(
    capsys, preprocess, print_result_expected, postprocess
):
    with open(filename, "rb") as f:
        buffer = f.read()
    f = BytesIO(buffer)

    if preprocess is not None:
        preprocess(f)

    grbs = pygrib.open(f)
    assert_print_result(grbs, capsys, print_result_expected)
    grbs.seek(0)
    assert_print_result(grbs, capsys, print_result_expected)
    grbs.close()

    if postprocess is not None:
        postprocess(f)
    f.close()
