import scipy.constants as spc
def joules_to_kT(E):
    return E / (spc.k * 310.2)

def meV_to_kT(E):
    return E / 25

def kcal_mol_to_kT(E):
    return E / 20.6

def kJ_mol_to_kT(E):
    return E / 2.5

def pNnm_to_kT(E):
    return E / 2.5


if __name__ == "__main__":
    r = joules_to_kT(3.7e-13)
    print(r)
