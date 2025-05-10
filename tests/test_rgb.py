# tests/test_rgb.py

import pytest

from gradpyent.rgb import RGB


def test_rgb_valid():
    rgb = RGB(10, 20, 30)
    assert rgb.red == 10
    assert rgb.green == 20
    assert rgb.blue == 30


@pytest.mark.parametrize("value", [-1, 256, 3.5, "red"])
def test_rgb_invalid_component(value):
    with pytest.raises((TypeError, ValueError)):
        RGB(value, 0, 0)
    with pytest.raises((TypeError, ValueError)):
        RGB(0, value, 0)
    with pytest.raises((TypeError, ValueError)):
        RGB(0, 0, value)


def test_rgb_equality_and_repr():
    assert RGB(1, 2, 3) == RGB(1, 2, 3)
    assert RGB(1, 2, 3) != RGB(3, 2, 1)
    assert repr(RGB(1, 2, 3)) == "RGB(1, 2, 3)"


def test_rgb_iter():
    r, g, b = RGB(1, 2, 3)
    assert (r, g, b) == (1, 2, 3)
