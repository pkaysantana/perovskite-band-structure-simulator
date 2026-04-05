"""
Crystal Field Extension for ABO₃ Tight-Binding Model
=====================================================

Builds on tight_binding.py (4-band d–pσ + constant O–O hopping).
Adds a minimal crystal field splitting: the single d level is split into
one effective e_g level and one effective t₂g level.

PURPOSE
-------
This file is a revision bridge between CHEM1010 coordination chemistry
(crystal field theory, d-d transitions, spin states) and solid-state
physics (band structures, charge-transfer gaps, dispersion).

It is explicitly a toy model.  It is correct at the qualitative level
for understanding orbital character and energy ordering.  It is NOT
suitable for quantitative prediction of optical spectra, magnetic
behaviour, or real perovskite band gaps.

HOW TO USE ALONGSIDE tight_binding.py
--------------------------------------
    from tight_binding import make_kpath, hopping_integral, pp_hopping
    from tight_binding import E_D, E_P, T_PP0

HOW THIS FILE IS STRUCTURED
-----------------------------
  Part A — Chemistry background (read the docstrings)
  Part B — Parameters: Δ_CF, typical values, what they mean
  Part C — 5×5 Hamiltonian (e_g + t₂g + 3 O p_σ)
  Part D — Solver and gap functions (analytical where possible)
  Part E — Plots: band structure, Δ_CF sweep, comparison grid
  Part F — Self-checks and main()

WHAT THIS MODEL CAN AND CANNOT DO
----------------------------------
  CAN:
    ✓ Show the energy splitting Δ_CF between t₂g and e_g bands
    ✓ Show that t₂g is non-dispersive (flat band = non-bonding)
    ✓ Show that e_g is dispersive (broadened by σ-overlap with O p_σ)
    ✓ Show the O 2p → t₂g charge-transfer gap vs Δ_CF
    ✓ Show the O 2p → e_g charge-transfer gap vs Δ_CF
    ✓ Show how a stronger crystal field (larger Δ_CF) raises e_g
      and lowers t₂g (barycentre preserved)

  CANNOT:
    ✗ Predict d-d absorption colour (model has no electron occupancy
      or electron-electron repulsion; Δ_CF is not the optical gap)
    ✗ Determine spin state (needs pairing energy P, not included)
    ✗ Quantitatively describe real oxides (single-orbital approximation
      per level, uniform coupling, no spin-orbit coupling)
    ✗ Produce gap variation with octahedral tilt (inherited limitation
      from tight_binding.py — requires zone-folding)

──────────────────────────────────────────────────────────────────────
CRYSTAL FIELD THEORY PRIMER  (first-year level)
──────────────────────────────────────────────────────────────────────

In an octahedral complex ML₆, the six ligands approach along ±x, ±y, ±z.
The five d orbitals split into two groups:

  e_g  (d_z², d_x²-y²):   lobes point ALONG the metal–ligand axes
                            → direct overlap with ligand → pushed UP
                            → raised by +0.6 Δ_oct above the barycentre

  t₂g  (d_xy, d_xz, d_yz): lobes point BETWEEN the ligand axes
                            → no direct σ-overlap → pushed DOWN
                            → lowered by −0.4 Δ_oct below the barycentre

Barycentre rule:  2 × (+0.6) + 3 × (−0.4) = 0  (energy conserved)

THE d–d TRANSITION AND COLOUR
    In a complex with d electrons (e.g. [Ti(H₂O)₆]³⁺, d¹), a photon
    can promote one electron from t₂g → e_g.  The absorbed energy is:
        E_absorbed = Δ_oct  (the splitting itself, not the charge-transfer gap)
    The observed colour is the COMPLEMENT of the absorbed colour.
    Example: [Ti(H₂O)₆]³⁺ absorbs ~500 nm (green) → appears purple.

    This is INTRA-METAL physics.  In this band model, Δ_CF = E_eg − E_t2g
    is directly readable, but to connect it to colour you must know the
    d-electron count and the d-d selection rules — neither is in this model.

CHARGE-TRANSFER GAP (what the band model primarily shows)
    The gap labelled "Gap(t₂g)" in this code is:
        E_t2g − VBM = (d orbital energy) − (O 2p band top)
    This is a METAL–OXYGEN charge-transfer energy, not a d–d transition.
    In d⁰ perovskites (Ti⁴⁺ in SrTiO₃) there are no d electrons, so
    there is no d–d absorption — the optical gap is purely this CT energy.
    These are two different quantities that both use the word "gap."

HIGH SPIN vs LOW SPIN (conceptual connection only)
    If many d electrons are present, whether they fill t₂g first (low spin)
    or spread across all d orbitals (high spin) depends on comparing:
        Δ_oct  vs  P  (electron pairing energy)
    Large Δ_oct (strong-field ligand: CN⁻, CO) → low spin
    Small Δ_oct (weak-field ligand: F⁻, Cl⁻)  → high spin
    This model shows Δ_oct but has NO electron occupancy and NO pairing
    energy.  Spin state cannot be read from this band structure.
"""

