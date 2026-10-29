"""Layout and shape contracts."""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra import numpy as hnp

from engg_math.core import (
    LayoutError,
    ShapeError,
    as_fortran,
    is_fortran,
    override,
    require_fortran,
    require_shape,
)

matrices = hnp.arrays(
    dtype=np.float64,
    shape=hnp.array_shapes(min_dims=2, max_dims=2, min_side=1, max_side=6),
    elements=st.floats(-1e6, 1e6),
)


@given(matrices)
def test_as_fortran_preserves_values_and_layout(a: np.ndarray) -> None:
    out = as_fortran(a)
    assert is_fortran(out)
    np.testing.assert_array_equal(out, a)


def test_as_fortran_does_not_copy_fortran_input() -> None:
    a = np.asfortranarray(np.ones((3, 3)))
    assert as_fortran(a) is a


def test_as_fortran_uses_configured_dtype() -> None:
    with override(precision="float32"):
        assert as_fortran([[1, 2], [3, 4]]).dtype == np.float32


def test_as_fortran_explicit_dtype_wins() -> None:
    assert as_fortran([[1, 2]], dtype=np.complex128).dtype == np.complex128


def test_require_fortran_rejects_c_order() -> None:
    c = np.ones((3, 4), order="C")
    with pytest.raises(LayoutError, match="mat"):
        require_fortran(c, "mat")


def test_require_fortran_passes_through() -> None:
    f = np.ones((3, 4), order="F")
    assert require_fortran(f) is f


@pytest.mark.parametrize(
    ("shape", "ok"),
    [((2, 3), True), ((2, None), True), ((None, None), True), ((3, 3), False), ((2,), False)],
)
def test_require_shape(shape: tuple[int | None, ...], ok: bool) -> None:
    a = np.zeros((2, 3))
    if ok:
        assert require_shape(a, shape) is a
    else:
        with pytest.raises(ShapeError):
            require_shape(a, shape)
