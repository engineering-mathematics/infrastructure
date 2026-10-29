"""assert_close."""

from __future__ import annotations

import numpy as np
import pytest

from engg_math.core import EnggMathError
from engg_math.devtools import ValidationError, assert_close


def test_passes_within_tolerance() -> None:
    assert_close([1.0, 2.0], [1.0 + 1e-10, 2.0], rtol=1e-8, atol=0.0)


def test_fails_and_reports_worst_index() -> None:
    with pytest.raises(ValidationError, match=r"index \(1, 0\)") as exc:
        assert_close(
            np.array([[1.0], [5.0]]), np.array([[1.0], [4.0]]), rtol=1e-6, atol=0.0, label="lu"
        )
    assert "lu:" in str(exc.value)
    assert "rtol=1e-06" in str(exc.value)


def test_shape_mismatch() -> None:
    with pytest.raises(ValidationError, match="shape"):
        assert_close([1.0, 2.0], [1.0], rtol=1e-6, atol=0.0)


def test_nan_never_equal() -> None:
    with pytest.raises(ValidationError):
        assert_close([np.nan], [np.nan], rtol=1.0, atol=1.0)


def test_zero_expected_reports_infinite_relative_error() -> None:
    with pytest.raises(ValidationError, match="rel inf"):
        assert_close([1e-3], [0.0], rtol=1e-6, atol=1e-9)


def test_atol_covers_zero() -> None:
    assert_close([1e-12], [0.0], rtol=0.0, atol=1e-9)


def test_is_ecosystem_and_assertion_error() -> None:
    assert issubclass(ValidationError, EnggMathError)
    assert issubclass(ValidationError, AssertionError)
