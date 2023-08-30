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


def analyze_best_fit_width(csv_data: csv.DictReader) -> Dict[str, int]:
    max_widths = {
        fieldname: len(fieldname) 
        for fieldname in csv_data.fieldnames
    }
    for row_data in csv_data:
        for fieldname in csv_data.fieldnames:
            data_width = len(row_data[fieldname])
            if data_width > max_widths[fieldname]:
                max_widths[fieldname] = data_width
    return max_widths


def adjust_field_width(treeview: ttk.Treeview, csv_data: csv.DictReader):
    max_widths = analyze_best_fit_width(csv_data)
    for fieldname in csv_data.fieldnames:
        treeview.column(
            fieldname,
            anchor=tk.W,
            width=10*max_widths[fieldname],
            stretch=0
        )
        treeview.heading(fieldname, text=fieldname, anchor=tk.W)


def insert_values(treeview: ttk.Treeview, csv_data: csv.DictReader):
    for row_idx, row_data in enumerate(csv_data):
        values = [row_data[fieldName] for fieldName in csv_data.fieldnames]
        treeview.insert(
            parent='',
            index=row_idx,
            values=values,
            tags=str(row_idx)
        )


def read_csv(
        treeview: ttk.Treeview, stringvar: tk.StringVar,
        scrollbar_ver: tk.Scrollbar, scrollbar_hor: tk.Scrollbar):
    
    with open(stringvar.get(), 'r') as f:
        csv_data = csv.DictReader(f)
        treeview['columns'] = csv_data.fieldnames
        adjust_field_width(treeview, csv_data)

        # Reset scrollbars
        scrollbar_ver.config(command=treeview.yview)
        scrollbar_hor.config(command=treeview.xview)

        # The entire file has been iterated at the first time,
        # so it is needed to seek to the beginning.
        f.seek(0)
        next(csv_data)
        insert_values(treeview, csv_data)


def draw():
    ...
