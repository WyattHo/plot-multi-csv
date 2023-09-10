import tkinter as tk
from tkinter import ttk
from typing import Sequence, Union, Dict

import pandas as pd


class Treeview(ttk.Treeview):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame], columns: Sequence[str], height: int):
        self.create_scrollbar(frame)
        super().__init__(
            frame,
            yscrollcommand=self.scrollbar_ver.set,
            xscrollcommand=self.scrollbar_hor.set,
            height=height
        )
        self.config(columns)

    def create_scrollbar(self, frame):
        self.scrollbar_ver = tk.Scrollbar(frame)
        self.scrollbar_ver.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_hor = tk.Scrollbar(frame, orient='horizontal')
        self.scrollbar_hor.pack(side=tk.BOTTOM, fill=tk.X)

    def config(self, columns):
        self.pack(fill='both')
        self.propagate(0)
        self.scrollbar_ver.config(command=self.yview)
        self.scrollbar_hor.config(command=self.xview)

        self['columns'] = columns
        self['show'] = 'headings'

        for column in columns:
            self.heading(column, text=column, anchor=tk.W)

    def clear(self):
        for item in self.get_children():
            self.delete(item)

    def insert_csv_names(self, csv_names: Sequence):
        for idx, csv_name in enumerate(csv_names):
            values = [idx + 1, csv_name]
            self.insert(
                parent='',
                index=idx,
                values=values,
                tags=str(idx)
            )

    def insert_csv_data(self, df: pd.DataFrame):
        for row_idx, row in df.iterrows():
            self.insert(
                parent='',
                index=row_idx,
                values=list(row.values),
                tags=str(row_idx)
            )

    def collect_all_csv_data(self) -> Dict[int, pd.DataFrame]:
        csv_data_all = {}
        for line in self.get_children():
            df_idx, path = self.item(line)['values']
            csv_data_all[df_idx] = pd.read_csv(path)
        return csv_data_all

    def adjust_column_width(self):
        COLUMN_WIDTH_RATIO = 9
        lengths = {
            column: [len(column), ] for column in self['columns']
        }
        for line in self.get_children():
            columns = self['columns']
            values = self.item(line)['values']
            for column, value in zip(columns, values):
                lengths[column].append(len(str(value)))

        for column in self['columns']:
            width = COLUMN_WIDTH_RATIO * max(lengths[column])
            self.column(
                column,
                anchor=tk.W,
                width=width,
                stretch=0,
            )


class Notebook(ttk.Notebook):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame]):
        super().__init__(frame)

    def create_new_tab(self, tabname: str) -> ttk.Frame:
        tab = ttk.Frame(self)
        self.add(tab, text=tabname)
        return tab

    def remove_tabs(self):
        while self.index('end') > 0:
            self.forget(0)

    def fill_curve_setting_widgets(self, tab: ttk.Frame, pads: Dict[str, float]):
        label = tk.Label(tab, text='CSV ID: ')
        entry = ttk.Combobox(tab)
        label.grid(row=0, column=0, sticky=tk.W, **pads)
        entry.grid(row=0, column=1, sticky=tk.W, **pads)

        label = tk.Label(tab, text='Field X: ')
        entry = ttk.Combobox(tab)
        label.grid(row=1, column=0, sticky=tk.W, **pads)
        entry.grid(row=1, column=1, sticky=tk.W, **pads)

        label = tk.Label(tab, text='Field Y: ')
        entry = ttk.Combobox(tab)
        label.grid(row=2, column=0, sticky=tk.W, **pads)
        entry.grid(row=2, column=1, sticky=tk.W, **pads)

        label = tk.Label(tab, text='Label: ')
        entry = tk.Entry(tab)
        label.grid(row=3, column=0, sticky=tk.W, **pads)
        entry.grid(row=3, column=1, sticky=tk.W, **pads)

    def initialize_notebook_for_curve_settings(self, pads: Dict[str, float]):
        self.remove_tabs()
        tab = self.create_new_tab(tabname='1')
        self.fill_curve_setting_widgets(tab, pads)
