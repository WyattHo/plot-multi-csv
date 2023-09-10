import tkinter as tk
from tkinter import ttk
from typing import Sequence, Union, Dict

import pandas as pd


class Treeview(ttk.Treeview):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame], columns: Sequence[str], height: int):
        scrollbar_ver = tk.Scrollbar(frame)
        scrollbar_hor = tk.Scrollbar(frame, orient='horizontal')
        scrollbar_ver.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_hor.pack(side=tk.BOTTOM, fill=tk.X)
        super().__init__(
            frame,
            yscrollcommand=scrollbar_ver.set,
            xscrollcommand=scrollbar_hor.set,
            height=height
        )
        self.pack(fill='both')
        scrollbar_ver.config(command=self.yview)
        scrollbar_hor.config(command=self.xview)
        self['columns'] = columns
        self['show'] = 'headings'
        for column in columns:
            self.heading(column, text=column, anchor=tk.W)

    def clear_content(self):
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

    def insert_csv_dataframe(self, df: pd.DataFrame):
        for idx, row in df.iterrows():
            self.insert(
                parent='',
                index=idx,
                values=list(row.values),
                tags=str(idx)
            )

    def get_data(self) -> pd.DataFrame:
        columns = self['columns']
        data = {column: [] for column in columns}
        for line in self.get_children():
            values = self.item(line)['values']
            for column, value in zip(columns, values):
                data[column].append(value)
        return pd.DataFrame(data)

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


class Tab(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.widgets = {}


class Notebook(ttk.Notebook):
    def __init__(self, frame: Union[tk.Frame, ttk.Frame]):
        super().__init__(frame)
        self.tabs_ = {}

    def create_new_tab(self, tabname: str) -> Tab:
        tab = Tab(self)
        self.add(tab, text=tabname)
        self.tabs_[tabname] = tab
        return tab

    def remove_tabs(self):
        self.tabs_ = {}
        while self.index('end') > 0:
            self.forget(0)

    def fill_curve_setting_widgets(
            self, tab: Tab, 
            pads: Dict[str, float]) -> Dict[str, ttk.Combobox]:

        label = tk.Label(tab, text='CSV ID: ')
        entry = ttk.Combobox(tab)
        label.grid(row=0, column=0, sticky=tk.W, **pads)
        entry.grid(row=0, column=1, sticky=tk.W, **pads)
        combobox_csv_idx = entry

        label = tk.Label(tab, text='Field X: ')
        entry = ttk.Combobox(tab)
        label.grid(row=1, column=0, sticky=tk.W, **pads)
        entry.grid(row=1, column=1, sticky=tk.W, **pads)
        combobox_field_x = entry

        label = tk.Label(tab, text='Field Y: ')
        entry = ttk.Combobox(tab)
        label.grid(row=2, column=0, sticky=tk.W, **pads)
        entry.grid(row=2, column=1, sticky=tk.W, **pads)
        combobox_field_y = entry

        label = tk.Label(tab, text='Label: ')
        entry = tk.Entry(tab)
        label.grid(row=3, column=0, sticky=tk.W, **pads)
        entry.grid(row=3, column=1, sticky=tk.W, **pads)

        curve_settings_widgets = {
            'csv_idx': combobox_csv_idx,
            'field_x': combobox_field_x,
            'field_y': combobox_field_y
        }
        return curve_settings_widgets

    def initialize_notebook_for_curve_settings(self, pads: Dict[str, float]):
        TABNAME = '1'
        self.remove_tabs()
        tab = self.create_new_tab(tabname=TABNAME)
        widgets = self.fill_curve_setting_widgets(tab, pads)
        self.tabs_[TABNAME].widgets = widgets

    def fill_widget_options(self, tabname: str, csv_data_pool: Dict[str, pd.DataFrame]):
        values_csv_idx = list(csv_data_pool.keys())
        self.tabs_[tabname].widgets['csv_idx'].config(values=values_csv_idx)
        self.tabs_[tabname].widgets['csv_idx'].current(0)
