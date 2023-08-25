from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# assign directory
directory = Path('D:\\my-analysis\\komatsu-xm25\\test\\tie_small_contact_lids_housing')
csvs = list(directory.glob('*.csv'))


# initial the figure
fig = plt.figure(figsize=(4.8, 2.4), tight_layout=True)
ax = plt.axes()


# plot data
labels = ['excite-x', 'excite-y', 'excite-z']
for label_idx, csv in enumerate(csvs):
    path = str(csv)
    df = pd.read_csv(path)
    ax.semilogx(df['frequency'], df['max_stress'], label=labels[label_idx])


# figure settings
ax.set_title(f'Maximum Stress Distribution')
ax.set_ylabel('Stress, MPa')
ax.set_xlabel('Frequency, Hz')
ax.set_xlim([10, 200])
ax.grid(visible=True, axis='both')
ax.legend()
plt.show()
