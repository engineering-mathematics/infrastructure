"""Shared unit registry and dimensional checking."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from engg_math.units.errors import DimensionalError
from engg_math.units.registry import get_registry
from engg_math.units.tracker import DimensionalTracker, check_compatible

try:
    __version__ = version("engg-math-units")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"

__all__ = [
    "DimensionalError",
    "DimensionalTracker",
    "__version__",
    "check_compatible",
    "get_registry",
]
