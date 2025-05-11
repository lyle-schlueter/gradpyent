from collections.abc import Iterable
from typing import Any

from .formats import format_color, get_verified_color
from .rgb import RGB, RGB_VAL_MAX, RGB_VAL_MIN


def calc_percent_color(start: int, end: int, percent: float) -> int:
    """Calculate the interpolated color component between start and end.

    Args:
        start (int): Starting color component (0-255).
        end (int): Ending color component (0-255).
        percent (float): Interpolation factor in [0.0, 1.0].

    Returns:
        int: Interpolated component as integer in [0, 255].

    Raises:
        TypeError: If input types are incorrect.
        ValueError: If values are out of expected ranges.

    """
    if not (isinstance(start, int) and isinstance(end, int)):
        error = "start and end must be integers"
        raise TypeError(error)
    if not (RGB_VAL_MIN <= start <= RGB_VAL_MAX) or not (
        RGB_VAL_MIN <= end <= RGB_VAL_MAX
    ):
        error = "start and end must be in the range [0, 255]"
        raise ValueError(error)
    if not (0.0 <= percent <= 1.0):
        error = "percent must be between 0.0 and 1.0"
        raise ValueError(error)
    return int(start + (end - start) * percent)


class Gradient:
    """Represents a color gradient between two points."""

    def __init__(
        self,
        gradient_start: RGB | list[int] | tuple[int, int, int] | str = None,
        gradient_end: RGB | list[int] | tuple[int, int, int] | str = None,
        opacity: float | None = 1.0,
    ) -> None:
        """Initialize a color gradient.

        Args:
            gradient_start: The start color (RGB, 3-list, 3-tuple, or color string).
            gradient_end: The end color (RGB, 3-list, 3-tuple, or color string).
            opacity: Opacity to use for KML output (0.0 - 1.0).

        """
        if gradient_start is None:
            gradient_start = RGB(RGB_VAL_MIN, RGB_VAL_MIN, RGB_VAL_MIN)
        if gradient_end is None:
            gradient_end = RGB(RGB_VAL_MAX, RGB_VAL_MAX, RGB_VAL_MAX)

        self.gradient_start: RGB = get_verified_color(gradient_start)
        self.gradient_end: RGB = get_verified_color(gradient_end)
        self.opacity: float = self._validate_opacity(opacity)

    @staticmethod
    def _validate_opacity(opacity: float | None) -> float:
        if opacity is None:
            return 1.0
        if not (0.0 <= opacity <= 1.0):
            error = "opacity must be between 0.0 and 1.0"
            raise ValueError(error)
        return float(opacity)

    def get_color_at(self, t: float) -> RGB:
        """Interpolate color at position `t` along the gradient.

        Args:
            t (float): Position between start and end, in [0.0, 1.0].

        Returns:
            RGB: Interpolated color at position `t`.

        Raises:
            ValueError: If `t` is not within [0.0, 1.0].

        """
        if not (0.0 <= t <= 1.0):
            error = "`t` must be between 0.0 and 1.0"
            raise ValueError(error)
        r = calc_percent_color(self.gradient_start.red, self.gradient_end.red, t)
        g = calc_percent_color(self.gradient_start.green, self.gradient_end.green, t)
        b = calc_percent_color(self.gradient_start.blue, self.gradient_end.blue, t)
        return RGB(r, g, b)

    def generate(self, steps: int) -> list[RGB]:
        """Generate a list of evenly spaced colors along the gradient.

        Args:
            steps (int): How many colors to generate (>=2).

        Returns:
            List[RGB]: List of RGB objects from start to end color.

        Raises:
            ValueError: If steps < 2.

        """
        min_steps = 2
        if steps < min_steps:
            error = f"steps must be at least {min_steps}, got {steps}."
            raise ValueError(error)
        return [self.get_color_at(i / (steps - 1)) for i in range(steps)]

    def get_gradient_series(
        self,
        series: Iterable[Any],
        fmt: str = "rgb",
        opacity: float | None = None,
    ) -> list[RGB | tuple[int, int, int] | str]:
        """Generate a gradient mapped to the values in a numeric series.

        Args:
            series (Iterable): Numeric iterable (ints or floats).
            fmt (str): Output color format: "rgb" (default), "html", or "kml".
            opacity (float, optional): Opacity for KML, overrides constructor
            value if set.

        Returns:
            List: List of colors in the requested format, one for each series value.

        Raises:
            ValueError: If the series is empty or contains non-numeric values.

        """
        values = list(series)
        if len(values) == 0:
            error = "Series is empty."
            raise ValueError(error)
        try:
            numeric_values = [float(v) for v in values]
        except (TypeError, ValueError) as exc:
            error = "All values in series must be numeric."
            raise ValueError(error) from exc

        min_val, max_val = min(numeric_values), max(numeric_values)
        if min_val == max_val:
            # If all values are the same, use the start color for all
            positions = [0.0 for _ in numeric_values]
        else:
            positions = [
                (val - min_val) / (max_val - min_val) for val in numeric_values
            ]

        # Determine final opacity to use
        effective_opacity = (
            self._validate_opacity(opacity) if opacity is not None else self.opacity
        )

        result = []
        for t in positions:
            rgb = self.get_color_at(t)
            color_val = format_color(rgb, fmt=fmt, opacity=effective_opacity)
            result.append(color_val)
        return result

    def __repr__(self) -> str:
        """Return string representation of the object."""
        return (
            f"Gradient("
            f"{self.gradient_start!r}, "
            f"{self.gradient_end!r}, "
            f"opacity={self.opacity})"
        )
