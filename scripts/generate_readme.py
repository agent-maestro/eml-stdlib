"""Generate the top-level README from catalog.json.

The README is the table of contents for the EML stdlib. Each row
shows: file -> module name, chain order, verified count, source.

Run after `build_stdlib.py`:

    python scripts/build_stdlib.py
    python scripts/generate_readme.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "eml_stdlib" / "catalog.json"
README  = ROOT / "README.md"


CATEGORY_ORDER = [
    ("math",     "Math primitives — transcendentals, special functions, identities."),
    ("signal",   "DSP — filters, FFT, windows, matched-filter."),
    ("control",  "Control — PID, Kalman, LQR, hysteresis, deadband."),
    ("physics",  "Physics — wave propagation, oscillators, blackbody, fluid flow."),
    ("circuits", "Analog circuits — RC, voltage divider, CMOS, MOSFET, PLL, LDO, buck."),
    ("sensors",  "Sensors — Hall effect, thermistor, RTD, accelerometer, strain gauge."),
    ("biology",  "Biology — vision, olfaction, magnetoreception, ion channels."),
    ("carriers", "Wave carriers — photonic, magnonic, phononic, ferronic."),
    ("quantum",  "Quantum gates — Hadamard, Pauli, phase, CNOT, Grover oracle."),
    ("ml",         "Machine learning — activations, attention, RoPE, layernorm, loss."),
    ("ballistics", "Exterior ballistics — drag, gravity, wind, Coriolis, spin drift, air density, muzzle velocity, time of flight."),

    # ── Gaming subcategories ────────────────────────────────────────
    ("gaming/noise",     "Procedural noise — Perlin (2D/3D), Simplex, Voronoi, Worley, value noise, FBM, turbulence."),
    ("gaming/textures",  "Procedural textures — wood, marble, brick, checkerboard, rust, water surface, caustics, fire."),
    ("gaming/shading",   "Shading models — Lambertian + half-Lambert, Cook-Torrance GGX/Smith, Schlick Fresnel, toon, matcap, Burley SSS."),
    ("gaming/lighting",  "Lighting — point + spot + area, ambient occlusion, exponential and squared-exponential fog."),
    ("gaming/terrain",   "Terrain — FBM heightmaps, thermal + hydraulic erosion, biome classification, cliff detection."),
    ("gaming/animation", "Animation — quadratic + cubic ease-in/out, smoothstep + smootherstep, damped springs, bounce, 2-bone IK."),
    ("gaming/particles", "Particles — radial emitter, exponential drag, gravity, lifetime fade, size-over-life."),
    ("gaming/camera",    "Camera — perspective FOV matrix, orbit (spherical), damped-noise shake, depth-of-field circle of confusion."),
    ("gaming/audio",     "Audio — distance attenuation (linear/inverse/inverse-square), Doppler shift, feedback delay reverb, 1-pole low-pass."),
    ("gaming/physics",   "Physics — semi-implicit Euler rigid-body 2D, AABB + circle collision, restitution-aware impulse resolve, Verlet, spring-damper, Archimedes buoyancy."),
]


def main() -> None:
    catalog = json.loads(CATALOG.read_text())
    by_cat: dict[str, list[dict]] = {}
    for module in catalog:
        by_cat.setdefault(module["category"], []).append(module)

    lines: list[str] = []
    lines += [
        "# eml-stdlib",
        "",
        "**The first verified standard library for game development.**",
        "Every shader, every texture, every physics formula — with a mathematical proof.",
        "",
        "Plus the math, signal-processing, control, biology, ballistics, and ML kernels",
        "that built the rest of the Monogate stack. Every module compiles to GDScript,",
        "GLSL, HLSL, C, Python, and Lean (and ~30 other backends via Forge); every",
        "`@verify` contract has a Lean proof obligation against MachLib.",
        "",
        "```bash",
        "pip install eml-stdlib",
        "eml-compile eml_stdlib/gaming/shading/pbr_specular.eml --target glsl",
        "```",
        "",
        "And get a verified PBR specular shader.",
        "",
    ]

    n_modules  = len(catalog)
    n_funcs    = sum(len(m["functions"]) for m in catalog)
    n_verified = sum(1 for m in catalog for f in m["functions"] if f["verified"])

    lines += [
        "## At a glance",
        "",
        f"- **{n_modules} modules** across **{len(CATEGORY_ORDER)} categories**",
        f"- **{n_funcs} functions** total",
        f"- **{n_verified} carry an `@verify(lean, …)` contract** ({n_verified * 100 // n_funcs}%)",
        "- Every function declares its **Pfaffian chain order** in the type",
        "",
        "## Use",
        "",
        "After `pip install`, import the location of the `.eml` source files",
        "into your Forge project:",
        "",
        "```python",
        "from eml_stdlib import path_to",
        "math_dir = path_to('math')           # Path to math/ subdir",
        "sigmoid  = path_to('math/sigmoid.eml')  # Specific module",
        "```",
        "",
        "Inside an EML source file, reference modules with `use`:",
        "",
        "```eml",
        "use stdlib::math::sigmoid;",
        "use stdlib::ml::attention;",
        "use stdlib::circuits::rc_filter;",
        "```",
        "",
        "## Directory map",
        "",
    ]

    # Per-category section.
    for category, blurb in CATEGORY_ORDER:
        modules = sorted(by_cat.get(category, []), key=lambda m: m["file"])
        if not modules:
            continue

        n_mod = len(modules)
        n_fns = sum(len(m["functions"]) for m in modules)
        n_ver = sum(1 for m in modules for f in m["functions"] if f["verified"])

        lines += [
            f"### `{category}/` — {n_mod} modules / {n_fns} fns / {n_ver} verified",
            "",
            blurb,
            "",
            "| File | Functions | Chain | Verified | Origin |",
            "|------|-----------|-------|----------|--------|",
        ]

        for m in modules:
            file_short = m["file"].split("/", 1)[1]
            fn_names = ", ".join(f["name"] for f in m["functions"])
            chains = sorted({
                f["chain_order"]
                for f in m["functions"]
                if f["chain_order"] is not None
            })
            chain_label = ",".join(str(c) for c in chains) if chains else "—"
            verified_count = sum(1 for f in m["functions"] if f["verified"])
            verified_label = (
                f"{verified_count}/{len(m['functions'])}"
                if m["functions"] else "—"
            )
            origin = "**new**" if m["source"] == "new" else m["source"]

            # Trim absurdly long fn lists in the table.
            if len(fn_names) > 60:
                head = ", ".join(f["name"] for f in m["functions"][:3])
                fn_names = f"{head}, … (+{len(m['functions']) - 3})"

            lines += [
                f"| `{file_short}` | {fn_names} | {chain_label} | {verified_label} | {origin} |"
            ]

        lines.append("")

    # Glossary.
    lines += [
        "## Vocabulary",
        "",
        "**Chain order** — the Pfaffian chain order, an upper bound on how many",
        "transcendental compositions deep a function reaches. Order 0 = pure",
        "polynomial / rational. Order 1 = single transcendental wrapping a",
        "polynomial argument (e.g. `exp`, `sin`, `ln`). Order 2 = two",
        "transcendentals composed (e.g. `tanh = sinh/cosh`). Forge uses chain",
        "order to bound termination, place transcendentals on FPGA / GPU, and",
        "select the right Lean tactic.",
        "",
        "**`@verify(lean, theorem = …)`** — the function carries a Lean proof",
        "obligation. The Forge Lean backend emits the obligation; closing it",
        "against MachLib is what makes the function *verified*.",
        "",
        "**Origin: `new`** — written for this stdlib. Otherwise the column",
        "shows the path under `~/monogate/` from which the module was copied",
        "(originals stay where they are; the stdlib is the curated home).",
        "",
        "## License",
        "",
        "MIT — see `LICENSE`.",
        "",
    ]

    README.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {README} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
