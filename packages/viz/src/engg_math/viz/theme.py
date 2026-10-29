"""Visual style tokens. Packages use these, never raw colours."""

from __future__ import annotations

from typing import Literal

from rich.theme import Theme

Kind = Literal["info", "success", "warning", "error", "math"]

# Concrete styles, so panels render on any Rich console, themed or not.
STYLES: dict[Kind, str] = {
    "info": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "bold red",
    "math": "magenta",
}

THEME = Theme({**{str(k): v for k, v in STYLES.items()}, "title": "bold", "muted": "dim"})
