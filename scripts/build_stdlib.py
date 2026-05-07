"""Build script for eml-stdlib.

Copies cataloged EML modules from the wider Monogate ecosystem into
the categorised layout under `eml_stdlib/<category>/<file>.eml`, then
emits `catalog.json` describing every shipped module so the README
generator and downstream Forge tooling can introspect the library.

Run from the repo root:

    python scripts/build_stdlib.py
"""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path.home() / "monogate"
STDLIB = Path(__file__).resolve().parent.parent / "eml_stdlib"

# (target_path, source_path_or_None_if_new) ─ if source is None the file
# is expected to already exist (because we wrote it directly with the
# Write tool); the build script only verifies presence.
COPY_MAP: list[tuple[str, str | None]] = [
    # ── math ─────────────────────────────────────────────────────
    ("math/gaussian.eml",  "forge/examples/gaussian.eml"),
    ("math/sigmoid.eml",   "forge/examples/sigmoid.eml"),
    ("math/softmax.eml",   "forge/industries/ml/activations/softmax.eml"),
    ("math/tanh.eml",      "forge/industries/ml/activations/tanh.eml"),
    ("math/relu.eml",      "forge/industries/ml/activations/relu.eml"),
    ("math/exp.eml",       None),
    ("math/log.eml",       None),
    ("math/sqrt.eml",      None),
    ("math/pow.eml",       None),
    ("math/abs.eml",       None),
    ("math/sin.eml",       None),
    ("math/cos.eml",       None),
    ("math/tan.eml",       None),
    ("math/atan.eml",      None),
    ("math/atan2.eml",     None),
    ("math/sinh.eml",      None),
    ("math/cosh.eml",      None),
    ("math/erf.eml",       None),
    ("math/gamma.eml",     None),
    ("math/bessel_j0.eml", None),

    # ── signal ───────────────────────────────────────────────────
    ("signal/fft_butterfly.eml",  "monogate-research/industries/signal_processing/kernels/fft_butterfly.eml"),
    ("signal/dft_single.eml",     "monogate-research/industries/signal_processing/kernels/dft_single.eml"),
    ("signal/chirp.eml",          "monogate-research/exploration/bat_sonar/eml/chirp.eml"),
    ("signal/matched_filter.eml", "monogate-research/exploration/bat_sonar/eml/matched_filter.eml"),
    ("signal/bandpass.eml",       None),
    ("signal/notch_filter.eml",   None),
    ("signal/lowpass.eml",        None),
    ("signal/highpass.eml",       None),
    ("signal/window_hann.eml",    None),
    ("signal/window_hamming.eml", None),

    # ── control ──────────────────────────────────────────────────
    ("control/pid.eml",        "forge/examples/pid_controller.eml"),
    ("control/bangbang.eml",   None),
    ("control/hysteresis.eml", None),
    ("control/kalman_1d.eml",  None),
    ("control/lqr_1d.eml",     None),
    ("control/deadband.eml",   None),

    # ── physics ──────────────────────────────────────────────────
    ("physics/wave_propagation.eml",  None),
    ("physics/damped_oscillator.eml", "forge/examples/damped_wave.eml"),
    ("physics/planck_radiation.eml",  "forge/industries/scientific/physics/planck_radiation.eml"),
    ("physics/stefan_boltzmann.eml",  "forge/industries/scientific/climate/stefan_boltzmann.eml"),
    ("physics/coulomb.eml",           None),
    ("physics/gravity.eml",           "forge/industries/gaming/physics/gravity.eml"),
    ("physics/hooke.eml",             None),
    ("physics/navier_stokes_1d.eml",  None),
    ("physics/diffusion.eml",         None),

    # ── circuits ─────────────────────────────────────────────────
    ("circuits/rc_filter.eml",       "forge/examples/rc_filter.eml"),
    ("circuits/voltage_divider.eml", "forge/examples/voltage_divider.eml"),
    ("circuits/cmos_inverter.eml",   "forge/examples/carriers/electronics/cmos_inverter.eml"),
    ("circuits/pll_loop.eml",        "forge/examples/carriers/electronics/pll_loop.eml"),
    ("circuits/h_bridge.eml",        None),
    ("circuits/ldo.eml",             None),
    ("circuits/buck_converter.eml",  None),
    ("circuits/mosfet_iv.eml",       "forge/examples/carriers/electronics/mosfet_iv.eml"),

    # ── sensors ──────────────────────────────────────────────────
    ("sensors/photodetector.eml", "forge/examples/photonics/components/photodetector.eml"),
    ("sensors/hall_effect.eml",   None),
    ("sensors/thermistor.eml",    None),
    ("sensors/accelerometer.eml", None),
    ("sensors/strain_gauge.eml",  None),
    ("sensors/rtd.eml",           None),

    # ── biology ──────────────────────────────────────────────────
    ("biology/rod_sensitivity.eml",    "monogate-research/exploration/cat_vision/eml/rod_sensitivity.eml"),
    ("biology/cone_s.eml",             "monogate-research/exploration/cat_vision/eml/cone_s.eml"),
    ("biology/cone_l.eml",             "monogate-research/exploration/cat_vision/eml/cone_l.eml"),
    ("biology/tapetum.eml",            "monogate-research/exploration/cat_vision/eml/tapetum.eml"),
    ("biology/michaelis_menten.eml",   "forge/industries/chemistry/kinetics/michaelis_menten.eml"),
    ("biology/hill_equation.eml",      "forge/industries/chemistry/kinetics/hill.eml"),
    ("biology/hodgkin_huxley.eml",     "forge/industries/scientific/biology/hodgkin_huxley_step.eml"),
    ("biology/goldman_equation.eml",   None),
    ("biology/receptor_binding.eml",   "monogate-research/exploration/dog_olfaction/eml/receptor_binding.eml"),
    ("biology/plume_diffusion.eml",    "monogate-research/exploration/dog_olfaction/eml/plume_diffusion.eml"),
    ("biology/cryptochrome.eml",       "monogate-research/exploration/pigeon_magnetoreception/eml/cryptochrome.eml"),
    ("biology/geomagnetic_field.eml",  "monogate-research/exploration/pigeon_magnetoreception/eml/geomagnetic_field.eml"),

    # ── carriers ─────────────────────────────────────────────────
    ("carriers/mach_zehnder.eml",       "forge/examples/carriers/photonics/mach_zehnder.eml"),
    ("carriers/ring_resonator.eml",     "forge/examples/carriers/photonics/ring_resonator.eml"),
    ("carriers/optical_neuron.eml",     "forge/examples/carriers/photonics/optical_neuron.eml"),
    ("carriers/magnon_dispersion.eml",  "forge/examples/carriers/spintronics/magnon_dispersion.eml"),
    ("carriers/spin_torque.eml",        "forge/examples/carriers/spintronics/spin_torque.eml"),
    ("carriers/magnon_logic.eml",       "forge/examples/carriers/spintronics/magnon_logic.eml"),
    ("carriers/phonon_bandgap.eml",     "forge/examples/carriers/phononics/phonon_bandgap.eml"),
    ("carriers/thermal_rectifier.eml",  "forge/examples/carriers/phononics/thermal_rectifier.eml"),
    ("carriers/acoustic_cloak.eml",     "forge/examples/carriers/phononics/acoustic_cloak.eml"),
    ("carriers/ferron_propagation.eml", "forge/examples/carriers/ferronics/ferron_propagation.eml"),
    ("carriers/ferron_emission.eml",    "forge/examples/carriers/ferronics/ferron_emission.eml"),
    ("carriers/ferron_logic.eml",       "forge/examples/carriers/ferronics/ferron_logic.eml"),

    # ── quantum ──────────────────────────────────────────────────
    ("quantum/hadamard.eml",      "forge/examples/carriers/quantum/hadamard.eml"),
    ("quantum/phase_gate.eml",    "forge/examples/carriers/quantum/phase_gate.eml"),
    ("quantum/cnot.eml",          "forge/examples/carriers/quantum/cnot.eml"),
    ("quantum/grover_oracle.eml", "forge/examples/carriers/quantum/grover_oracle.eml"),
    ("quantum/pauli_x.eml",       "monogate-research/industries/quantum/kernels/pauli_x.eml"),
    ("quantum/pauli_z.eml",       "monogate-research/industries/quantum/kernels/pauli_z.eml"),
    ("quantum/rotation_rz.eml",   "monogate-research/industries/quantum/kernels/rotation.eml"),

    # ── ml ───────────────────────────────────────────────────────
    ("ml/gelu.eml",          "forge/industries/ml/activations/gelu.eml"),
    ("ml/silu.eml",          None),
    ("ml/relu.eml",          "forge/industries/ml/activations/relu.eml"),
    ("ml/leaky_relu.eml",    None),
    ("ml/softmax.eml",       "forge/industries/ml/activations/softmax.eml"),
    ("ml/layernorm.eml",     None),
    ("ml/attention.eml",     None),
    ("ml/rotary_embed.eml",  None),
    ("ml/cross_entropy.eml", "forge/industries/ml/loss/cross_entropy.eml"),
]


