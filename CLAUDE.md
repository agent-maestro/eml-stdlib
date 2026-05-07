# eml-stdlib — Agent Handoff

## What this is

The verified standard library for the EML language. Math, signal, control, physics, biology, ballistics, ML, and game-development kernels — every module declares its Pfaffian chain order and ~89% carry `@verify(lean, …)` contracts.

## Architecture in one paragraph

`eml_stdlib/<category>/<file>.eml` is the source-of-truth layout. The gaming category is nested one level deeper (`eml_stdlib/gaming/<subcat>/<file>.eml`). The Python side is just a thin introspection layer (`eml_stdlib/__init__.py` exposes `path_to`, `list_modules`, `categories`, `load_catalog`). The build pipeline is two scripts:

1. `python scripts/build_stdlib.py` — copies external sources into the layout (per `COPY_MAP`), parses every `.eml`, writes `eml_stdlib/catalog.json`.
2. `python scripts/generate_readme.py` — reads `catalog.json`, writes the per-category README sections.

`pyproject.toml` ships `**/*.eml` and `catalog.json` as package data, so `pip install eml-stdlib` lands the `.eml` source files inside `site-packages` for downstream Forge projects.

## Where the math comes from

This *is* the source-of-truth. Other Monogate projects (longshot, apex-predator) mirror these kernels in GDScript; if a kernel changes here, find the mirrors via `grep -rn "<fn_name>" ~/monogate/{longshot,apex-predator}` and update them.

## How to run tests

```bash
python -m pytest tests/ -q
```

Expected: 11 passed. Tests cover version, category roster, path resolution, catalog completeness, gaming subcategories, ballistics roster, verified-fn count regression guard.

## How to add a module

1. Write `eml_stdlib/<category>/<file>.eml` with `module`, `@verify`, `where chain_order <=`.
2. Append a `("<category>/<file>.eml", None)` row to `COPY_MAP` in `scripts/build_stdlib.py`.
3. If creating a new category, add a row to `CATEGORY_ORDER` in `scripts/generate_readme.py` with a one-line blurb.
4. `python scripts/build_stdlib.py && python scripts/generate_readme.py && python -m pytest tests/ -q`.
5. Bump `pyproject.toml` + `eml_stdlib/__init__.py` if the API surface changed; bump regression guard in `tests/test_smoke.py` if module count grew.

## Repo-specific gotchas

- Nested `gaming/<subcat>/file.eml` paths require the build script to derive `category` from the first **2** path segments. Already wired; if you add another nested category, the existing logic in `build_stdlib.py` (line ~360) handles it.
- README is regenerated, not hand-edited. Don't touch `README.md` directly — change `generate_readme.py` and re-run.

## Status

**v0.3.0** — 168 modules / 491 fns / 436 verified (89%). Public on GitHub at `agent-maestro/eml-stdlib`.
