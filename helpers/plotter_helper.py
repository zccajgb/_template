import logging
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import yaml
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata, make_interp_spline

plt.style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 2

def _row_and_column_label(gs, rows, cols):
    for i, col in zip(range(len(cols)), cols):
        ax = plt.subplot(gs[0:1, i:i + 1])
        ax.annotate(col, xy=(0.5, 1), xytext=(0, 5), xycoords='axes fraction', textcoords='offset points', size='x-large', ha='center', va='baseline')
    for i, row in zip(range(len(rows)), rows):
        ax = plt.subplot(gs[i:i + 1, 0:1])
        ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad, 0), xycoords=ax.yaxis.label, textcoords='offset points', size='x-large', ha='right', va='center')

def _smooth_data(x, y, smooth):
    x = np.linspace(min(x), max(x), len(x))
    xn = np.linspace(min(x), max(x), 300)
    spl = make_interp_spline(x, y.tolist(), k=smooth)
    yn = spl(xn)
    return yn, xn

def plot(df, xl, yl="Surface Coverage", ax=None, color_int=None, xlabel=None, ylabel=None, linestyle='-', smooth=0, color=None, log=False, scatter=False):
    if ax is None:
        fig, ax = plt.subplots()
    if color_int is None and color is None:
        color = list(iter(plt.rcParams['axes.prop_cycle']))[0]['color']
    if color is None:
        color = list(iter(plt.rcParams['axes.prop_cycle']))[color_int]['color']

    y = df[yl]
    if xl == None:
        x = range(len(y))
    else:
        x = df[xl]

    if smooth > 0:
        y,x = _smooth_data(x, y, smooth)
    if log:
        ax.semilogx(x, y, color=color, linestyle=linestyle)
    elif scatter:
        ax.scatter(x, y, color=color)
    else:
        ax.plot(x, y, color=color, linestyle=linestyle)
    if xlabel is None:
        xlabel = xl
    if ylabel is None:
        ylabel = yl
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    return ax


def generate_cmap(string):
    if string == "BuGnYlRd":
        cmap = LinearSegmentedColormap.from_list('custom', ['#008fd5', '#6d904f', '#e5ae38', '#fc4f30'], N=256)
    if string == "BuGnYl":
        cmap = LinearSegmentedColormap.from_list('custom', ['#008fd5', '#6d904f', '#e5ae38'], N=256)
    if string == "GnYlRd":
        cmap = LinearSegmentedColormap.from_list('custom', ['#6d904f', '#e5ae38', '#fc4f30'], N=256)
    if string == "BuGn":
        cmap = LinearSegmentedColormap.from_list('custom', ['#008fd5', '#6d904f'], N=256)
    if string == "GnYl":
        cmap = LinearSegmentedColormap.from_list('custom', ['#6d904f', '#e5ae38'], N=256)
    if string == "YlRd":
        cmap = LinearSegmentedColormap.from_list('custom', ['#e5ae38', '#fc4f30'], N=256)
    return cmap


def contourplot(*, data: pd.DataFrame, x: str, y: str, hue: str, binary=False, title=None, ax=None, xlabel=None, ylabel=None, levels=None, customcmap=True, cmap='RdBu_r',
                cbar=True, v=None):
    if hue == "Total Energy" or x == "Total Energy" or y == "Total Energy":
        data = calculate_total_energy(data)

    _contourplot_guardclauses(data, hue, x, y)

    df = data[[x, y, hue]]
    df = df.drop_duplicates()
    y_length = len(df[y].unique())
    x_length = len(df[x].unique())
    Z = df[hue].values.reshape(y_length, x_length)
    if binary:
        Z = np.sign(Z)
        levels = [-1, 0, 1]

    ax, cmap = set_ax_properties(ax, cmap, customcmap, title, x, xlabel, y, ylabel)
    try:
        if v is None:
            cplot = ax.contourf(df[x].unique(), df[y].unique(), Z, levels=levels, cmap=cmap)
        else:
            cplot = ax.contourf(df[x].unique(), df[y].unique(), Z, levels=levels, cmap=cmap, vmin=v[0], vmax=v[1])
    except TypeError as e:
        print(f"Lenghts: df={len(df)}, x={len(df[x].unique())}, y={len(df[y].unique())}, z={len(Z)}")
        raise e

    if cbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        plt.colorbar(cplot, cax=cax)
    return cplot

