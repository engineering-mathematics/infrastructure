"""Console factory."""

from __future__ import annotations

import os
import sys

from rich.console import Console

from engg_math.viz.theme import THEME


def make_console(*, stderr: bool = False) -> Console:
    """Return a themed console.

    Colour is off when ``NO_COLOR`` is set or the stream is not a terminal.
    """
    stream = sys.stderr if stderr else sys.stdout
    return Console(
        theme=THEME,
        file=stream,
        stderr=stderr,
        no_color=bool(os.environ.get("NO_COLOR")),
        highlight=False,
    )
