# Project Summary: Perovskite Band Structure Simulator

## Overview

An **interactive web application** that visualizes the relationship between crystal structure distortion and electronic band structure in ABO₃ perovskite oxides. The simulator demonstrates how octahedral tilting (quantified by the B–O–B angle) affects d–p orbital overlap and consequently the width of electronic bands.

---

## Scientific Foundation

### Electronic Structure Theory

The electronic properties of transition-metal oxides are governed by the interaction between:

- **Transition metal d-orbitals** (B-site, e.g., Ti 3d)
- **Oxygen p-orbitals** (O-site, 2p)

This interaction creates **hybridized bands** whose width depends on the **hopping integral** *t*, which quantifies how easily electrons can "hop" between neighboring orbitals.

### Harrison's Scaling Law

The hopping integral follows Harrison's empirical scaling:

```
t ∝ (d₀/d)³·⁵
```

where *d* is the bond length. A longer bond → weaker hopping → narrower bands.

### Angular Dependence

For perovskites, the **B–O–B angle** (θ) introduces a geometric factor:

```
t_eff = t_radial × |cos(180° - θ)|
```

- **θ = 180° (cubic)**: Perfect σ-orbital alignment → maximum overlap → wide bands
- **θ < 180° (distorted)**: Misaligned orbitals → reduced overlap → narrow bands

### Tight-Binding Hamiltonian

The simulator solves a simplified 2×2 Hamiltonian at each k-point:

```
H(k) = | E_d      2t·f(k) |
       | 2t·f(k)    E_p   |

f(k) = cos(kₓ) + cos(kᵧ) + cos(kᵤ)  (simple cubic dispersion)
```

Diagonalization yields two eigenvalues:

- **E₁(k)** — Valence band (primarily O 2p character)
- **E₂(k)** — Conduction band (primarily B d character)

The **band width** is the energy range of E₂(k), and the **band gap** is min(E₂) - max(E₁).

---

## Code Architecture

### Layer 1: Scientific Core (Python + JavaScript)

**Python (`perovskite_simulator.py`)**:

- Reference implementation using NumPy
- Generates `ground_truth.json` for validation
- Serves as the "gold standard" for physics correctness

**JavaScript (`js/physics.js`)**:

- Production physics engine
- Identical algorithms to Python (validated to < 1e-15 error)
- Runs entirely in the browser (client-side)

### Layer 2: Visualization

**Orbital Renderer (`js/orbitals.js`)**:

- HTML5 Canvas with `createRadialGradient()` API
- Simulates electron density probability clouds
- Dynamically rotates p-orbitals based on B–O–B angle
- Overlap regions use alpha-blended gradients (intensity ∝ overlap factor)

**Band Structure Plotter (`js/plotter.js`)**:

- Plotly.js for interactive E(k) plots
- Animated transitions when parameters change
- Dark-mode theme with cyan/magenta color scheme

### Layer 3: Reactive Architecture

**SimulationEngine (`js/app.js`)**:

- **State Management**: Single Source of Truth pattern
- **Observer Pattern**: UI changes trigger `compute()` → `render()` pipeline
- **Slider-to-Canvas Loop**:
  1. User moves slider → state updates
  2. Physics engine recalculates bands
  3. All three panels re-render in <100ms

This architecture is **reusable** — the same pattern will be applied to the future Keto Acids simulator.

---

## Key Results

### Validation

| Metric | Python | JavaScript | Error |
|--------|--------|-----------|-------|
| Overlap (180°) | 1.000000 | 1.000000 | 0.00e+0 |
| Band Width (180°) | 11.350655 eV | 11.350655 eV | 1.78e-15 |
| Overlap (150°) | 0.866025 | 0.866025 | 0.00e+0 |
| Band Width (150°) | 9.605171 eV | 9.605171 eV | 1.78e-15 |

### Physics Demonstration

Dragging the angle slider from 180° → 150° shows:

- **Conduction band narrows** by ~15% (11.35 → 9.61 eV)
- **Overlap factor drops** from 1.0 → 0.866
- **Orbitals visibly misalign** in panels (a) and (b)

This directly demonstrates the **structure-property relationship** central to materials science.

---

## Educational Value

This simulator is designed for:

- **Undergraduate solid-state physics** — visualizing abstract orbital concepts
- **Materials science** — understanding why LaMnO₃ is insulating while SrTiO₃ can be metallic
- **Computational chemistry** — seeing tight-binding theory in action

The **"Aha!" moment** occurs when students realize that *geometry* (the angle) directly controls *electronic properties* (the band width).

---

## Technical Highlights

1. **No Backend Required**: Pure client-side computation using validated JavaScript
2. **Sub-100ms Updates**: Efficient eigenvalue solver for 150 k-points
3. **Production-Grade UX**: Glassmorphism, micro-animations, responsive design
4. **Scientifically Rigorous**: Harrison's scaling + validated against NumPy

---

## File Manifest

| File | Purpose | Lines | Key Technology |
|------|---------|-------|---------------|
| `index.html` | UI structure | 134 | Semantic HTML5 |
| `index.css` | Dark-mode styling | 350+ | CSS gradients, glassmorphism |
| `js/physics.js` | Physics engine | 160 | Vanilla JS, eigenvalue solver |
| `js/orbitals.js` | Canvas renderer | 200+ | HTML5 Canvas, radial gradients |
| `js/plotter.js` | Band plotter | 80 | Plotly.js |
| `js/app.js` | State management | 140 | Observer pattern |
| `perovskite_simulator.py` | Reference | 180 | NumPy, JSON |
| `validate_physics.js` | Unit tests | 90 | Node.js |

---

## Future Directions

See [project_extension.md](project_extension.md) for the **Keto Acids Metabolism Simulator**, which will reuse the `SimulationEngine` architecture to visualize:

- α-keto acids (Krebs cycle, transamination)
- β-keto acids (β-oxidation, ketone bodies)
- pH-dependent protonation states
- Metabolic flux through pathways
