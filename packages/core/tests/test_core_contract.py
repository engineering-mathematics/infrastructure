"""Package contract."""

from __future__ import annotations

import importlib
import importlib.resources
import pkgutil

import engg_math
import engg_math.core as pkg


def test_namespace_is_implicit() -> None:
    assert getattr(engg_math, "__file__", None) is None


def test_typed_marker_present() -> None:
    assert importlib.resources.files(pkg).joinpath("py.typed").is_file()


def test_all_resolves() -> None:
    assert all(hasattr(pkg, name) for name in pkg.__all__)


def test_modules_import() -> None:
    for info in pkgutil.walk_packages(pkg.__path__, prefix=f"{pkg.__name__}."):
        importlib.import_module(info.name)
