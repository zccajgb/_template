import typing
import numpy as np


class SimulationData:

    def constuctor(self, receptor_types: str, example_int_min, example_int_max, example_int_step,
                   example_float_min, example_float_max, example_float_step):
        self.receptor_types = receptor_types
        self.example_int_min = example_int_min
        self.example_int_max = example_int_max
        self.example_int_step = example_int_step
        self.example_float_min = example_float_min
        self.example_float_max = example_float_max
        self.example_float_step = example_float_step


    def set_id(self, id_):
        self.id = id_

    def load_from_yml(self, yml):
        self.receptor_types = yml['receptor_types']
        self.example_int_min = int(yml['example_int']['min'])
        self.example_int_max = int(yml['example_int']['max'])
        self.example_int_step = int(yml['example_int']['step'])
        self.example_float_min = float(yml['example_float']['min'])
        self.example_float_max = float(yml['example_float']['max'])
        self.example_float_step = int(yml['example_float']['step'])
        self.create_linspaces()

    def create_linspaces(self):
        self.example_int = [round(x) for x in np.linspace(self.example_int_min, self.example_int_max, self.example_int_step)]
        self.example_float = np.linspace(self.example_float_min, self.example_float_max, self.example_float_step)
