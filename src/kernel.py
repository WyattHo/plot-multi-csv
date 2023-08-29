import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import Sequence, Dict


def open_dir(stringvar: tk.StringVar):
    dir_name = filedialog.askopenfilename(title='Choose the directory')
    stringvar.set(dir_name)


def clear_treeview(treeview: ttk.Treeview):
    for item in treeview.get_children():
        treeview.delete(item)


def analyze_best_fit_width(
        fieldnames: Sequence[str],
        csv_data: csv.DictReader) -> Dict[str, int]:
    max_widths = {fieldname: len(fieldname) for fieldname in fieldnames}
    print(type(max_widths))
    for row_data in csv_data:
        for fieldname in fieldnames:
            data_width = len(row_data[fieldname])
            if data_width > max_widths[fieldname]:
                max_widths[fieldname] = data_width
    return max_widths


def adjust_field_width(
        treeview: ttk.Treeview, fieldnames: Sequence[str],
        max_widths: Dict[str, int]):
    for fieldname in fieldnames:
        treeview.column(
            fieldname,
            anchor=tk.W,
            width=10*max_widths[fieldname],
            stretch=0
        )
        treeview.heading(fieldname, text=fieldname, anchor=tk.W)


def insert_values(
        treeview: ttk.Treeview, fieldnames: Sequence[str],
        csv_data: csv.DictReader):
    for row_idx, row_data in enumerate(csv_data):
        values = [row_data[fieldName] for fieldName in fieldnames]
        treeview.insert(
            parent='',
            index=row_idx,
            values=values,
            tags=str(row_idx)
        )


def read_csv(
        treeview: ttk.Treeview, stringvar: tk.StringVar,
        scrollbar_ver_left: tk.Scrollbar, scrollbar_hor_left: tk.Scrollbar):
    clear_treeview(treeview)
    with open(stringvar.get(), 'r') as f:
        csv_data = csv.DictReader(f)
        fieldnames = csv_data.fieldnames

        treeview['columns'] = fieldnames
        max_widths = analyze_best_fit_width(fieldnames, csv_data)
        adjust_field_width(treeview, fieldnames, max_widths)

        # Reset scrollbars
        scrollbar_ver_left.config(command=treeview.yview)
        scrollbar_hor_left.config(command=treeview.xview)

        # The entire file has been iterated at the first time,
        # so it is needed to seek to the beginning.
        f.seek(0)
        next(csv_data)
        
        insert_values(treeview, fieldnames, csv_data)
