"""Ecosystem dependency-graph policy: acyclic, and edges never point up the tiers."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence

PREFIX = "engg-math-"
TOOLING_TIER = 99  # may depend on anything; nothing may depend on it

_INFRA = {"core": 0, "units": 0, "viz": 0}
_FOUNDATIONS = [
    "linear-systems",
    "continuous-analysis",
    "dynamical-systems",
    "discrete-structures",
    "stochastic-systems",
    "numerical-computation",
    "optimization",
    "transform-analysis",
]
_MODELLING = [
    "state-space",
    "transfer-functions",
    "graph-models",
    "physical-systems",
    "constraint-models",
]
_DOMAIN = [
    "biomedical",
    "cfd",
    "communications",
    "control",
    "fem",
    "machine-learning",
    "navigation",
    "power-systems",
    "robotics",
    "signal-processing",
]

TIERS: dict[str, int] = {
    **{f"{PREFIX}{n}": t for n, t in _INFRA.items()},
    **{f"{PREFIX}{n}": 1 for n in _FOUNDATIONS},
    **{f"{PREFIX}{n}": 2 for n in _MODELLING},
    **{f"{PREFIX}{n}": 3 for n in _DOMAIN},
    f"{PREFIX}devtools": TOOLING_TIER,
    f"{PREFIX}cli": TOOLING_TIER,
}

_NAME = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


@dataclass(frozen=True, slots=True)
class Violation:
    """One policy violation."""

    kind: str  # "cycle" | "upward" | "unknown"
    detail: str


def _normalise(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def requirement_name(requirement: str) -> str | None:
    """Normalised distribution name of a PEP 508 string, or None if unparsable."""
    match = _NAME.match(requirement)
    return _normalise(match.group(1)) if match else None


def load_deps(pyprojects: Iterable[Path]) -> dict[str, set[str]]:
    """Map each ``engg-math-*`` distribution to its ``engg-math-*`` deps (extras included)."""
    graph: dict[str, set[str]] = {}
    for path in pyprojects:
        project = tomllib.loads(path.read_text()).get("project", {})
        name = _normalise(project.get("name", ""))
        if not name.startswith(PREFIX):
            continue
        reqs = list(project.get("dependencies", []))
        for extra in project.get("optional-dependencies", {}).values():
            reqs.extend(extra)
        deps = {n for r in reqs if (n := requirement_name(r)) and n.startswith(PREFIX)}
        graph[name] = deps - {name}
    return graph


def _find_cycle(graph: Mapping[str, set[str]]) -> list[str] | None:
    state: dict[str, int] = {}  # 1 = on stack, 2 = done
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        state[node] = 1
        stack.append(node)
        for dep in sorted(graph.get(node, ())):
            if state.get(dep) == 1:
                return [*stack[stack.index(dep) :], dep]
            if dep not in state and (cycle := visit(dep)):
                return cycle
        stack.pop()
        state[node] = 2
        return None

    for start in sorted(graph):
        if start not in state and (cycle := visit(start)):
            return cycle
    return None


def check_graph(graph: Mapping[str, set[str]], tiers: Mapping[str, int] = TIERS) -> list[Violation]:
    """Return all violations: unknown packages, upward edges, and one cycle if present."""
    found: list[Violation] = []
    for pkg in sorted(graph):
        if pkg not in tiers:
            found.append(Violation("unknown", f"{pkg} has no tier; register it in TIERS"))
            continue
        for dep in sorted(graph[pkg]):
            if dep not in tiers:
                found.append(Violation("unknown", f"{dep} (needed by {pkg}) has no tier"))
            elif tiers[dep] > tiers[pkg]:
                found.append(
                    Violation(
                        "upward", f"{pkg} (tier {tiers[pkg]}) depends on {dep} (tier {tiers[dep]})"
                    )
                )
    cycle = _find_cycle(graph)
    if cycle:
        found.append(Violation("cycle", " -> ".join(cycle)))
    return found


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: check the given ``pyproject.toml`` files. Exit 1 on violations."""
    parser = argparse.ArgumentParser(prog="engg_math.devtools.graph", description=__doc__)
    parser.add_argument("pyprojects", nargs="+", type=Path)
    args = parser.parse_args(argv)
    violations = check_graph(load_deps(args.pyprojects))
    for v in violations:
        sys.stdout.write(f"{v.kind}: {v.detail}\n")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
