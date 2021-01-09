import time

from helpers.data_helper import save_data
from models.multi_receptors_data import MultipleReceptorsData
from models.multiple_receptors_simulation_data import MultipleReceptorsSimulationData
from plot import plot
from helpers.updaters import *
# from helpers.multiple_receptor_updaters import *
# from helpers.multiple_receptor_results_helper import *
from helpers.results_helper import *
from master.master import load_data, load_multiple_receptor_data
from functools import partial
from models.combined_data import CombinedData
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    start = time.time()
    virus_data, receptors_data, proteoglycan_data, insertion_data, binding_data, simulation_data = load_data()
    data = CombinedData(binding_data, insertion_data, proteoglycan_data, receptors_data, virus_data)

    ace2_func = partial(multithreaded_receptor_loop, simulation_data.number_of_receptors)
    # tmprss2_func = multithread_loop_creator(ace2_func, tmprss_number_of_receptors_updater, simulation_data.number_of_tmprss2)
    # t_be_func = multithread_loop_creator(tmprss2_func, tmprss2_be_updater, simulation_data.tmprss2_be)
    # a_be_func = multithread_loop_creator(t_be_func, ace2_be_updater, simulation_data.ace2_be)
    # radius_func = multithread_loop_creator(ace2_func, radius_updater, simulation_data.radius)
    # conc_func = multithread_outer_loop_creator(ace2_func, conc_updater, simulation_data.concentration)
    # number_of_spikes_func = multithread_loop_creator(r_func, number_spikes_updater, simulation_data.number_of_spikes)
    # hs_be_func = multithread_loop_creator(ace2_func, hs_be_updater, simulation_data.hs_be)
    simulation_data.fraction_binding_sites_per_chain = [i*0.1 for i in range(1,11)]
    fraction_binding_sites_per_chain_func = multithread_loop_creator(ace2_func, fraction_binding_sites_per_chain_updater, simulation_data.fraction_binding_sites_per_chain)
    number_of_units_per_chain_func = multithread_loop_creator(ace2_func, number_units_per_chain_updater, simulation_data.chain_length)
    # hs_kuhn_length_func = multithread_loop_creator(number_of_units_per_chain_func, hs_kuhn_length_updater, simulation_data.hs_kuhn_length)
    # mean_binding_distance_func = multithread_loop_creator(hs_kuhn_length_func, mean_binding_distance_updater, simulation_data.mean_binding_distance)
    # branch_length_func = multithread_loop_creator(mean_binding_distance_func, branch_length_updater, simulation_data.branch_length)
    # number_of_branches_func = multithread_loop_creator(branch_length_func, number_branches_updater, simulation_data.number_of_branches)
    # r_be_func = multithread_loop_creator(number_of_branches_func, r_be_updater, simulation_data.receptor_be)
    # receptor_tether_length_func = multithread_loop_creator(r_be_func, tether_length_updater, simulation_data.receptor_tether_length)
    nhs_func = multithread_outer_loop_creator(number_of_units_per_chain_func, nhs_updater, simulation_data.number_of_hs_chains)

    df = nhs_func(data)
    end = time.time()
    logging.info(f"Time taken: {end - start}")
    temp_data = True
    df.columns = df.columns.str.replace("_", " ").str.title()

    path, df = save_data(df, simulation_data, temp_data)
    # plot(df, path)

