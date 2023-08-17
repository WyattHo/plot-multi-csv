import os

import matplotlib.pyplot as plt
import pandas as pd


# assign directory
csv_directory = 'D:\\my-analysis\\kubota-package-7-module\\data\\output\\freq_1_200\\modal_linear_50'
csv_names = os.listdir(csv_directory)


# initial the figure
fig = plt.figure(figsize=(4.8, 2.4), tight_layout=True)
ax = plt.axes()


# plot data
labels = ['excite-x', 'excite-y', 'excite-z']
for label_idx, name in enumerate(csv_names):
    path = os.path.join(csv_directory, name)
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
