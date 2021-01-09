import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, interp1d
from matplotlib.ticker import ScalarFormatter, MaxNLocator
from helpers.data_helper import load_calcs
from helpers.plotter_helper import *



def plot_example(ax, df_example):
    df_example['Chain Length'] = df_example['Chain Length'] * 1e9
    df_example['Chain Length'] = df_example['Chain Length'].round(0)

    # palette = color_pallete("GnYlRd")
    palette = color_pallete("YlRd")
    # palette = color_pallete("BuGn")
    alpha = 0.2

    df2 = df_example.loc[df_example['Chain Length'] == 13]
    c = next(palette)
    plot(df2, "Number Of Hs Chains", "Insertive Repulsion", ylabel="Repulsive Energy", ax=ax, color=c)
    y0 = df2['Insertive Repulsion']
    ax.fill_between(df2["Number Of Hs Chains"], y0, color=c, alpha=alpha)

    df2 = df_example.loc[df_example['Chain Length'] == 24]
    c = next(palette)
    plot(df2, "Number Of Hs Chains", "Insertive Repulsion", ylabel="Repulsive Energy", ax=ax, color=c)
    y1 = df2['Insertive Repulsion']
    ax.fill_between(df2["Number Of Hs Chains"], y0, y1, color=c, alpha=alpha)
    y0 = df2['Insertive Repulsion']

    ax.legend([f"Chain Length = {x} nm" for x in range(10,60,10)])


if __name__ == "__main__":
    path_2 = os.getcwd() + '//..//output//temp//'
    df_example = load_calcs(path_2 + "df_example")
