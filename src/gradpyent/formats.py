"""Output formatting of colors."""

import re
from collections.abc import Sequence
from functools import singledispatch

from gradpyent import colors
from gradpyent.rgb import RGB


@singledispatch
def get_verified_color(arg: str | RGB | Sequence[int]) -> RGB:
    """Convert an input value to an RGB instance.

    Supported input types are:
        - str: color name or HTML/KML hexadecimal color
        - RGB: color instance (returned as-is)
        - sequence of three integers: RGB tuple or list

    Args:
        arg (Any): Color value to convert.

    Returns:
        RGB: The equivalent RGB color.

    Raises:
        ValueError: If the input type or value is unrecognized.

    """
    error = f"Unrecognized color value or type: {arg!r}"
    raise ValueError(error) from None


@get_verified_color.register
def _(arg: str) -> RGB:
    """Return RGB object from a string representation.

    Supported string formats:
        - Named color (as in known colors)
        - HTML hexadecimal (e.g. '#RRGGBB')
        - KML hexadecimal (e.g. '#AARRGGBB')

    Args:
        arg (str): Color string.

    Returns:
        RGB: The parsed RGB object.

    Raises:
        ValueError: If the string is not a recognized color format.

    """
    html_req_len = 7
    kml_req_len = 9
    known_colors = colors.known_colors()
    if arg in known_colors:
        return known_colors[arg]
    if arg.startswith("#"):
        if len(arg) == html_req_len:
            return _get_rgb_from_html(arg)
        if len(arg) == kml_req_len:
            return _get_rgb_from_kml(arg)
        error = (
            f'Color string "{arg}" must be of length 7 (HTML) or 9 (KML) including "#"'
        )
        raise ValueError(error) from None
    error = f'Color string "{arg}" must be a named color or a valid hex string.'
    raise ValueError(error) from None


@get_verified_color.register
def _(arg: RGB) -> RGB:
    """Return the RGB object itself.

    Args:
        arg (RGB): An RGB instance.

    Returns:
        RGB: The same object.

    """
    return arg


@get_verified_color.register
def _(arg: Sequence) -> RGB:
    """Return RGB object from a tuple or list of three integers.

    Args:
        arg (Sequence): A sequence (tuple or list) of three integers.

    Returns:
        RGB: Parsed color.

    Raises:
        ValueError: If sequence is not length 3 or not integer values.

    """
    req_sequence_len = 3
    if len(arg) != req_sequence_len:
        error = f"Expected a sequence of three integers, got {len(arg)} values."
        raise ValueError(error) from None
    try:
        return RGB(int(arg[0]), int(arg[1]), int(arg[2]))
    except Exception as exc:
        error = f"Could not parse sequence as RGB: {arg}"
        raise ValueError(error) from exc


def _get_rgb_from_html(code: str) -> RGB:
    """Extract RGB object from HTML string (e.g. '#RRGGBB').

    Args:
        code (str): HTML color string.

    Returns:
        RGB: Corresponding RGB object.

    Raises:
        ValueError: If the format is invalid.

    """
    max_input_len = 7
    if not (code.startswith("#") and len(code) == max_input_len):
        error = f'Invalid HTML color: "{code}".'
        raise ValueError(error) from None
    try:
        return RGB(int(code[1:3], 16), int(code[3:5], 16), int(code[5:7], 16))
    except Exception as exc:
        error = f"Could not parse HTML RGB: {code}"
        raise ValueError(error) from exc


def _get_rgb_from_kml(code: str) -> RGB:
    """Extract RGB object from KML string (e.g. '#AARRGGBB').

    Args:
        code (str): KML color string (with alpha channel).

    Returns:
        RGB: Corresponding RGB object (alpha ignored).

    Raises:
        ValueError: If the format is invalid.

    """
    max_input_len = 9
    if not (code.startswith("#") and len(code) == max_input_len):
        error = f'Invalid KML color: "{code}".'
        raise ValueError(error) from None
    try:
        return RGB(int(code[3:5], 16), int(code[5:7], 16), int(code[7:9], 16))
    except Exception as exc:
        error = f"Could not parse KML RGB: {code}"
        raise ValueError(error) from exc


def _verify_two_char_hex(code: str) -> bool:
    """Verify if a string is a two character hex code.

    Args:
        code: hex string

    Returns:
        True if matched, else False

    """
    return bool(re.fullmatch(r"[0-9A-Fa-f]{2}", code))


def _get_kml_from_rgb(rgb: RGB, opacity: float | None = 1.0) -> str:
    """Convert RGB to KML format.

    Args:
        rgb: Color
        opacity: Optionally, set opacity, 0-1

    Returns:
        KML formatted color, with transparency #TTBBGGRR

    """
    return (
        f"{format(int(opacity * 255), '02x')}{format(int(rgb.blue), '02x')}"
        f"{format(int(rgb.green), '02x')}{format(int(rgb.red), '02x')}"
    )


def _get_html_from_rgb(rgb: RGB) -> str:
    """Convert RGB to HTML format.

    Args:
        rgb: Color

    Returns:
        HTML formatted color #RRGGBB

    """
    return (
        f"#{format(int(rgb.red), '02x')}"
        f"{format(int(rgb.green), '02x')}"
        f"{format(int(rgb.blue), '02x')}"
    )


def format_color(
    rgb: RGB,
    fmt: str | None = "rgb",
    opacity: float | None = 1.0,
) -> str | tuple[int, int, int]:
    """Format output to desired style.

    Args:
        rgb: The RGB object to convert to a different format
        fmt: Desired format
        opacity: If fmt is 'kml' an optional opacity 0-1 can be passed

    Returns:
        Formatted color as a string (HTML/KML) or tuple (RGB)

    """
    if fmt == "kml":
        formatted_color = _get_kml_from_rgb(rgb=rgb, opacity=opacity)
    elif fmt == "html":
        formatted_color = _get_html_from_rgb(rgb=rgb)
    elif fmt == "rgb":
        formatted_color = (rgb.red, rgb.green, rgb.blue)
    else:
        error = f"Requested format: {fmt}, is not available"
        raise NotImplementedError(error)

    return formatted_color
