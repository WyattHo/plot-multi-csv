import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import Sequence, Union


PADS = {
    'padx': 5,
    'pady': 5,
    'ipadx': 1,
    'ipady': 1,
}


def clear_treeview(treeview: ttk.Treeview):
    for item in treeview.get_children():
        treeview.delete(item)


def insert_filenames(treeview: ttk.Treeview, filenames: Sequence):
    for idx, filename in enumerate(filenames):
        values = [idx + 1, filename]
        treeview.insert(
            parent='',
            index=idx,
            values=values,
            tags=str(idx)
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


def open_files(treeview: ttk.Treeview):
    clear_treeview(treeview)
    filenames = filedialog.askopenfilenames(
        title='Choose csv files',
        filetypes=[('csv files', '*.csv')]
    )
    insert_filenames(treeview, filenames)
    adjust_column_width(treeview)


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


def create_tab(
        notebook: ttk.Notebook,
        tabname: str) -> Sequence[ttk.Frame]:

    tab = ttk.Frame(notebook)
    notebook.add(tab, text=tabname)
    return tab


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


def create_subframe(frame: ttk.Frame):
    label = tk.Label(frame, text='CSV ID: ')
    entry = ttk.Combobox(frame)
    label.grid(row=0, column=0, sticky=tk.W, **PADS)
    entry.grid(row=0, column=1, sticky=tk.W, **PADS)

    label = tk.Label(frame, text='Field X: ')
    entry = ttk.Combobox(frame)
    label.grid(row=1, column=0, sticky=tk.W, **PADS)
    entry.grid(row=1, column=1, sticky=tk.W, **PADS)

    label = tk.Label(frame, text='Field Y: ')
    entry = ttk.Combobox(frame)
    label.grid(row=2, column=0, sticky=tk.W, **PADS)
    entry.grid(row=2, column=1, sticky=tk.W, **PADS)

    label = tk.Label(frame, text='Label: ')
    entry = ttk.Combobox(frame)
    label.grid(row=3, column=0, sticky=tk.W, **PADS)
    entry.grid(row=3, column=1, sticky=tk.W, **PADS)


def clear_tabs(notebook: ttk.Notebook):
    while notebook.index('end') > 0:
        notebook.forget(0)


def initial_tabs_with_treeview(notebook: ttk.Notebook):
    clear_tabs(notebook)
    tab = create_tab(notebook, tabname='1')
    create_treeview(tab, columns=('',), height=25)


def initial_tabs_with_frame(notebook: ttk.Notebook):
    clear_tabs(notebook)
    tab = create_tab(notebook, tabname='1')
    create_subframe(tab)


def create_and_populate_tab(treeview_filenames: ttk.Treeview, notebook: ttk.Notebook):
    for line in treeview_filenames.get_children():
        tab_id, path = treeview_filenames.item(line)['values']
        tab = create_tab(notebook, tab_id)
        with open(path, 'r') as f:
            csv_data = csv.DictReader(f)
            treeview_data = create_treeview(tab, csv_data.fieldnames, 25)
            insert_csv_values(treeview_data, csv_data)
            adjust_column_width(treeview_data)


def import_csv(treeview_filenames: ttk.Treeview, notebook: ttk.Notebook):
    try:
        if not treeview_filenames.get_children():
            raise Exception('No CSV file chosen.')
    except Exception as e:
        tk.messagebox.showerror(title='Error', message=e)
    else:
        clear_tabs(notebook)
        create_and_populate_tab(treeview_filenames, notebook)


def create_curve_setting(treeview: ttk.Treeview, spinbox: tk.Spinbox):
    exist_num = len(treeview.get_children())
    tgt_num = int(spinbox.get())
    if tgt_num > exist_num:
        for row_idx in range(exist_num, tgt_num):
            treeview.insert(
                parent='',
                index=row_idx,
                values=(row_idx + 1, ),
                tags=str(row_idx + 1)
            )

    elif tgt_num < exist_num:
        lines = treeview.get_children()
        for row_idx in range(tgt_num, exist_num):
            treeview.delete(lines[row_idx])


def draw():
    ...
