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


def collect_csvs_from_directory(data_dir: str) -> Sequence[str]:
    csvs = list(Path(data_dir).glob('*.csv'))
    return csvs


def initialize_figure(figsize: Sequence[float]) -> Tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=figsize, tight_layout=True)
    ax = plt.axes()
    return fig, ax


def plot_data(
        ax: plt.Axes, csvs: Sequence[str], labels: Sequence[str],
        fieldnames: Sequence[Dict[str, str]]):
    for csv, fieldname, label in zip(csvs, fieldnames, labels):
        df = pd.read_csv(csv)
        values_x = df[fieldname['x']]
        values_y = df[fieldname['y']]
        ax.semilogx(values_x, values_y, label=label)


def set_axes(ax: plt.Axes, misc_config: Dict):
    ax.set_title(misc_config.get('title', ''))
    ax.set_xlabel(misc_config.get('xlabel', ''))
    ax.set_ylabel(misc_config.get('ylabel', ''))
    ax.set_xlim(misc_config.get('xlim'))
    ax.set_ylim(misc_config.get('ylim'))
    ax.grid(visible=misc_config.get('grid_visible'), axis='both')
    if misc_config['legend_visible']:
        ax.legend()


def main(config_name: str = 'config.json'):
    config = read_configurations(config_name)
    data_dir = config['plot']['data_dir']
    figsize = config['plot']['figsize']
    labels = config['plot']['labels']
    fieldnames = config['plot']['fieldnames']
    misc_config = config['plot']['misc']

    csvs = collect_csvs_from_directory(data_dir)
    fig, ax = initialize_figure(figsize)
    plot_data(ax, csvs, labels, fieldnames)
    set_axes(ax, misc_config)
    plt.show()


if __name__ == '__main__':
    main()
