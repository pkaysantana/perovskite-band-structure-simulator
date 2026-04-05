"""
Tight-Binding Band Structure for ABO₃ Perovskites
==================================================

4-band d–pσ + O–O hopping model on a simple cubic lattice.

BASIS (one formula unit)
  |d,  B ⟩  — one B-site d orbital at (0, 0, 0)
  |px, Ox⟩  — O p_σ orbital at (a/2, 0,   0  ), pointing toward B along x
  |py, Oy⟩  — O p_σ orbital at (0,   a/2, 0  ), pointing toward B along y
  |pz, Oz⟩  — O p_σ orbital at (0,   0,   a/2), pointing toward B along z

BLOCH HAMILTONIAN  H(k) is 4×4:

    ┌                                                   ┐
    │ E_d    Tx(k)     Ty(k)     Tz(k)                  │
    │ Tx     E_p       Pxy(k)    Pxz(k)                 │
    │ Ty     Pxy(k)    E_p       Pyz(k)                 │
    │ Tz     Pxz(k)    Pyz(k)    E_p                    │
    └                                                   ┘

    Tα(k)  = 2 t_eff cos(kα/2)           — B–O hopping (unchanged)
    Pxy(k) = 4 t_pp  cos(kx/2) cos(ky/2) — Ox–Oy hopping (new)
    Pxz(k) = 4 t_pp  cos(kx/2) cos(kz/2)
    Pyz(k) = 4 t_pp  cos(ky/2) cos(kz/2)

── EXACT RESULTS WITHIN THIS MODEL ──────────────────────────────────────────

(1) Bloch phase factors for O–O terms  [rigorous]
    Each Ox at (½,0,0) has four nearest Oy at face-diagonal distance a/√2.
    Unit-cell offsets and Bloch phases:
        Oy (0, 0,0): e^{i(−kx/2+ky/2)},  Oy (1, 0,0): e^{i(+kx/2+ky/2)}
        Oy (0,−1,0): e^{i(−kx/2−ky/2)},  Oy (1,−1,0): e^{i(+kx/2−ky/2)}
    Sum = 4 cos(kx/2) cos(ky/2).  Same factored form holds for all three pairs.

(2) R-point decoupling  [rigorous]
    At R = (π,π,π): all cos(kα/2) = 0.  Both Tα and Pαβ vanish identically.
    Eigenvalues are exactly E_d (once) and E_p (three times), independent of
    t_eff, t_pp, or any distortion parameter.
    → CBM ≡ E_d at R, for any distortion in this single-unit-cell model.

(3) VBM from antibonding O states  [rigorous by symmetry]
    At Γ, the 3×3 O-block (with O–O coupling) has eigenvalues:
        E_p + 8t_pp  — symmetric combination, couples to d, pushed down (t_pp < 0)
        E_p − 4t_pp  — doubly degenerate, antisymmetric (e.g. px−py)
    The antisymmetric states have zero matrix element with d at every k-point
    by construction (d couples equally to all three Oα, so antisymmetric O
    combinations cancel exactly).  Their energy E_p − 4t_pp is therefore exact.
    These states are the VBM.  With t_pp < 0: VBM = E_p + 4|t_pp| > E_p.
    The band is flat along Γ→X (shown analytically in comments on make_kpath).

(4) Band gap in this model  [rigorous]
    Gap = CBM − VBM = E_d − (E_p − 4t_pp) = (E_d − E_p) + 4t_pp
    With E_d=−2, E_p=−6, t_pp=−0.4:  Gap = 4.0 + 4(−0.4) = 2.4 eV.

── HEURISTIC CHOICES ────────────────────────────────────────────────────────

(5) O–O coupling parameter  t_pp  [heuristic magnitude; sign well-motivated]
    Two-centre decomposition for px on Ox, py on Oy, bond l = (−1/√2,1/√2,0):
        t(px,py) = lx·ly·(V_ppσ − V_ppπ) = −½(V_ppσ − V_ppπ)
    For oxides: V_ppσ ≈ +0.5 eV, V_ppπ ≈ −0.1 eV → t_pp ≈ −0.3 eV.
    The same value applies to all three O–O pairs by cubic symmetry.
    T_PP0 = −0.4 eV is within the plausible range; exact value depends on
    the specific material and is not derived here from first principles.

(6) t_eff ∝ cos(φ)  [heuristic; captures the dominant geometric effect]
    For a rigid octahedral rotation the B–O bond direction rotates by φ,
    reducing the p_σ–d overlap.  The cos(φ) factor is a reasonable projection
    but neglects bond-length changes and cooperative effects between cells.

── WHAT THIS MODEL DOES NOT CAPTURE ─────────────────────────────────────────

(A) Gap variation with distortion:
    For a rigid octahedral tilt, the O–O bond length and relative p_σ–p_σ
    orientation are PRESERVED (the octahedron rotates as a rigid body; both
    O atoms and their orbitals rotate together).  Therefore t_pp is constant
    under rigid tilts, VBM = E_p − 4t_pp is constant, CBM = E_d is constant,
    and the gap does not change with distortion in this single-unit-cell model.
    Gap opening requires one of:
      • Zone-folding: the distorted cell doubles (a√2 × a√2 × 2a supercell),
        folding the R-point back to Γ in the new BZ and opening a gap there.
      • Non-rigid distortions: B-site off-centering, breathing-mode O
        displacements, or Jahn–Teller splitting change bond lengths and break
        the orbital cancellation above.
      • Many-body effects: Mott–Hubbard U or self-interaction corrections.

(B) Crystal field splitting:
    The real d manifold splits into t₂g (lower) and e_g (upper) in an
    octahedral field.  See EXTENSIONS at the bottom of this file.

(C) Multi-orbital O-p basis:
    Each O atom has three p orbitals, only one of which (p_σ) is included here.
    The two π-type p orbitals on each O are neglected.

References
----------
Harrison, W.A. (1989) Electronic Structure and the Properties of Solids.
Goodenough, J.B. (1955) Phys. Rev. 100, 564.
"""

