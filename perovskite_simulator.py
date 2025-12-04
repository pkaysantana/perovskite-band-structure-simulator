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

if __name__ == "__main__":
    # Molecular complex
    al = MetalIon("Al", 3, coordination_number=6)
    water = Ligand("H2O", lone_pairs=2)

    for _ in range(6):
        al.bind_ligand(water)

    print("Molecular complex:")
    print(" ", al.complex_formula())
    print()

    # Solid-state perovskite
    cubic = Perovskite("Ca", "Ti", distortion_type="cubic")
    distorted = Perovskite("Ca", "Ti", distortion_type="distorted")

    print("Perovskite models:")
    print(" ", cubic.summary())
    print(" ", distorted.summary())
