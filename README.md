# eml-stdlib

**The first verified standard library for game development.**
Every shader, every texture, every physics formula — with a mathematical proof.

Plus the math, signal-processing, control, biology, ballistics, and ML kernels
that built the rest of the Monogate stack. Every module compiles to GDScript,
GLSL, HLSL, C, Python, and Lean (and ~30 other backends via Forge); every
`@verify` contract has a Lean proof obligation against MachLib.

```bash
pip install eml-stdlib
eml-compile eml_stdlib/gaming/shading/pbr_specular.eml --target glsl
```

And get a verified PBR specular shader.

## At a glance

- **180 modules** across **22 categories**
- **529 functions** total
- **468 carry an `@verify(lean, …)` contract** (88%)
- Every function declares its **Pfaffian chain order** in the type

## Used by

Four Godot 4 prototypes are live consumers of the kernels here. Each one is
a working application of a different stdlib slice; together they cover most
of what game engines actually do at runtime.

| Prototype | Stdlib slice exercised | What it proves |
|-----------|------------------------|----------------|
| **spellforge** | `math/`, `signal/` | Verified expression-tree gameplay — every spell is an EML expression that type-checks as a function |
| **longshot** | `ballistics/` (mirrored line-for-line) | Real exterior ballistics in a 2D sniper sim — drag, gravity, wind, Coriolis, spin drift |
| **apex-predator** | `ballistics/` + `biology/` + `biology/abilities/` + `signal/` | Asymmetric PvP with split-screen + per-viewport fragment-shader fog of war; 25 species evolve a beast through 4 stages |
| **monowave** | local `eml/` mirrors of `signal/` + `gaming/noise/` + `gaming/shading/` | Deterministic music visualizer — same audio in, same visuals out, no randomness anywhere |

The 10 kernels in `biology/abilities/` were promoted up from apex-predator's
local `eml/abilities/` directory in v0.4.0. The local copies remain in that
repo because `scripts/build_stdlib.py` reads from them as the source-of-truth;
deleting them locally would break the stdlib build.

## Use

After `pip install`, import the location of the `.eml` source files
into your Forge project:

```python
from eml_stdlib import path_to
math_dir = path_to('math')           # Path to math/ subdir
sigmoid  = path_to('math/sigmoid.eml')  # Specific module
```

Inside an EML source file, reference modules with `use`:

```eml
use stdlib::math::sigmoid;
use stdlib::ml::attention;
use stdlib::circuits::rc_filter;
```

## Directory map

### `math/` — 20 modules / 67 fns / 63 verified

Math primitives — transcendentals, special functions, identities.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `abs.eml` | abs_kernel, sign, saturate, softsign | 0 | 4/4 | **new** |
| `atan.eml` | atan_kernel, atan_at_zero, atan_at_one | 0,1 | 3/3 | **new** |
| `atan2.eml` | atan2_pos_x, atan2_neg_x_upper, atan2_neg_x_lower, … (+2) | 0,2 | 5/5 | **new** |
| `bessel_j0.eml` | bessel_j0_small, bessel_j0_large, bessel_j0_at_zero | 0,1 | 3/3 | **new** |
| `cos.eml` | cos_kernel, cos_at_zero, cos_sq, pythagorean | 0,1 | 4/4 | **new** |
| `cosh.eml` | cosh_kernel, cosh_at_zero | 0,1 | 2/2 | **new** |
| `erf.eml` | erf_kernel, erf_at_zero, erfc, erf_as | 0,1 | 4/4 | **new** |
| `exp.eml` | exp_kernel, exp_neg, expm1 | 1 | 3/3 | **new** |
| `gamma.eml` | ln_gamma_stirling, gamma_stirling, gamma_at_one | 0,1,2 | 3/3 | **new** |
| `gaussian.eml` | gaussian | 1 | 0/1 | forge/examples/gaussian.eml |
| `log.eml` | ln_kernel, log2, log10, log_b, log1p | 1,2 | 5/5 | **new** |
| `pow.eml` | pow_kernel, sq, cube, pow4, pow8 | 0,2 | 5/5 | **new** |
| `relu.eml` | relu, leaky_relu, relu6, prelu | 0 | 3/4 | forge/industries/ml/activations/relu.eml |
| `sigmoid.eml` | sigmoid, silu | 2 | 0/2 | forge/examples/sigmoid.eml |
| `sin.eml` | sin_kernel, sin_at_zero, sin_sq | 0,1 | 3/3 | **new** |
| `sinh.eml` | sinh_kernel, sinh_at_zero | 0,1 | 2/2 | **new** |
| `softmax.eml` | softmax_shift_exp, softmax_normalize, softmax_two_logit, … (+1) | 0,1,2 | 4/4 | forge/industries/ml/activations/softmax.eml |
| `sqrt.eml` | sqrt_kernel, hypot2, hypot3, rsqrt | 1 | 4/4 | **new** |
| `tan.eml` | tan_kernel, tan_at_zero, two_tan | 0,2 | 3/3 | **new** |
| `tanh.eml` | tanh_activation, tanh_from_sigmoid, hard_tanh | 0,1,2 | 3/3 | forge/industries/ml/activations/tanh.eml |