@dataclass
class FunctionEntry:
    name: str
    chain_order: int | None
    verified: bool


@dataclass
class ModuleEntry:
    category: str
    file: str
    module: str
    functions: list[FunctionEntry]
    description: str
    source: str  # original source path (relative to ~/monogate) or "new"


# ── Lightweight parser ──────────────────────────────────────────────
#
# We deliberately stay textual rather than depending on the Forge
# parser; the goal is to introspect the shipped sources for a README
# table, not to type-check them. Full type checks happen via the
# Forge compiler in CI.

MODULE_RE  = re.compile(r"^\s*module\s+([A-Za-z_][A-Za-z0-9_]*)\s*;", re.MULTILINE)
FN_RE      = re.compile(r"^\s*fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.MULTILINE)
CHAIN_RE   = re.compile(r"chain_order\s*<=\s*(\d+)")
VERIFY_RE  = re.compile(r"@verify\s*\(", re.MULTILINE)
HEADER_RE  = re.compile(r"^//[^\n]*--\s*([^\n]+)", re.MULTILINE)

# Research-kernel format: a YAML-ish spec layout (@kernel/@params/@body)
# used by the monogate-research exploration tree. Different syntactic
# universe from the Forge module syntax above; we parse it just enough
# to populate the catalog.
KERNEL_BLOCK_RE  = re.compile(
    r"@kernel\b[\s\S]*?name:\s*\"?([A-Za-z_][A-Za-z0-9_]*)\"?",
    re.MULTILINE,
)
KERNEL_CHAIN_RE  = re.compile(r"chain_order:\s*(\d+)")
KERNEL_VERIFY_RE = re.compile(r"^@verify\b", re.MULTILINE)
HASH_HEADER_RE   = re.compile(r"^#[^\n]*[—-]+\s*([^\n]+)", re.MULTILINE)


def parse_research_kernel(text: str) -> tuple[str, list[FunctionEntry], str] | None:
    """Parse the @kernel / @params / @body research-spec format.

    Returns None if the file isn't in this format; otherwise returns
    (module_name, [single FunctionEntry], description).
    """
    name_match = KERNEL_BLOCK_RE.search(text)
    if not name_match:
        return None
    name = name_match.group(1)
    chain_match = KERNEL_CHAIN_RE.search(text)
    chain = int(chain_match.group(1)) if chain_match else None
    verified = bool(KERNEL_VERIFY_RE.search(text))

    header = HASH_HEADER_RE.search(text)
    description = header.group(1).strip() if header else ""

    return name, [FunctionEntry(name=name, chain_order=chain, verified=verified)], description


def parse_eml(text: str) -> tuple[str, list[FunctionEntry], str]:
    module_match = MODULE_RE.search(text)
    if not module_match:
        # Not a Forge module -- try the research-kernel format.
        kernel = parse_research_kernel(text)
        if kernel is not None:
            return kernel
    module = module_match.group(1) if module_match else "<unknown>"

    # First descriptive line in the file header.
    header = HEADER_RE.search(text)
    description = header.group(1).strip() if header else ""

    fns: list[FunctionEntry] = []
    for fn_match in FN_RE.finditer(text):
        name = fn_match.group(1)
        # Look ahead ~400 chars for chain_order and @verify before the
        # next `fn` declaration.
        end = fn_match.end()
        next_fn = FN_RE.search(text, end)
        block = text[fn_match.start():next_fn.start() if next_fn else len(text)]

        chain_match = CHAIN_RE.search(block)
        chain = int(chain_match.group(1)) if chain_match else None

        # Look back ~200 chars for the @verify decorator that precedes
        # this fn declaration.
        before = text[max(0, fn_match.start() - 400):fn_match.start()]
        verified = bool(VERIFY_RE.search(before))

        fns.append(FunctionEntry(name=name, chain_order=chain, verified=verified))

    return module, fns, description


def main() -> None:
    catalog: list[ModuleEntry] = []

    for target_rel, source_rel in COPY_MAP:
        target = STDLIB / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)

        if source_rel is not None:
            source = ROOT / source_rel
            if not source.exists():
                raise FileNotFoundError(f"missing source: {source}")
            shutil.copy(source, target)
            origin = source_rel
        else:
            if not target.exists():
                raise FileNotFoundError(
                    f"expected hand-written file at {target_rel} -- create it before "
                    "running build_stdlib.py"
                )
            origin = "new"

        text = target.read_text(encoding="utf-8")
        module, fns, description = parse_eml(text)
        catalog.append(ModuleEntry(
            category=target_rel.split("/", 1)[0],
            file=target_rel,
            module=module,
            functions=fns,
            description=description,
            source=origin,
        ))

    catalog.sort(key=lambda m: (m.category, m.file))
    out_path = STDLIB / "catalog.json"
    out_path.write_text(
        json.dumps([asdict(m) for m in catalog], indent=2) + "\n",
        encoding="utf-8",
    )
    n_modules  = len(catalog)
    n_funcs    = sum(len(m.functions) for m in catalog)
    n_verified = sum(1 for m in catalog for f in m.functions if f.verified)
    print(f"wrote {n_modules} modules / {n_funcs} fns / {n_verified} verified -> {out_path}")


if __name__ == "__main__":
    main()
