"""eml-stdlib -- verified standard library for the EML language.

This package ships *.eml source files (not Python modules). Use
the helpers below to locate them so a Forge project can wire them
into its `use stdlib::...` resolver.

Example:

    from eml_stdlib import path_to, list_modules, load_catalog

    sigmoid = path_to('math/sigmoid.eml')   # absolute Path
    math_dir = path_to('math')              # category directory
    print(load_catalog()[0])                # introspection metadata
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

__version__ = "0.4.0"

_PACKAGE_ROOT = Path(__file__).resolve().parent
_CATALOG_PATH = _PACKAGE_ROOT / "catalog.json"


def root() -> Path:
    """Return the directory holding all category subfolders."""
    return _PACKAGE_ROOT


def path_to(relative: str) -> Path:
    """Resolve a path inside the stdlib (file or directory).

    Raises FileNotFoundError if the resolved path doesn't exist.
    """
    target = (_PACKAGE_ROOT / relative).resolve()
    if not str(target).startswith(str(_PACKAGE_ROOT)):
        raise ValueError(f"path escapes stdlib: {relative}")
    if not target.exists():
        raise FileNotFoundError(target)
    return target


def list_modules(category: str | None = None) -> list[Path]:
    """Return paths to every .eml file in the stdlib (or one category).

    `category` accepts both flat ("math") and nested ("gaming/noise")
    paths. Nested subcategories under gaming/ are picked up via rglob
    so `list_modules("gaming")` returns all 60 gaming kernels.
    """
    if category is None:
        return sorted(_PACKAGE_ROOT.rglob("*.eml"))
    cat_dir = _PACKAGE_ROOT / category
    if not cat_dir.is_dir():
        raise FileNotFoundError(cat_dir)
    return sorted(cat_dir.rglob("*.eml"))


def categories() -> list[str]:
    """Return the names of every shipped category subdir."""
    return sorted(
        p.name for p in _PACKAGE_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")
    )


def load_catalog() -> list[dict[str, Any]]:
    """Return the parsed catalog (function-level introspection)."""
    return json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))


__all__ = [
    "__version__",
    "root",
    "path_to",
    "list_modules",
    "categories",
    "load_catalog",
]