### `signal/` — 10 modules / 20 fns / 20 verified

DSP — filters, FFT, windows, matched-filter.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `bandpass.eml` | bandpass_step, alphas_from_cutoffs | 0 | 2/2 | **new** |
| `chirp.eml` | chirp_frequency | 0 | 1/1 | monogate-research/exploration/bat_sonar/eml/chirp.eml |
| `dft_single.eml` | dft_single | 1 | 1/1 | monogate-research/industries/signal_processing/kernels/dft_single.eml |
| `fft_butterfly.eml` | fft_butterfly | 1 | 1/1 | monogate-research/industries/signal_processing/kernels/fft_butterfly.eml |
| `highpass.eml` | hpf1_step, alpha_from_rc_dt, alpha_from_cutoff | 0 | 3/3 | **new** |
| `lowpass.eml` | lpf1_step, alpha_from_rc_dt, alpha_from_cutoff | 0 | 3/3 | **new** |
| `matched_filter.eml` | matched_filter_score | 0 | 1/1 | monogate-research/exploration/bat_sonar/eml/matched_filter.eml |
| `notch_filter.eml` | notch_coeffs, notch_step | 0,1 | 2/2 | **new** |
| `window_hamming.eml` | hamming, hamming_at_start, hamming_apply | 0,1 | 3/3 | **new** |
| `window_hann.eml` | hann, hann_at_start, hann_apply | 0,1 | 3/3 | **new** |

### `control/` — 8 modules / 20 fns / 14 verified

Control — PID, Kalman, LQR, hysteresis, deadband.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `bangbang.eml` | bangbang, bangbang_symmetric | 0 | 2/2 | **new** |
| `deadband.eml` | deadband, deadband_asymmetric | 0 | 2/2 | **new** |
| `hysteresis.eml` | hysteresis_step | 0 | 1/1 | **new** |
| `kalman2d_predict.eml` | predict_state, cov_predict | 0 | 1/2 | **new** |
| `kalman2d_update.eml` | innovation, gain, update_state, … (+3) | 0 | 1/6 | **new** |
| `kalman_1d.eml` | kalman1d_predict, kalman1d_update, kalman1d_step | 0 | 3/3 | **new** |
| `lqr_1d.eml` | riccati, lqr_gain, lqr_control | 0,1 | 3/3 | **new** |
| `pid.eml` | pid | 0 | 1/1 | forge/examples/pid_controller.eml |

### `physics/` — 9 modules / 30 fns / 28 verified

