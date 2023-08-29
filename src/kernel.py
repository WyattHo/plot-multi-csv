import json
from pathlib import Path
from typing import Sequence, Tuple

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


def plot_data(csvs: Sequence[str], ax: plt.Axes) -> plt.Axes:
    labels = ['excite-x', 'excite-y', 'excite-z']
    for label_idx, csv in enumerate(csvs):
        path = str(csv)
        df = pd.read_csv(path)
        ax.semilogx(df['frequency'], df['max_stress'], label=labels[label_idx])


def set_axes(ax: plt.Axes):
    ax.set_title(f'Maximum Stress Distribution')
    ax.set_ylabel('Stress, MPa')
    ax.set_xlabel('Frequency, Hz')
    ax.set_xlim([10, 200])
    ax.grid(visible=True, axis='both')
    ax.legend()


def main(config_name: str = 'config.json'):
    config = read_configurations(config_name)
    data_dir = config['plot']['data_dir']
    figsize = config['plot']['figsize']

    csvs = collect_csvs_from_directory(data_dir)
    fig, ax = initialize_figure(figsize)
    plot_data(csvs, ax)
    set_axes(ax)
    plt.show()


if __name__ == '__main__':
    main()
