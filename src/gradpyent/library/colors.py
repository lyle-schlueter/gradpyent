"""Collection of common colors."""
from gradpyent.library.rgb import RGB


def known_colors() -> dict:
    """A dictionary containing common color names.

    Returns:
        dict: A dictionary with color names as keys and their RGB representations as values.
            Example:
            "red": RGB([255, 0, 0]),
            "blue": RGB([0, 0, 255]),

    """
    return {
        "red": RGB(*[255, 0, 0]),
        "blue": RGB(*[0, 0, 255]),
        "green": RGB(*[0, 255, 0]),
        "white": RGB(*[255, 255, 255]),
        "black": RGB(*[0, 0, 0]),
        "yellow": RGB(*[255, 255, 0]),
        "lightyellow": RGB(*[240, 255, 120]),
        "orange": RGB(*[255, 128, 0]),
        "purple": RGB(*[127, 0, 255]),
        "pink": RGB(*[240, 0, 120])
    }