Physics — wave propagation, oscillators, blackbody, fluid flow.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `coulomb.eml` | force, field, potential_energy, potential | 0 | 4/4 | **new** |
| `damped_oscillator.eml` | damped_wave | 2 | 0/1 | forge/examples/damped_wave.eml |
| `diffusion.eml` | concentration, sigma, fick_first_law | 0,1 | 3/3 | **new** |
| `gravity.eml` | newtonian_acceleration, surface_gravity_step | 0 | 1/2 | forge/industries/gaming/physics/gravity.eml |
| `hooke.eml` | force, potential_energy, series_stiffness, … (+2) | 0,1 | 5/5 | **new** |
| `navier_stokes_1d.eml` | pressure_term, viscous_term, convective_term, rhs, reynolds | 0 | 5/5 | **new** |
| `planck_radiation.eml` | spectral_radiance, wien_lambda_max, rayleigh_jeans_radiance | 0,1 | 3/3 | forge/industries/scientific/physics/planck_radiation.eml |
| `stefan_boltzmann.eml` | radiative_flux, net_exchange, wien_peak_wavelength | 0,1 | 3/3 | forge/industries/scientific/climate/stefan_boltzmann.eml |
| `wave_propagation.eml` | wave, wavelength, frequency, phase_velocity | 0,1 | 4/4 | **new** |

### `circuits/` — 8 modules / 37 fns / 26 verified

Analog circuits — RC, voltage divider, CMOS, MOSFET, PLL, LDO, buck.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `buck_converter.eml` | circuit, output_voltage, inductor_ripple, … (+2) | 0 | 4/5 | **new** |
| `cmos_inverter.eml` | vout_at_low_input, vout_at_high_input, switching_threshold, … (+3) | 0 | 3/6 | forge/examples/carriers/electronics/cmos_inverter.eml |
| `h_bridge.eml` | circuit, forward_voltage, reverse_voltage, dead_time_loss | 0 | 3/4 | **new** |
| `ldo.eml` | circuit, output_voltage, efficiency, … (+2) | 0 | 4/5 | **new** |
| `mosfet_iv.eml` | drain_current_sat, id_at_threshold, id_prefactor | 0 | 2/3 | forge/examples/carriers/electronics/mosfet_iv.eml |
| `pll_loop.eml` | loop_gain, steady_state_error_at_zero_offset, loop_gain_certificate, … (+1) | 0 | 2/4 | forge/examples/carriers/electronics/pll_loop.eml |
| `rc_filter.eml` | circuit, tau, vout_steady, … (+3) | 0,1 | 5/6 | forge/examples/rc_filter.eml |
| `voltage_divider.eml` | circuit, vout_divider, rsum, vout_symmetric | 0 | 3/4 | forge/examples/voltage_divider.eml |

### `sensors/` — 6 modules / 24 fns / 23 verified

Sensors — Hall effect, thermistor, RTD, accelerometer, strain gauge.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `accelerometer.eml` | lsb_to_si, tilt_angle, tilt_two_axis, magnitude | 0,1,2 | 4/4 | **new** |
| `hall_effect.eml` | hall_voltage, hall_coefficient, b_from_voltage | 0 | 3/3 | **new** |
| `photodetector.eml` | photocurrent, current_at_zero_power, nonneg_current | 0 | 2/3 | forge/examples/photonics/components/photodetector.eml |
| `rtd.eml` | resistance_pos, resistance_neg, temperature_pos | 0,1 | 3/3 | **new** |
| `strain_gauge.eml` | resistance_change, strain_from_dr, quarter_bridge_voltage, … (+3) | 0 | 6/6 | **new** |
| `thermistor.eml` | resistance_beta, temperature_beta, inv_temperature_steinhart, … (+2) | 0,1 | 5/5 | **new** |

### `biology/` — 12 modules / 18 fns / 15 verified