import numpy as np
import matplotlib.pyplot as plt


# ─── 1. PHYSICAL PARAMETERS ──────────────────────────────────────────────────

E_D = -2.0    # B-site d orbital on-site energy (eV)
E_P = -6.0    # O 2p orbital on-site energy (eV)
# Charge-transfer energy: ΔE = E_D − E_P = 4.0 eV

V_PD_SIGMA = 2.2   # eV, Harrison Vpdσ at reference Ti–O distance
D0         = 1.96  # Å,  Ti–O in CaTiO₃

# O–O nearest-neighbour hopping (eV).
# Negative = net bonding character (antibonding O combination is pushed up).
# Estimate: t_pp ≈ −½(V_ppσ − V_ppπ) ≈ −0.3 eV; −0.4 eV used here.
# For a rigid octahedral tilt this value is CONSTANT — see module docstring (A).
T_PP0 = -0.4


# ─── 2. GEOMETRY & EFFECTIVE HOPPING ─────────────────────────────────────────

def tilt_angle_deg(bond_angle_deg):
    """
    B–O–B bond angle θ → octahedral tilt angle φ = (180° − θ) / 2.

    φ = 0° in the cubic phase (θ = 180°).
    φ = 20° for a strongly tilted structure (θ = 140°).
    """
    return (180.0 - bond_angle_deg) / 2.0


def hopping_integral(bond_angle_deg, bond_length_ang=D0):
    """
    Effective d–p hopping  t_eff = V_pdσ × (d₀/d)^3.5 × cos(φ)  [eV].

    Heuristic: the p_σ orbital on O rotates by φ when the octahedron tilts,
    reducing its overlap with the B d orbital by one factor of cos(φ).
    The d^−3.5 Harrison scaling is empirical but well-established for d-p bonds.
    """
    phi = np.radians(tilt_angle_deg(bond_angle_deg))
    return V_PD_SIGMA * (D0 / bond_length_ang) ** 3.5 * np.cos(phi)


