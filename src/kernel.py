from pathlib import Path
from typing import Sequence, Tuple

import matplotlib.pyplot as plt
import pandas as pd


def collect_csvs_from_directory(tgt_dir: str) -> Sequence[str]:
    path_obj = Path(tgt_dir)
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


def main(tgt_dir: str, figsize: Tuple[float]):
    csvs = collect_csvs_from_directory(tgt_dir)
    fig, ax = initialize_figure(figsize)
    plot_data(csvs, ax)
    set_axes(ax)
    plt.show()


if __name__ == '__main__':
    tgt_dir = 'D:\\my-analysis\\komatsu-xm25\\test\\tie_small_contact_lids_housing'
    figsize = (4.8, 2.4)
    main(tgt_dir, figsize)