Biology — vision, olfaction, magnetoreception, ion channels.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `cone_l.eml` | cone_l_sensitivity | 1 | 1/1 | monogate-research/exploration/cat_vision/eml/cone_l.eml |
| `cone_s.eml` | cone_s_sensitivity | 1 | 1/1 | monogate-research/exploration/cat_vision/eml/cone_s.eml |
| `cryptochrome.eml` | cryptochrome_yield | 1 | 1/1 | monogate-research/exploration/pigeon_magnetoreception/eml/cryptochrome.eml |
| `geomagnetic_field.eml` | geomagnetic_field | 1 | 1/1 | monogate-research/exploration/pigeon_magnetoreception/eml/geomagnetic_field.eml |
| `goldman_equation.eml` | membrane_potential, nernst | 1 | 2/2 | **new** |
| `hill_equation.eml` | hill_velocity, hill_logit | 1,2 | 1/2 | forge/industries/chemistry/kinetics/hill.eml |
| `hodgkin_huxley.eml` | voltage_step, gating_step | 0 | 2/2 | forge/industries/scientific/biology/hodgkin_huxley_step.eml |
| `michaelis_menten.eml` | velocity, lineweaver_burk, eadie_hofstee | 0 | 1/3 | forge/industries/chemistry/kinetics/michaelis_menten.eml |
| `plume_diffusion.eml` | plume_concentration | 1 | 1/1 | monogate-research/exploration/dog_olfaction/eml/plume_diffusion.eml |
| `receptor_binding.eml` | receptor_binding | 0 | 1/1 | monogate-research/exploration/dog_olfaction/eml/receptor_binding.eml |
| `rod_sensitivity.eml` | rod_sensitivity | 1 | 1/1 | monogate-research/exploration/cat_vision/eml/rod_sensitivity.eml |
| `tapetum.eml` | tapetum_gain, tapetum_amplify | 1 | 2/2 | monogate-research/exploration/cat_vision/eml/tapetum.eml |

### `biology/abilities/` — 10 modules / 30 fns / 30 verified

Biology / abilities — creature combat, movement, and cover: elastic energy, locomotion, chromatophore camouflage, toxin pharmacokinetics, ballistic armor, bioelectric discharge, texture matching, sprint metabolism, muscle power, bite force.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `abilities/ballistic_armor.eml` | kinetic_energy, energy_absorbed, energy_penetrating, … (+1) | 0,1 | 4/4 | apex-predator/eml/abilities/ballistic_armor.eml |
| `abilities/bite_force.eml` | bite_force_n, damage_per_bite, stage_multiplier | 0,1 | 3/3 | apex-predator/eml/abilities/bite_force.eml |
| `abilities/chromatophore.eml` | bragg_wavelength, transparency, detection_contrast | 0,1 | 3/3 | apex-predator/eml/abilities/chromatophore.eml |
| `abilities/discharge.eml` | voltage, voltage_default, pulse_energy | 0,1 | 3/3 | apex-predator/eml/abilities/discharge.eml |
| `abilities/elastic_energy.eml` | takeoff_velocity, jump_height, jump_range | 0,1 | 3/3 | apex-predator/eml/abilities/elastic_energy.eml |
| `abilities/locomotion.eml` | ground_speed, speed_multiplier, wall_climb_capable | 0 | 3/3 | apex-predator/eml/abilities/locomotion.eml |
| `abilities/muscle_power.eml` | total_power, power_to_weight, top_speed_proxy | 0,1 | 3/3 | apex-predator/eml/abilities/muscle_power.eml |
| `abilities/sprint.eml` | velocity, distance_covered | 1 | 2/2 | apex-predator/eml/abilities/sprint.eml |
| `abilities/texture_match.eml` | match_score, detection_probability, ink_visibility | 0,1 | 3/3 | apex-predator/eml/abilities/texture_match.eml |
| `abilities/toxin.eml` | concentration, damage_rate, total_damage | 1 | 3/3 | apex-predator/eml/abilities/toxin.eml |

### `carriers/` — 12 modules / 40 fns / 24 verified

