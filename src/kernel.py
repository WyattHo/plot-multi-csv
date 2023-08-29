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
    path_obj = Path(data_dir)
    csvs = list(path_obj.glob('*.csv'))
    return csvs


def initialize_figure(figsize: Sequence[float]) -> Tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=figsize, tight_layout=True)
    ax = plt.axes()
    return fig, ax


def plot_data(ax: plt.Axes, csvs: Sequence[str], labels: Sequence[str]):
    for csv, label in zip(csvs, labels):
        path = str(csv)
        df = pd.read_csv(path)
        ax.semilogx(df['frequency'], df['max_stress'], label=label)


def set_axes(ax: plt.Axes, misc_config: Dict):
    if misc_config['title']:
        ax.set_title(misc_config['title'])
    if misc_config['xlabel']:
        ax.set_xlabel(misc_config['xlabel'])
    if misc_config['ylabel']:
        ax.set_ylabel(misc_config['ylabel'])
    if misc_config['xlim']:
        ax.set_xlim(misc_config['xlim'])
    if misc_config['ylim']:
        ax.set_ylim(misc_config['ylim'])
    if misc_config['grid_visible']:
        ax.grid(visible=True, axis='both')
    if misc_config['legend_visible']:
        ax.legend()


def main(config_name: str = 'config.json'):
    config = read_configurations(config_name)
    DATA_DIR = config['plot']['data_dir']
    FIG_SIZE = config['plot']['figsize']
    LABELS = config['plot']['labels']
    misc_config = config['plot']['misc']

    csvs = collect_csvs_from_directory(DATA_DIR)
    fig, ax = initialize_figure(FIG_SIZE)
    plot_data(ax, csvs, LABELS)
    set_axes(ax, misc_config)
    plt.show()


if __name__ == '__main__':
    main()
