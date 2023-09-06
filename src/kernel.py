import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import Sequence


def insert_values(treeview: ttk.Treeview, data: Sequence):
    for row_idx, row_data in enumerate(data):
        values = [row_idx + 1, row_data]
        treeview.insert(
            parent='',
            index=row_idx,
            values=values,
            tags=str(row_idx)
        )


def open_files(treeview: ttk.Treeview):
    clear_treeview(treeview)
    filenames = filedialog.askopenfilenames(
        title='Choose csv files',
        filetypes=[('csv files', '*.csv')]
    )
    insert_values(treeview, filenames)
    adjust_column_width(treeview)


def clear_treeview(treeview: ttk.Treeview):
    for item in treeview.get_children():
        treeview.delete(item)


def insert_csv_values(treeview: ttk.Treeview, csv_data: csv.DictReader):
    for row_idx, row_data in enumerate(csv_data):
        values = [
            row_data[fieldName].strip() for fieldName in csv_data.fieldnames
        ]
        treeview.insert(
            parent='',
            index=row_idx,
            values=values,
            tags=str(row_idx)
        )


def adjust_column_width(treeview: ttk.Treeview):
    COLUMN_WIDTH_RATIO = 9
    lengths = {
        fieldname: [len(fieldname), ] for fieldname in treeview['columns']
    }
    for line in treeview.get_children():
        fieldnames = treeview['columns']
        values = treeview.item(line)['values']
        for fieldname, value in zip(fieldnames, values):
            lengths[fieldname].append(len(str(value)))

    for fieldname in treeview['columns']:
        width = COLUMN_WIDTH_RATIO * max(lengths[fieldname])
        treeview.column(
            fieldname,
            anchor=tk.W,
            width=width,
            stretch=0,
        )


def create_tab(
        notebook: ttk.Notebook,
        tabname: str) -> Sequence[ttk.Frame]:
    
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=tabname)
    return tab


def create_treeview(
        frame: tk.Frame | ttk.Frame,
        columns: Sequence[str]) -> ttk.Treeview:

    scrollbar_ver = tk.Scrollbar(frame)
    scrollbar_ver.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_hor = tk.Scrollbar(frame, orient='horizontal')
    scrollbar_hor.pack(side=tk.BOTTOM, fill=tk.X)

    treeview = ttk.Treeview(
        frame,
        yscrollcommand=scrollbar_ver.set,
        xscrollcommand=scrollbar_hor.set,
        height=15
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


def clear_tabs(notebook: ttk.Notebook):
    while notebook.index('end') > 0:
        notebook.forget(0)


def initial_tabs(notebook: ttk.Notebook) :
    clear_tabs(notebook)
    tab = create_tab(notebook, tabname='1')
    create_treeview(tab, columns=('',))


def import_csv(treeview_filenames: ttk.Treeview, notebook: ttk.Notebook):
    clear_tabs(notebook)
    for line in treeview_filenames.get_children():
        tab_id, path = treeview_filenames.item(line)['values']
        tab = create_tab(notebook, tab_id)
        with open(path, 'r') as f:
            csv_data = csv.DictReader(f)
            treeview_data = create_treeview(tab, csv_data.fieldnames)
            insert_csv_values(treeview_data, csv_data)
            adjust_column_width(treeview_data)


def draw():
    ...
