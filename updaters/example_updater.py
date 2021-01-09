from models.simulation_data import SimulationData
from copy import deepcopy

def example_updater(cdata, x):
    data = deepcopy(cdata)
    data.variable = x
    return data




