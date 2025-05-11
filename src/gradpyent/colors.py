"""Collection of common colors."""

from gradpyent.rgb import RGB


def known_colors() -> dict[str, RGB]:
    """Return a dictionary mapping known color names to RGB values.

    The returned dictionary includes standard color names as keys and their
    corresponding RGB objects as values.

    Returns:
        Dict[str, RGB]: Mapping of color name (lowercase) to corresponding RGB object.

    """
    return {
        "black": RGB(0, 0, 0),
        "white": RGB(255, 255, 255),
        "red": RGB(255, 0, 0),
        "lime": RGB(0, 255, 0),
        "blue": RGB(0, 0, 255),
        "yellow": RGB(255, 255, 0),
        "cyan": RGB(0, 255, 255),
        "magenta": RGB(255, 0, 255),
        "silver": RGB(192, 192, 192),
        "gray": RGB(128, 128, 128),
        "maroon": RGB(128, 0, 0),
        "olive": RGB(128, 128, 0),
        "green": RGB(0, 128, 0),
        "purple": RGB(128, 0, 128),
        "teal": RGB(0, 128, 128),
        "navy": RGB(0, 0, 128),
    }
