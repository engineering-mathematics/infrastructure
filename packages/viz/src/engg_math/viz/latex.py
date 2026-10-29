"""LaTeX rendering through the external ``txm`` binary. Never installs anything."""

from __future__ import annotations

import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from rich.markup import escape

from engg_math.viz.console import make_console
from engg_math.viz.panels import panel

if TYPE_CHECKING:
    from rich.console import Console

TIMEOUT_S = 10


def txm_path() -> str | None:
    """Locate ``txm`` on PATH or in ``~/.cargo/bin``."""
    found = shutil.which("txm")
    if found:
        return found
    cargo = Path.home() / ".cargo" / "bin" / "txm"
    return str(cargo) if cargo.is_file() and os.access(cargo, os.X_OK) else None


def render_latex(latex: str, title: str = "LaTeX", *, console: Console | None = None) -> bool:
    """Render ``latex`` in a panel. Returns False when it fell back to plain text."""
    out = console or make_console()
    binary = txm_path()
    if binary is not None:
        try:
            result = subprocess.run(  # noqa: S603 - argv list, binary resolved above
                [binary, latex], capture_output=True, text=True, timeout=TIMEOUT_S, check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            result = None
        if result is not None and result.returncode == 0 and result.stdout.strip():
            out.print(panel(escape(result.stdout.rstrip()), title, "math"))
            return True
    out.print(panel(escape(latex), f"{title} (plain)", "math"))
    return False


class LatexRenderable(ABC):
    """Mixin for objects with a LaTeX form."""

    @abstractmethod
    def _to_latex(self) -> str:
        """Return the LaTeX source."""

    @property
    def _title(self) -> str:
        return type(self).__name__

    def render(self, console: Console | None = None) -> bool:
        """Render via ``render_latex``."""
        return render_latex(self._to_latex(), self._title, console=console)