import numpy as np
import matplotlib.pyplot as plt

# Import base-model functions and constants
from tight_binding import (make_kpath, hopping_integral, pp_hopping,
                            E_D, E_P, T_PP0)


# ─── A. CRYSTAL FIELD PARAMETERS ─────────────────────────────────────────────

# Δ_CF (eV): crystal field splitting between t₂g and e_g.
# Typical values for first-row transition metals in octahedral O²⁻ environments:
#   Ti³⁺  (d¹, weak-field oxide):  ~1.8–2.0 eV  (~15,000–17,000 cm⁻¹)
#   V³⁺   (d²):                    ~1.8 eV
#   Cr³⁺  (d³):                    ~2.1 eV  (~17,000 cm⁻¹)
#   Mn²⁺  (d⁵, weak field):        ~0.9 eV  (~7,500 cm⁻¹)
#   Co²⁺  (d⁷):                    ~1.2 eV  (~10,000 cm⁻¹)
#   [Ti(H₂O)₆]³⁺:                  ~2.4 eV  (~20,300 cm⁻¹)
# Conversion: 1 eV = 8065 cm⁻¹
DELTA_CF = 1.5   # eV — default, representative 3d oxide value


def cf_energies(delta_cf=DELTA_CF, e_d=E_D):
    """
    Compute e_g and t₂g on-site energies from the d barycentre E_d.

    Returns (E_eg, E_t2g) in eV.

        E_eg  = E_d + 0.6 · Δ_CF   [antibonding e_g, σ-overlap with O p_σ]
        E_t2g = E_d − 0.4 · Δ_CF   [non-bonding t₂g, no σ-overlap]

    The 0.6 / 0.4 weights are exact in the electrostatic model:
    they are required to preserve the barycentre:
        2(+0.6Δ) + 3(−0.4Δ) = 0

    IMPORTANT — why 0.6 for e_g and 0.4 for t₂g, not the other way?
    The barycentre rule: 2 × (Δ_eg) + 3 × (Δ_t2g) = 0
    With Δ_eg = +0.6Δ, Δ_t2g = −0.4Δ:
        2(0.6Δ) + 3(−0.4Δ) = 1.2Δ − 1.2Δ = 0  ✓
    The fraction for each level is the COMPLEMENT of its multiplicity:
    there are 2 e_g levels and 3 t₂g levels, so e_g gets the larger per-level
    shift (0.6 > 0.5) to compensate for having fewer levels.

    Heuristic note: E_d is treated as the unperturbed barycentre.  In a
    covalent picture the barycentre shifts slightly upward (the antibonding
    average is not exactly E_d) — this correction is neglected here.
    """
    return e_d + 0.6 * delta_cf, e_d - 0.4 * delta_cf


# ─── B. 5×5 BLOCH HAMILTONIAN ────────────────────────────────────────────────

