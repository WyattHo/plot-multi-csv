import tkinter as tk
from tkinter import ttk
from typing import Sequence, Union, Dict

import pandas as pd


class TreeviewTools:
    '''
    tool should be inherit from tk object and expand the functionality
    '''
    def create_treeview(
            frame: Union[tk.Frame, ttk.Frame],
            columns: Sequence[str], height: int) -> ttk.Treeview:

        scrollbar_ver = tk.Scrollbar(frame)
        scrollbar_ver.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_hor = tk.Scrollbar(frame, orient='horizontal')
        scrollbar_hor.pack(side=tk.BOTTOM, fill=tk.X)

        treeview = ttk.Treeview(
            frame,
            yscrollcommand=scrollbar_ver.set,
            xscrollcommand=scrollbar_hor.set,
            height=height
        )

        treeview.pack(fill='both')
        treeview.propagate(0)
        scrollbar_ver.config(command=treeview.yview)
        scrollbar_hor.config(command=treeview.xview)

        treeview['columns'] = columns
        treeview['show'] = 'headings'

        for column in columns:
            treeview.heading(column, text=column, anchor=tk.W)
        return treeview

    def clear_treeview(treeview: ttk.Treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def insert_csv_names(treeview: ttk.Treeview, csv_names: Sequence):
        for idx, csv_name in enumerate(csv_names):
            values = [idx + 1, csv_name]
            treeview.insert(
                parent='',
                index=idx,
                values=values,
                tags=str(idx)
            )

    def insert_csv_data(treeview: ttk.Treeview, df: pd.DataFrame):
        for row_idx, row in df.iterrows():
            treeview.insert(
                parent='',
                index=row_idx,
                values=list(row.values),
                tags=str(row_idx)
            )

    def adjust_column_width(treeview: ttk.Treeview):
        COLUMN_WIDTH_RATIO = 9
        lengths = {
            column: [len(column), ] for column in treeview['columns']
        }
        for line in treeview.get_children():
            columns = treeview['columns']
            values = treeview.item(line)['values']
            for column, value in zip(columns, values):
                lengths[column].append(len(str(value)))

        for column in treeview['columns']:
            width = COLUMN_WIDTH_RATIO * max(lengths[column])
            treeview.column(
                column,
                anchor=tk.W,
                width=width,
                stretch=0,
            )


class NotebookTools:
    '''
    tool should be inherit from tk object and expand the functionality
    '''
    def create_new_tab(notebook: ttk.Notebook, tabname: str) -> ttk.Frame:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tabname)
        return tab

    def remove_tabs(notebook: ttk.Notebook):
        while notebook.index('end') > 0:
            notebook.forget(0)

    def fill_curve_setting_widgets(tab: ttk.Frame, pads: Dict[str, float]):
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

    def initialize_notebook_for_curve_settings(
            notebook: ttk.Notebook, pads: Dict[str, float]):
        NotebookTools.remove_tabs(notebook)
        tab = NotebookTools.create_new_tab(notebook, tabname='1')
        NotebookTools.fill_curve_setting_widgets(tab, pads)