Wave carriers — photonic, magnonic, phononic, ferronic.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `acoustic_cloak.eml` | shell_index, outer_boundary_index, shell_thickness | 0 | 2/3 | forge/examples/carriers/phononics/acoustic_cloak.eml |
| `ferron_emission.eml` | thz_power, power_at_zero_drive, k_emit_certificate | 0 | 2/3 | forge/examples/carriers/ferronics/ferron_emission.eml |
| `ferron_logic.eml` | output_amplitude, constructive_certificate, p_squared_witness, … (+0) | 1 | 2/3 | forge/examples/carriers/ferronics/ferron_logic.eml |
| `ferron_propagation.eml` | polarization, envelope, polarization_at_origin, … (+1) | 1 | 2/4 | forge/examples/carriers/ferronics/ferron_propagation.eml |
| `mach_zehnder.eml` | intensity_out, intensity_at_zero, cos_sq_at_zero | 1 | 2/3 | forge/examples/carriers/photonics/mach_zehnder.eml |
| `magnon_dispersion.eml` | omega, omega_at_zero_k, fmr_freq | 0 | 2/3 | forge/examples/carriers/spintronics/magnon_dispersion.eml |
| `magnon_logic.eml` | output_amplitude, constructive_certificate, intensity_witness, … (+0) | 1 | 2/3 | forge/examples/carriers/spintronics/magnon_logic.eml |
| `optical_neuron.eml` | activation, dark_output, isat_certificate | 0,1 | 2/3 | forge/examples/carriers/photonics/optical_neuron.eml |
| `phonon_bandgap.eml` | transmission, transmission_at_zero, sin_sq_at_zero | 1 | 2/3 | forge/examples/carriers/phononics/phonon_bandgap.eml |
| `ring_resonator.eml` | transmission, peak_transmission, fsr_separation | 0,1 | 2/3 | forge/examples/carriers/photonics/ring_resonator.eml |
| `spin_torque.eml` | larmor_frequency, damping_prefactor, larmor_certificate, … (+1) | 0 | 2/4 | forge/examples/carriers/spintronics/spin_torque.eml |
| `thermal_rectifier.eml` | forward_conductance, rectification_ratio, asymmetry, … (+2) | 0 | 2/5 | forge/examples/carriers/phononics/thermal_rectifier.eml |

### `quantum/` — 7 modules / 23 fns / 14 verified

Quantum gates — Hadamard, Pauli, phase, CNOT, Grover oracle.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `cnot.eml` | cnot_control_zero_passes, cnot_self_inverse_amp, cnot_zero_certificate, … (+2) | 0 | 3/5 | forge/examples/carriers/quantum/cnot.eml |
| `grover_oracle.eml` | reflect, reflect_at_mean, squared_witness, fixed_point_value | 0 | 2/4 | forge/examples/carriers/quantum/grover_oracle.eml |
| `hadamard.eml` | h_norm_2x_squared_unnormalised, twice_input_norm, h0_norm_unnormalised, … (+2) | 0 | 3/5 | forge/examples/carriers/quantum/hadamard.eml |
| `pauli_x.eml` | pauli_x | 0 | 1/1 | monogate-research/industries/quantum/kernels/pauli_x.eml |
| `pauli_z.eml` | pauli_z | 0 | 1/1 | monogate-research/industries/quantum/kernels/pauli_z.eml |
| `phase_gate.eml` | r_real, r_imag, r_modulus_sq, … (+3) | 1 | 3/6 | forge/examples/carriers/quantum/phase_gate.eml |
| `rotation_rz.eml` | rx | 1 | 1/1 | monogate-research/industries/quantum/kernels/rotation.eml |

### `ml/` — 9 modules / 34 fns / 32 verified