def bloch_hamiltonian_cf(k, t, t_pp=0.0, delta_cf=DELTA_CF, e_d=E_D, e_p=E_P):
    """
    5×5 Bloch Hamiltonian including crystal field splitting.

    Basis: [e_g, t₂g, px@Ox, py@Oy, pz@Oz]

        ┌                                         ┐
        │ E_eg   0      Tx     Ty     Tz          │  e_g: σ-bonds with O p_σ
        │ 0      E_t2g  0      0      0           │  t₂g: zero σ-overlap (exact)
        │ Tx     0      E_p    Pxy    Pxz         │
        │ Ty     0      Pxy    E_p    Pyz         │
        │ Tz     0      Pxz    Pyz    E_p         │
        └                                         ┘

    WHY t₂g HAS ZERO COUPLING TO O p_σ  [this is exact, not an approximation]
        In O_h symmetry, the p_σ orbital on each O (pointing along the B–O
        bond axis) belongs to the a₁g, eg, and t₁u representations of the
        octahedron.  The t₂g orbitals belong to t₂g.  These representations
        do not overlap: ⟨t₂g | p_σ⟩ = 0 by symmetry.
        Consequence in the band model: the t₂g row and column are entirely
        zero off-diagonal → t₂g never hybridises → flat band at E_t2g.
        This is "non-bonding" made mathematically explicit.

    WHY e_g HAS THE SAME COUPLING AS THE ORIGINAL SINGLE-d MODEL
        Both e_g orbitals (d_z², d_x²-y²) have large σ-overlap with the O p_σ
        orbital along their respective bond axes.  A single effective e_g level
        with uniform coupling t to all three oxygens is adequate for qualitative
        purposes (the real angular factors differ for d_z² vs d_x²-y², but the
        scale is the same).

    Parameters
    ----------
    k        : (3,) array — wavevector in units of 1/a
    t        : float      — e_g–O σ-hopping (eV); same as original t_eff
    t_pp     : float      — O–O hopping (eV), constant
    delta_cf : float      — crystal field splitting Δ_oct (eV)
    """
    e_eg, e_t2g = cf_energies(delta_cf, e_d)
    kx, ky, kz  = k

    Tx  = 2.0 * t    * np.cos(kx / 2.0)
    Ty  = 2.0 * t    * np.cos(ky / 2.0)
    Tz  = 2.0 * t    * np.cos(kz / 2.0)
    Pxy = 4.0 * t_pp * np.cos(kx / 2.0) * np.cos(ky / 2.0)
    Pxz = 4.0 * t_pp * np.cos(kx / 2.0) * np.cos(kz / 2.0)
    Pyz = 4.0 * t_pp * np.cos(ky / 2.0) * np.cos(kz / 2.0)

    return np.array([
        [e_eg,  0.0,   Tx,   Ty,   Tz ],
        [0.0,   e_t2g, 0.0,  0.0,  0.0],   # t₂g: all off-diagonal = 0
        [Tx,    0.0,   e_p,  Pxy,  Pxz],
        [Ty,    0.0,   Pxy,  e_p,  Pyz],
        [Tz,    0.0,   Pxz,  Pyz,  e_p],
    ], dtype=float)


# ─── C. SOLVER ────────────────────────────────────────────────────────────────

def compute_bands_cf(kpoints, bond_angle_deg, bond_length_ang=1.96,
                     t_pp0=T_PP0, delta_cf=DELTA_CF, e_d=E_D, e_p=E_P):
    """
    Diagonalise the 5×5 CF Hamiltonian at each k-point.

    Returns (N_k, 5) eigenvalue array, sorted ascending.

    CAUTION ON BAND INDICES
        eigvalsh sorts by eigenvalue at each k independently.
        With default parameters (E_D=−2, E_P=−6, T_PP0=−0.4, Δ_CF=1.5 eV):
            E_t2g = −2.6 eV  >  VBM = −4.4 eV  >  E_p = −6 eV
        So the ordering is stable:
            cols 0–2: O 2p–derived bands
            col  3:   t₂g flat band
            col  4:   e_g conduction band
        This ordering can SWAP if Δ_CF is very large (E_t2g approaches VBM).
        Use the analytical functions below rather than hard-coded indices
        wherever robustness matters.
    """
    t    = hopping_integral(bond_angle_deg, bond_length_ang)
    t_pp = pp_hopping(t_pp0)

    return np.array([
        np.linalg.eigvalsh(
            bloch_hamiltonian_cf(k, t, t_pp, delta_cf, e_d, e_p))
        for k in kpoints
    ])


# ─── D. ANALYTICAL GAP FUNCTIONS ─────────────────────────────────────────────
# These use exact results from the model (no band-index assumptions).
# See tight_binding.py module docstring sections (2)–(4) for derivations.

def analytical_vbm(t_pp0=T_PP0, e_p=E_P):
    """
    VBM = E_p − 4·t_pp   [exact within the model]

    The antibonding O–O combination sits at this energy everywhere along
    Γ→X (flat by symmetry) and at Γ on the R→Γ path.  It is the VBM.
    Independent of Δ_CF, t_eff, and bond angle.
    """
    return e_p - 4.0 * pp_hopping(t_pp0)