def pp_hopping(t_pp0=T_PP0):
    """
    O–O hopping parameter  t_pp  [eV].

    Returns t_pp0 unchanged.  t_pp is CONSTANT under rigid octahedral tilts:
    the O–O bond length and the relative orientation of the two p_σ orbitals
    are both preserved when the whole BO₆ octahedron rotates as a rigid body
    (see module docstring section A for the two-centre integral proof).

    The parameter is kept as a function (rather than a bare constant) so that
    future extensions — e.g. breathing-mode distortions that change d_OO —
    can be slotted in here without touching the rest of the code.
    """
    return t_pp0


# ─── 3. BLOCH HAMILTONIAN ────────────────────────────────────────────────────

def bloch_hamiltonian(k, t, t_pp=0.0, e_d=E_D, e_p=E_P):
    """
    Build H(k) as a (4, 4) real symmetric matrix.

    Basis: [d, px@Ox, py@Oy, pz@Oz]

    d–O terms  Tα = 2t cos(kα/2):
        Phase from summing over the two B–O hops along each axis
        (B→Oα at +a/2 same cell; B→Oα at −a/2 adjacent cell).

    O–O terms  Pαβ = 4t_pp cos(kα/2) cos(kβ/2):
        Phase from summing over the four Oα–Oβ face-diagonal hops.
        See module docstring (1) for the explicit Bloch sum.

    Special k-points:
        Γ = (0,0,0):   all Tα = 2t, all Pαβ = 4t_pp  — maximum hybridisation
        X = (π,0,0):   Tx = 0, Pxy = Pxz = 0; only Pyz = 4t_pp active
        M = (π,π,0):   all Pαβ = 0; O bands return to E_p
        R = (π,π,π):   all Tα = 0, all Pαβ = 0; d and p fully decouple
    """
    kx, ky, kz = k

    Tx  = 2.0 * t    * np.cos(kx / 2.0)
    Ty  = 2.0 * t    * np.cos(ky / 2.0)
    Tz  = 2.0 * t    * np.cos(kz / 2.0)
    Pxy = 4.0 * t_pp * np.cos(kx / 2.0) * np.cos(ky / 2.0)
    Pxz = 4.0 * t_pp * np.cos(kx / 2.0) * np.cos(kz / 2.0)
    Pyz = 4.0 * t_pp * np.cos(ky / 2.0) * np.cos(kz / 2.0)

    return np.array([
        [e_d, Tx,  Ty,  Tz ],
        [Tx,  e_p, Pxy, Pxz],
        [Ty,  Pxy, e_p, Pyz],
        [Tz,  Pxz, Pyz, e_p],
    ], dtype=float)


# ─── 4. K-PATH ───────────────────────────────────────────────────────────────

