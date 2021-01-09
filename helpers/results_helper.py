import multiprocessing
import logging
from master.master import run
from models.results_object import ResultsObject
from functools import partial
import pandas as pd
import copy

def multithread_loop_creator(inner_func, updater, loop_list):
    return partial(multithreaded_loop, inner_func, updater, loop_list)

def multithread_outer_loop_creator(inner_func, updater, loop_list):
    return partial(multithreaded_outer_loop, inner_func, updater, loop_list)

def test_multithread_outer_loop_creator(inner_func, updater, loop_list):
    return partial(multithreaded_loop, inner_func, updater, loop_list)

def multithreaded_receptor_loop(NR, data):
    df2 = pd.DataFrame([])
    for n in NR:
        data.virus_data.number_of_receptors = [int(round(n))]
        try:
            v, i, p, r = run(data.virus_data, data.receptor_data, data.proteoglycan_data, data.insertion_data, data.binding_data)
            ro = ResultsObject(v, i, p, r)
            df2 = df2.append(vars(ro), ignore_index=True)
        except Exception as ex:
            logging.error(f"Exception raised for calculation: {data}")
            logging.error(f"Inner Exception: {ex}")
            raise ex
    # df2 = calculate_max_selectivity(df2)
    return df2

def multithreaded_loop(inner_function, data_updater, loop_list, data):
    df2 = pd.DataFrame([])
    for l in loop_list:
        try:
            data = data_updater(data, l)
        except Exception as e:
            logging.error(e)
            return df2
        df = inner_function(data)
        df2 = df2.append(df, ignore_index=True)
    return df2

def multithreaded_outer_loop(inner_function, data_updater, loop_list, data):
    check_side_effects(data, data_updater)
    updater2 = partial(data_updater, data)
    data_list = map(updater2, loop_list)
    pool = multiprocessing.Pool()
    res = pool.map(inner_function, data_list)
    pool.close()
    pool.join()
    df = pd.concat(res)
    return df

def check_side_effects(data, data_updater):
    orig = copy.deepcopy(data)
    _ = data_updater(data, 0)
    if orig != data:
        raise ValueError("Data updater has side effects, and modifies the data object. This will not work with multithreading")