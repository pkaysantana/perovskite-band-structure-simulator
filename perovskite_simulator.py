class MetalIon:
    def __init__(self, element, charge, coordination_number=6):
        self.element = element
        self.charge = charge
        self.coordination_number = coordination_number
        self.bound_ligands = []

class Ligand:
    def __init__(self, name, lone_pairs):
        self.name = name
        self.lone_pairs = lone_pairs

if __name__ == "__main__":
    al = MetalIon("Al", 3, coordination_number=6)
    water = Ligand("H2O", lone_pairs=2)

    print(f"Metal ion: {al.element}³⁺, coordination = {al.coordination_number}")
    print(f"Ligand: {water.name}, lone pairs = {water.lone_pairs}")
