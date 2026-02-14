# Perovskite Band Structure Simulator

🎨 **Interactive web application** for visualizing orbital overlap and electronic band structure in ABO₃ perovskite oxides.

![Status](https://img.shields.io/badge/status-ready-success)![Physics](https://img.shields.io/badge/physics-validated-blue) ![Client-Side](https://img.shields.io/badge/architecture-client--side-orange)

---

## ✨ Features

### Three Interactive Panels

**(a) Cubic Pm-3̄m Structure** — Visualize effective d–p orbital overlap at perfect 180° B–O–B angle with radial gradient electron density clouds

**(b) Distorted Pnma Structure** — See how octahedral tilting reduces orbital overlap as you adjust the angle slider

**(c) Band Structure E(k)** — Real-time dispersion plot showing O 2p valence and B d conduction bands narrowing as distortion increases

### Real-Time Physics

- **Harrison's d⁻³·⁵ Scaling Law** for bond length dependency
- **2-Band Tight-Binding Hamiltonian** computing eigenvalues for 150 k-points along Γ→X→M→Γ
- **Client-side computation** — no server needed, sub-100ms updates
- **Validated against Python reference** —  JavaScript port matches within 1e-15 tolerance

### Premium UX

- 🌙 **Dark "Lab Mode"** aesthetic with glassmorphism panels
- 💨 **Smooth animations** on all parameter changes
- 📱 **Fully responsive** design
- 🎚️ **Interactive controls**: B–O–B angle slider (140°–180°), metal/cation selectors, orbital/bond toggles

---

## 🚀 Quick Start

### Option 1: Direct Browser (Recommended)

Simply open `index.html` in any modern browser:

```bash
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

No installation, dependencies, or server needed!

### Option 2: Local Development Server

If you prefer a local server:

```bash
# Python 3
python -m http.server 8000

# Node.js
npx serve
```

Then navigate to `http://localhost:8000`

---

## 🧪 Scientific Background

### ABO₃ Perovskite Structure

- **A-site**: Large cation (Ca²⁺, Sr²⁺, Ba²⁺, La³⁺)
- **B-site**: Transition metal (Ti⁴⁺, Mn³⁺) with d-orbitals
- **O-site**: Oxide anions (O²⁻) with p-orbitals

### Orbital Overlap Mechanism

The **B–O–B angle** controls electronic properties:

- **180° (Cubic)**: Maximum σ-bonding overlap → Wide bands → Metallic/small-gap
- **<180° (Distorted)**: Reduced overlap → Narrow bands → Insulating/large-gap

This is visualized through **radial gradient electron density clouds** showing constructive/destructive orbital interference.

### Tight-Binding Model

```
H = | E_d      2t·f(k) |
    | 2t·f(k)    E_p   |

where t ∝ (d₀/d)³·⁵ × cos(180° - θ)
```

- **E_d** = -2.0 eV (Ti 3d level)
- **E_p** = -6.0 eV (O 2p level)
- **t** = Hopping integral with Harrison's scaling
- **f(k)** = cos(kₓ) + cos(kᵧ) + cos(kᵤ) for simple cubic

---

## 📂 Project Structure

```
perovskite-band-structure-simulator/
├── index.html              # Main application
├── index.css               # Dark-mode styling
├── js/
│   ├── physics.js          # Tight-binding engine (production)
│   ├── orbitals.js         # Canvas orbital renderer
│   ├── plotter.js          # Plotly.js band structure plotter
│   └── app.js              # SimulationEngine (state management)
├── perovskite_simulator.py # Python reference implementation
├── ground_truth.json       # Validation data
└── validate_physics.js     # Unit tests (Node.js)
```

---

## 🔬 Validation

The JavaScript physics engine is validated against the Python reference implementation:

```bash
node validate_physics.js
```

**Expected output:**

```
✅ ALL TESTS PASSED - Physics port validated!
   Tolerance: < 1e-5
```

Both scenarios (Cubic 180° and Distorted 150°) pass with errors < 1e-15.

---

## 🎯 Usage Guide

1. **Adjust the B–O–B angle slider** (140° to 180°)
   - Watch the orbital overlap regions glow/dim in panels (a) and (b)
   - See the conduction band width shrink in panel (c)
   - Observe the band gap increase

2. **Change the B-site metal** (Ti ↔ Mn)
   - Shifts the d-orbital energy level
   - Changes band positions

3. **Toggle orbital lobes and bonds**
   - Hide/show electron density clouds
   - Simplify view to focus on geometry

---

## 🧬 The "Aha!" Moment

Drag the slider from **180° → 150°**:

- ✅ Conduction band width narrows (11.35 eV → 9.61 eV)
- ✅ Band gap remains constant (4.00 eV)
- ✅ Overlap factor drops (1.000 → 0.866)

This demonstrates **why** distorted perovskites are often insulating while cubic ones can be metallic!

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Physics** | Vanilla JS (tight-binding solver) |
| **Visualization** | HTML5 Canvas (orbitals) + Plotly.js (bands) |
| **Styling** | Vanilla CSS (glassmorphism, gradients) |
| **Architecture** | Client-side heavy, no backend |
| **Validation** | Python (NumPy) reference |

---

## 📚 Future Extensions

See [project_extension.md](project_extension.md) for the planned **Keto Acids Metabolism Simulator**, reusing the `SimulationEngine` reactive pattern for biochemical pathway visualization.

---

## 📄 License

Educational/research use. Built with scientific rigor and production-grade architecture.

---

**Built with:** Harrison's Solid State Tables, Tight-Binding Theory, and a passion for beautiful physics visualization.
