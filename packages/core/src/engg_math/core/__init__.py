"""Shared configuration, errors and array contracts."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from engg_math.core.arrays import as_fortran, is_fortran, require_fortran, require_shape
from engg_math.core.conditioning import check_condition
from engg_math.core.config import Settings, configure, from_env, get_settings, override, reset
from engg_math.core.errors import (
    ConditioningWarning,
    ConfigError,
    EnggMathError,
    IllConditionedError,
    LayoutError,
    NumericalError,
    ShapeError,
)

try:
    __version__ = version("engg-math-core")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"

__all__ = [
    "ConditioningWarning",
    "ConfigError",
    "EnggMathError",
    "IllConditionedError",
    "LayoutError",
    "NumericalError",
    "Settings",
    "ShapeError",
    "__version__",
    "as_fortran",
    "check_condition",
    "configure",
    "from_env",
    "get_settings",
    "is_fortran",
    "override",
    "require_fortran",
    "require_shape",
    "reset",
]