def analytical_gaps(delta_cf=DELTA_CF, t_pp0=T_PP0, e_d=E_D, e_p=E_P):
    """
    Charge-transfer gaps computed analytically.

    Returns (gap_t2g, gap_eg, delta_cf_itself) all in eV.

    gap_t2g = E_t2g − VBM   (O 2p → t₂g transition)
    gap_eg  = E_eg  − VBM   (O 2p → e_g transition)
    delta_cf_itself = E_eg − E_t2g  (the d–d splitting, Δ_oct in LFT)

    IMPORTANT DISTINCTION — which gap is which:
        gap_t2g and gap_eg are CHARGE-TRANSFER gaps.
        They describe moving electron density from O to the metal.
        This is NOT the same as the d–d transition observed in UV/vis
        spectroscopy of coordination complexes.

        The d–d transition energy = delta_cf_itself = Δ_oct.
        This is the quantity relevant to colour in [M(H₂O)₆]^n+ complexes.
        It equals E_eg − E_t2g in this model.

    Note: gap_eg − gap_t2g = delta_cf_itself  (always, by algebra).
    """
    e_eg, e_t2g = cf_energies(delta_cf, e_d)
    vbm = analytical_vbm(t_pp0, e_p)
    return e_t2g - vbm, e_eg - vbm, e_eg - e_t2g


# ─── E. PLOTTING ─────────────────────────────────────────────────────────────

_CF_COLOURS = ['#1565C0', '#42A5F5', '#90CAF9', '#43A047', '#E53935']
_CF_LABELS  = [
    'O 2p bonding',
    'O 2p mixed',
    'O 2p antibonding  (VBM)',
    't₂g  — flat, non-bonding  (no σ-overlap with O)',
    'e_g  — dispersive, antibonding  (σ-bond with O)',
]


def plot_cf_bands(delta_cf=DELTA_CF, theta=180.0, n_k=80,
                  t_pp0=T_PP0, save=True):
    """
    Band structure with crystal field splitting labelled.

    Reading this plot:
      GREEN flat line  = t₂g band.  Perfectly flat because zero hopping.
                         This is "non-bonding" visualised directly in k-space.
                         In LFT this is the lower d level in the energy diagram.
      RED dispersive   = e_g conduction band.  Disperses because e_g has
                         strong σ-overlap with O p_σ → finite t_eff → finite bandwidth.
                         In LFT this is the upper, antibonding d level.
      PALE BLUE        = O 2p antibonding VBM.  Flat along Γ→X (see tight_binding.py).
                         This is the highest filled oxygen band.

      ARROWS show two distinct gaps:
        Δ_CF  (red)    = E_eg − E_t2g  — this IS the crystal field splitting Δ_oct
                         from CHEM1010.  It is the d–d excitation energy.
        CT gap (green) = E_t2g − VBM  — charge-transfer gap (O→metal).
                         Different physics, different experiment.
    """
    kpoints, ticks, tick_labels = make_kpath(n_k)
    x = np.arange(len(kpoints))

    bands    = compute_bands_cf(kpoints, theta, t_pp0=t_pp0, delta_cf=delta_cf)
    vbm      = analytical_vbm(t_pp0)
    g_ct, g_eg_ct, delta = analytical_gaps(delta_cf, t_pp0)
    e_eg, e_t2g          = cf_energies(delta_cf)

    fig, ax = plt.subplots(figsize=(9, 6))

    for b in range(5):
        ax.plot(x, bands[:, b], color=_CF_COLOURS[b], lw=2.0,
                label=_CF_LABELS[b])

    # Arrow: CT gap (VBM → t₂g)
    mid = len(x) // 5
    ax.annotate('', xy=(mid, e_t2g), xytext=(mid, vbm),
                arrowprops=dict(arrowstyle='<->', color='#2E7D32', lw=1.5))
    ax.text(mid + 3, (e_t2g + vbm) / 2,
            f'CT gap\n= {g_ct:.2f} eV\n(O→t₂g)',
            fontsize=8, color='#2E7D32', va='center')

    # Arrow: Δ_CF (t₂g → e_g, at R where e_g = E_eg exactly)
    r_idx = 3 * (len(x) // 4)   # approximate R-point position
    ax.annotate('', xy=(r_idx, e_eg), xytext=(r_idx, e_t2g),
                arrowprops=dict(arrowstyle='<->', color='#C62828', lw=1.5))
    ax.text(r_idx + 3, (e_eg + e_t2g) / 2,
            f'Δ_CF = {delta:.2f} eV\n(d–d splitting)',
            fontsize=8, color='#C62828', va='center')

    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels, fontsize=12)
    for xi in ticks[1:-1]:
        ax.axvline(xi, color='lightgray', lw=0.8)
    ax.axhline(vbm, color='#90CAF9', lw=0.8, ls=':')

    ax.set_ylabel('Energy (eV)', fontsize=11)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(-13, 7)
    ax.legend(fontsize=7.5, loc='lower right')
    ax.set_title(
        f'Crystal Field Band Structure  |  Δ_CF = {delta_cf:.2f} eV  |  θ = {theta:.0f}°',
        fontsize=11)

    ax.text(0.01, 0.99,
            f'E_eg      = {e_eg:.2f} eV\n'
            f'E_t2g     = {e_t2g:.2f} eV\n'
            f'Δ_CF      = {delta:.2f} eV  (d–d gap)\n'
            f'VBM       = {vbm:.2f} eV\n'
            f'CT gap    = {g_ct:.2f} eV  (O→t₂g)\n'
            f'CT gap_eg = {g_eg_ct:.2f} eV  (O→e_g)',
            transform=ax.transAxes, va='top', ha='left',
            fontsize=8, family='monospace',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.85))

    plt.tight_layout()
    if save:
        plt.savefig('cf_band_structure.png', dpi=150, bbox_inches='tight')
        print('Saved cf_band_structure.png')
    plt.show()


