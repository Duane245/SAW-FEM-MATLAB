<div align="center">

[中文](README.md) · **English**

# DuanSAW · sawsim

**Piezoelectric coupled finite-element solver for SAW resonator unit cells**
Q9 / Hex27 · PML · Bloch periodicity · verified against a reference FEM solution

[![CI](https://github.com/Duane245/DuanSAW/actions/workflows/ci.yml/badge.svg)](https://github.com/Duane245/DuanSAW/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20362278.svg)](https://doi.org/10.5281/zenodo.20362278)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-AGPL--3.0-blue)

**DuanSAW** is the project and citation name; **sawsim** is the Python package, the command and the hosted service at [sawsim.com](https://sawsim.com).

</div>

---

## Install and use

```bash
pip install git+https://github.com/Duane245/DuanSAW
pip install "sawsim[fast]"     # optional: MKL PARDISO direct solver
```

```python
from sawsim import Model, sweep

r = sweep(Model("sp_double_layer", pitch_um=1.085, points=101), "out/dbl")
r.frequency_ghz, r.admittance, r.peak_frequency_ghz
```

```bash
sawsim templates
sawsim run config.json -o out/dbl
```

Headless Linux needs `libglu1-mesa libopengl0` for Gmsh. See [Getting started](docs/getting-started.en.md).

## Capabilities

| | |
|---|---|
| **Models** | 9 unit-cell templates: five 2D (Q9, incl. TC-SAW) and four 2.5D periodic slices (Hex27), one to four layers |
| **Physics** | Fully coupled displacement–potential; ME0 plane strain or ME1 out-of-plane extension; anisotropic crystals rotated by intrinsic ZXZ Euler angles |
| **Boundaries** | Bloch periodicity left/right, complex-coordinate-stretched PML at the bottom |
| **Meshing** | Parametric geometry via the Gmsh Python API, quadratic isoparametric elements |
| **Solve** | Real block form of the complex sparse system, MKL PARDISO or SciPy SuperLU, frequency-parallel sweeps |
| **Output** | Y11 admittance (CSV / NPZ / JSON), mesh, displacement and potential field plots, material snapshots and source hashes; every run is fully reproducible |
| **Materials** | Built-in LiNbO₃ (literature), Si, SiO₂, poly-Si, Si₃N₄, Al, Cu; custom JSON import |

## Validation

Each template is compared point by point with an independent reference FEM solution; resonance and anti-resonance frequencies agree for all templates, errors around the main resonance are 0.1 – 2 %, and 2D multilayers deviate above 2.4 GHz in the higher-order mode region. Full error table, figures and discussion in [Validation](docs/validation.en.md). `pytest` reproduces the comparison at 5 – 6 frequencies per template.

<div align="center">
<img src="docs/figures/compare_2p5d_double.png" width="640"><br>
<sub>2.5D SP double layer (LiNbO₃ 0.6 µm / Si 6.51 µm), 251 points. Dashed: sawsim, solid: reference; relative L2 error of |Y| 0.15 %.</sub>
</div>

## Documentation

- [Getting started](docs/getting-started.en.md) — install, first run, output files, units
- [Models](docs/models.en.md) — the nine templates, parameters, displacement models, boundaries, known limitations
- [Materials and orientation](docs/materials-and-orientation.en.md) — built-in materials, record format, custom import, ZXZ Euler angles
- [Validation](docs/validation.en.md) — point-by-point comparison with the reference and how to read it

## Repository layout

```
src/sawsim/        Python package (api, cli, config, models, solver, saw2d, sp_meshes, sp_hex_meshes, material_library)
tests/             regression and API tests; tests/data holds the reference curves
docs/              documentation and figures
matlab/            the v0.x MATLAB + Gmsh implementation (historical, MIT)
tools/             maintenance scripts
```

## License

The Python package `sawsim` is released under **AGPL-3.0-or-later** (it links the GPL-licensed Gmsh library through its Python API). The historical MATLAB implementation under `matlab/` stays MIT. Contact the author for other licensing arrangements.

## Citation

Cite the concept DOI [10.5281/zenodo.20362278](https://doi.org/10.5281/zenodo.20362278), which always resolves to the latest version; see [CITATION.cff](CITATION.cff) for the format.
