import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import Dict


def open_dir(stringvar: tk.StringVar):
    dir_name = filedialog.askopenfilename(title='Choose the directory')
    stringvar.set(dir_name)


def clear_treeview(treeview: ttk.Treeview):
    for item in treeview.get_children():
        treeview.delete(item)


def insert_fieldnames(treeview: ttk.Treeview, csv_data: csv.DictReader):
    treeview['columns'] = csv_data.fieldnames
    for fieldname in csv_data.fieldnames:
        treeview.heading(fieldname, text=fieldname, anchor=tk.W)


def insert_values(treeview: ttk.Treeview, csv_data: csv.DictReader):
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
            lengths[fieldname].append(len(value))

    for fieldname in treeview['columns']:
        width = COLUMN_WIDTH_RATIO * max(lengths[fieldname])
        treeview.column(
            fieldname,
            anchor=tk.W,
            width=width,
            stretch=0,
        )


def read_csv(treeview: ttk.Treeview, stringvar: tk.StringVar):
    with open(stringvar.get(), 'r') as f:
        csv_data = csv.DictReader(f)
        insert_fieldnames(treeview, csv_data)
        insert_values(treeview, csv_data)
        adjust_column_width(treeview)
        

def draw():
    ...