def plot_cf_sweep(delta_cf_range=None, t_pp0=T_PP0, save=True):
    """
    How band levels and gaps change as Δ_CF varies from 0 to 3 eV.

    Panel (a): Level energies — shows the 0.6/0.4 split directly
    Panel (b): Charge-transfer gaps — CT gap to t₂g decreases with Δ_CF;
               CT gap to e_g increases; their difference = Δ_CF always
    Panel (c): Δ_CF itself (the d–d splitting from LFT) vs input value
               — trivially a straight line, included as a reality check
               and to make the quantity explicit

    The visible light window (1.8–3.1 eV) is shaded on panel (b) to show
    which Δ_CF values would put the CT gap in the visible range.
    NOTE: this does NOT directly predict colour from d–d transitions.
    Colour from d–d transitions depends on Δ_CF itself (panel c), electron
    count, and selection rules — none of which are in this model.
    """
    if delta_cf_range is None:
        delta_cf_range = np.linspace(0.0, 3.0, 61)

    vbm = analytical_vbm(t_pp0)
    results = np.array([analytical_gaps(d, t_pp0) for d in delta_cf_range])
    g_ct, g_eg_ct, delta_out = results[:, 0], results[:, 1], results[:, 2]
    e_eg_vals  = np.array([cf_energies(d)[0] for d in delta_cf_range])
    e_t2g_vals = np.array([cf_energies(d)[1] for d in delta_cf_range])

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 9), sharex=True)

    # Panel 1: level positions
    ax1.plot(delta_cf_range, e_eg_vals,  '-', color='#E53935', lw=2,
             label='E_eg = E_d + 0.6·Δ')
    ax1.plot(delta_cf_range, e_t2g_vals, '-', color='#43A047', lw=2,
             label='E_t2g = E_d − 0.4·Δ')
    ax1.axhline(E_D, color='gray', lw=0.8, ls='--',
                label=f'E_d (barycentre) = {E_D:.1f} eV')
    ax1.axhline(vbm, color='#90CAF9', lw=0.8, ls=':',
                label=f'VBM = {vbm:.2f} eV (constant)')
    ax1.set_ylabel('Level energy (eV)', fontsize=11)
    ax1.set_title('Crystal field splitting: energy levels and gaps', fontsize=11)
    ax1.legend(fontsize=8, loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.text(0.5, 0.08,
             'Barycentre preserved: 2×(+0.6Δ) + 3×(−0.4Δ) = 0',
             transform=ax1.transAxes, ha='center', fontsize=8,
             style='italic', color='gray')

    # Panel 2: charge-transfer gaps
    ax2.plot(delta_cf_range, g_ct,    '-', color='#43A047', lw=2,
             label='CT gap (O→t₂g) = E_t2g − VBM')
    ax2.plot(delta_cf_range, g_eg_ct, '-', color='#E53935', lw=2,
             label='CT gap (O→e_g)  = E_eg − VBM')
    ax2.axhspan(1.8, 3.1, alpha=0.08, color='gold',
                label='Visible light: 1.8–3.1 eV')
    ax2.axhline(0, color='black', lw=0.5)
    ax2.set_ylabel('Charge-transfer gap (eV)', fontsize=11)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    ax2.text(0.5, 0.55,
             'These are O→metal (charge-transfer) energies.\n'
             'They are NOT the d–d transition energies from LFT.',
             transform=ax2.transAxes, ha='center', fontsize=8,
             style='italic', color='#4A148C',
             bbox=dict(boxstyle='round', facecolor='#F3E5F5', alpha=0.7))

    # Panel 3: the d–d gap = Δ_CF itself
    ax3.plot(delta_cf_range, delta_out, 'D-', color='#7B1FA2', lw=2, ms=3,
             label='Δ_CF = E_eg − E_t2g  (d–d splitting)')
    ax3.axhspan(1.8, 3.1, alpha=0.08, color='gold',
                label='Visible light: 1.8–3.1 eV')
    ax3.set_ylabel('Δ_CF  (eV)', fontsize=11)
    ax3.set_xlabel('Input Δ_CF  (eV)', fontsize=11)
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    ax3.text(0.5, 0.25,
             'This IS the LFT d–d splitting Δ_oct.\n'
             'When Δ_CF falls in the visible window, a d–d\n'
             'transition can produce colour (given d electrons\n'
             'and allowed selection rules — not in this model).',
             transform=ax3.transAxes, ha='center', fontsize=8,
             style='italic', color='#4A148C',
             bbox=dict(boxstyle='round', facecolor='#F3E5F5', alpha=0.7))

    plt.tight_layout()
    if save:
        plt.savefig('cf_sweep.png', dpi=150, bbox_inches='tight')
        print('Saved cf_sweep.png')
    plt.show()


def plot_cf_comparison(delta_cf_values=(0.5, 1.5, 2.5),
                        theta=180.0, n_k=80, t_pp0=T_PP0, save=True):
    """
    Side-by-side band structures for three Δ_CF values.

    What to look for:
      • t₂g (green) moves DOWN as Δ_CF increases — the barycentre rule
      • e_g (red)  moves UP  as Δ_CF increases
      • O 2p bands (blue) are completely UNCHANGED — they don't depend on Δ_CF
      • The CT gap to t₂g SHRINKS (t₂g approaches VBM)
      • Δ_CF itself (labelled) GROWS between the two d levels
    """
    kpoints, ticks, tick_labels = make_kpath(n_k)
    x = np.arange(len(kpoints))
    n = len(delta_cf_values)

    fig, axes = plt.subplots(1, n, figsize=(6 * n, 6), sharey=True)

    for ax, delta_cf in zip(axes, delta_cf_values):
        bands    = compute_bands_cf(kpoints, theta, t_pp0=t_pp0,
                                    delta_cf=delta_cf)
        vbm      = analytical_vbm(t_pp0)
        g_ct, _, delta = analytical_gaps(delta_cf, t_pp0)
        e_eg, e_t2g    = cf_energies(delta_cf)

        for b in range(5):
            ax.plot(x, bands[:, b], color=_CF_COLOURS[b], lw=1.8,
                    label=_CF_LABELS[b] if ax is axes[0] else None)

        ax.axhline(vbm, color='#90CAF9', lw=0.8, ls=':')
        ax.set_xticks(ticks)
        ax.set_xticklabels(tick_labels, fontsize=11)
        for xi in ticks[1:-1]:
            ax.axvline(xi, color='lightgray', lw=0.8)
        ax.set_title(f'Δ_CF = {delta_cf:.1f} eV', fontsize=12)
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(-13, 7)
        ax.text(0.97, 0.97,
                f'E_eg   = {e_eg:.2f} eV\n'
                f'E_t2g  = {e_t2g:.2f} eV\n'
                f'Δ_CF   = {delta:.2f} eV\n'
                f'CT gap = {g_ct:.2f} eV',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=8.5, family='monospace',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.85))

    axes[0].set_ylabel('Energy (eV)')
    axes[0].legend(fontsize=7, loc='lower right')
    fig.suptitle(
        f'Effect of Δ_CF on Band Structure  |  θ = {theta:.0f}°',
        fontsize=12, y=1.01)
    plt.tight_layout()
    if save:
        plt.savefig('cf_comparison.png', dpi=150, bbox_inches='tight')
        print('Saved cf_comparison.png')
    plt.show()


