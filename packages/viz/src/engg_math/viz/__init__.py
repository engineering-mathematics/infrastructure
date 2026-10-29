"""Terminal output layer."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from engg_math.viz.console import make_console
from engg_math.viz.latex import LatexRenderable, render_latex, txm_path
from engg_math.viz.output import emit
from engg_math.viz.panels import kv_table, panel
from engg_math.viz.theme import STYLES, THEME, Kind

try:
    __version__ = version("engg-math-viz")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"

__all__ = [
    "STYLES",
    "THEME",
    "Kind",
    "LatexRenderable",
    "__version__",
    "emit",
    "kv_table",
    "make_console",
    "panel",
    "render_latex",
    "txm_path",
]