Machine learning — activations, attention, RoPE, layernorm, loss.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `attention.eml` | scale_factor, score_qk, attention_step, … (+2) | 0,1 | 5/5 | **new** |
| `cross_entropy.eml` | bce_loss, bce_with_logits, categorical_ce_pair, … (+1) | 0,1,2 | 3/4 | forge/industries/ml/loss/cross_entropy.eml |
| `gelu.eml` | gelu_tanh, quick_gelu | 1 | 2/2 | forge/industries/ml/activations/gelu.eml |
| `layernorm.eml` | layernorm_step, layernorm_default, rmsnorm_step | 1 | 3/3 | **new** |
| `leaky_relu.eml` | leaky_relu, leaky_relu_default, prelu, leaky_relu_grad | 0 | 4/4 | **new** |
| `relu.eml` | relu, leaky_relu, relu6, prelu | 0 | 3/4 | forge/industries/ml/activations/relu.eml |
| `rotary_embed.eml` | theta, theta_default, rotate_pair_even, … (+2) | 1 | 5/5 | **new** |
| `silu.eml` | silu, swish, silu_grad | 1 | 3/3 | **new** |
| `softmax.eml` | softmax_shift_exp, softmax_normalize, softmax_two_logit, … (+1) | 0,1,2 | 4/4 | forge/industries/ml/activations/softmax.eml |

### `ballistics/` — 9 modules / 40 fns / 40 verified

Exterior ballistics — drag, gravity, wind, Coriolis, spin drift, air density, muzzle velocity, time of flight.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `air_density.eml` | density_isothermal, density_with_temperature, density_humid, … (+1) | 1 | 4/4 | **new** |
| `ballistic_solver.eml` | solve_tof, solve_drop, solve_wind_drift, … (+5) | 0,1 | 8/8 | **new** |
| `coriolis.eml` | horizontal_accel, vertical_accel, horizontal_drift, … (+1) | 1 | 4/4 | **new** |
| `drag.eml` | drag_force, drag_deceleration, drag_decel_from_bc | 0 | 3/3 | **new** |
| `gravity.eml` | drop, drop_at_zero, drop_earth, hold_up_mil | 0 | 4/4 | **new** |
| `muzzle_velocity.eml` | corrected_velocity, corrected_default, percent_change | 0 | 3/3 | **new** |
| `spin_drift.eml` | drift_inches_litz, drift_metres_litz, drift_metres_surrogate, … (+1) | 0,1 | 4/4 | **new** |
| `time_of_flight.eml` | tof_vacuum, tof_constant_decel, tof_pejsa, … (+2) | 0,1 | 5/5 | **new** |
| `wind.eml` | drift, relative_airspeed, perp_component, … (+2) | 0,1 | 5/5 | **new** |

### `gaming/noise/` — 9 modules / 25 fns / 18 verified

Procedural noise — Perlin (2D/3D), Simplex, Voronoi, Worley, value noise, FBM, turbulence.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `noise/fbm.eml` | fbm2, fbm2_default, fbm2_unit | 1 | 3/3 | **new** |
| `noise/perlin_2d.eml` | _grad_dot, perlin2, perlin2_unit | 1 | 2/3 | **new** |
| `noise/perlin_3d.eml` | _grad_dot3, perlin3 | 1 | 1/2 | **new** |
| `noise/simplex_2d.eml` | _grad_dot, simplex2, _contribution | 1 | 1/3 | **new** |
| `noise/turbulence.eml` | turbulence2, turbulence2_default | 1 | 2/2 | **new** |
| `noise/value_noise.eml` | value2, value2_signed | 1 | 2/2 | **new** |
| `noise/voronoi_2d.eml` | distance_to_nearest, _cell_distance, f2_minus_f1 | 1 | 2/3 | **new** |
| `noise/white_noise.eml` | hash2, hash3, hash2_at_origin | 0,1 | 3/3 | **new** |
| `noise/worley.eml` | squared_distance, _cell_sq_dist, manhattan_distance, … (+1) | 0 | 2/4 | **new** |

### `gaming/textures/` — 8 modules / 12 fns / 12 verified

