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


def initial_main_window() -> tk.Tk:
    root = tk.Tk()
    root.title('PlotCSV')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.state('zoomed')
    root.configure()
    return root


def create_directory_table(subframe: tk.Frame) -> ttk.Treeview:
    scrollbar_ver = tk.Scrollbar(subframe)
    scrollbar_ver.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_hor = tk.Scrollbar(subframe, orient='horizontal')
    scrollbar_hor.pack(side=tk.BOTTOM, fill=tk.X)

    treeview = ttk.Treeview(
        subframe,
        yscrollcommand=scrollbar_ver.set,
        xscrollcommand=scrollbar_hor.set,
        height=15
    )
    treeview.pack(fill='both')
    treeview.propagate(0)
    scrollbar_ver.config(command=treeview.yview)
    scrollbar_hor.config(command=treeview.xview)
    treeview['columns'] = ('Number', 'Path')
    treeview['show'] = 'headings'
    treeview.heading('Number', text='Number', anchor=tk.W)
    treeview.heading('Path', text='Path', anchor=tk.W)
    return treeview


def create_directory_frame(
        root: tk.Tk, font_label: font.Font,
        font_btn: font.Font) -> ttk.Treeview:

    frame = tk.LabelFrame(root, text='Choose the csv file')
    frame.grid(row=0, column=0, sticky=tk.NSEW, **PADS)
    frame['font'] = font_label

    subframe_left = tk.Frame(frame)
    subframe_left.grid(row=0, column=0)
    subframe_right = tk.Frame(frame)
    subframe_right.grid(row=0, column=1, rowspan=2)

    table = create_directory_table(subframe_left)
    button = tk.Button(
        subframe_right,
        text='Choose',
        command=lambda: kernel.open_files(table),
        width=6
    )
    button.grid(row=0, column=0, **PADS)
    button['font'] = font_btn
    return table


def create_working_subframes(frame: tk.LabelFrame) -> Tuple[tk.Frame]:
    subframe_left_1 = tk.Frame(frame, width=250, height=300)
    subframe_left_1.grid(row=0, column=0, **PADS)
    subframe_left_1.propagate(0)

    subframe_left_2 = tk.Frame(frame)
    subframe_left_2.grid(row=1, column=0)
    subframe_left_2.propagate(0)

    subframe_right_1 = tk.Frame(frame, width=250, height=300)
    subframe_right_1.grid(row=0, column=1, **PADS)
    subframe_right_1.propagate(0)

    subframe_right_2 = tk.Frame(frame)
    subframe_right_2.grid(row=1, column=1)
    subframe_right_2.propagate(0)
    return subframe_left_1, subframe_left_2, subframe_right_1, subframe_right_2


def fill_subframe_left_1(subframe: tk.Frame) -> ttk.Treeview:
    scrollbar_ver = tk.Scrollbar(subframe)
    scrollbar_ver.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_hor = tk.Scrollbar(subframe, orient='horizontal')
    scrollbar_hor.pack(side=tk.BOTTOM, fill=tk.X)

    treeview = ttk.Treeview(
        subframe,
        yscrollcommand=scrollbar_ver.set,
        xscrollcommand=scrollbar_hor.set,
        height=15
    )
    treeview.pack(fill='both')
    treeview.propagate(0)
    scrollbar_ver.config(command=treeview.yview)
    scrollbar_hor.config(command=treeview.xview)
    treeview['columns'] = ('1', )
    treeview['show'] = 'headings'
    treeview.column('1')
    treeview.heading('1', text='')
    return treeview


def fill_subframe_left_2(
        subframe: tk.Frame, treeview_data: ttk.Treeview,
        treeview_filenames: ttk.Treeview, font_btn: font.Font):

    read_btn = tk.Button(
        subframe,
        text='Read',
        command=lambda: kernel.read_csv(
            treeview_data,
            treeview_filenames
        ),
        width=6
    )
    clear_btn = tk.Button(
        subframe,
        text='clear',
        command=lambda: kernel.clear_treeview(
            treeview_data
        ),
        width=6
    )
    read_btn.grid(row=0, column=0, **PADS)
    clear_btn.grid(row=0, column=1, **PADS)
    read_btn['font'] = font_btn
    clear_btn['font'] = font_btn


def fill_subframe_right_1(subframe: tk.Frame):
    scrollbar_ver = tk.Scrollbar(subframe)
    scrollbar_ver.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_hor = tk.Scrollbar(subframe, orient='horizontal')
    scrollbar_hor.pack(side=tk.BOTTOM, fill=tk.X)

    treeview = ttk.Treeview(
        subframe,
        yscrollcommand=scrollbar_ver.set,
        xscrollcommand=scrollbar_hor.set,
        height=15
    )
    treeview.pack(fill='both')
    treeview.propagate(0)
    scrollbar_ver.config(command=treeview.yview)
    scrollbar_hor.config(command=treeview.xview)
    treeview['columns'] = ('1', )
    treeview['show'] = 'headings'
    treeview.column('1')
    treeview.heading('1', text='')


def fill_subframe_right_2(subframe: tk.Frame, font_btn: font.Font):
    draw_btn = tk.Button(
        subframe,
        text='Draw',
        command=lambda: kernel.draw(),
        width=6
    )
    clear_btn = tk.Button(
        subframe,
        text='Clear',
        command=lambda: kernel.clear(),
        width=6
    )
    draw_btn.grid(row=0, column=0, **PADS)
    clear_btn.grid(row=0, column=1, **PADS)
    draw_btn['font'] = font_btn
    clear_btn['font'] = font_btn


def create_working_frame(
        root: tk.Tk, font_label: font.Font,
        font_btn: font.Font, treeview_filenames: ttk.Treeview):

    frame = tk.LabelFrame(root, text='Working area')
    frame.grid(row=1, column=0, sticky=tk.NSEW, **PADS)
    frame.propagate(0)
    frame['font'] = font_label

    subframe_left_1, subframe_left_2, subframe_right_1, subframe_right_2\
        = create_working_subframes(frame)

    treeview_data = fill_subframe_left_1(subframe_left_1)
    fill_subframe_left_2(
        subframe_left_2,
        treeview_data,
        treeview_filenames,
        font_btn
    )
    fill_subframe_right_1(subframe_right_1)
    fill_subframe_right_2(subframe_right_2, font_btn)


def main():
    root = initial_main_window()
    font_label = font.Font(family='Helvetica', size=10)
    font_btn = font.Font(family='Helvetica', size=10)
    directory_table = create_directory_frame(root, font_label, font_btn)
    create_working_frame(root, font_label, font_btn, directory_table)
    root.mainloop()


if __name__ == '__main__':
    main()
