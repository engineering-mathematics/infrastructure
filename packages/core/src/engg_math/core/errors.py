"""Exception hierarchy shared by all ecosystem packages."""

from __future__ import annotations


class EnggMathError(Exception):
    """Base class for all ecosystem errors."""


class ConfigError(EnggMathError, ValueError):
    """Invalid configuration value."""


class ShapeError(EnggMathError, ValueError):
    """Array shape or rank violates a contract."""


class LayoutError(EnggMathError, ValueError):
    """Array memory layout violates a contract."""


class NumericalError(EnggMathError, ArithmeticError):
    """Base class for numerical failures."""


class IllConditionedError(NumericalError):
    """Condition number exceeds the configured error threshold."""


class ConditioningWarning(UserWarning):
    """Condition number exceeds the configured warning threshold."""
