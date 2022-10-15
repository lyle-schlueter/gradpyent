"""Tests for formats library."""
import pytest
from gradpyent.library import formats
from gradpyent.library.rgb import RGB
from contextlib import ExitStack


class TestGetRgbFromHtml:  # pylint: disable=too-few-public-methods
    """Tests for HTML."""

    @pytest.mark.parametrize(
        "code,expected",
        [
            [
                "#ffffff",
                RGB(255, 255, 255)
            ],
            [
                "#000000",
                RGB(0, 0, 0)
            ],
            [
                # red
                "#ff0000",
                RGB(255, 0, 0)
            ],
            [
                # green
                "#00ff00",
                RGB(0, 255, 0)
            ],
            [
                # blue
                "#0000ff",
                RGB(0, 0, 255)
            ]
        ],
    )
    def test_return(self, code: str, expected: RGB) -> None:
        """

        Args:
            code: html string
            expected: The expected RGB object to compare with

        """
        rgb = formats._get_rgb_from_html(code)

        assert rgb.red == expected.red
        assert rgb.green == expected.green
        assert rgb.blue == expected.blue

    @pytest.mark.parametrize(
        "code,verify_hex,expected",
        [
            [
                "#00ffzz",
                False,
                pytest.raises(ValueError)
            ],
            [
                "#ffffff",
                True,
                ExitStack()
            ],
            [
                0,
                None,
                pytest.raises(AttributeError)
            ]
        ],
    )
    def test_exceptions(self, code: str, verify_hex: bool, expected: Exception, mocker) -> None:
        """Test exceptions raised by `_get_rgb_from_kml`.

        Args:
            code: HTML string
            verify_hex: Value to be returned from mocked `_verify_two_char_hex`
            expected: The expected exception that will be raised

        """
        mocker.patch(
            'gradpyent.library.formats._verify_two_char_hex',
            return_value=verify_hex
        )
        with expected:
            assert (formats._get_rgb_from_html(code) is not None)


class TestGetRgbFromKml:  # pylint: disable=too-few-public-methods
    """Tests for KML."""

    @pytest.mark.parametrize(
        "code,expected",
        [
            [
                "#00ffffff",
                RGB(255, 255, 255)
            ],
            [
                "#ff000000",
                RGB(0, 0, 0)
            ],
            [
                # blue
                "#ffff0000",
                RGB(0, 0, 255)
            ],
            [
                # green
                "#ff00ff00",
                RGB(0, 255, 0)
            ],
            [
                # red
                "#ff0000ff",
                RGB(255, 0, 0)
            ]
        ],
    )
    def test_return(self, code: str, expected: RGB) -> None:
        """

        Args:
            code: html string
            expected: The expected RGB object to compare with

        """
        rgb = formats._get_rgb_from_kml(code)

        assert rgb.red == expected.red
        assert rgb.green == expected.green
        assert rgb.blue == expected.blue

    @pytest.mark.parametrize(
        "code,verify_hex,expected",
        [
            [
                "#0000ffzz",
                False,
                pytest.raises(ValueError)
            ],
            [
                "#00ffffff",
                True,
                ExitStack()
            ],
            [
                0,
                None,
                pytest.raises(AttributeError)
            ]
        ],
    )
    def test_exceptions(self, code: str, verify_hex: bool, expected: Exception, mocker) -> None:
        """

        Args:
            code: html string
            verify_hex: Value to be returned from mocked `_verify_two_char_hex`
            expected: The expected exception that will be raised

        """
        mocker.patch(
            'gradpyent.library.formats._verify_two_char_hex',
            return_value=verify_hex
        )
        with expected:
            assert (formats._get_rgb_from_kml(code) is not None)


class TestVerifyTwoCharHex:  # pylint: disable=too-few-public-methods
    @pytest.mark.parametrize(
        "code,expected",
        [
            [
                "zz",
                False
            ],
            [
                "0",
                False
            ],
            [
                "F",
                False
            ],
            [
                "00",
                True
            ],
            [
                "FF",
                True
            ],
            [
                "ff",
                True
            ]
        ],
    )
    def test_return(self, code: str, expected: bool) -> None:
        """

        Args:
            code: html string
            expected: The expected exception that will be raised

        """
        assert formats._verify_two_char_hex(code) == expected


class TestGetKmlFromRgb:
    @pytest.mark.parametrize(
        "color,opacity,expected",
        [
            [
                RGB(255, 0, 0),
                1,
                "ff0000ff"
            ],
            [
                RGB(255, 0, 0),
                0,
                "000000ff"
            ],
            [
                RGB(0, 255, 0),
                1,
                "ff00ff00"
            ],
            [
                RGB(0, 0, 255),
                1,
                "ffff0000"
            ],
        ],
    )
    def test_return(self, color: RGB, opacity: float, expected: str) -> None:
        """Test ``_get_kml_from_rgb``.

        Args:
            color: RGB object
            opacity: Opacity value
            expected: The expected exception that will be raised

        """
        assert formats._get_kml_from_rgb(rgb=color, opacity=opacity) == expected


class TestGetHtmlFromRgb:
    @pytest.mark.parametrize(
        "color,expected",
        [
            [
                RGB(255, 0, 0),
                "#ff0000"
            ],
            [
                RGB(0, 255, 0),
                "#00ff00"
            ],
            [
                RGB(0, 0, 255),
                "#0000ff"
            ],
        ],
    )
    def test_return(self, color: RGB, expected: str) -> None:
        """Test ``_get_html_from_rgb``.

        Args:
            color: RGB object
            expected: The expected exception that will be raised

        """
        assert formats._get_html_from_rgb(rgb=color) == expected


class TestFormatColor:
    @pytest.mark.parametrize(
        "color,fmt,opacity,mock_func",
        [
            [
                # kml
                RGB(255, 0, 0),
                "kml",
                0,
                "_get_kml_from_rgb",
            ],
            [
                # html
                RGB(255, 0, 0),
                "html",
                None,
                "_get_html_from_rgb"
            ],
            # [
            #     # rgb
            #     RGB(255, 0, 0),
            # ],
        ],
    )
    def test_return(self, color: RGB, fmt: str, opacity: float, mock_func, mocker) -> None:
        """Test ``format_color``.

        Args:
            color: RGB object
            fmt: Requested format
            opacity: Opacity (for KML)
            mock_func: Name of the function to be mocked, if any

        """
        # setup
        mock = mocker.patch(
            f"gradpyent.library.formats.{mock_func}",
            # return_value=verify_hex
        )

        # run
        formats.format_color(rgb=color, fmt=fmt, opacity=opacity)

        # test
        if fmt == "kml":
            mock.assert_called_once_with(rgb=color, opacity=opacity)

        if fmt == "html":
            mock.assert_called_once_with(rgb=color)
