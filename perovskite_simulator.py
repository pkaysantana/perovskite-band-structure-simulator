import numpy as np
import json
import matplotlib.pyplot as plt
from dataclasses import dataclass, asdict

# --- 1. CONFIGURATION & CONSTANTS ---
# Harrison's Solid State Table parameters (approximate for Perovskites)
# Energy levels in eV
E_d = -2.0  # Metal d-orbital energy (Ti 3d)
E_p = -6.0  # Oxygen p-orbital energy (O 2p)

# Hopping parameters (V_pd sigma) at reference bond length d0
V_pd_sigma_0 = 2.2  # eV
d0 = 1.96           # Angstroms (Reference Ti-O bond length)

@dataclass
class SimulationResult:
    angle: float
    bond_length: float
    k_path: list
    bands: list  # List of energy arrays [band_index][k_point]
    overlap_factor: float

class PerovskiteModel:
    def __init__(self, metal_symbol="Ti"):
        self.metal = metal_symbol
        # Simple effective parameters can be swapped based on metal
        if metal_symbol == "Ti":
            self.E_d = -2.0
        elif metal_symbol == "Mn":
            self.E_d = -4.0 # Lower d-levels
        else:
            self.E_d = -2.0

    def get_hopping_integral(self, d, angle_deg):
        """
        Calculates effective hopping integral t using Harrison's scaling.
        t ~ 1/d^3.5
        Angle dependence: t_eff = t_sigma * cos(180 - angle) for distortion
        """
        # Harrison's scaling for bond length
        V_scaled = V_pd_sigma_0 * (d0 / d)**3.5
        
        # Angular dependence (geometric reduction of overlap)
        # 180 deg = Max overlap (factor 1.0)
        # 90 deg = Zero overlap (factor 0.0)
        # We approximate the projection as |cos(theta_deviation)|
        # Deviation is (180 - angle) / 2 roughly for the tilting
        # Simplified effective model: t_eff scales linearly with cos of the tilt.
        # Let's use a geometric factor representing the bond bending.
        # For a bond angle alpha (e.g. 160), the overlap reduction is roughly cos(180-alpha)
        # But in perovskite tilting, the reduction is subtle. 
        # We will model it as: V_eff = V * cos(tilt_angle)
        # where tilt_angle approx (180 - angle_deg).
        
        tilt_rad = np.radians(180 - angle_deg)
        angular_factor = np.abs(np.cos(tilt_rad)) # Simple projection
        
        return V_scaled * angular_factor, angular_factor

    def solve_hamiltonian(self, angle_deg, d_bond, k_points):
        """
        Solves a simplified 2-band Tight-Binding Hamiltonian.
        H = | E_d      2t*cos(k) |
            | 2t*cos(k)  E_p     |
        Expanded to 3D simple cubic lattice for dispersion.
        """
        t, overlap_factor = self.get_hopping_integral(d_bond, angle_deg)
        
        # Band structure storage
        # We will store 2 bands (Bonding/Antibonding)
        bands = [[], []] 
        
        for k in k_points:
            kx, ky, kz = k
            
            # Dispersion factor for simple cubic (sum of cosines)
            # Gamma(0,0,0) -> sum=3
            # M(pi,pi,0) -> sum=0 (approx)
            # This is a simplified dispersion for the B-O interaction
            f_k = np.cos(kx) + np.cos(ky) + np.cos(kz)
            
            # Off-diagonal interaction element
            # This represents the hybridization width
            interaction = 2 * t * f_k
            
            # 2x2 Hamiltonian Matrix
            # | E_d       interaction |
            # | interaction   E_p     |
            
            H = np.array([
                [self.E_d, interaction],
                [interaction, E_p]
            ])
            
            eigenvalues = np.linalg.eigvalsh(H)
            bands[0].append(eigenvalues[0]) # Lower band (Valence/p-like)
            bands[1].append(eigenvalues[1]) # Upper band (Conduction/d-like)
            
        return bands, overlap_factor

def generate_k_path(num_points=100):
    """
    Generates k-points for path Gamma -> X -> M -> Gamma
    Gamma=(0,0,0), X=(pi,0,0), M=(pi,pi,0)
    """
    path = []
    labels = []
    
    # Segment 1: Gamma -> X
    for i in range(num_points):
        val = np.pi * (i / num_points)
        path.append([val, 0, 0])
        
    # Segment 2: X -> M
    for i in range(num_points):
        val = np.pi * (i / num_points)
        path.append([np.pi, val, 0])

    # Segment 3: M -> Gamma
    for i in range(num_points):
        val = np.pi * (1 - i / num_points)
        path.append([val, val, 0])
        
    return path

def main():
    print("--- Perovskite Simulator: Reference Generator ---")
    
    # 1. Setup
    model = PerovskiteModel(metal_symbol="Ti")
    k_path = generate_k_path(50) # 50 points per segment
    
    # 2. Run Scenarios
    scenarios = [
        {"angle": 180.0, "d": 1.96, "label": "Cubic (Ideal)"},
        {"angle": 150.0, "d": 1.96, "label": "Distorted (Tilted)"}
    ]
    
    results = {}
    
    for s in scenarios:
        bands, overlap = model.solve_hamiltonian(s["angle"], s["d"], k_path)
        
        # Calculate Band Width (Conduction Band)
        cb = bands[1]
        width = max(cb) - min(cb)
        
        # Calculate Gap
        vb = bands[0]
        gap = min(cb) - max(vb)
        
        print(f"Scenario: {s['label']}")
        print(f"  Overlap Factor: {overlap:.4f}")
        print(f"  Band Width (CB): {width:.4f} eV")
        print(f"  Band Gap:       {gap:.4f} eV")
        print("-" * 30)
        
        results[s["label"]] = {
            "angle": s["angle"],
            "overlap_factor": overlap,
            "band_width": width,
            "band_gap": gap,
            "bands": bands # [ [E_val...], [E_cond...] ]
        }

    # 3. Export Ground Truth
    with open("ground_truth.json", "w") as f:
        json.dump(results, f, indent=2)
    print(">> Generated ground_truth.json")

    # 4. Optional: Quick Viz to verify physics before coding JS
    # (Commented out for production, useful for debug)
    # plt.plot(results["Cubic (Ideal)"]["bands"][1], label="Cubic CB")
    # plt.plot(results["Distorted (Tilted)"]["bands"][1], label="Distorted CB")
    # plt.legend()
    # plt.show()

if __name__ == "__main__":
    main()