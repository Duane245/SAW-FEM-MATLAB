<div align="center">

# 2D TCSAW Demo

**Self-contained 2D temperature-compensated SAW (TC-SAW) periodic-cell demo**

**English** · [简体中文](README.zh-CN.md)

![MATLAB](https://img.shields.io/badge/MATLAB-R2023a%2B-EE6B27?logo=mathworks&logoColor=white)
![Method](https://img.shields.io/badge/Method-Piezoelectric%20FEM%20%2B%20PML-555555)
![License](https://img.shields.io/badge/License-MIT-blue)

</div>

---

## Overview

A self-contained MATLAB demo of a 2D temperature-compensated SAW (TC-SAW) periodic-cell simulation: LiNbO₃ substrate with SiO₂ / Si₃N₄ compensation layers and Al interdigital electrodes. Spatial discretization uses 9-node quadrilateral (Q9) elements; Bloch periodic boundaries on the left and right; a complex-coordinate-stretched perfectly matched layer (PML) at the bottom absorbs outgoing bulk waves. A frequency-domain sweep yields the Y₁₁ admittance curve.

---

## Run

```bash
cd 2DTCSAW
matlab -batch "SolveSAW"
```

Or, inside an interactive MATLAB session:

```matlab
cd 2DTCSAW
SolveSAW
```

**Expected output**

| File / figure | Content |
|---|---|
| `Y11.mat` | `fre` (201 frequency points), `Q`, `Y` |
| Figure 1 | Mesh |
| Figure 2 | Displacement field |
| Figure 3 | Electric potential |
| Figure 4 | Y₁₁ admittance curve |

The 201-point sweep takes **≈ 4–5 minutes** on a typical workstation (single process, no Parallel Computing Toolbox needed).

---

## Parameters

| Item | Value |
|---|---|
| Piezoelectric substrate | LiNbO₃ |
| Compensation stack | SiO₂ + Si₃N₄ |
| Electrode | Al (interdigital IDT) |
| Pitch | 1.9936 µm |
| Metallization ratio | 0.46 |
| Element | Q9 (9-node quadrilateral) |
| Boundary | Bloch periodic (left/right) · PML (bottom) |
| Sweep range | 1.60 – 2.00 GHz |
| Frequency points | 201 |

---

## Files

```
2DTCSAW/
├── SolveSAW.m                          Main driver
├── initial_material_parameters.m       Material parameters (LiNbO3 / Al / SiO2 / Si3N4)
├── initialPML.m                        PML initialization (complex stretching)
├── readGmsh.m                          Mesh reader
├── findSAWBoundary.m                   Boundary-node identification
├── codes/                              Solver core
│   ├── AssemblyKM2D.m                      K / M assembly entry point
│   ├── boundary_idx_2DS.m                  SP boundary indexing
│   ├── boundaryPeriodic2D.m                Bloch periodic constraints
│   ├── forces.m / solution.m               RHS / linear solve
│   ├── formStiffnessMass2D*.m              Piezoelectric coupling blocks (uu / φφ / uφ)
│   ├── formStiffnessMass2DPML*.m           PML-region assembly (complex stretch)
│   ├── gaussQuadrature.m                   Gauss quadrature
│   ├── shapeFunctionsQ2D.m                 Q9 shape functions
│   ├── Jacobian.m                          Jacobian utilities
│   ├── oulaTransfer.m                      Euler-angle rotation of crystal tensors
│   ├── ComputingC2D.m                      Stiffness tensor construction
│   ├── SortLR_2d.m                         Left/right periodic-boundary node ordering
│   └── plot_*.m  /  plotY11.m              Visualization helpers
└── mesh/
    ├── SAW_PeriodBC1_TC.m                  MATLAB mesh (generated from the .py below)
    └── SAW-PeriodBC1_TC_1.py               Gmsh parametric geometry script
```

---

## Requirements

- MATLAB R2023a or later
- No additional toolbox required (single-process sequential sweep)
- The MATLAB mesh `.m` file ships with the repo; regenerating it from `.py` requires [Gmsh](https://gmsh.info) and Python

---

## Methodology

- **Unknown fields** `[u₁, u₂, φ]` (displacement + potential) coupled by the piezoelectric constitutive law
- **Assembly** of `K` and `M` in `[u | φ]` block form
- **PML** via complex coordinate stretching `α = 1 + d/(iω)`, attenuating outgoing waves along a polynomial profile `d`
- **Sweep** solves `(-ω²M + K) x = f` at every frequency, then evaluates `Y₁₁ = |iωQ/V|` from the induced charge `Q` on the signal electrode

---

## Citation

If this demo is useful in your work, please consider citing the repository:

```bibtex
@software{duan2026_saw,
  author = {Shaoqing Duan},
  title  = {SAW: a piezoelectric FEM solver with TC-SAW 2D demo},
  year   = {2026},
  url    = {https://github.com/Duane245/SAW}
}
```

---

## License

Released under the [MIT License](../LICENSE) · Copyright © 2026 [Shaoqing Duan](https://github.com/Duane245)
