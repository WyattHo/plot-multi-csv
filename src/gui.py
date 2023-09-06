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
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.state('zoomed')
    root.minsize(**ROOT_MINSIZE)
    root.configure()
    return root


def create_directory_frame(
        root: tk.Tk, font_label: font.Font,
        font_btn: font.Font) -> ttk.Treeview:

    frame = tk.LabelFrame(root, text='Choose csv files')
    frame.grid(row=0, column=0, sticky=tk.NSEW, **PADS)
    frame['font'] = font_label

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    subframe_directory = tk.Frame(frame)
    subframe_directory.grid(row=0, column=0, sticky=tk.NSEW)

    subframe_action = tk.Frame(frame)
    subframe_action.grid(row=0, column=1)

    columns = ('Index', 'Path')
    treeview = kernel.create_treeview(subframe_directory, columns, 15)
    button = tk.Button(
        subframe_action,
        text='Choose',
        command=lambda: kernel.open_files(treeview),
        width=6
    )
    button.grid(row=0, column=0, **PADS)
    button['font'] = font_btn
    return treeview


def create_review_subframes(frame: tk.LabelFrame) -> Tuple[tk.Frame]:
    subframe_data = tk.Frame(frame)
    subframe_data.grid(row=0, column=0, sticky=tk.NSEW)

    subframe_review = tk.Frame(frame)
    subframe_review.grid(row=1, column=0)

    subframe_setting = tk.Frame(frame)
    subframe_setting.grid(row=0, column=1)

    subframe_plot = tk.Frame(frame)
    subframe_plot.grid(row=1, column=1)
    return subframe_data, subframe_review, subframe_setting, subframe_plot


def fill_subframe_data(subframe: tk.Frame) -> ttk.Notebook:
    subframe.rowconfigure(0, weight=1)
    subframe.columnconfigure(0, weight=1)
    notebook = ttk.Notebook(subframe)
    notebook.grid(row=0, column=0, sticky=tk.NSEW)
    kernel.initial_tabs(notebook)
    return notebook


def fill_subframe_review(
        subframe: tk.Frame, treeview_filenames: ttk.Treeview,
        font_btn: font.Font, notebook: ttk.Notebook):

    import_btn = tk.Button(
        subframe,
        text='Import',
        command=lambda: kernel.import_csv(
            treeview_filenames,
            notebook
        ),
        width=6
    )
    clear_btn = tk.Button(
        subframe,
        text='Clear',
        command=lambda: kernel.initial_tabs(notebook),
        width=6
    )
    import_btn.grid(row=0, column=0, **PADS)
    clear_btn.grid(row=0, column=1, **PADS)
    import_btn['font'] = font_btn
    clear_btn['font'] = font_btn


def fill_subframe_setting(subframe: tk.Frame):
    subframe.rowconfigure(0, weight=1)
    subframe.columnconfigure(0, weight=1)

    frame_curve = tk.LabelFrame(subframe, text='Curve settings')
    frame_curve.grid(row=0, column=0)

    frame_curve.rowconfigure(0, weight=1)
    frame_curve.rowconfigure(1, weight=1)
    frame_curve.columnconfigure(0, weight=1)
    frame_curve.columnconfigure(1, weight=1)

    label = tk.Label(frame_curve, text='Curve numbers')
    label.grid(row=0, column=0, sticky=tk.W, **PADS)

    spinbox = tk.Spinbox(frame_curve, from_=1, to=20, width=3)
    spinbox.grid(row=0, column=0, sticky=tk.E, **PADS)

    frame_treeview = tk.Frame(frame_curve)
    frame_treeview.grid(row=1, column=0, columnspan=2)

    columns = ('Curve Index', 'CSV Index', 'Field X', 'Field Y', 'Label')
    treeview = kernel.create_treeview(frame_treeview, columns, 5)
    kernel.adjust_column_width(treeview)


def fill_subframe_plot(subframe: tk.Frame, font_btn: font.Font):
    button = tk.Button(
        subframe,
        text='Draw',
        command=lambda: kernel.draw(),
        width=6
    )
    button.grid(row=0, column=0, **PADS)
    button['font'] = font_btn


def create_review_frame(
        root: tk.Tk, font_label: font.Font,
        font_btn: font.Font, treeview_filenames: ttk.Treeview):

    frame = tk.LabelFrame(root, text='Review data')
    frame.grid(row=1, column=0, sticky=tk.NSEW, **PADS)
    frame['font'] = font_label

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    subframe_data, subframe_review, subframe_setting, subframe_plot\
        = create_review_subframes(frame)

    notebook = fill_subframe_data(subframe_data)
    fill_subframe_review(
        subframe_review,
        treeview_filenames,
        font_btn,
        notebook,
    )
    fill_subframe_setting(subframe_setting)
    fill_subframe_plot(subframe_plot, font_btn)


def main():
    root = initial_main_window()
    font_label = font.Font(family='Helvetica', size=10)
    font_btn = font.Font(family='Helvetica', size=10)
    treeview_filenames = create_directory_frame(root, font_label, font_btn)
    create_review_frame(root, font_label, font_btn, treeview_filenames)
    root.mainloop()


if __name__ == '__main__':
    main()
