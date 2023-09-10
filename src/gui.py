import tkinter as tk
from tkinter import font
from tkinter import filedialog
from typing import Tuple

import pandas as pd

from customization import Treeview, Notebook


class MyApp:
    PADS = {
        'padx': 5, 'pady': 5,
        'ipadx': 1, 'ipady': 1,
    }
    ROOT_MINSIZE = {
        'width': 400, 'height': 400
    }

    # typesetting
    def __init__(self):
        self.root = self.initialize_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_button = font.Font(family='Helvetica', size=10)
        self.treeview_csv_names = self.create_frame_for_csv_names()
        self.notebook_csv_data = self.create_frame_for_csv_data()
        self.notebook_curve_settings, self.spinbox\
            = self.create_frame_for_curve_settings()
        self.create_frame_for_axes_settings()
        self.root.mainloop()

    def initialize_main_window(self) -> tk.Tk:
        root = tk.Tk()
        root.title('PlotCSV')
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)
        root.state('zoomed')
        root.minsize(**self.ROOT_MINSIZE)
        root.configure()
        return root

    def create_frame_for_csv_names(self) -> Treeview:
        frame = tk.LabelFrame(self.root, text='Choose CSV files')
        frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame['font'] = self.font_label

        subframe = tk.Frame(frame)
        subframe.grid(row=0, column=0, sticky=tk.NSEW)
        columns = ('CSV ID', 'CSV Path')
        treeview = Treeview(subframe, columns, 5)

        subframe = tk.Frame(frame)
        subframe.grid(row=0, column=1)
        button = tk.Button(
            subframe,
            text='Choose',
            command=lambda: self.open_files(),
            width=6
        )
        button.grid(row=0, column=0, **self.PADS)
        button['font'] = self.font_button
        return treeview

    def create_frame_for_csv_data(self) -> Notebook:
        frame = tk.LabelFrame(self.root, text='Review CSV data')
        frame.grid(row=1, column=0, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame['font'] = self.font_label

        notebook = Notebook(frame)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        tab = notebook.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=25)

        button = tk.Button(
            frame,
            text='Import',
            command=lambda: self.import_csv(),
            width=6
        )
        button.grid(row=1, column=0, **self.PADS)
        button['font'] = self.font_button

        button = tk.Button(
            frame,
            text='Clear',
            command=lambda: self.clear_csv_data_notebook(),
            width=6
        )
        button.grid(row=1, column=1, **self.PADS)
        button['font'] = self.font_button
        return notebook

    def create_frame_for_curve_settings(self) -> Tuple[Notebook, tk.Spinbox]:
        frame = tk.LabelFrame(self.root, text='Curve settings')
        frame.grid(row=1, column=1, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = Notebook(frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        notebook.initialize_notebook_for_curve_settings(MyApp.PADS)

        label = tk.Label(frame, text='Curve numbers')
        label.grid(row=0, column=0, **self.PADS)

        spinbox = tk.Spinbox(
            frame, from_=1, to=20, width=3,
            command=lambda: self.adjust_curve_settings_tabs()
        )
        spinbox.grid(row=0, column=1, **self.PADS)
        return notebook, spinbox

    def create_frame_for_axes_settings(self):
        frame = tk.LabelFrame(self.root, text='Axes settings')
        frame.grid(row=1, column=2, sticky=tk.NSEW, **self.PADS)
        button = tk.Button(
            frame,
            text='Draw',
            command=lambda: self.draw(),
            width=6
        )
        button.grid(row=0, column=0, **self.PADS)
        button['font'] = self.font_button

    # actions
    def open_files(self):
        self.treeview_csv_names.clear_content()
        csv_names = filedialog.askopenfilenames(
            title='Choose csv files',
            filetypes=[('csv files', '*.csv')]
        )
        self.treeview_csv_names.insert_csv_names(csv_names)
        self.treeview_csv_names.adjust_column_width()

    def import_csv(self):
        try:
            if not self.treeview_csv_names.get_children():
                raise Exception('No CSV file chosen.')
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)
        else:
            self.notebook_csv_data.remove_tabs()
            self.csv_names = self.treeview_csv_names.get_data()
            self.csv_data_pool = {}
            for row_idx, row in self.csv_names.iterrows():
                csv_idx = row['CSV ID']
                path = row['CSV Path']
                csv_dataframe = pd.read_csv(path)
                self.csv_data_pool[csv_idx] = csv_dataframe
                tab = self.notebook_csv_data.create_new_tab(csv_idx)
                treeview = Treeview(tab, list(csv_dataframe.columns), 25)
                treeview.insert_csv_dataframe(csv_dataframe)
                treeview.adjust_column_width()

            self.notebook_curve_settings.fill_widget_options(
                '1',
                self.csv_data_pool
            )

    def clear_csv_data_notebook(self):
        self.notebook_csv_data.remove_tabs()
        tab = self.notebook_csv_data.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=25)

    def adjust_curve_settings_tabs(self):
        exist_num = len(self.notebook_curve_settings.tabs_)
        tgt_num = int(self.spinbox.get())
        if tgt_num > exist_num:
            for tab_idx in range(exist_num, tgt_num):
                tabname = str(tab_idx + 1)
                tab = self.notebook_curve_settings.create_new_tab(
                    tabname=tabname
                )
                widgets = self.notebook_curve_settings.fill_curve_setting_widgets(
                    tab, self.PADS
                )
                tab.widgets = widgets
                self.notebook_curve_settings.fill_widget_options(
                    tabname,
                    self.csv_data_pool
                )
        elif tgt_num < exist_num:
            tab_idx = self.notebook_curve_settings.index('end') - 1
            self.notebook_curve_settings.forget(tab_idx)

    def draw(self):
        ...


if __name__ == '__main__':
    MyApp()
