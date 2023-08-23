"""Output formatting of colors."""
import re
from collections.abc import Sequence
from functools import singledispatch
from typing import Optional, Tuple, Union

import gradpyent.library.colors as colors
from gradpyent.library.rgb import RGB


@singledispatch
def get_verified_color(arg):
    """Dispatch calls to convert input color to RGB.

    Args:
        arg: Color, can be RGB, Sequence (RGB), or str (HTML/KML)
    """
    raise ValueError(f'{arg} is not a known color value')


@get_verified_color.register
def _(arg: RGB):
    """Return RGB object.

    If the input is already an RGB object, it can be returned without modification.

    Args:
        arg: RGB object

    Returns:
        RGB object
    """
    return arg


@get_verified_color.register
def _(arg: Sequence):
    """Return RGB object from Sequence.

    If the input is a Sequence, try to convert to an RGB object.

    Args:
        arg: Sequence

    Returns:
        RGB object
    """
    # attempt to convert the given value to RGB format
    return RGB(*arg)


@get_verified_color.register
def _(arg: str):
    """Return RGB object from string.

    If the input is a string, try to convert to an RGB object.

    Args:
        arg: String representation of color

    Returns:
        RGB object
    """
    known_colors = colors.known_colors()
    if arg in known_colors:
        # if value is in colors, it is a known color, and we can use it as-is
        verified_color = known_colors[arg]
    elif arg[0] == "#":
        # if value starts with '#' it's likely either html or kml fmt
        if len(arg) == 7:
            verified_color = _get_rgb_from_html(arg)
        elif len(arg) == 9:
            verified_color = _get_rgb_from_kml(arg)
        else:
            raise ValueError(f'Unknown string "{arg}" does not match known color, html, or kml type')
    else:
        raise ValueError("Color", arg, " does not exist")

    return verified_color


def _verify_two_char_hex(code: str) -> bool:
    """Verify if a string is a two character hex code.

    Args:
        code: hex string

    Returns:
        True if matched, else False
    """
    return False if (re.search(r'[\dA-Fa-f]{2}', code) is None) else True


def _get_rgb_from_html(code: str) -> RGB:
    """Return RGB object from HTML color code.

    Args:
        code: HTML color code

    Notes:
        HTML color codes are RRGGBB
    """
    code = code.lower().replace('#', '')

    red = code[0:2]
    green = code[2:4]
    blue = code[4:6]

    for hex_value in [red, green, blue]:
        if not _verify_two_char_hex(hex_value):
            raise ValueError(f"Expected two-character hex value but got {hex_value}")

    return RGB(
        int(red, 16),  # hex to dec for red
        int(green, 16),  # hex to dec for green
        int(blue, 16)  # hex to dec for blue
    )


def _get_rgb_from_kml(code: str) -> RGB:
    """Return RGB object from KML color code.

    Args:
        code: KML color code

    Notes:
        The first two characters of KML are the alpha (opacity)
        int(code[0:2], 16) / 255
        https://developers.google.com/kml/documentation/kmlreference#color
        The order of expression is aabbggrr
    """
    code = code.lower().replace('#', '')

    # alpha = code[0:2]
    blue = code[2:4]
    green = code[4:6]
    red = code[6:8]

    for hex_value in [red, green, blue]:
        if not _verify_two_char_hex(hex_value):
            raise ValueError(f"Expected two-character hex value but got {hex_value}")

    return RGB(
        int(red, 16),  # hex to dec for red
        int(green, 16),  # hex to dec for green
        int(blue, 16)  # hex to dec for blue
    )


def _get_kml_from_rgb(rgb: RGB, opacity: Optional[float] = 1.0) -> str:
    """Convert RGB to KML format.

    Args:
        rgb: Color
        opacity: Optionally, set opacity, 0-1

    Returns:
        KML formatted color, with transparency #TTBBGGRR
    """
    return f'{format(int(opacity * 255), "02x")}{format(int(rgb.blue), "02x")}' \
           f'{format(int(rgb.green), "02x")}{format(int(rgb.red), "02x")}'


def _get_html_from_rgb(rgb: RGB) -> str:
    """Convert RGB to HTML format.

    Args:
        rgb: Color

    Returns:
        HTML formatted color #RRGGBB
    """
    return f'#{format(int(rgb.red), "02x")}{format(int(rgb.green), "02x")}{format(int(rgb.blue), "02x")}'


def format_color(
        rgb: RGB, fmt: Optional[str] = 'rgb', opacity: Optional[float] = 1.0) -> Union[str, Tuple[int, int, int]]:
    """Format output to desired style.

    Args:
        rgb: The RGB object to convert to a different format
        fmt: Desired format
        opacity: If fmt is 'kml' an optional opacity 0-1 can be passed

    Returns:
        Formatted color as a string (HTML/KML) or tuple (RGB)
    """
    if fmt == 'kml':
        formatted_color = _get_kml_from_rgb(rgb=rgb, opacity=opacity)
    elif fmt == 'html':
        formatted_color = _get_html_from_rgb(rgb=rgb)
    elif fmt == 'rgb':
        formatted_color = (rgb.red, rgb.green, rgb.blue)
    else:
        raise NotImplementedError(f"Requested format: {fmt}, is not available")

    return formatted_color
