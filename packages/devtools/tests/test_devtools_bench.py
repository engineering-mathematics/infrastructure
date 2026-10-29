"""Benchmark helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from engg_math.devtools import BenchResult, find_regressions, load_baseline, measure, save_baseline

if TYPE_CHECKING:
    from pathlib import Path


def test_measure_counts_calls() -> None:
    calls = []
    result = measure(lambda: calls.append(1), repeat=3, warmup=2)
    assert len(calls) == 5
    assert result.repeat == 3
    assert 0 <= result.min_s <= result.median_s


def test_measure_rejects_zero_repeat() -> None:
    with pytest.raises(ValueError, match="repeat"):
        measure(lambda: None, repeat=0)


def test_baseline_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "base.json"
    save_baseline(path, {"b": BenchResult(2.0, 3.0, 5), "a": BenchResult(1.0, 1.5, 5)})
    assert load_baseline(path) == {"a": 1.0, "b": 2.0}
    assert path.read_text().index('"a"') < path.read_text().index('"b"')


def test_regressions_respect_tolerance() -> None:
    base = {"fast": 1.0, "same": 1.0, "gone": 1.0}
    cur = {"fast": 1.5, "same": 1.1, "new": 9.0}
    found = find_regressions(base, cur, tolerance=0.2)
    assert [(r.name, round(r.ratio, 2)) for r in found] == [("fast", 1.5)]


def test_negative_tolerance_rejected() -> None:
    with pytest.raises(ValueError, match="tolerance"):
        find_regressions({}, {}, tolerance=-0.1)
