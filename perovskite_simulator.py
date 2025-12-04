import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # noqa: F401 (enables 3D plotting)


def orbital_overlap(r_BO: float, theta_deg: float) -> float:
    """
    Simple d–p overlap model.
    S_dp ∝ exp(-r^2/2) * |cos(theta - 180°)|
    r_BO in Å, theta_deg is B–O–B angle in degrees.
    """
    distance_factor = math.exp(-(r_BO ** 2) / 2.0)
    angle_rad = math.radians(theta_deg)
    angle_factor = abs(math.cos(angle_rad - math.pi))
    return distance_factor * angle_factor

class MetalIon:
    def __init__(self, element, charge, coordination_number=6):
        self.element = element
        self.charge = charge
        self.coordination_number = coordination_number
        self.bound_ligands = []

    def bind_ligand(self, ligand):
        if len(self.bound_ligands) < self.coordination_number and ligand.lone_pairs > 0:
            self.bound_ligands.append(ligand)
            ligand.lone_pairs -= 1
            return True
        return False

    def complex_formula(self):
        if not self.bound_ligands:
            return f"{self.element}^{self.charge}+"

        # assume all ligands are same type for now
        ligand_name = self.bound_ligands[0].name
        n = len(self.bound_ligands)
        return f"[{self.element}({ligand_name}){n}]{self.charge}+"


class Ligand:
    def __init__(self, name, lone_pairs):
        self.name = name
        self.lone_pairs = lone_pairs

class Perovskite:
    """
    Simple ABO3 perovskite model.
    A = large cation (e.g. Ca2+)
    B = smaller transition-metal cation (e.g. Ti4+)
    O = oxide ligand
    """

    def __init__(self, A_element: str, B_element: str, distortion_type: str = "cubic"):
        self.A_element = A_element
        self.B_element = B_element
        self.distortion_type = distortion_type  # "cubic" or "distorted" for now

        # For now just store some basic geometry parameters
        self.bo_angle = self._bo_angle_from_distortion()
        self.bo_distance = 2.0  # Å, placeholder constant for now

    def _bo_angle_from_distortion(self) -> float:
        if self.distortion_type == "cubic":
            return 180.0
        elif self.distortion_type == "distorted":
            return 155.0
        else:
            return 180.0

    def summary(self) -> str:
        return (
            f"{self.A_element}{self.B_element}O3 "
            f"({self.distortion_type}, B–O–B ≈ {self.bo_angle}°)"
        )

    def orbital_overlap(self) -> float:
        """Return d–p overlap for this B–O–B geometry."""
        return orbital_overlap(self.bo_distance, self.bo_angle)

def _octahedral_positions(distorted: bool = False) -> np.ndarray:
    """Return coordinates of 6 oxygens around B."""
    if not distorted:
        # perfect octahedron
        return np.array([
            [1, 0, 0],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0],
            [0, 0, 1],
            [0, 0, -1],
        ], dtype=float)
    else:
        # slightly tilted/elongated octahedron
        return np.array([
            [1.0, 0, 0.1],
            [-1.0, 0, -0.1],
            [0, 1.05, 0],
            [0, -1.05, 0],
            [0, 0, 0.85],
            [0, 0, -0.85],
        ], dtype=float)


def plot_octahedra():
    """Plot cubic vs distorted BO6 octahedra side by side."""
    fig = plt.figure(figsize=(10, 4))

    # Cubic
    ax1 = fig.add_subplot(121, projection="3d")
    pos_cubic = _octahedral_positions(distorted=False)
    ax1.scatter([0], [0], [0], c="blue", s=200, label="B cation")
    ax1.scatter(*pos_cubic.T, c="red", s=80, label="O anions")
    for p in pos_cubic:
        ax1.plot([0, p[0]], [0, p[1]], [0, p[2]], "k-", alpha=0.7)
    ax1.set_title("Cubic (B–O–B = 180°)")
    ax1.set_box_aspect((1, 1, 1))

    # Distorted
    ax2 = fig.add_subplot(122, projection="3d")
    pos_dist = _octahedral_positions(distorted=True)
    ax2.scatter([0], [0], [0], c="blue", s=200, label="B cation")
    ax2.scatter(*pos_dist.T, c="red", s=80, label="O anions")
    for p in pos_dist:
        ax2.plot([0, p[0]], [0, p[1]], [0, p[2]], "k-", alpha=0.7)
    ax2.set_title("Distorted (B–O–B < 180°)")
    ax2.set_box_aspect((1, 1, 1))

    for ax in (ax1, ax2):
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Molecular complex
    al = MetalIon("Al", 3, coordination_number=6)
    water = Ligand("H2O", lone_pairs=2)

    for _ in range(6):
        al.bind_ligand(water)

    print("Molecular complex:")
    print(" ", al.complex_formula())
    print()

    # Solid-state perovskites
    cubic = Perovskite("Ca", "Ti", distortion_type="cubic")
    distorted = Perovskite("Ca", "Ti", distortion_type="distorted")

    print("Perovskite models:")
    print(" ", cubic.summary(), f"S_dp ≈ {cubic.orbital_overlap():.4f}")
    print(" ", distorted.summary(), f"S_dp ≈ {distorted.orbital_overlap():.4f}")

    print()
    print("Generating 3D BO6 octahedron visualisation (cubic vs distorted)...")
    plot_octahedra()
    