# ─── F. CHECKS AND MAIN ──────────────────────────────────────────────────────

def _run_cf_checks():
    """Numerical self-checks for the CF extension."""
    e_eg, e_t2g = cf_energies(DELTA_CF)

    # 1. Barycentre preserved
    assert np.isclose(2 * 0.6 - 3 * 0.4, 0.0, atol=1e-12), \
        "Barycentre coefficients wrong"

    # 2. R-point: eigenvalues must be {E_p×3, E_t2g, E_eg} (all hoppings vanish)
    H_R = bloch_hamiltonian_cf(np.array([np.pi, np.pi, np.pi]),
                                t=2.2, t_pp=T_PP0, delta_cf=DELTA_CF)
    eigs_R = np.linalg.eigvalsh(H_R)
    expected_R = sorted([E_P, E_P, E_P, e_t2g, e_eg])
    assert np.allclose(eigs_R, expected_R, atol=1e-12), \
        f"R-point check failed: {eigs_R} vs {expected_R}"

    # 3. t₂g band must be flat at E_t2g everywhere (zero hopping = zero dispersion)
    kpoints, _, _ = make_kpath(30)
    bands = compute_bands_cf(kpoints, 180.0, delta_cf=DELTA_CF)
    # Find the band that equals E_t2g at R — it should be flat
    # (We identify it by checking which column is closest to E_t2g at the R-point)
    r_eigs = np.linalg.eigvalsh(
        bloch_hamiltonian_cf(np.array([np.pi, np.pi, np.pi]),
                              t=2.2, t_pp=T_PP0, delta_cf=DELTA_CF))
    t2g_col = np.argmin(np.abs(r_eigs - e_t2g))
    assert np.allclose(bands[:, t2g_col], e_t2g, atol=1e-10), \
        "t₂g band is not flat — off-diagonal coupling must be zero"

    # 4. H(k) is real and symmetric at an arbitrary k
    k_test = np.array([1.1, 2.3, 0.7])
    H_k = bloch_hamiltonian_cf(k_test, t=2.0, t_pp=T_PP0, delta_cf=DELTA_CF)
    assert np.allclose(H_k, H_k.T, atol=1e-15), "H_cf(k) not symmetric"
    assert np.isrealobj(H_k), "H_cf(k) not real"

    # 5. Analytical gaps self-consistent: gap_eg − gap_t2g = Δ_CF (exactly)
    g_ct, g_eg, delta = analytical_gaps(DELTA_CF, T_PP0)
    assert np.isclose(g_eg - g_ct, delta, atol=1e-12), \
        "Analytical gap difference ≠ Δ_CF"

    print("All CF checks passed.")