def make_kpath(n_per_segment=50):
    """
    High-symmetry k-path: Γ → X → M → R → Γ  (simple cubic BZ, a = 1).

    Key points and the active O–O couplings at each:
        Γ: all Pαβ = 4t_pp        — VBM band at E_p − 4t_pp (flat from here to X)
        X: only Pyz = 4t_pp        — px decouples; VBM still at E_p − 4t_pp
        M: all Pαβ = 0             — O bands flatten to E_p
        R: all Tα = 0, Pαβ = 0    — CBM = E_d exactly

    Why the VBM band is flat Γ→X  [analytical]:
        Along k = (kx, 0, 0): Pxy = 4t_pp cos(kx/2), Pxz = 4t_pp cos(kx/2),
        Pyz = 4t_pp (constant).
        The antisymmetric Oy–Oz combination |(py−pz)/√2⟩ has:
            ⟨(py−pz)/√2 | Pxy−Pxz | px⟩ = (Pxy−Pxz)/√2 = 0  [they cancel]
        So this state decouples from px and d along the entire Γ→X segment,
        remaining at the eigenvalue E_p − 4t_pp of the Pyz block.

    Returns
    -------
    kpoints        : (N, 3) array
    tick_positions : list of int
    tick_labels    : list of str
    """
    G = np.array([0.,    0.,    0.   ])
    X = np.array([np.pi, 0.,    0.   ])
    M = np.array([np.pi, np.pi, 0.   ])
    R = np.array([np.pi, np.pi, np.pi])

    waypoints = [G, X, M, R, G]
    labels    = ['Γ', 'X', 'M', 'R', 'Γ']

    kpoints, tick_positions = [], []
    for i in range(len(waypoints) - 1):
        segment = np.linspace(waypoints[i], waypoints[i + 1],
                              n_per_segment, endpoint=False)
        tick_positions.append(len(kpoints))
        kpoints.extend(segment)

    tick_positions.append(len(kpoints))
    kpoints.append(waypoints[-1])

    return np.array(kpoints), tick_positions, labels


# ─── 5. BAND STRUCTURE SOLVER ────────────────────────────────────────────────

def compute_bands(kpoints, bond_angle_deg, bond_length_ang=D0,
                  t_pp0=T_PP0, e_d=E_D, e_p=E_P):
    """
    Diagonalise H(k) at every k-point; return (N_k, 4) eigenvalue array.

    Column assignments (ascending energy at each k):
        0 — deep bonding band (O 2p symmetric combination, pushed far below E_p)
        1 — intermediate O 2p band (mixed bonding character)
        2 — antibonding O 2p band (VBM; flat at E_p − 4t_pp along Γ→X)
        3 — conduction band (d-like near R, strongly antibonding near Γ)

    Note: 'column 2 = VBM' holds for the chosen parameters; if t_pp were
    made positive, the ordering could change.  Always check the actual
    eigenvalue ordering rather than assuming band index = orbital character.
    """
    t    = hopping_integral(bond_angle_deg, bond_length_ang)
    t_pp = pp_hopping(t_pp0)   # constant — see pp_hopping docstring

    return np.array([
        np.linalg.eigvalsh(bloch_hamiltonian(k, t, t_pp, e_d, e_p))
        for k in kpoints
    ])


def band_gap(bands):
    """
    Indirect band gap = min(col 3) − max(col 2)  [eV].

    Exact within the model:
        min(col 3) = E_d   (at R-point, CBM)
        max(col 2) = E_p − 4t_pp   (antibonding O state, VBM)
        → Gap = (E_d − E_p) + 4t_pp  [constant for fixed t_pp]

    The gap does NOT vary with bond angle in this single-unit-cell model.
    See module docstring section (A) for why, and what physics is needed
    to get gap variation.
    """
    return float(np.min(bands[:, 3]) - np.max(bands[:, 2]))


def bandwidth(bands, band_index=3):
    """Width of a single band (default: conduction band d)."""
    return float(np.max(bands[:, band_index]) - np.min(bands[:, band_index]))


# ─── 6. SWEEP OVER DISTORTION ────────────────────────────────────────────────

def sweep_distortion(angles_deg, bond_length_ang=D0, t_pp0=T_PP0, n_k=50):
    """
    Sweep B–O–B angle from cubic (180°) to distorted (~140°).

    Returns: gaps, widths, tilts, t_vals, tpp_vals

    Expected behaviour after the t_pp correction:
        gaps   — CONSTANT (gap = (E_d − E_p) + 4t_pp, independent of angle)
        widths — DECREASING (conduction band narrows as t_eff drops)
        t_pp   — CONSTANT (same value at every angle; confirms the correction)
    """
    kpoints, _, _ = make_kpath(n_k)
    n = len(angles_deg)
    gaps, widths, t_vals = np.zeros(n), np.zeros(n), np.zeros(n)
    t_pp = pp_hopping(t_pp0)
    tpp_vals = np.full(n, t_pp)   # constant array — useful as a visual sanity check

    for i, theta in enumerate(angles_deg):
        bands      = compute_bands(kpoints, theta, bond_length_ang, t_pp0)
        gaps[i]    = band_gap(bands)
        widths[i]  = bandwidth(bands)
        t_vals[i]  = hopping_integral(theta, bond_length_ang)

    tilts = np.array([tilt_angle_deg(a) for a in angles_deg])
    return gaps, widths, tilts, t_vals, tpp_vals


