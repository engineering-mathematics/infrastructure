"""Unit errors."""

from __future__ import annotations

from engg_math.core import EnggMathError


class DimensionalError(EnggMathError):
    """Operation violates dimensional consistency."""
