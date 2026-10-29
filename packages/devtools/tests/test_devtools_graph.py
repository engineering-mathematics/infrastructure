"""Dependency-graph policy."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from engg_math.devtools import TIERS, check_graph, load_deps
from engg_math.devtools.graph import main, requirement_name

if TYPE_CHECKING:
    from pathlib import Path

LS, CA, DS = (
    "engg-math-linear-systems",
    "engg-math-continuous-analysis",
    "engg-math-dynamical-systems",
)
CORE, DEV, CTRL = "engg-math-core", "engg-math-devtools", "engg-math-control"


def test_clean_downward_graph() -> None:
    assert check_graph({CTRL: {DS}, DS: {CA, LS}, CA: {LS}, LS: {CORE}, CORE: set()}) == []


def test_upward_edge_flagged() -> None:
    (v,) = check_graph({LS: {CTRL}, CTRL: set()})
    assert v.kind == "upward"
    assert "tier 1" in v.detail
    assert "tier 3" in v.detail


def test_same_tier_allowed_but_cycle_flagged() -> None:
    violations = check_graph({LS: {CA}, CA: {LS}})
    assert [v.kind for v in violations] == ["cycle"]
    assert violations[0].detail == f"{CA} -> {LS} -> {CA}"


def test_nobody_may_depend_on_devtools() -> None:
    assert [v.kind for v in check_graph({LS: {DEV}, DEV: {LS}})] == ["upward", "cycle"]


def test_devtools_may_depend_on_libraries() -> None:
    assert check_graph({DEV: {LS, CORE}, LS: set(), CORE: set()}) == []


def test_unknown_packages_flagged() -> None:
    kinds = [v.kind for v in check_graph({"engg-math-mystery": {CORE}, LS: {"engg-math-ghost"}})]
    assert kinds == ["unknown", "unknown"]


def test_tiers_cover_planned_packages() -> None:
    assert TIERS[CORE] == 0
    assert TIERS[LS] == 1
    assert TIERS["engg-math-state-space"] == 2
    assert TIERS[CTRL] == 3


@pytest.mark.parametrize(
    ("req", "name"),
    [
        ("numpy>=1.26", "numpy"),
        ("Engg_Math.Core >=0.1,<0.2", "engg-math-core"),
        ("  rich[extra]; python_version>'3'", "rich"),
        ("!!", None),
    ],
)
def test_requirement_name(req: str, name: str | None) -> None:
    assert requirement_name(req) == name


def _project(tmp: Path, name: str, deps: list[str], extras: list[str] | None = None) -> Path:
    path = tmp / f"{name}.toml"
    opt = f"\n[project.optional-dependencies]\nx = {extras!r}\n".replace("'", '"') if extras else ""
    dep_list = ", ".join(f'"{d}"' for d in deps)
    path.write_text(
        f'[project]\nname = "{name}"\nversion = "0"\ndependencies = [{dep_list}]\n{opt}'
    )
    return path


def test_load_deps_reads_dependencies_and_extras(tmp_path: Path) -> None:
    a = _project(tmp_path, LS, ["numpy", f"{CORE}>=0.1"], extras=[f"{CA}"])
    other = _project(tmp_path, "unrelated", [CORE])
    graph = load_deps([a, other])
    assert graph == {LS: {CORE, CA}}


def test_main_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    good = _project(tmp_path, LS, [CORE])
    assert main([str(good)]) == 0
    bad = _project(tmp_path, CORE, [LS])
    assert main([str(good), str(bad)]) == 1
    out = capsys.readouterr().out
    assert "upward" in out
    assert "cycle" in out
