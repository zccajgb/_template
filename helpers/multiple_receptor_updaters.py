from models.multi_receptors_data import MultipleReceptorsData 
from copy import deepcopy

def tmprss_number_of_receptors_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.receptors_data.tmprss2.number_of_receptors = x
    return data

def nhs_updater(cdata, x):
    data = deepcopy(cdata)
    data.proteoglycan_data.number_of_proteoglycan_chains = x
    return data
def number_of_binding_sites_per_chain_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.proteoglycan_data.number_of_binding_sites_per_chain = int(x)
    return data
def fraction_binding_sites_per_chain_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    sites = int(x * data.proteoglycan_data.number_of_units_per_chain)
    data.proteoglycan_data.binding_fraction = x
    data.proteoglycan_data.number_of_binding_sites_per_chain = sites if sites > 0 else 1
    return data
def number_units_per_chain_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    chain_length = x
    units = round(chain_length ** 2 / data.insertion_data.kuhn_length ** 2)
    data.proteoglycan_data.number_of_units_per_chain = units if units > 0 else 1
    return data
def hs_be_updater(cdata, x):
    data = deepcopy(cdata)
    data.proteoglycan_data.binding_energy = x
    return data
def ace2_be_updater(cdata, x):
    data = deepcopy(cdata)
    data.receptors_data.ace2.binding_energy = x
    return data
def tmprss2_be_updater(cdata, x):
    data = deepcopy(cdata)
    data.receptors_data.tmprss2.binding_energy = x
    return data
def radius_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.virus_data.radius = x
    return data
def conc_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.virus_data.virus_concentration = x
    return data
def bs_nuc_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.proteoglycan_data.number_of_units_per_chain = x
    data.proteoglycan_data.number_of_binding_sites_per_chain = round(x/2)
    return data
def tether_length_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.insertion_data.receptor_tether_length = x
    return data
def number_spikes_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.virus_data.number_of_spikes = x
    return data
def hs_kuhn_length_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.insertion_data.kuhn_length = x
    return data
def ace2_mean_binding_distance_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.receptors_data.ace2.mean_binding_distance = x
    return data
def glycan_kuhn_length_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.receptors_data.ace2.kuhn_length = x
    return data
def branch_length_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.receptor_data.ace2.branch_length = x
    return data
def number_branches_updater(cdata: MultipleReceptorsData, x):
    data = deepcopy(cdata)
    data.receptor_data.ace2.number_of_branches = x
    return data




