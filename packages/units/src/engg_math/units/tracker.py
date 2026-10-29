"""Axis-level unit tracking for matrices."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import pint

from engg_math.units.errors import DimensionalError
from engg_math.units.registry import get_registry

UnitLike = str | pint.Unit


def _as_unit(unit: UnitLike) -> pint.Unit:
    return get_registry().Unit(unit) if isinstance(unit, str) else unit


class DimensionalTracker:
    """Units along one matrix axis.

    ``A[i, j]`` has unit ``row[i] / col[j]``. ``A @ B`` is valid when A's column
    dimensions equal B's row dimensions; dimensionless axes match anything.
    """

    def __init__(
        self, units: UnitLike | Sequence[UnitLike] | None = None, length: int | None = None
    ) -> None:
        """Build from nothing (dimensionless), one unit repeated ``length`` times, or a sequence."""
        reg = get_registry()
        if units is None:
            self.units: list[pint.Unit] = [reg.dimensionless] * (length or 0)
        elif isinstance(units, str | pint.Unit):
            self.units = [_as_unit(units)] * (length or 1)
        elif isinstance(units, Sequence):
            self.units = [_as_unit(u) for u in units]
            if length is not None and len(self.units) != length:
                raise ValueError(f"{len(self.units)} units given for axis length {length}")
        else:
            raise TypeError("units must be a str, pint.Unit, or a sequence of them")

    def __len__(self) -> int:
        """Axis length."""
        return len(self.units)

    def __getitem__(self, index: int) -> pint.Unit:
        """Return the unit at ``index``."""
        return self.units[index]

    def __eq__(self, other: object) -> bool:
        """Equal when every axis unit is equal."""
        return isinstance(other, DimensionalTracker) and self.units == other.units

    __hash__ = None  # type: ignore[assignment]

    @staticmethod
    def _dimensionless(unit: pint.Unit) -> bool:
        return bool(unit.dimensionless)

    @classmethod
    def validate_matmul(cls, a_cols: DimensionalTracker, b_rows: DimensionalTracker) -> None:
        """Raise ``DimensionalError`` unless ``A @ B`` is dimensionally valid."""
        if len(a_cols) != len(b_rows):
            raise DimensionalError(
                f"shape mismatch: A has {len(a_cols)} columns, B has {len(b_rows)} rows"
            )
        for i, (a, b) in enumerate(zip(a_cols.units, b_rows.units, strict=True)):
            if cls._dimensionless(a) or cls._dimensionless(b):
                continue
            if a.dimensionality != b.dimensionality:
                raise DimensionalError(
                    f"index {i}: A column unit [{a}] incompatible with B row unit [{b}]"
                )

    def __repr__(self) -> str:
        """Debug representation."""
        return f"DimensionalTracker({[str(u) for u in self.units]})"


def check_compatible(a: pint.Quantity[Any] | pint.Unit, b: pint.Quantity[Any] | pint.Unit) -> None:
    """Raise ``DimensionalError`` unless ``a`` and ``b`` share a dimensionality."""
    da = a.dimensionality
    db = b.dimensionality
    if da != db:
        raise DimensionalError(f"incompatible dimensions: {da} vs {db}")
