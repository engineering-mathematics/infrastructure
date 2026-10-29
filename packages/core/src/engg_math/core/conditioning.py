"""Condition-number policy for solves."""

from __future__ import annotations

import math
import warnings

from engg_math.core.config import get_settings
from engg_math.core.errors import ConditioningWarning, IllConditionedError


def check_condition(kappa: float, context: str = "system") -> None:
    """Apply the configured thresholds to a condition number.

    Raises ``IllConditionedError`` at ``kappa_error`` (or at ``kappa_warning`` in strict mode);
    warns with ``ConditioningWarning`` between the two.
    """
    settings = get_settings()
    if math.isnan(kappa) or kappa >= settings.kappa_error:
        raise IllConditionedError(
            f"{context}: condition number {kappa:.3e} >= {settings.kappa_error:.1e}"
        )
    if kappa >= settings.kappa_warning:
        message = f"{context}: condition number {kappa:.3e} >= {settings.kappa_warning:.1e}"
        if settings.strict_mode:
            raise IllConditionedError(message)
        warnings.warn(message, ConditioningWarning, stacklevel=2)