# ─── 7. PLOTTING ─────────────────────────────────────────────────────────────

_BAND_COLOURS = ['#1565C0', '#42A5F5', '#90CAF9', '#E53935']
_BAND_LABELS  = ['O 2p bonding', 'O 2p mixed', 'O 2p antibonding (VBM)', 'B d (conduction)']


def plot_band_structure(angles_to_show=(180, 150), n_k=80, t_pp0=T_PP0, save=True):
    """
    Side-by-side band structure plots for two distortion levels.

    What is new compared to the original 4-band model:
      - Band 2 (pale blue) is no longer flat: it bows up near Γ (where
        Pαβ is largest) and falls back to E_p at M and R (where Pαβ → 0).
      - The VBM is higher than E_p by 4|t_pp| — O–O covalency raises it.
      - The gap is smaller than E_d − E_p by the same amount.

    What is the SAME as the original model:
      - The gap does not change between the two panels: VBM = E_p − 4t_pp
        and CBM = E_d are both pinned by k-points where hoppings vanish.
      - Conduction bandwidth narrows with increasing tilt (t_eff drops).
    """
    kpoints, ticks, tick_labels = make_kpath(n_k)
    x = np.arange(len(kpoints))

    fig, axes = plt.subplots(1, len(angles_to_show),
                             figsize=(6 * len(angles_to_show), 6), sharey=True)
    if len(angles_to_show) == 1:
        axes = [axes]

    for ax, theta in zip(axes, angles_to_show):
        bands = compute_bands(kpoints, theta, t_pp0=t_pp0)
        t     = hopping_integral(theta)
        t_pp  = pp_hopping(t_pp0)
        phi   = tilt_angle_deg(theta)

        for b in range(4):
            ax.plot(x, bands[:, b], color=_BAND_COLOURS[b], lw=1.8,
                    label=_BAND_LABELS[b])

        vbm = np.max(bands[:, 2])
        cbm = np.min(bands[:, 3])
        ax.axhline(vbm, color='#90CAF9', lw=0.8, ls=':', alpha=0.9)
        ax.axhline(cbm, color='#E53935',  lw=0.8, ls=':', alpha=0.9)

        ax.text(0.97, 0.97,
                f't_eff = {t:.3f} eV\n'
                f't_pp  = {t_pp:.3f} eV  [const]\n'
                f'W_d   = {bandwidth(bands):.2f} eV\n'
                f'Gap   = {cbm - vbm:.2f} eV\n'
                f'VBM   = {vbm:.2f} eV',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=8.5, family='monospace',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax.set_xticks(ticks)
        ax.set_xticklabels(tick_labels, fontsize=12)
        for xi in ticks[1:-1]:
            ax.axvline(xi, color='lightgray', lw=0.8)

        ax.set_title(f'θ = {theta:.0f}°  (φ = {phi:.1f}°)', fontsize=12)
        ax.set_ylabel('Energy (eV)' if ax is axes[0] else '')
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(-13, 7)
        ax.legend(fontsize=8, loc='lower right')

    fig.suptitle(
        f'ABO₃ 4-Band d–pσ + O–O  |  t_pp = {t_pp0:.2f} eV (constant)',
        fontsize=12, y=1.01)
    plt.tight_layout()
    if save:
        plt.savefig('band_structure.png', dpi=150, bbox_inches='tight')
        print('Saved band_structure.png')
    plt.show()


def plot_distortion_curves(angles_deg=None, t_pp0=T_PP0, save=True):
    """
    Three panels showing what distortion does (and does not) change.

    (a) Hopping parameters vs tilt φ:
        t_eff decreases (cos(φ) — d–p overlap reduced by tilt)
        t_pp  is flat    (constant — rigid rotation preserves O–O geometry)

    (b) Conduction bandwidth vs φ:
        Narrows with tilt because t_eff ∝ cos(φ).  This is the physical
        result the model does capture correctly.

    (c) Band gap vs φ:
        FLAT LINE.  This is the honest result of the corrected model.
        Gap = (E_d − E_p) + 4t_pp = constant because both CBM (pinned at
        E_d by R-point decoupling) and VBM (pinned at E_p − 4t_pp by O–O
        symmetry) are independent of t_eff and t_pp.
        The flat line is not a bug — it correctly shows the limitation of
        the single-unit-cell model.  Gap variation requires zone-folding.
    """
    if angles_deg is None:
        angles_deg = np.linspace(140, 180, 41)

    gaps, widths, tilts, t_vals, tpp_vals = sweep_distortion(angles_deg, t_pp0=t_pp0)
    analytic_gap = (E_D - E_P) + 4 * t_pp0   # exact formula from docstring

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 9), sharex=True)

    # Panel 1: hopping parameters
    ax1.plot(tilts, t_vals,           'o-', color='#7B1FA2', lw=2, ms=3,
             label='t_eff  ∝ cos(φ)  [heuristic]')
    ax1.plot(tilts, np.abs(tpp_vals), 's-', color='#388E3C', lw=2, ms=3,
             label='|t_pp|  = const  [exact for rigid tilt]')
    ax1.set_ylabel('Hopping magnitude (eV)', fontsize=11)
    ax1.set_title(f'Distortion effects  (t_pp₀ = {t_pp0:.2f} eV)', fontsize=11)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel 2: conduction bandwidth
    ax2.plot(tilts, widths, 's-', color='#E53935', lw=2, ms=3)
    ax2.set_ylabel('Conduction bandwidth (eV)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    w0 = widths[np.argmin(tilts)]
    w1 = widths[np.argmax(tilts)]
    ax2.annotate(f'−{100*(w0-w1)/w0:.1f}% cubic → max tilt',
                 xy=(tilts[-1], w1), xytext=(tilts[-1] - 7, w1 + 0.4),
                 fontsize=9, color='#E53935',
                 arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.2))

    # Panel 3: band gap — flat line with explanation
    ax3.plot(tilts, gaps, 'D-', color='#F57F17', lw=2, ms=4)
    ax3.axhline(analytic_gap, color='#F57F17', lw=0.8, ls='--', alpha=0.6,
                label=f'Analytic: (E_d−E_p) + 4t_pp = {analytic_gap:.2f} eV')
    ax3.set_ylabel('Band gap (eV)', fontsize=11)
    ax3.set_xlabel('Tilt angle φ (°)', fontsize=11)
    ax3.set_ylim(0, analytic_gap * 1.6)
    ax3.legend(fontsize=8, loc='upper right')
    ax3.grid(True, alpha=0.3)
    ax3.text(0.5, 0.18,
             'Gap is constant: CBM = E_d (R-point) and VBM = E_p − 4t_pp (O–O symmetry)\n'
             'are both pinned at k-points where all hoppings vanish.\n'
             'Gap variation requires zone-folding (doubled unit cell) — next step.',
             transform=ax3.transAxes, ha='center', fontsize=8.5,
             style='italic', color='#5D4037',
             bbox=dict(boxstyle='round', facecolor='#FFF8E1', alpha=0.8))

    # Secondary x-axis: B–O–B angle
    ax3b = ax3.twiny()
    ax3b.set_xlim(ax3.get_xlim())
    tick_tilts = ax3.get_xticks()
    ax3b.set_xticks(tick_tilts)
    ax3b.set_xticklabels([f'{180 - 2*φ:.0f}°' for φ in tick_tilts], fontsize=8)
    ax3b.set_xlabel('B–O–B angle θ (°)', fontsize=10)

    plt.tight_layout()
    if save:
        plt.savefig('distortion_curves.png', dpi=150, bbox_inches='tight')
        print('Saved distortion_curves.png')
    plt.show()


