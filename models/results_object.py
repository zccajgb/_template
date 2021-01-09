from calculators.insertion import Insertion
from calculators.proteoglycan import Proteoglycan
from calculators.receptor import Receptor
from calculators.base_virus import BaseVirus


class ResultsObject:
    def __init__(self, x):
        self.example = x.example