def surfplot(*, data: pd.DataFrame, x: str, y: str, hue: str, title=None, ax=None, xlabel=None, ylabel=None, customcmap=True, cmap='RdBu_r', cbar=True, v=None):
    if hue == "Total Energy" or x == "Total Energy" or y == "Total Energy":
        data = calculate_total_energy(data)

    _contourplot_guardclauses(data, hue, x, y)

    df = data[[x, y, hue]]
    df = df.drop_duplicates()
    y_length = len(df[y].unique())
    x_length = len(df[x].unique())
    X, Y = np.meshgrid(df[x], df[y])
    Z = griddata((df[x], df[y]), df[hue], (X, Y), method='cubic')
    if v is not None:
        Z[Z < v[0]] = np.nan
        Z[Z > v[1]] = np.nan

    ax, cmap = set_ax_properties(ax, cmap, customcmap, title, x, xlabel, y, ylabel, zlabel=hue)
    try:
        if v is None:
            cplot = ax.plot_surface(X, Y, Z, cmap=cmap)
        else:
            cplot = ax.plot_surface(X, Y, Z, cmap=cmap, vmin=v[0], vmax=v[1])
            ax.set_zlim(v[0], v[1])

    except Exception as e:
        print(f"Lenghts: df={len(df)}, x={len(df[x].unique())}, y={len(df[y].unique())}, z={len(Z)}")
        raise e

    if cbar:
        plt.colorbar(cplot, shrink=0.5, aspect=5)
    return cplot

def color_pallete(name):
    GnYlRd = ['#6d904f', '#7f9849', '#939f43', '#aaa53d', '#c2aa39', '#d0a631', '#dea02c', '#ec9a2a', '#f18a25', '#f67925', '#f96529', '#fc4f30']
    BuGnYl = ['#008fd5', '#0096c7', '#0099ad', '#00998e', '#33976f', '#519960', '#6c9a52', '#859a47', '#9aa141', '#b1a63b', '#caab38', '#e5ae38']
    YlRd = ['#fc4f30', '#f86c27', '#f38524', '#ec9a2a', '#e5ae38']
    BuGn = ['#008fd5', '#0097bf', '#009999', '#33976f', '#6d904f']

    if name == 'GnYlRd':
        return (i for i in GnYlRd)
    if name == 'BuGnYl':
        return (i for i in BuGnYl)
    if name == 'BuGn':
        return (i for i in BuGn)
    if name == 'YlRd':
        return (i for i in YlRd)

def set_ax_properties(ax, cmap, customcmap, title, x, xlabel, y, ylabel, zlabel=None):
    if ax is None:
        fig, ax = plt.subplots()
    if title is not None:
        ax.set_title(title)
    if xlabel is None:
        xlabel = x
    if ylabel is None:
        ylabel = y
    if zlabel is not None:
        ax.set_zlabel(zlabel)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if customcmap:
        if cmap is None:
            cmap = "BuGnYlRd"
        cmap = generate_cmap(cmap)
    return ax, cmap


def contour_subplot_loop(df, gs, ns, cols, rows, x, y, hue, xlabel, ylabel, binary=True, cbar=False, v=None, cmap='RdYlGn_r', fig=None, log=False):
    cbar_in = True if cbar == "multi" else False
    for g, b in zip(gs, ns):
        df2 = df.loc[df[rows] == b[0]].loc[df[cols] == b[1]]
        if df2.empty:
            logging.error("df2 is empty")
            if df.loc[df[rows] == b[0]].empty:
                str_err = f"rows are empty: row = {rows}, value = {b[0]}"
                logging.error(f"Accepted Values: {df[cols].unique()}")
                logging.error(str_err)
                raise ValueError(str_err)
            elif df.loc[df[cols] == b[1]].empty:
                str_err = f"cols are empty: col = {cols}, value = {b[1]}"
                logging.error(str_err)
                logging.error(f"Accepted Values: {df[cols].unique()}")
                raise ValueError(str_err)
            else:
                str_err = "combination of values {b[0]} and {b[1]} is empty"
                logging.error(str_err)
                raise ValueError(str_err)

        ax = plt.subplot(g)
        cplot = contourplot(data=df2, x=x, y=y, hue=hue, ax=ax, binary=binary, ylabel=ylabel, xlabel=xlabel, cbar=cbar_in, v=v, cmap=cmap)
        if log:
            ax.set(xscale="log", yscale="log")

    if "single" in cbar:
        fig.subplots_adjust(right=0.9)
        cax = fig.add_axes([0.93, 0.07, 0.01, 0.8])
        cb = fig.colorbar(cplot, cax=cax)
        if binary:
            cb.set_ticks([-1, 1])
            cb.ax.set_yticklabels(["Attractive", "Repulsive"])
            if "sc" in cbar:
                cb.ax.set_yticklabels([0, 1])
        plt.subplots_adjust(left=0.13, wspace=0.3, hspace=0.3)


def _contourplot_guardclauses(data: pd.DataFrame, hue, x, y):
    if x not in data:
        raise KeyError(f"x: {x} is not a valid key")
    if y not in data:
        raise KeyError(f"y: {y} is not a valid key")
    if hue not in data:
        raise KeyError(f"Hue: {hue} is not a valid key")


def calculate_total_energy(df2):
    df2["Total Energy"] = df2["Hs Binding Energy"] + df2["Receptor Binding Energy"] + df2["Insertive Repulsion"]
    return df2


def show_or_save(fig, path=None, tight_layout=True):
    fig.set_size_inches(19, 9.5)
    if tight_layout:
        plt.tight_layout()
    if path is None:
        plt.show()
    else:
        plt.savefig(path, bbox_inches='tight')


def setup():
    with open('helpers//styles.yml') as file:
        styles = yaml.load(file, yaml.Loader)
    sns.set_theme(rc=styles)