def compare_models(theta=180.0, n_k=80, t_pp0=T_PP0, save=True):
    """
    Direct comparison: original 4-band (t_pp=0) vs extended (t_pp=T_PP0).

    The difference is entirely in the valence bands:
      - Original: bands 1 and 2 are flat at E_p everywhere
      - Extended: band 2 bows up near Γ (antibonding O–O), band 1 disperses
      - Gap is reduced in the extended model by 4|t_pp| = 1.6 eV
    """
    kpoints, ticks, tick_labels = make_kpath(n_k)
    x = np.arange(len(kpoints))

    bands_no_pp  = compute_bands(kpoints, theta, t_pp0=0.0)
    bands_with_pp = compute_bands(kpoints, theta, t_pp0=t_pp0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    for ax, bands, label in [
        (ax1, bands_no_pp,  'Original  (t_pp = 0)'),
        (ax2, bands_with_pp, f'Extended  (t_pp = {t_pp0:.2f} eV)'),
    ]:
        for b in range(4):
            ax.plot(x, bands[:, b], color=_BAND_COLOURS[b], lw=1.8,
                    label=_BAND_LABELS[b])
        vbm = np.max(bands[:, 2])
        cbm = np.min(bands[:, 3])
        ax.axhline(vbm, color='#90CAF9', lw=0.8, ls=':')
        ax.axhline(cbm, color='#E53935',  lw=0.8, ls=':')
        ax.set_xticks(ticks)
        ax.set_xticklabels(tick_labels, fontsize=11)
        for xi in ticks[1:-1]:
            ax.axvline(xi, color='lightgray', lw=0.8)
        ax.set_title(label, fontsize=11)
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(-13, 7)
        ax.text(0.97, 0.97, f'VBM = {vbm:.2f} eV\nGap = {cbm-vbm:.2f} eV',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=9, family='monospace',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax.legend(fontsize=8, loc='lower right')
    ax1.set_ylabel('Energy (eV)')
    fig.suptitle(f'Model Comparison  |  θ = {theta:.0f}° (cubic)', fontsize=12, y=1.01)
    plt.tight_layout()
    if save:
        plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
        print('Saved model_comparison.png')
    plt.show()


# ─── 8. MAIN ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("ABO₃ Tight-Binding  |  4-band d–pσ + O–O hopping")
    print(f"  t_pp = {T_PP0:.2f} eV (constant under rigid tilts)")
    print(f"  Analytic gap = (E_d−E_p) + 4·t_pp = {(E_D-E_P) + 4*T_PP0:.3f} eV")
    print("=" * 65)

    kpoints, _, _ = make_kpath(n_per_segment=60)

    print(f"\n{'θ':>7}  {'φ':>6}  {'t_eff':>8}  {'t_pp':>8}  {'W_d':>8}  {'Gap':>8}  {'VBM':>8}")
    print("-" * 65)
    for theta in [180.0, 170.0, 160.0, 150.0, 140.0]:
        bands = compute_bands(kpoints, theta)
        print(f"{theta:>7.1f}  {tilt_angle_deg(theta):>6.1f}"
              f"  {hopping_integral(theta):>8.4f}"
              f"  {pp_hopping():>8.4f}"
              f"  {bandwidth(bands):>8.4f}"
              f"  {band_gap(bands):>8.4f}"
              f"  {np.max(bands[:, 2]):>8.4f}")

    print("\n[All energies in eV]")
    print("Expected: Gap constant across all rows (model limitation).")
    print("Expected: W_d decreasing with tilt (model success).")
    print("Expected: t_pp constant across all rows (correct physics for rigid tilts).")

    # Numerical self-checks
    _run_checks()

    print("\nGenerating plots...")
    compare_models(theta=180.0)
    plot_band_structure(angles_to_show=(180, 150))
    plot_distortion_curves()


def _run_checks():
    """Quick numerical assertions — run on every import for sanity."""
    t_pp = T_PP0

    # 1. R-point: all couplings must vanish; eigenvalues = {E_p×3, E_d}
    H_R = bloch_hamiltonian(np.array([np.pi, np.pi, np.pi]), t=2.2, t_pp=t_pp)
    eigs_R = np.linalg.eigvalsh(H_R)
    assert np.allclose(eigs_R, sorted([E_P, E_P, E_P, E_D]), atol=1e-12), \
        f"R-point check failed: {eigs_R}"

    # 2. VBM at Γ must equal E_p − 4*t_pp (exact by symmetry)
    H_G = bloch_hamiltonian(np.array([0., 0., 0.]), t=2.2, t_pp=t_pp)
    eigs_G = np.linalg.eigvalsh(H_G)
    expected_vbm = E_P - 4 * t_pp
    assert np.isclose(eigs_G[2], expected_vbm, atol=1e-10), \
        f"VBM check failed: got {eigs_G[2]:.6f}, expected {expected_vbm:.6f}"

    # 3. H(k) is real and symmetric at an arbitrary k
    k_test = np.array([1.1, 2.3, 0.7])
    H_k = bloch_hamiltonian(k_test, t=1.5, t_pp=t_pp)
    assert np.allclose(H_k, H_k.T, atol=1e-15), "H(k) not symmetric"
    assert np.isrealobj(H_k), "H(k) not real"

    # 4. t_pp=0 recovers flat valence bands
    kpoints, _, _ = make_kpath(20)
    bands_flat = compute_bands(kpoints, 180.0, t_pp0=0.0)
    assert np.allclose(bands_flat[:, 1], E_P, atol=1e-10), \
        "Band 1 not flat with t_pp=0"
    assert np.allclose(bands_flat[:, 2], E_P, atol=1e-10), \
        "Band 2 not flat with t_pp=0"

    # 5. Gap is constant across distortion sweep (key correction check)
    angles = np.linspace(140, 180, 10)
    gaps, *_ = sweep_distortion(angles, n_k=20)
    assert np.allclose(gaps, gaps[0], atol=1e-8), \
        f"Gap not constant: range = {gaps.max()-gaps.min():.2e} eV"

    print("All checks passed.")


# ─── EXTENSIONS ──────────────────────────────────────────────────────────────
#
# Next step — zone-folding to open a distortion-dependent gap:
#   Build a 2×2×2 supercell Hamiltonian.  The R-point of the cubic BZ folds
#   to Γ in the new BZ.  Symmetry-allowed avoided crossings open a gap there,
#   whose magnitude scales with the tilt order parameter.
#   This is the minimal physically correct route to gap variation with θ.
#
# Crystal field splitting:
#   E_t2g = E_D − 0.4·Δ_CF   (dxy/dyz/dxz — π-bonding with O)
#   E_eg  = E_D + 0.6·Δ_CF   (dz²/dx²-y²  — σ-bonding with O)
#   Extend the basis to separate t₂g and e_g blocks with different V_pd.
#
# Non-rigid distortions (breathing modes, B-site off-centering):
#   These change individual B–O bond lengths, so d_OO changes, and t_pp
#   acquires a distortion dependence via Harrison d^−2.5 scaling.
#   Slot in here: pp_hopping(t_pp0, d_OO) = t_pp0 * (d_OO_ref / d_OO)**2.5

if __name__ == "__main__":
    main()
