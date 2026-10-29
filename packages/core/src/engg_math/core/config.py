"""Process-wide numerical settings.

Resolution order: ``override()`` context > ``configure()`` > environment > defaults.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, Literal

import numpy as np

from engg_math.core.errors import ConfigError

if TYPE_CHECKING:
    from collections.abc import Iterator

Precision = Literal["float32", "float64"]
_PRECISIONS = ("float32", "float64")
_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off", ""}


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated, immutable settings."""

    precision: Precision = "float64"
    strict_mode: bool = False
    kappa_warning: float = 1e5
    kappa_error: float = 1e7

    def __post_init__(self) -> None:
        """Validate on construction."""
        if self.precision not in _PRECISIONS:
            raise ConfigError(f"precision must be one of {_PRECISIONS}, got {self.precision!r}")
        if not 0 < self.kappa_warning < self.kappa_error:
            raise ConfigError(
                "need 0 < kappa_warning < kappa_error, "
                f"got {self.kappa_warning} / {self.kappa_error}"
            )

    @property
    def float_dtype(self) -> np.dtype[Any]:
        """Real dtype for ``precision``."""
        return np.dtype(self.precision)

    @property
    def complex_dtype(self) -> np.dtype[Any]:
        """Complex dtype matching ``precision``."""
        return np.dtype("complex64" if self.precision == "float32" else "complex128")


def _parse_bool(name: str, raw: str) -> bool:
    value = raw.strip().lower()
    if value in _TRUE:
        return True
    if value in _FALSE:
        return False
    raise ConfigError(f"{name} must be a boolean, got {raw!r}")


def _parse_float(name: str, raw: str) -> float:
    try:
        return float(raw)
    except ValueError:
        raise ConfigError(f"{name} must be a number, got {raw!r}") from None


def from_env(environ: dict[str, str] | os._Environ[str] | None = None) -> Settings:
    """Build ``Settings`` from ``ENGG_MATH_*`` variables."""
    env = os.environ if environ is None else environ
    kwargs: dict[str, Any] = {}
    if (raw := env.get("ENGG_MATH_PRECISION")) is not None:
        kwargs["precision"] = raw.strip().lower()
    if (raw := env.get("ENGG_MATH_STRICT")) is not None:
        kwargs["strict_mode"] = _parse_bool("ENGG_MATH_STRICT", raw)
    if (raw := env.get("ENGG_MATH_KAPPA_WARNING")) is not None:
        kwargs["kappa_warning"] = _parse_float("ENGG_MATH_KAPPA_WARNING", raw)
    if (raw := env.get("ENGG_MATH_KAPPA_ERROR")) is not None:
        kwargs["kappa_error"] = _parse_float("ENGG_MATH_KAPPA_ERROR", raw)
    return Settings(**kwargs)


_current: ContextVar[Settings | None] = ContextVar("engg_math_settings", default=None)


class _State:
    """Process-wide base settings; ``None`` means "read the environment on next access"."""

    base: Settings | None = None


def get_settings() -> Settings:
    """Return the active settings."""
    active = _current.get()
    if active is not None:
        return active
    if _State.base is None:
        _State.base = from_env()
    return _State.base


def configure(**changes: object) -> Settings:
    """Replace process-wide settings with the current ones plus ``changes``."""
    _State.base = replace(get_settings(), **changes)  # type: ignore[arg-type]
    return _State.base


@contextmanager
def override(**changes: object) -> Iterator[Settings]:
    """Apply ``changes`` within the context only (task- and thread-local)."""
    token = _current.set(replace(get_settings(), **changes))  # type: ignore[arg-type]
    try:
        yield get_settings()
    finally:
        _current.reset(token)


def reset() -> None:
    """Drop ``configure()`` state; the environment is re-read on next access."""
    _State.base = None
