import os

import matplotlib.pyplot as plt
import pandas as pd


this_dir = os.path.dirname(__file__)
csv_directory = os.path.join(this_dir, os.pardir, 'data\\output')
csv_names = os.listdir(csv_directory)

fig_subtitles = ['Contact', 'Tie', 'Tie_Screw']
labels = ['excite-x', 'excite-y', 'excite-z']
csv_prenames =[
    'xm25_hks_frf_maximum_stress_subcase',
    'xm25_hks_frf_tie_maximum_stress_subcase',
    'xm25_hks_frf_tie_small_maximum_stress_subcase'
]


csv_name_init, fig_idx, label_idx = 'init', 0, 0
for name in csv_names:
    if label_idx == 0:
        fig = plt.figure(figsize=(4.8, 2.4), tight_layout=True)
        ax = plt.axes()

    path = os.path.join(csv_directory, name)
    df = pd.read_csv(path)
    ax.plot(df['frequency'], df['max_stress'], label=labels[label_idx])

    if label_idx == 2:
        subtitle = fig_subtitles[fig_idx]
        ax.set_title(f'Maximum Stress Distribution - {subtitle}')
        ax.set_ylabel('Stress, MPa')
        ax.set_xlabel('Frequency, Hz')
        ax.set_xlim([0, 200])
        ax.grid(visible=True, axis='both')
        ax.legend()
        plt.show()
        label_idx = 0
        fig_idx += 1
    else:
        label_idx += 1
