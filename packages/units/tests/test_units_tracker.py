"""Dimensional tracking."""

from __future__ import annotations

import pytest

from engg_math.core import EnggMathError
from engg_math.units import DimensionalError, DimensionalTracker, check_compatible, get_registry


def test_registry_is_shared() -> None:
    assert get_registry() is get_registry()
    q = get_registry().Quantity(2.0, "m") + get_registry().Quantity(50, "cm")
    assert q.to("m").magnitude == pytest.approx(2.5)


def test_error_is_ecosystem_error() -> None:
    assert issubclass(DimensionalError, EnggMathError)


def test_default_is_dimensionless() -> None:
    t = DimensionalTracker(length=3)
    assert len(t) == 3
    assert all(u.dimensionless for u in t.units)


def test_single_unit_repeats() -> None:
    t = DimensionalTracker("m", length=4)
    assert len(t) == 4
    assert t[0] == t[3]


def test_single_unit_defaults_to_length_one() -> None:
    assert len(DimensionalTracker("s")) == 1


def test_sequence_and_length_check() -> None:
    assert len(DimensionalTracker(["m", "s"], length=2)) == 2
    with pytest.raises(ValueError, match="axis length"):
        DimensionalTracker(["m", "s"], length=3)


def test_rejects_bad_type() -> None:
    with pytest.raises(TypeError):
        DimensionalTracker(3.0)  # type: ignore[arg-type]


def test_equality_and_repr() -> None:
    assert DimensionalTracker(["m", "s"]) == DimensionalTracker(["m", "s"])
    assert DimensionalTracker(["m"]) != DimensionalTracker(["s"])
    assert DimensionalTracker(["m"]) != "m"
    assert "meter" in repr(DimensionalTracker(["m"]))


def test_matmul_compatible_dimensions() -> None:
    DimensionalTracker.validate_matmul(
        DimensionalTracker(["m", "s"]), DimensionalTracker(["cm", "ms"])
    )


def test_matmul_dimension_mismatch() -> None:
    with pytest.raises(DimensionalError, match="index 1"):
        DimensionalTracker.validate_matmul(
            DimensionalTracker(["m", "s"]), DimensionalTracker(["m", "kg"])
        )


def test_matmul_shape_mismatch() -> None:
    with pytest.raises(DimensionalError, match="shape mismatch"):
        DimensionalTracker.validate_matmul(
            DimensionalTracker("m", length=2), DimensionalTracker("m", length=3)
        )


def test_dimensionless_matches_anything() -> None:
    DimensionalTracker.validate_matmul(DimensionalTracker(length=1), DimensionalTracker(["kg"]))
    DimensionalTracker.validate_matmul(DimensionalTracker(["kg"]), DimensionalTracker(length=1))


def test_check_compatible() -> None:
    reg = get_registry()
    check_compatible(reg.Quantity(1, "m"), reg.Quantity(1, "km"))
    with pytest.raises(DimensionalError):
        check_compatible(reg.Quantity(1, "m"), reg.Quantity(1, "s"))
