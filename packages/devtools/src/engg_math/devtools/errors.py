"""Devtools errors."""

from __future__ import annotations

from engg_math.core import EnggMathError


class ValidationError(EnggMathError, AssertionError):
    """A numerical result is outside its stated tolerance."""
