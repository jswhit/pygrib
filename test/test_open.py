from io import BytesIO, SEEK_CUR
from pathlib import Path
import os

import pygrib
import pytest

filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../sampledata/flux.grb"
)

message_lines_expected_for_data_with_zero_offset = """
1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200
2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
""".lstrip()

message_lines_expected_for_data_with_4bytes_offset = """
1:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
2:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
3:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
""".lstrip()


def assert_message_lines(grbs, capsys, expected):
    for grb in grbs:
        print(grb)
    captured = capsys.readouterr()
    assert captured.out == expected


def test_open_for_filename(capsys):
    grbs = pygrib.open(filename)
    assert type(grbs.name) == str

    assert_message_lines(grbs, capsys, message_lines_expected_for_data_with_zero_offset)
    assert_message_lines(grbs, capsys, "")
    grbs.seek(0)
    assert_message_lines(grbs, capsys, message_lines_expected_for_data_with_zero_offset)

    grbs.close()


def test_open_for_path_object(capsys):
    path = Path(filename)
    grbs = pygrib.open(path)
    assert type(grbs.name) == str

    assert_message_lines(grbs, capsys, message_lines_expected_for_data_with_zero_offset)
    assert_message_lines(grbs, capsys, "")
    grbs.seek(0)
    assert_message_lines(grbs, capsys, message_lines_expected_for_data_with_zero_offset)

    grbs.close()


def test_open_for_bufferedreader_object(capsys):
    f = open(filename, "rb")
    grbs = pygrib.open(f)
    assert type(grbs.name) == str

    assert_message_lines(grbs, capsys, message_lines_expected_for_data_with_zero_offset)
    assert_message_lines(grbs, capsys, "")
    grbs.seek(0)
    assert_message_lines(grbs, capsys, message_lines_expected_for_data_with_zero_offset)

    grbs.close()
    f.close()


@pytest.mark.xfail(reason="unimplemented")
def test_open_for_bytesio_object(capsys):
    with open(filename, "rb") as f:
        buffer = f.read()
    f = BytesIO(buffer)
    grbs = pygrib.open(f)
    assert type(grbs.name) == str

    assert_message_lines(grbs, capsys, message_lines_expected_for_data_with_zero_offset)
    assert_message_lines(grbs, capsys, "")
    grbs.seek(0)
    assert_message_lines(grbs, capsys, message_lines_expected_for_data_with_zero_offset)

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
    "preprocess, message_lines_expected, postprocess",
    [
        (read_indicator, message_lines_expected_for_data_with_4bytes_offset, None,),
        (
            read_indicator_and_seek_to_starting_point,
            message_lines_expected_for_data_with_zero_offset,
            None,
        ),
        (
            None,
            message_lines_expected_for_data_with_zero_offset,
            reread_end_section_using_raw_file_access,
        ),
        (
            read_indicator_and_seek_to_starting_point,
            message_lines_expected_for_data_with_zero_offset,
            reread_end_section_using_raw_file_access,
        ),
    ],
)
def test_open_for_bufferedreader_object_with_raw_file_reading(
    capsys, preprocess, message_lines_expected, postprocess
):
    f = open(filename, "rb")

    if preprocess is not None:
        preprocess(f)

    grbs = pygrib.open(f)
    assert_message_lines(grbs, capsys, message_lines_expected)
    grbs.seek(0)
    assert_message_lines(grbs, capsys, message_lines_expected)
    grbs.close()

    if postprocess is not None:
        postprocess(f)
    f.close()


@pytest.mark.parametrize(
    "preprocess, message_lines_expected, postprocess",
    [
        (read_indicator, message_lines_expected_for_data_with_4bytes_offset, None,),
        (
            read_indicator_and_seek_to_starting_point,
            message_lines_expected_for_data_with_zero_offset,
            None,
        ),
        (
            None,
            message_lines_expected_for_data_with_zero_offset,
            reread_end_section_using_raw_file_access,
        ),
        (
            read_indicator_and_seek_to_starting_point,
            message_lines_expected_for_data_with_zero_offset,
            reread_end_section_using_raw_file_access,
        ),
    ],
)
@pytest.mark.xfail(reason="unimplemented")
def test_open_for_bytesio_object_with_raw_file_reading(
    capsys, preprocess, message_lines_expected, postprocess
):
    with open(filename, "rb") as f:
        buffer = f.read()
    f = BytesIO(buffer)

    if preprocess is not None:
        preprocess(f)

    grbs = pygrib.open(f)
    assert_message_lines(grbs, capsys, message_lines_expected)
    grbs.seek(0)
    assert_message_lines(grbs, capsys, message_lines_expected)
    grbs.close()

    if postprocess is not None:
        postprocess(f)
    f.close()
