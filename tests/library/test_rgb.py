"""Tests for RGB class"""
import pytest
from gradpyent.library.rgb import RGB


class TestClassInit:  # pylint: disable=too-few-public-methods
    """Tests for RGB"""

    @pytest.mark.parametrize(
        "red,green,blue,expected",
        [
            [
                0,
                0,
                0,
                RGB(0, 0, 0)
            ]
        ],
    )
    def test_return(self, red: int, green: int, blue: int, expected: RGB) -> None:
        """

        Args:
            red: Red, as int of 0-255
            green: Green, as int of 0-255
            blue: Blue, as int of 0-255
            expected: The expected RGB object to compare with

        """
        rgb = RGB(red, green, blue)

        assert rgb.red == expected.red
        assert rgb.green == expected.green
        assert rgb.blue == expected.blue


class TestVerify:  # pylint: disable=too-few-public-methods
    """Tests for RGB _verify method"""

    @pytest.mark.parametrize(
        "color,expected",
        [
            [
                0,
                0
            ],
            [
                255,
                255
            ]
        ],
    )
    def test_return(self, color: int, expected: int) -> None:
        """

        Args:
            color: Color, as int of 0-255
            expected: The expected RGB object to compare with

        """
        result = RGB._verify(color)

        assert result == expected

    @pytest.mark.parametrize(
        "color,expected_exception",
        [
            [
                1.0,
                TypeError
            ],
            [
                -1,
                ValueError
            ],
            [
                256,
                ValueError
            ]
        ],
    )
    def test_exceptions(self, color: int, expected_exception: Exception) -> None:
        """

        Args:
            color: Color, as int of 0-255
            expected_exception: The expected exception that will be raised

        """
        with pytest.raises(expected_exception):
            RGB._verify(color)
