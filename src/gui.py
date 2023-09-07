import tkinter as tk
from tkinter import font
from tkinter import ttk
from typing import Tuple

import kernel


PADS = {
    'padx': 5,
    'pady': 5,
    'ipadx': 1,
    'ipady': 1,
}
ROOT_MINSIZE = {
    'width': 400,
    'height': 400
}


def initial_main_window() -> tk.Tk:
    root = tk.Tk()
    root.title('PlotCSV')
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=5)
    root.state('zoomed')
    root.minsize(**ROOT_MINSIZE)
    root.configure()
    return root


def create_directory_frame(
        root: tk.Tk, font_label: font.Font,
        font_btn: font.Font) -> ttk.Treeview:

    frame = tk.LabelFrame(root, text='Choose csv files')
    frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, **PADS)
    frame['font'] = font_label

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    subframe_directory = tk.Frame(frame)
    subframe_directory.grid(row=0, column=0, sticky=tk.NSEW)

    subframe_action = tk.Frame(frame)
    subframe_action.grid(row=0, column=1)

    columns = ('CSV ID', 'CSV Path')
    treeview = kernel.create_treeview(subframe_directory, columns, 5)
    button = tk.Button(
        subframe_action,
        text='Choose',
        command=lambda: kernel.open_files(treeview),
        width=6
    )
    button.grid(row=0, column=0, **PADS)
    button['font'] = font_btn
    return treeview


def create_data_frame(
        root: tk.Tk, font_label: font.Font,
        font_btn: font.Font, treeview_filenames: ttk.Treeview):

    frame = tk.LabelFrame(root, text='Review data')
    frame.grid(row=1, column=0, sticky=tk.NSEW, **PADS)
    frame['font'] = font_label

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    
    notebook = ttk.Notebook(frame)
    notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
    kernel.initial_tabs(notebook)

    import_btn = tk.Button(
        frame,
        text='Import',
        command=lambda: kernel.import_csv(
            treeview_filenames,
            notebook
        ),
        width=6
    )
    import_btn.grid(row=1, column=0, **PADS)
    import_btn['font'] = font_btn

    clear_btn = tk.Button(
        frame,
        text='Clear',
        command=lambda: kernel.initial_tabs(notebook),
        width=6
    )
    clear_btn.grid(row=1, column=1, **PADS)
    clear_btn['font'] = font_btn
    return notebook


def create_curve_frame(root: tk.Tk):
    frame = tk.LabelFrame(root, text='Curve settings')
    frame.grid(row=1, column=1, sticky=tk.NSEW, **PADS)

    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    frame_treeview = tk.Frame(frame)
    frame_treeview.grid(row=0, column=0, sticky=tk.NSEW)

    columns = ('Curve ID', 'CSV ID', 'Field X', 'Field Y', 'Label')
    treeview = kernel.create_treeview(frame_treeview, columns, 15)
    treeview.insert(
        parent='',
        index=0,
        values=(1,),
        tags='0'
    )
    kernel.adjust_column_width(treeview)

    label = tk.Label(frame, text='Curve numbers')
    label.grid(row=1, column=0, sticky=tk.W, **PADS)

    spinbox = tk.Spinbox(
        frame, from_=1, to=20, width=3,
        command=lambda: kernel.create_curve_setting(treeview, spinbox)
    )
    spinbox.grid(row=1, column=0, sticky=tk.E, **PADS)


def create_axes_frame(root: tk.Tk, font_btn: font.Font):
    frame = tk.LabelFrame(root, text='Axes settings')
    frame.grid(row=1, column=2, sticky=tk.NSEW, **PADS)
    button = tk.Button(
        frame,
        text='Draw',
        command=lambda: kernel.draw(),
        width=6
    )
    button.grid(row=0, column=0, **PADS)
    button['font'] = font_btn


def main():
    root = initial_main_window()
    font_label = font.Font(family='Helvetica', size=10)
    font_btn = font.Font(family='Helvetica', size=10)
    treeview_filenames = create_directory_frame(root, font_label, font_btn)
    notebook_data = create_data_frame(root, font_label, font_btn, treeview_filenames)
    create_curve_frame(root)
    create_axes_frame(root, font_btn)
    root.mainloop()


if __name__ == '__main__':
    main()
