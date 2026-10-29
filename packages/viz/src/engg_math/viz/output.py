"""Human/machine output switch."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from engg_math.viz.console import make_console

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from rich.console import Console


def emit(
    data: Mapping[str, Any],
    *,
    as_json: bool,
    render: Callable[[Console], None] | None = None,
    console: Console | None = None,
) -> None:
    """Write ``data`` as sorted JSON when ``as_json``; otherwise call ``render(console)``.

    JSON goes to stdout with no styling so it can be piped. Without ``render``,
    the human form is a plain ``key: value`` listing.
    """
    out = console or make_console()
    if as_json:
        out.file.write(json.dumps(data, sort_keys=True, default=str) + "\n")
        return
    if render is not None:
        render(out)
        return
    for key, value in data.items():
        out.print(f"{key}: {value}", markup=False)
