"""Single process-wide unit registry."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pint

if TYPE_CHECKING:
    from pint.registry import ApplicationRegistry


def get_registry() -> ApplicationRegistry:
    """Return the shared registry (pint's application registry)."""
    return pint.get_application_registry()  # type: ignore[no-untyped-call,no-any-return]
