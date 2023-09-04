import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import Sequence


def insert_values(treeview: ttk.Treeview, data: Sequence):
    for row_idx, row_data in enumerate(data):
        values = [row_idx, row_data]
        treeview.insert(
            parent='',
            index=row_idx,
            values=values,
            tags=str(row_idx)
        )


def open_files(treeview: ttk.Treeview):
    filenames = filedialog.askopenfilenames(
        title='Choose csv files',
        filetypes=[('csv files', '*.csv')]
    )
    insert_values(treeview, filenames)
    adjust_column_width(treeview)


def clear_treeview(treeview: ttk.Treeview):
    for item in treeview.get_children():
        treeview.delete(item)


def insert_fieldnames(treeview: ttk.Treeview, csv_data: csv.DictReader):
    treeview['columns'] = csv_data.fieldnames
    for fieldname in csv_data.fieldnames:
        treeview.heading(fieldname, text=fieldname, anchor=tk.W)


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


def read_csv(treeview_data: ttk.Treeview, treeview_filenames: ttk.Treeview):
    for line in treeview_filenames.get_children():
        path = treeview_filenames.item(line)['values'][-1]
        with open(path, 'r') as f:
            csv_data = csv.DictReader(f)
            insert_fieldnames(treeview_data, csv_data)
            insert_csv_values(treeview_data, csv_data)
            adjust_column_width(treeview_data)


def draw():
    ...
