# tests/test_formats.py

import pytest

from gradpyent.formats import (
    _get_html_from_rgb,
    _get_kml_from_rgb,
    _get_rgb_from_html,
    _get_rgb_from_kml,
    _verify_two_char_hex,
    format_color,
    get_verified_color,
)
from gradpyent.rgb import RGB


@pytest.mark.parametrize(
    "arg,expected",
    [
        ("#ffffff", RGB(255, 255, 255)),
        ("#000000", RGB(0, 0, 0)),
        (RGB(1, 2, 3), RGB(1, 2, 3)),
        ([4, 5, 6], RGB(4, 5, 6)),
        ((14, 15, 16), RGB(14, 15, 16)),
    ],
)
def test_get_verified_color_variants(arg, expected):
    assert get_verified_color(arg) == expected


@pytest.mark.parametrize(
    "bad_arg",
    ["#fff", "#00000", "notacolor", [1, 2], [1, "a", 3], object()],
)
def test_get_verified_color_invalid(bad_arg):
    with pytest.raises(ValueError):
        get_verified_color(bad_arg)


@pytest.mark.parametrize(
    "code,result",
    [("#112233", RGB(17, 34, 51)), ("#AABBCC", RGB(170, 187, 204))],
)
def test_get_rgb_from_html(code, result):
    assert _get_rgb_from_html(code) == result


@pytest.mark.parametrize("bad_code", ["#12345", "abc", "#xyzxyz"])
def test_get_rgb_from_html_bad(bad_code):
    with pytest.raises(ValueError):
        _get_rgb_from_html(bad_code)


@pytest.mark.parametrize(
    "code,result",
    [
        # KML color order is not standard RGB
        ("#ff0000ff", RGB(0, 0, 255)),  # blue
        ("#ff00ff00", RGB(0, 255, 0)),  # green
        ("#ffff0000", RGB(255, 0, 0)),  # red
    ],
)
def test_get_rgb_from_kml(code, result):
    assert _get_rgb_from_kml(code) == result


@pytest.mark.parametrize(
    "bad_code",
    [
        "#AABBCC",  # not 9 chars
        "#123456",  # not 9 chars
        "#ff00x011",  # invalid hex in green channel
        "#ff0000xx",  # invalid hex in blue channel
    ],
)
def test_get_rgb_from_kml_bad(bad_code):
    with pytest.raises(ValueError):
        _get_rgb_from_kml(bad_code)


@pytest.mark.parametrize(
    "text,valid",
    [("ff", True), ("00", True), ("GG", False), ("abc", False)],
)
def test_two_char_hex(text, valid):
    assert _verify_two_char_hex(text) == valid


def test_get_kml_from_rgb_and_html():
    rgb = RGB(18, 52, 86)
    kml = _get_kml_from_rgb(rgb, 0.5)
    assert kml.startswith("7f")  # 0.5 opacity
    html = _get_html_from_rgb(rgb)
    assert html == "#123456"


@pytest.mark.parametrize(
    "fmt,expected",
    [("rgb", (10, 20, 30)), ("html", "#0a141e"), ("kml", "ff1e140a")],
)
def test_format_color_formats(fmt, expected):
    rgb = RGB(10, 20, 30)
    if fmt == "kml":
        assert format_color(rgb, fmt=fmt).endswith("1e140a")
    else:
        assert format_color(rgb, fmt=fmt) == expected


def test_format_color_invalid():
    rgb = RGB(1, 2, 3)
    with pytest.raises(NotImplementedError):
        format_color(rgb, fmt="notarealformat")
