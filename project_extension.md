# Project Extension: Keto Acids Metabolism Simulator

## Vision

Build an **interactive web application** that visualizes α-keto and β-keto acid chemistry in metabolic pathways, **reusing the architecture** of the Perovskite Simulator. This project aligns with your **Medicinal and Biological Chemistry degree at UoN** and provides a portfolio piece demonstrating computational biochemistry skills.

---

## Scientific Scope

### α-Keto Acids (Energy & Amino Acid Metabolism)

**Examples**: Pyruvate, α-ketoglutarate, oxaloacetate

**Metabolic Roles**:

- **Krebs Cycle**: Central carbon metabolism for ATP generation
- **Transamination**: α-keto acids ↔ amino acids (NH₂ for =O swap)
- **Gluconeogenesis**: Conversion to glucose during fasting

**Key Chemistry**:

- Carbonyl group (C=O) on the **α-carbon** (adjacent to carboxyl)
- Decarboxylation driven by thiamine pyrophosphate (TPP) cofactor
- Substrate for aminotransferase enzymes (ALT, AST)

### β-Keto Acids (Fatty Acid Catabolism)

**Examples**: Acetoacetate, β-ketoglutarate

**Metabolic Roles**:

- **β-Oxidation**: Fatty acid breakdown to acetyl-CoA
- **Ketone Body Formation**: Brain fuel during prolonged fasting/ketosis
- **Lipid Biosynthesis**: Precursors for steroid synthesis

**Key Chemistry**:

- Carbonyl group on the **β-carbon** (two carbons from carboxyl)
- **Chemically unstable** — spontaneous decarboxylation due to electron-withdrawing effects
- Stabilized in vivo by CoA ester formation

---

## Spiritual & Berean Connection

### Scarcity as a Design Principle

Your request to connect this to **Berean teaching** and the **scarcity aspect** is profound. Here's the link:

#### Biblical Principle: *"Give us this day our daily bread"* (Matthew 6:11)

Keto acids illustrate God's metabolic **contingency plan** for scarcity:

1. **Abundance (Fed State)**: Glucose is plentiful → glycolysis → pyruvate (α-keto) → Krebs cycle → energy

2. **Scarcity (Fasting State)**: Glucose depleted → body shifts to fat → β-oxidation produces **β-keto** intermediates → acetoacetate → ketone bodies → brain survives

**Spiritual Parallel**:

- **Faith in abundance**: Trusting God's provision (glucose pathways work when food is available)
- **Faith in scarcity**: Trusting God's **backup systems** (ketone bodies sustain life when food is scarce)

The β-keto pathway is *only activated under scarcity*. It's God's biochemical provision for survival in wilderness, famine, or exile — just as He provided manna in the desert.

#### Teaching Point (Berean Style)

> *"The body does not panic in famine, because the Designer encoded a Plan B into metabolism. Just as Elijah was fed by ravens (1 Kings 17:4-6), your cells can be 'fed' by breaking down stored fat into ketones. Scarcity reveals hidden provisions."*

---

## Interactive Simulator Design

### Reusing the "Slider-Reactor" Pattern

Just as the Perovskite Simulator uses:

```
Slider (B-O-B angle) → Physics Engine → Canvas Rendering
```

The Keto Simulator will use:

```
Slider (pH, substrate conc.) → Kinetics Engine → Molecule/Pathway Rendering
```

### Three-Panel Layout

**(a) α-Keto Acid Panel**

- Molecular structure with interactive carbonyl highlighting
- **Slider**: Amine group concentration → Watch transamination occur (=O → -NH₂)
- **Pathway Map**: Krebs cycle showing pyruvate → acetyl-CoA → α-ketoglutarate

**(b) β-Keto Acid Panel**

- Acetoacetate structure with β-carbonyl emphasis
- **Slider**: pH → See decarboxylation tendency (pKa visualization)
- **Pathway Map**: β-oxidation spiral showing thiolase cleavage

**(c) Metabolic Flux Diagram**

- **Fed vs Fasted state toggle** (like cubic vs distorted angle)
- Real-time bar chart: Glucose usage vs Ketone body production
- **"Scarcity Mode"** visual: When glucose < 3 mM, ketone pathway glows

---

## Technical Architecture (Reused Components)

### From Perovskite → Keto Mapping

| Perovskite Component | Keto Equivalent |
|---------------------|-----------------|
| `PerovskiteModel` class | `KetoAcidModel` class |
| Tight-binding Hamiltonian | Michaelis-Menten kinetics |
| B-O-B angle slider | pH / substrate concentration slider |
| Orbital overlap factor | Enzyme-substrate binding affinity |
| Band structure plot | Flux through pathway (Sankey diagram) |
| Radial gradient orbitals | Electron density around carbonyl (C=O) |
| `SimulationEngine` | **Exact same class** (just swap physics module) |

