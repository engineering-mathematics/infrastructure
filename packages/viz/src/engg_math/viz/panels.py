"""Panels and tables in the shared style."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.panel import Panel
from rich.table import Table

from engg_math.viz.theme import STYLES, Kind

if TYPE_CHECKING:
    from collections.abc import Mapping


def panel(body: str, title: str, kind: Kind = "info") -> Panel:
    """Boxed block with a themed border."""
    return Panel(body, title=f"[bold]{title}[/bold]", border_style=STYLES[kind], expand=False)


def kv_table(rows: Mapping[str, object], title: str | None = None) -> Table:
    """Two-column key/value table."""
    table = Table(title=title, show_header=False, box=None, pad_edge=False)
    table.add_column(style="dim", no_wrap=True)
    table.add_column()
    for key, value in rows.items():
        table.add_row(str(key), str(value))
    return table
