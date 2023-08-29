import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def open_dir(stringvar: tk.StringVar):
    dir_name = filedialog.askopenfilename(title='Choose the directory')
    stringvar.set(dir_name)


def read_csv(
        treeview_read: ttk.Treeview, stringvar: tk.StringVar,
        scrollbar_ver_left: tk.Scrollbar, scrollbar_hor_left: tk.Scrollbar):
    # Clear items first
    for item in treeview_read.get_children():
        treeview_read.delete(item)

    # Read csv
    tgtfile_name = stringvar.get()
    with open(tgtfile_name, 'r') as f:
        csv_data = csv.DictReader(f)
        fieldnames = csv_data.fieldnames
        treeview_read['columns'] = fieldnames

        # Analyze best-fit width for each field
        max_widths = {}
        for fieldname in fieldnames:
            max_widths[fieldname] = len(fieldname)

        for row_idx, row_data in enumerate(csv_data):
            for fieldname in fieldnames:
                data_width = len(row_data[fieldname])

                if data_width > max_widths[fieldname]:
                    max_widths[fieldname] = data_width

        # Set fields
        for fieldname in fieldnames:
            treeview_read.column(
                fieldname,
                anchor=tk.W,
                width=10*max_widths[fieldname],
                stretch=0
            )
            treeview_read.heading(fieldname, text=fieldname, anchor=tk.W)

        # Reset scrollbars
        scrollbar_ver_left.config(command=treeview_read.yview)
        scrollbar_hor_left.config(command=treeview_read.xview)

        # The entire file has been iterated at the first time,
        # so it is needed to seek to the beginning.
        f.seek(0)
        next(csv_data)

        # Insert values
        for row_idx, row_data in enumerate(csv_data):
            values = [row_data[fieldName] for fieldName in fieldnames]
            treeview_read.insert(
                parent='',
                index=row_idx,
                values=values,
                tags=str(row_idx)
            )
