# tests/test_gradient.py

import pytest

from gradpyent.gradient import Gradient
from gradpyent.rgb import RGB


def test_gradient_init_various_types():
    g = Gradient((0, 0, 0), (255, 128, 64))
    assert isinstance(g.gradient_start, RGB)
    assert isinstance(g.gradient_end, RGB)
    assert g.gradient_start == RGB(0, 0, 0)
    assert g.gradient_end == RGB(255, 128, 64)
    # Test with string/hex
    g2 = Gradient("#000000", "#ffffff")
    assert g2.gradient_start == RGB(0, 0, 0)
    assert g2.gradient_end == RGB(255, 255, 255)
    # Test with RGB objects
    g3 = Gradient(RGB(2, 3, 4), RGB(5, 6, 7), opacity=0.8)
    assert g3.opacity == 0.8


@pytest.mark.parametrize("opacity", [-0.1, 1.1, "bad"])
def test_gradient_invalid_opacity(opacity):
    with pytest.raises((ValueError, TypeError)):
        Gradient(RGB(0, 0, 0), RGB(1, 1, 1), opacity=opacity)


@pytest.mark.parametrize(
    "t,result",
    [
        (0.0, RGB(0, 0, 0)),
        (1.0, RGB(10, 20, 30)),
        (0.5, RGB(5, 10, 15)),
    ],
)
def test_get_color_at(t, result):
    g = Gradient((0, 0, 0), (10, 20, 30))
    assert g.get_color_at(t) == result


@pytest.mark.parametrize("t", [-0.01, 1.01, "bad"])
def test_get_color_at_invalid(t):
    g = Gradient(RGB(0, 0, 0), RGB(10, 10, 10))
    with pytest.raises((ValueError, TypeError)):
        g.get_color_at(t)


def test_generate_basic():
    g = Gradient((0, 0, 0), (10, 10, 10))
    colors = g.generate(3)
    assert colors == [RGB(0, 0, 0), RGB(5, 5, 5), RGB(10, 10, 10)]


def test_generate_steps_too_low():
    g = Gradient((0, 0, 0), (255, 255, 255))
    with pytest.raises(ValueError):
        g.generate(1)


def test_get_gradient_series_linear():
    g = Gradient((0, 0, 0), (255, 0, 0))
    out = g.get_gradient_series([0, 0.5, 1])
    assert out == [(0, 0, 0), (127, 0, 0), (255, 0, 0)]


def test_get_gradient_series_formats():
    g = Gradient((0, 0, 0), (255, 255, 255))
    series = [0, 1]
    html = g.get_gradient_series(series, fmt="html")
    kml = g.get_gradient_series(series, fmt="kml")
    assert html == ["#000000", "#ffffff"]
    assert all(isinstance(color, str) and len(color) == 8 for color in kml)


def test_get_gradient_series_const_series():
    g = Gradient((1, 2, 3), (4, 5, 6))
    out = g.get_gradient_series([7, 7, 7])
    # All should be gradient_start for constant series
    assert all(color == (1, 2, 3) for color in out)


def test_get_gradient_series_non_numeric():
    g = Gradient((0, 0, 0), (1, 1, 1))
    with pytest.raises(ValueError):
        g.get_gradient_series(["a", "b"])


def test_get_gradient_series_empty():
    g = Gradient((0, 0, 0), (1, 1, 1))
    with pytest.raises(ValueError):
        g.get_gradient_series([])


def test_repr():
    g = Gradient((1, 2, 3), (4, 5, 6), opacity=0.3)
    r = repr(g)
    assert "Gradient(" in r
    assert "opacity=0.3" in r