Procedural textures — wood, marble, brick, checkerboard, rust, water surface, caustics, fire.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `textures/brick.eml` | pattern | 0 | 1/1 | **new** |
| `textures/caustics.eml` | intensity | 1 | 1/1 | **new** |
| `textures/checkerboard.eml` | checker, checker_tiled | 0 | 2/2 | **new** |
| `textures/fire.eml` | intensity | 1 | 1/1 | **new** |
| `textures/marble.eml` | marble | 1 | 1/1 | **new** |
| `textures/rust.eml` | mask | 1 | 1/1 | **new** |
| `textures/water_surface.eml` | height, height_default, normal_y | 1 | 3/3 | **new** |
| `textures/wood.eml` | grain, knot_mask | 1 | 2/2 | **new** |

### `gaming/shading/` — 6 modules / 18 fns / 18 verified

Shading models — Lambertian + half-Lambert, Cook-Torrance GGX/Smith, Schlick Fresnel, toon, matcap, Burley SSS.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `shading/fresnel.eml` | schlick, schlick_at_grazing, schlick_at_normal, f0_from_ior | 0 | 4/4 | **new** |
| `shading/matcap.eml` | uv_u, uv_v | 0 | 2/2 | **new** |
| `shading/pbr_diffuse.eml` | lambert, lambert_normalised, half_lambert | 0 | 3/3 | **new** |
| `shading/pbr_specular.eml` | d_ggx, v_smith, specular, roughness_to_alpha | 0,1 | 4/4 | **new** |
| `shading/subsurface.eml` | wrap, back_scatter, sss_total | 0,1 | 3/3 | **new** |
| `shading/toon.eml` | cel_diffuse, rim_light | 0,1 | 2/2 | **new** |

### `gaming/lighting/` — 6 modules / 12 fns / 12 verified

Lighting — point + spot + area, ambient occlusion, exponential and squared-exponential fog.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `lighting/ambient_occlusion.eml` | sample_contribution, ao_factor | 0 | 2/2 | **new** |
| `lighting/area_light.eml` | closest_on_sphere, solid_angle_fraction | 1 | 2/2 | **new** |
| `lighting/fog_exp.eml` | fog_factor, transmittance | 1 | 2/2 | **new** |
| `lighting/fog_exp2.eml` | fog_factor, transmittance | 1 | 2/2 | **new** |
| `lighting/point_light.eml` | attenuation, inverse_square | 0 | 2/2 | **new** |
| `lighting/spot_light.eml` | cone_attenuation, attenuation | 0 | 2/2 | **new** |

### `gaming/terrain/` — 5 modules / 12 fns / 12 verified

Terrain — FBM heightmaps, thermal + hydraulic erosion, biome classification, cliff detection.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `terrain/biome_select.eml` | biome_id | 0 | 1/1 | **new** |
| `terrain/cliff_detect.eml` | gradient_magnitude, is_cliff | 1 | 2/2 | **new** |
| `terrain/erosion_hydraulic.eml` | capacity, eroded_amount, deposited_amount, updated_water | 0 | 4/4 | **new** |
| `terrain/erosion_thermal.eml` | material_transfer, apply_self, apply_neighbour | 0 | 3/3 | **new** |
| `terrain/heightmap.eml` | height, ridged_height | 1 | 2/2 | **new** |

### `gaming/animation/` — 6 modules / 14 fns / 14 verified

Animation — quadratic + cubic ease-in/out, smoothstep + smootherstep, damped springs, bounce, 2-bone IK.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `animation/bounce.eml` | bounce_out, bounce_in | 0 | 2/2 | **new** |
| `animation/ease_in.eml` | ease_in_quad, ease_in_cubic | 0 | 2/2 | **new** |
| `animation/ease_in_out.eml` | smoothstep, smootherstep | 0 | 2/2 | **new** |
| `animation/ease_out.eml` | ease_out_quad, ease_out_cubic | 0 | 2/2 | **new** |
| `animation/ik_2bone.eml` | elbow_angle, shoulder_offset, reachable | 0,1 | 3/3 | **new** |
| `animation/spring.eml` | underdamped, critically_damped, time_constant | 0,1 | 3/3 | **new** |

### `gaming/particles/` — 5 modules / 11 fns / 11 verified

