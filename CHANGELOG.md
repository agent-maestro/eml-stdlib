# Changelog

## 0.5.1 — erratum

0.5.0 declared `where chain_order <= 0` on three functions that call `sqrt`, whose chain order is 1:

| function | declared in 0.5.0 | computed |
|---|---|---|
| `control/ekf_range_bearing.eml::range` | 0 | 1 |
| `control/ekf_range_bearing.eml::range_jacobian` | 0 | 1 |
| `control/attitude_quaternion.eml::quat_normalize` | 0 | 1 |

Each declared bound was false by one, from the day the files were written. Forge enforces `where chain_order`
bounds since 2026-09-14, so `eml-compile` refuses both files under 0.5.0's declarations (E001). 0.5.1 declares
the bound Forge's checker computes, and the catalog says 1 for the three functions.

Nothing else changes: the kernels' bodies and every other file are 0.5.0's. A library-wide check is a separate,
later release.
