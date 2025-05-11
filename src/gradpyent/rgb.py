from collections.abc import Iterator

RGB_VAL_MIN = 0
RGB_VAL_MAX = 255


class RGB:
    """Represents a color in RGB format."""

    def __init__(self, red: int, green: int, blue: int) -> None:
        """Initialize an RGB color instance.

        Args:
            red (int): Red component (0-255).
            green (int): Green component (0-255).
            blue (int): Blue component (0-255).

        Raises:
            TypeError: If a component is not an integer.
            ValueError: If a component is out of range [0, 255].

        """
        self._red: int = self._verify(red)
        self._green: int = self._verify(green)
        self._blue: int = self._verify(blue)

    @staticmethod
    def _verify(color: int) -> int:
        """Verify a color component is a valid integer in [0, 255].

        Args:
            color (int): Color component value.

        Returns:
            int: Validated color component.

        Raises:
            TypeError: If not an int.
            ValueError: If not in [0, 255].

        """
        if not isinstance(color, int):
            error = f"color must be of type 'int', not '{type(color)}'"
            raise TypeError(error)
        if not RGB_VAL_MIN <= color <= RGB_VAL_MAX:
            error = f"color must be in range [{RGB_VAL_MIN}, {RGB_VAL_MAX}]"
            raise ValueError(error)
        return color

    @property
    def red(self) -> int:
        """int: Red component value."""
        return self._red

    @property
    def green(self) -> int:
        """int: Green component value."""
        return self._green

    @property
    def blue(self) -> int:
        """int: Blue component value."""
        return self._blue

    def __eq__(self, other: object) -> bool:
        """Check equality with another RGB color."""
        if not isinstance(other, RGB):
            return NotImplemented
        return (
            self._red == other._red
            and self._green == other._green
            and self._blue == other._blue
        )

    def __repr__(self) -> str:
        """Return the official string representation of the object."""
        return f"RGB({self._red}, {self._green}, {self._blue})"

    def __iter__(self) -> Iterator:
        """Allow unpacking: tuple(rgb) → (r, g, b)."""
        yield self._red
        yield self._green
        yield self._blue
