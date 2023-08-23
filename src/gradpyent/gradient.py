"""Gradient."""
import warnings
from typing import Optional, Union

import numpy
import pandas

import gradpyent.library.formats as formats
from gradpyent.library.rgb import RGB


class Gradient:
    """Gradient class."""

    def __init__(self, gradient_start: Union[RGB, list, tuple, str] = RGB(0, 0, 0),
                 gradient_end: Union[RGB, list, tuple, str] = RGB(255, 255, 255),
                 opacity: Optional[float] = 1.0):
        """Initialize the gradient object.

        Args:
            gradient_start: Gradient 'start' color
            gradient_end: Gradient 'end' color
            opacity: Opacity (for use with KML format)
        """
        self.gradient_start = gradient_start
        self.gradient_end = gradient_end
        self.opacity = opacity

        warnings.formatwarning = self._format_warning

    @staticmethod
    def _format_warning(message: str, category, filename: str, lineno: int, line='') -> str:
        """Create nice looking warnings.

        Args:
            message: The warning message
            category: Category of warning
            filename: File warning is from
            lineno: Line number generating warning
            line: Line
        """
        return f'{filename}:{lineno}\n{category.__name__}: {message}: {line if line is not None else ""}\n'

    # 'public' methods
    def get_gradient_series(self, series: Union[numpy.array, pandas.Series, list], fmt: Optional[str] = None,
                            default: Optional[str] = 'black', force_rescale: Optional[bool] = False) -> list:
        """Create the gradient series.

        Args:
            series: Input series to create color gradient from
            fmt: Desired output format
            default: Default color for nulls
            force_rescale: Force rescale (even if not needed)

        Returns:
            List of color in specified format
        """
        default_rgb = formats.get_verified_color(default)
        lst_colors = []

        # in case numpy.array or list was passed, turn it into a series (also works on an existing series)
        series = pandas.Series(series)

        if series.dtype == 'O':
            warnings.warn("series dtype is object and will be factorized", UserWarning)
            series = pandas.Series(pandas.factorize(series)[0])

        if (series.max() > 1) | (series.min() < 0 | force_rescale):
            warnings.warn("series was out of bounds and will be scaled", UserWarning)
            series = (series - series.min()) / (series.max() - series.min())

        for item in series.values:
            # hacky workaround for numpy float values of 1
            item = min(item, 1)

            # set the gradient color to the list
            if numpy.isnan(item):
                lst_colors.append(formats.format_color(default_rgb, fmt=fmt, opacity=self.opacity))
            else:
                lst_colors.append(self._get_color_from_gradient(item, fmt=fmt))

        return lst_colors

    @property
    def gradient_start(self):
        """Return the gradient starting value as an RGB object."""
        return self._gradient_start

    @gradient_start.setter
    def gradient_start(self, value: Union[RGB, list, tuple, str]):
        """Set the gradient start color.

        Args:
            value: Color
        """
        self._gradient_start = formats.get_verified_color(value)

    @property
    def gradient_end(self):
        """Return the gradient ending value as an RGB object."""
        return self._gradient_end

    @gradient_end.setter
    def gradient_end(self, value: Union[RGB, list, tuple, str]):
        """Set the gradient end color.

        Args:
            value: Color
        """
        self._gradient_end = formats.get_verified_color(value)

    @property
    def opacity(self):
        """Return the opacity value as a float."""
        return self._opacity

    @opacity.setter
    def opacity(self, opacity: float):
        """Set the alpha (opacity) for KML.

        Args:
            opacity: Opacity 0-1
        """
        if (opacity < 0) | (opacity > 1):
            raise ValueError('Opacity value must be in range 0-1 (decimal)')

        # set the property
        self._opacity = opacity
        # hex can be calculated thusly: "hex": format(int(self.o * 255), '02x')

    def set_gradient_bounds(self, gradient_start: Union[RGB, list, tuple, str],
                            gradient_end: Union[RGB, list, tuple, str]):
        """Set gradient start and end colors.

        Args:
            gradient_start: Start color
            gradient_end: End color

        Returns:
            None
        """
        self.gradient_start = gradient_start
        self.gradient_end = gradient_end

    def _get_color_from_gradient(self, percent_gradient: float, fmt: Optional[str] = None) -> Union[str, tuple]:
        """Get gradient color for the given value.

        Args:
            percent_gradient: Percent of gradient range
            fmt: Color output format

        Returns:
            Color in specified format
        """

        def calc_percent_color(start: int, end: int, percent: float):
            return int(start - ((start - end) * percent))

        if not (percent_gradient >= 0) and (percent_gradient <= 1):
            raise ValueError('Gradient percentage must be 0-1')

        rgb = RGB(
            calc_percent_color(self._gradient_start.red, self._gradient_end.red, percent_gradient),
            calc_percent_color(self._gradient_start.green, self._gradient_end.green, percent_gradient),
            calc_percent_color(self._gradient_start.blue, self._gradient_end.blue, percent_gradient)
        )

        return formats.format_color(rgb, fmt, opacity=self.opacity)
