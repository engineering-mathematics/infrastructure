"""Array layout and shape contracts. Dense data is column-major (Fortran order)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
import numpy.typing as npt

from engg_math.core.config import get_settings
from engg_math.core.errors import LayoutError, ShapeError

if TYPE_CHECKING:
    from collections.abc import Sequence


def as_fortran(data: npt.ArrayLike, dtype: npt.DTypeLike | None = None) -> npt.NDArray[Any]:
    """Return ``data`` as a Fortran-contiguous array; copies only if needed.

    ``dtype`` defaults to the configured float dtype.
    """
    target = get_settings().float_dtype if dtype is None else dtype
    return np.asfortranarray(data, dtype=target)


def is_fortran(array: npt.NDArray[Any]) -> bool:
    """Whether ``array`` is Fortran-contiguous."""
    return bool(array.flags["F_CONTIGUOUS"])


def require_fortran(array: npt.NDArray[Any], name: str = "array") -> npt.NDArray[Any]:
    """Return ``array`` unchanged or raise ``LayoutError`` if it is not Fortran-contiguous."""
    if not is_fortran(array):
        raise LayoutError(f"{name} must be Fortran-contiguous (column-major)")
    return array


def require_shape(
    array: npt.NDArray[Any], shape: Sequence[int | None], name: str = "array"
) -> npt.NDArray[Any]:
    """Check rank and dimensions; ``None`` matches any size."""
    if array.ndim != len(shape) or any(
        want is not None and got != want for got, want in zip(array.shape, shape, strict=True)
    ):
        raise ShapeError(f"{name} must have shape {tuple(shape)}, got {array.shape}")
    return array
