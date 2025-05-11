"""Library."""

from .colors import known_colors
from .formats import get_verified_color
from .gradient import Gradient
from .rgb import RGB

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    # For Python<3.8 (not relevant in your case, just for completeness)
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("gradpyent")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["RGB", "Gradient", "get_verified_color", "known_colors"]
