"""Smoke tests for the eml-stdlib introspection surface."""

from __future__ import annotations

import json

import eml_stdlib


def test_version_exposed() -> None:
    assert eml_stdlib.__version__ == "0.4.0"


def test_categories_match_directory_layout() -> None:
    cats = eml_stdlib.categories()
    expected = {
        "math", "signal", "control", "physics", "circuits",
        "sensors", "biology", "carriers", "quantum", "ml",
        "ballistics", "gaming",
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
    assert len(cat) >= 168
    for entry in cat:
        assert {"category", "file", "module", "functions", "description", "source"} <= set(entry)
        assert isinstance(entry["functions"], list)


def test_catalog_minimum_verified_count() -> None:
    cat = eml_stdlib.load_catalog()
    verified = sum(1 for m in cat for f in m["functions"] if f["verified"])
    # Regression guard: never drop below v0.4 coverage (466).
    assert verified >= 460, f"verified count regressed: {verified}"


def test_ballistics_category_present() -> None:
    files = eml_stdlib.list_modules("ballistics")
    file_names = {f.name for f in files}
    expected = {
        "drag.eml", "gravity.eml", "wind.eml", "coriolis.eml",
        "spin_drift.eml", "air_density.eml", "muzzle_velocity.eml",
        "time_of_flight.eml", "ballistic_solver.eml",
    }
    assert expected <= file_names, f"missing: {expected - file_names}"


def test_gaming_subcategories_complete() -> None:
    """Every gaming/<subcat>/ has its full module roster."""
    expected = {
        "gaming/noise":     {"perlin_2d.eml", "perlin_3d.eml", "simplex_2d.eml",
                             "voronoi_2d.eml", "fbm.eml", "turbulence.eml",
                             "white_noise.eml", "value_noise.eml", "worley.eml"},
        "gaming/textures":  {"wood.eml", "marble.eml", "brick.eml",
                             "checkerboard.eml", "rust.eml", "water_surface.eml",
                             "caustics.eml", "fire.eml"},
        "gaming/shading":   {"pbr_diffuse.eml", "pbr_specular.eml", "fresnel.eml",
                             "toon.eml", "matcap.eml", "subsurface.eml"},
        "gaming/lighting":  {"point_light.eml", "spot_light.eml", "area_light.eml",
                             "ambient_occlusion.eml", "fog_exp.eml", "fog_exp2.eml"},
        "gaming/terrain":   {"heightmap.eml", "erosion_thermal.eml",
                             "erosion_hydraulic.eml", "biome_select.eml",
                             "cliff_detect.eml"},
        "gaming/animation": {"ease_in.eml", "ease_out.eml", "ease_in_out.eml",
                             "spring.eml", "bounce.eml", "ik_2bone.eml"},
        "gaming/particles": {"emitter_radial.eml", "drag.eml",
                             "gravity_particle.eml", "fade.eml",
                             "size_over_life.eml"},
        "gaming/camera":    {"fov_projection.eml", "orbit.eml", "shake.eml",
                             "dof_blur.eml"},
        "gaming/audio":     {"distance_attenuation.eml", "doppler.eml",
                             "reverb_delay.eml", "lowpass_audio.eml"},
        "gaming/physics":   {"rigid_body_2d.eml", "aabb_overlap.eml",
                             "circle_collision.eml", "impulse_resolve.eml",
                             "verlet.eml", "spring_damper.eml", "buoyancy.eml"},
    }
    for subcat, modules in expected.items():
        files = eml_stdlib.list_modules(subcat)
        names = {f.name for f in files}
        missing = modules - names
        assert not missing, f"{subcat} missing: {missing}"


def test_gaming_total_60_modules() -> None:
    """The gaming roof totals 60 modules across 10 subcategories."""
    files = eml_stdlib.list_modules("gaming")
    assert len(files) == 60, f"got {len(files)}"