Particles — radial emitter, exponential drag, gravity, lifetime fade, size-over-life.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `particles/drag.eml` | velocity, distance_covered | 1 | 2/2 | **new** |
| `particles/emitter_radial.eml` | velocity_magnitude, disc_offset | 0 | 2/2 | **new** |
| `particles/fade.eml` | alpha, alpha_in_out | 0 | 2/2 | **new** |
| `particles/gravity_particle.eml` | position, velocity, position_earth | 0 | 3/3 | **new** |
| `particles/size_over_life.eml` | radius_linear, radius_power | 0,1 | 2/2 | **new** |

### `gaming/camera/` — 4 modules / 11 fns / 11 verified

Camera — perspective FOV matrix, orbit (spherical), damped-noise shake, depth-of-field circle of confusion.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `camera/dof_blur.eml` | circle_of_confusion, circle_of_confusion_clamped | 0 | 2/2 | **new** |
| `camera/fov_projection.eml` | m00, m11, m22, m23 | 0,2 | 4/4 | **new** |
| `camera/orbit.eml` | position_x, position_y, position_z, norm_witness | 1 | 4/4 | **new** |
| `camera/shake.eml` | shake1d | 1 | 1/1 | **new** |

### `gaming/audio/` — 4 modules / 10 fns / 10 verified

Audio — distance attenuation (linear/inverse/inverse-square), Doppler shift, feedback delay reverb, 1-pole low-pass.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `audio/distance_attenuation.eml` | inverse, inverse_square, linear | 0 | 3/3 | **new** |
| `audio/doppler.eml` | observed_frequency, observed_frequency_air | 0 | 2/2 | **new** |
| `audio/lowpass_audio.eml` | alpha_from_cutoff, step | 0 | 2/2 | **new** |
| `audio/reverb_delay.eml` | feedback_safe, delay_step, t60_seconds | 0,1 | 3/3 | **new** |

### `gaming/physics/` — 7 modules / 21 fns / 21 verified

Physics — semi-implicit Euler rigid-body 2D, AABB + circle collision, restitution-aware impulse resolve, Verlet, spring-damper, Archimedes buoyancy.

| File | Functions | Chain | Verified | Origin |
|------|-----------|-------|----------|--------|
| `physics/aabb_overlap.eml` | overlap_2d, penetration_depth_x | 0 | 2/2 | **new** |
| `physics/buoyancy.eml` | force, force_in_water, sphere_submerged_volume | 0 | 3/3 | **new** |
| `physics/circle_collision.eml` | collides, penetration_depth, inv_distance | 1 | 3/3 | **new** |
| `physics/impulse_resolve.eml` | impulse_magnitude, velocity_a_after, velocity_b_after | 0 | 3/3 | **new** |
| `physics/rigid_body_2d.eml` | integrate_vx, integrate_vy, integrate_omega, … (+3) | 0 | 6/6 | **new** |
| `physics/spring_damper.eml` | force, critical_damping | 0,1 | 2/2 | **new** |
| `physics/verlet.eml` | step, distance_constraint_correction | 0 | 2/2 | **new** |

## Vocabulary

**Chain order** — the Pfaffian chain order, an upper bound on how many
transcendental compositions deep a function reaches. Order 0 = pure
polynomial / rational. Order 1 = single transcendental wrapping a
polynomial argument (e.g. `exp`, `sin`, `ln`). Order 2 = two
transcendentals composed (e.g. `tanh = sinh/cosh`). Forge uses chain
order to bound termination, place transcendentals on FPGA / GPU, and
select the right Lean tactic.

**`@verify(lean, theorem = …)`** — the function carries a Lean proof
obligation. The Forge Lean backend emits the obligation; closing it
against MachLib is what makes the function *verified*.

**Origin: `new`** — written for this stdlib. Otherwise the column
shows the path under `~/monogate/` from which the module was copied
(originals stay where they are; the stdlib is the curated home).

## License

MIT — see `LICENSE`.
