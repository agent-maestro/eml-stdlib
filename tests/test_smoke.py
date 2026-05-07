"""Smoke tests for the eml-stdlib introspection surface."""

from __future__ import annotations

import json

import eml_stdlib


def test_version_exposed() -> None:
    assert eml_stdlib.__version__ == "0.1.0"


def test_categories_match_directory_layout() -> None:
    cats = eml_stdlib.categories()
    expected = {
        "math", "signal", "control", "physics", "circuits",
        "sensors", "biology", "carriers", "quantum", "ml",
    }
    assert set(cats) == expected


def test_path_to_resolves_known_module() -> None:
    p = eml_stdlib.path_to("math/sigmoid.eml")
    assert p.exists()
    assert p.name == "sigmoid.eml"


def test_path_to_rejects_escape_attempts() -> None:
    import pytest
    with pytest.raises((ValueError, FileNotFoundError)):
        eml_stdlib.path_to("../forge/secret.eml")


def test_list_modules_returns_eml_files() -> None:
    files = eml_stdlib.list_modules()
    assert len(files) >= 99
    assert all(f.suffix == ".eml" for f in files)


def test_list_modules_filtered_by_category() -> None:
    math_files = eml_stdlib.list_modules("math")
    assert len(math_files) == 20
    assert all(f.parent.name == "math" for f in math_files)


def test_catalog_loadable_and_well_formed() -> None:
    cat = eml_stdlib.load_catalog()
    assert isinstance(cat, list)
    assert len(cat) == 99
    for entry in cat:
        assert {"category", "file", "module", "functions", "description", "source"} <= set(entry)
        assert isinstance(entry["functions"], list)


def test_catalog_minimum_verified_count() -> None:
    cat = eml_stdlib.load_catalog()
    verified = sum(1 for m in cat for f in m["functions"] if f["verified"])
    # Regression guard: never drop below the launch coverage.
    assert verified >= 250, f"verified count regressed: {verified}"
