"""Wall-clock benchmarks and regression comparison."""

from __future__ import annotations

import json
import statistics
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class BenchResult:
    """Timing summary in seconds."""

    min_s: float
    median_s: float
    repeat: int


@dataclass(frozen=True, slots=True)
class Regression:
    """A benchmark slower than baseline by more than the tolerance."""

    name: str
    baseline_s: float
    current_s: float

    @property
    def ratio(self) -> float:
        """``current / baseline``."""
        return self.current_s / self.baseline_s


def measure(fn: Callable[[], object], *, repeat: int = 7, warmup: int = 1) -> BenchResult:
    """Time ``fn`` ``repeat`` times after ``warmup`` untimed calls."""
    if repeat < 1:
        raise ValueError("repeat must be >= 1")
    for _ in range(warmup):
        fn()
    samples = []
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return BenchResult(min(samples), statistics.median(samples), repeat)


def save_baseline(path: Path, results: Mapping[str, BenchResult]) -> None:
    """Write minimum times (least noisy statistic) to JSON."""
    path.write_text(json.dumps({k: v.min_s for k, v in sorted(results.items())}, indent=2) + "\n")


def load_baseline(path: Path) -> dict[str, float]:
    """Read a baseline written by ``save_baseline``."""
    data = json.loads(path.read_text())
    return {str(k): float(v) for k, v in data.items()}


def find_regressions(
    baseline: Mapping[str, float], current: Mapping[str, float], *, tolerance: float
) -> list[Regression]:
    """Benchmarks present in both whose time grew by more than ``tolerance`` (0.2 = 20 %)."""
    if tolerance < 0:
        raise ValueError("tolerance must be >= 0")
    return [
        Regression(name, baseline[name], current[name])
        for name in sorted(baseline.keys() & current.keys())
        if current[name] > baseline[name] * (1 + tolerance)
    ]