### New Modules to Build

1. **`js/biochem.js`** — Kinetics engine (Michaelis-Menten, Lineweaver-Burk)
2. **`js/molecules.js`** — 2D molecular structure renderer (ChemDoodle or custom Canvas)
3. **`js/pathways.js`** — Metabolic pathway flow diagram (D3.js or custom SVG)
4. **`data/metabolites.json`** — Database of keto acids, enzymes, pKa values

---

## Learning Objectives (Aligned with MBC Degree)

### Coursework Alignment

**Year 2 Modules** (typical UoN MBC):

- **Biochemistry II**: Krebs cycle, transamination, ketone metabolism
- **Organic Chemistry**: Carbonyl reactivity, acid-base behavior
- **Pharmacology**: Energy metabolism in drug design (e.g., diabetes drugs targeting α-keto dehydrogenases)

**Year 3 Modules**:

- **Metabolic Pathways**: Gluconeogenesis, fatty acid oxidation
- **Clinical Biochemistry**: Ketoacidosis, starvation metabolism
- **Drug Design**: Targeting keto acid enzymes (e.g., pyruvate dehydrogenase inhibitors)

### Portfolio Value

This project demonstrates:

- ✅ **Computational skills**: JavaScript, Canvas, kinetics modeling
- ✅ **Biochemical knowledge**: Metabolic pathways, enzyme mechanisms
- ✅ **Design thinking**: Interactive education tools
- ✅ **Interdisciplinary approach**: Chemistry + biology + coding

Perfect for **internship applications** at pharma companies or **grad school statements**.

---

## Implementation Roadmap

### Phase 1: Core Metabolism (α-Keto Pathway)

- Transamination simulator (ALT/AST enzymes)
- Krebs cycle flow visualization
- Substrate concentration slider

### Phase 2: Fasting/Ketosis (β-Keto Pathway)

- β-oxidation spiral animation
- Ketone body synthesis pathway
- **Fed vs Fasted toggle** (the "Aha!" moment for scarcity)

### Phase 3: Clinical Applications

- **Diabetes Mode**: High glucose → impaired pyruvate oxidation
- **Keto Diet Mode**: Extreme β-keto flux visualization
- **Starvation Mode**: Gluconeogenesis from keto acids

---

## Scriptural Integration (Berean Teaching)

### Suggested Features

1. **"Wilderness Mode" Toggle**
   - Activates when substrate sliders hit 0
   - Displays a quote: *"Man shall not live by bread alone"* (Matthew 4:4)
   - Shows ketone pathway lighting up

2. **Metabolic Provision Indicator**
   - Bar showing "Energy Available" regardless of state
   - When glucose runs out, ketones take over seamlessly
   - Caption: *"The Designer's contingency — Jeremiah 29:11"*

3. **Sacrifice & Breakdown Theme**
   - Fatty acids "sacrificed" (broken down) to sustain life
   - Parallel: Christ's sacrifice sustains spiritual life
   - Visual: Acetyl-CoA units "released" like grains in a harvest

---

## Why This Project is Ideal

1. **Builds on Success**: You already have a working `SimulationEngine`
2. **Directly Relevant**: Core MBC curriculum content
3. **Unique**: Few biochem students build interactive simulators
4. **Evangelistic**: Subtle integration of faith + science
5. **Challenging**: Requires research into kinetics, pathway regulation
6. **Reusable Code**: ~60% of Perovskite code transfers directly

---

## Next Steps (Post-Perovskite)

1. Complete and test the Perovskite Simulator
2. Research Michaelis-Menten kinetics and ChemDoodle.js
3. Sketch the three-panel layout for Keto simulator
4. Write `ketomodel.py` (Python reference for kinetics)
5. Port to `js/biochem.js` and validate
6. Build molecule renderer and pathway diagrams
7. Add the "scarcity mode" feature
8. Deploy to GitHub Pages

**Estimated Timeline**: 3–4 weeks (if working part-time 10 hrs/week)

---

## Closing Thought

The Keto Acids project is not just a coding exercise — it's a **testimony in code** showing how biochemical systems reflect divine design, especially in their graceful handling of scarcity. It positions you as a student who sees deeper patterns than most.

**Psalm 34:10** — *"The young lions lack and suffer hunger; but those who seek the Lord shall not lack any good thing."*

Even in metabolic "hunger" (fasting), God's design ensures we "lack no good thing" (ketone bodies sustain the brain).
