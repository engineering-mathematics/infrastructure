"""Reference-solution comparison with explicit tolerances."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from engg_math.devtools.errors import ValidationError


def assert_close(
    actual: npt.ArrayLike,
    expected: npt.ArrayLike,
    *,
    rtol: float,
    atol: float,
    label: str = "result",
) -> None:
    """Require ``|actual - expected| <= atol + rtol * |expected|`` elementwise.

    Tolerances have no defaults: state and justify them at the call site.
    NaNs never compare equal.
    """
    a = np.asarray(actual)
    e = np.asarray(expected)
    if a.shape != e.shape:
        raise ValidationError(f"{label}: shape {a.shape} != {e.shape}")
    if np.all(np.isclose(a, e, rtol=rtol, atol=atol, equal_nan=False)):
        return
    diff = np.abs(a - e)
    bad = np.where(np.isnan(diff), np.inf, diff)
    idx = np.unravel_index(int(np.argmax(bad)), bad.shape)
    with np.errstate(divide="ignore", invalid="ignore"):
        rel = diff[idx] / abs(e[idx]) if e[idx] != 0 else float("inf")
    raise ValidationError(
        f"{label}: max abs error {diff[idx]:.3e} (rel {rel:.3e}) "
        f"at index {tuple(int(i) for i in idx)}; allowed rtol={rtol:g}, atol={atol:g}"
    )
