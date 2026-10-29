"""Test-time tooling. Never imported by libraries."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from engg_math.devtools.bench import (
    BenchResult,
    Regression,
    find_regressions,
    load_baseline,
    measure,
    save_baseline,
)
from engg_math.devtools.errors import ValidationError
from engg_math.devtools.graph import TIERS, Violation, check_graph, load_deps
from engg_math.devtools.validation import assert_close

try:
    __version__ = version("engg-math-devtools")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"

__all__ = [
    "TIERS",
    "BenchResult",
    "Regression",
    "ValidationError",
    "Violation",
    "__version__",
    "assert_close",
    "check_graph",
    "find_regressions",
    "load_baseline",
    "load_deps",
    "measure",
    "save_baseline",
]
