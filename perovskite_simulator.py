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


if __name__ == "__main__":
    al = MetalIon("Al", 3, coordination_number=6)
    water = Ligand("H2O", lone_pairs=2)

    for _ in range(6):
        al.bind_ligand(water)

    print(al.complex_formula())  # e.g. [Al(H2O)6]
