"""Console, panels and output switch."""

from __future__ import annotations

import io
import json
import stat
import sys
from pathlib import Path

import pytest
from rich.console import Console

from engg_math.viz import (
    LatexRenderable,
    emit,
    kv_table,
    make_console,
    panel,
    render_latex,
    txm_path,
)


def _capture() -> tuple[Console, io.StringIO]:
    buf = io.StringIO()
    return Console(file=buf, force_terminal=False, width=60), buf


def test_make_console_respects_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    assert make_console().no_color is True
    monkeypatch.delenv("NO_COLOR")
    assert make_console().no_color is False


def test_make_console_stderr() -> None:
    assert make_console(stderr=True).file is sys.stderr


def test_panel_and_table_render() -> None:
    con, buf = _capture()
    con.print(panel("body", "T", "success"))
    con.print(kv_table({"a": 1, "b": "x"}, title="tbl"))
    text = buf.getvalue()
    assert "body" in text
    assert "T" in text
    assert "tbl" in text
    assert "a" in text


def test_emit_json_is_sorted_and_plain() -> None:
    con, buf = _capture()
    emit({"b": 1, "a": {"x": 2}}, as_json=True, console=con)
    assert buf.getvalue() == '{"a": {"x": 2}, "b": 1}\n'
    assert json.loads(buf.getvalue()) == {"a": {"x": 2}, "b": 1}


def test_emit_json_stringifies_unknown_types() -> None:
    con, buf = _capture()
    emit({"p": Path("x")}, as_json=True, console=con)
    assert json.loads(buf.getvalue()) == {"p": "x"}


def test_emit_human_uses_render() -> None:
    con, buf = _capture()
    emit({"a": 1}, as_json=False, render=lambda c: c.print("custom"), console=con)
    assert buf.getvalue().strip() == "custom"


def test_emit_human_default_listing_keeps_brackets_literal() -> None:
    con, buf = _capture()
    emit({"k": "[bold]v[/bold]"}, as_json=False, console=con)
    assert "k: [bold]v[/bold]" in buf.getvalue()


def test_latex_falls_back_without_txm(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    con, buf = _capture()
    assert txm_path() is None
    assert render_latex(r"\frac{1}{s}", "TF", console=con) is False
    assert r"\frac{1}{s}" in buf.getvalue()
    assert "plain" in buf.getvalue()


@pytest.mark.skipif(sys.platform == "win32", reason="shell-script stand-in for txm")
def test_latex_uses_txm_when_available(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    fake = tmp_path / "txm"
    fake.write_text("#!/bin/sh\necho RENDERED:$1\n")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", str(tmp_path))
    con, buf = _capture()
    assert render_latex("x^2", "Sq", console=con) is True
    assert "RENDERED:x^2" in buf.getvalue()


@pytest.mark.skipif(sys.platform == "win32", reason="shell-script stand-in for txm")
def test_latex_falls_back_when_txm_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    fake = tmp_path / "txm"
    fake.write_text("#!/bin/sh\nexit 3\n")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", str(tmp_path))
    con, buf = _capture()
    assert render_latex("y", console=con) is False
    assert "y" in buf.getvalue()


def test_latex_renderable_mixin(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    class Eq(LatexRenderable):
        def _to_latex(self) -> str:
            return "E=mc^2"

    con, buf = _capture()
    assert Eq().render(console=con) is False
    assert "Eq" in buf.getvalue()
    assert "E=mc^2" in buf.getvalue()