def main():
    print("=" * 65)
    print("Crystal Field Extension  |  tight_binding_cf.py")
    print(f"  Δ_CF default = {DELTA_CF:.2f} eV  |  barycentre E_d = {E_D:.2f} eV")
    print("=" * 65)

    print(f"\n{'Δ_CF':>6}  {'E_eg':>7}  {'E_t2g':>7}  {'CT(t2g)':>9}  "
          f"{'CT(eg)':>8}  {'d-d Δ':>7}")
    print("-" * 55)
    for d in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        g_ct, g_eg, delta = analytical_gaps(d, T_PP0)
        e_eg, e_t2g = cf_energies(d)
        print(f"{d:>6.1f}  {e_eg:>7.3f}  {e_t2g:>7.3f}  "
              f"{g_ct:>9.3f}  {g_eg:>8.3f}  {delta:>7.3f}")

    print(f"\n  VBM = E_p − 4|t_pp| = {analytical_vbm():.3f} eV  [constant, all rows]")
    print("  CT(t2g) = O 2p → t₂g charge-transfer gap  (NOT the d–d gap)")
    print("  d-d Δ   = E_eg − E_t2g = Δ_CF  (the d–d splitting from LFT)")

    _run_cf_checks()

    print("\nGenerating plots...")
    plot_cf_bands(delta_cf=DELTA_CF)
    plot_cf_sweep()
    plot_cf_comparison(delta_cf_values=(0.5, 1.5, 2.5))


if __name__ == "__main__":
    main()
