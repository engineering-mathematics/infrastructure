"""Condition-number policy."""

from __future__ import annotations

import math
import warnings

import pytest

from engg_math.core import ConditioningWarning, IllConditionedError, check_condition, override


def test_below_warning_is_silent() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        check_condition(10.0)


def test_between_thresholds_warns() -> None:
    with pytest.warns(ConditioningWarning, match="solve"):
        check_condition(1e6, "solve")


def test_at_error_threshold_raises() -> None:
    with pytest.raises(IllConditionedError):
        check_condition(1e7)


def test_strict_mode_promotes_warning() -> None:
    with override(strict_mode=True), pytest.raises(IllConditionedError):
        check_condition(1e6)


@pytest.mark.parametrize("kappa", [math.nan, math.inf])
def test_nan_and_inf_fail(kappa: float) -> None:
    with pytest.raises(IllConditionedError):
        check_condition(kappa)


def test_thresholds_follow_override() -> None:
    with override(kappa_warning=1.0, kappa_error=2.0), pytest.raises(IllConditionedError):
        check_condition(2.0)
