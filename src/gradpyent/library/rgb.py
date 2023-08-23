"""RGB color objects."""


class RGB:
    """Represents a color in RGB format."""

    def __init__(self, red: int, green: int, blue: int) -> None:
        """Instantiate the class.

        Args:
            red: red component of RGB color, 0-255
            green: green component of RGB color, 0-255
            blue: blue component of RGB color, 0-255

        Returns:
            None
        """
        self._red = self._verify(red)
        self._green = self._verify(green)
        self._blue = self._verify(blue)

    @staticmethod
    def _verify(color: int) -> int:
        """Verify a given color's value is within acceptable range of 0-255.

        Args:
            color: value of component RGB color, 0-255

        Returns:
            color component, if valid

        Raises:
            TypeError: if color is not an integer
            ValueError: if color is not in range of 0-255
        """
        if not isinstance(color, int):
            raise TypeError("color must be of type 'int'")

        if not ((color >= 0) and (color <= 255)):
            raise ValueError("color must be in range of [0, 255]")

        return color

    # getters
    @property
    def red(self) -> int:
        """Get red component value.

        Returns:
            red component value
        """
        return self._red

    @property
    def green(self) -> int:
        """Get green component value.

        Returns:
            green component value
        """
        return self._green

    @property
    def blue(self) -> int:
        """Get blue component value.

        Returns:
            blue component value
        """
        return self._blue
