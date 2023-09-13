import json
from pathlib import Path
from typing import Sequence, Tuple, Dict

import matplotlib.pyplot as plt
import pandas as pd


def read_configurations(config_name: str):
    parent = Path(__file__).parent
    config_path = parent.joinpath(config_name)
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def get_data_pool(config: Dict) -> Sequence[pd.DataFrame]:
    data_dir = config['data']['directory']
    csvs = list(Path(data_dir).glob('*.csv'))
    return [pd.read_csv(path) for path in csvs]


def initialize_figure(config: Dict) -> Tuple[plt.Figure, plt.Axes]:
    figsize = config['figure']['size']
    fig = plt.figure(figsize=figsize, tight_layout=True)
    ax = plt.axes()
    return fig, ax


def get_plot_function(config: Dict, ax: plt.Axes):
    scale_x = config['axis_x']['scale']
    scale_y = config['axis_y']['scale']
    if scale_x == 'linear' and scale_y == 'linear':
        plot_function = ax.plot
    elif scale_x == 'log' and scale_y == 'linear':
        plot_function = ax.semilogx
    elif scale_x == 'linear' and scale_y == 'log':
        plot_function = ax.semilogy
    elif scale_x == 'log' and scale_y == 'log':
        plot_function = ax.loglog
    return plot_function


def plot_data(
        config: Dict, data_pool: Sequence[pd.DataFrame],
        plot_function):

    fieldnames = config['data']['fieldnames']
    labels = config['data']['labels']
    for df, fieldname, label in zip(data_pool, fieldnames, labels):
        values_x = df[fieldname['x']]
        values_y = df[fieldname['y']]
        plot_function(values_x, values_y, label=label)


def set_axes(config: Dict, ax: plt.Axes):
    ax.set_title(config['figure'].get('title', ''))
    ax.set_xlabel(config['axis_x'].get('label', ''))
    ax.set_xlim(config['axis_x'].get('lim', ''))
    ax.set_ylabel(config['axis_y'].get('label', ''))
    ax.set_ylim(config['axis_y'].get('lim', ''))
    ax.grid(
        visible=config['figure'].get('grid_visible', ''),
        axis='both'
    )
    if config['figure']['legend_visible']:
        ax.legend()


def main(config_name: str = 'config.json'):
    config = read_configurations(config_name)
    data_pool = get_data_pool(config)
    fig, ax = initialize_figure(config)
    plot_function = get_plot_function(config, ax)
    plot_data(config, data_pool, plot_function)
    set_axes(config, ax)
    plt.show()


if __name__ == '__main__':
    main()
