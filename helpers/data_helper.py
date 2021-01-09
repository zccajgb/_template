import collections
import json
import os
from typing import List
from shutil import copyfile
import pandas as pd
import yaml
import logging
logging.basicConfig(level=logging.INFO)

from models.simulation_data import SimulationData

def load_calcs(path):
    df = pd.read_feather(path + '//dataframe.feather')
    return df

def load_calcs_without_results(path):
    with open(path + '//selectivity.yml') as file:
        selectivity = yaml.load(file, Loader=Loader)
    with open(path + '//simulation_data.yml') as file:
        simulation_input = yaml.load(file, Loader=yaml.FullLoader)
    simulation_data = SimulationData()
    simulation_data.load_from_yml(simulation_input)

    return selectivity, simulation_data

def save_data(df, simulation_data, temp_data: bool):
    cwd = os.getcwd()
    output_path = f'{cwd}//output'
    if temp_data:
        output_path = output_path + "//temp"

    id_ = create_id(output_path)
    simulation_data.set_id(id_)
    try:
        calc_path = f'{output_path}//{id_}'
        os.mkdir(calc_path)
    except:
        id_int = int(id_) + 1
        id_ = f"{id_int:06d}"
        simulation_data.set_id(id_)
    logging.info(f"Persisting data, path: {calc_path}")
    copy_input(calc_path, cwd)
    dump_simulation_data(calc_path, cwd)
    # write_to_csv(output_path, simulation_data)
    dump_dataframe(df, calc_path)

    if not temp_data:
        copy_init_file(calc_path, cwd)
        copy_plot_file(calc_path, cwd)
    return calc_path, df

def dump_dataframe(df, calc_path):
    df = df.reset_index()
    df.to_feather(f"{calc_path}//dataframe.feather")

def copy_init_file(calc_path, cwd):
    copyfile(f"{cwd}//__init__.py", f"{calc_path}//__init__.py")

def copy_input(calc_path, cwd):
    copyfile(f"{cwd}//input.yml", f"{calc_path}//input.yml")

def copy_plot_file(calc_path, cwd):
    copyfile(f"{cwd}//plot.py", f"{calc_path}//plot.py")


def create_id(output_path):
    if os.path.exists(output_path + '//output.csv'):
        with open(output_path + '//output.csv') as f:
            line = f.readlines()[-1]
        id_int = int(line.partition(",")[0]) + 1
    else:
        create_csv(output_path)
        id_int = 1
    id_ = f"{id_int:06d}"
    return id_

def create_csv(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    with open(output_path+"//output.csv", "a+") as f:
        raise Exception("Not Implemented")
        f.write("id, receptor_types, min_number_of_receptors, max_number_of_receptors, nr_step, min_receptor_kd, max_receptor_kd,  receptor_kd_step, min_hs_kd, max_hs_kd, hs_kd_step,  min_number_of_binding_sites_per_chain, max_number_of_binding_sites_per_chain,  nbsc_step,  min_number_of_chains_per_receptor, max_number_of_chains_per_receptor, ncr_step,  min_mean_binding_distance, max_mean_binding_distance, mbd_step, min_receptor_khun_length, max_receptor_khun_length, rkl_step, min_number_of_units_per_branch, max_number_of_units_per_branch, nub_step, min_receptor_tether_length, max_receptor_tether_length, rtl_step, other")

def dump_simulation_data(calc_path, cwd):
    copyfile(f"{cwd}//simulation_data.yml", f"{calc_path}//simulation_data.yml")


def dump_results(calc_path, results, selectivity):
    r_path = f'{calc_path}/results.yml'
    s_path = f'{calc_path}/selectivity.yml'
    with open(r_path, 'w') as f:
        yaml.dump(results, f)
    with open(s_path, 'w') as f:
        yaml.dump(selectivity, f)


def dump_list(calc_path, obj_list):
    var_name = get_name(obj_list)
    obj_list = flatten(obj_list)
    virus_path = f'{calc_path}/{var_name}'
    os.mkdir(virus_path)
    i = 0
    for v in obj_list:
        v_path = f'{virus_path}/{var_name}{i}.yml'
        with open(v_path, 'w') as f:
            yaml.dump(v, f)
        i = i + 1


def flatten(li):
    for el in li:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def get_name(li):
    while isinstance(li, collections.Iterable) and not isinstance(li, (str, bytes)):
        li = li[0]
    return type(li).__name__
