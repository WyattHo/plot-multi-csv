import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk
from typing import Tuple

import pandas as pd

from customization import Treeview, Notebook, Tab


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
        self.treeview_filenames = self.create_frame_for_filenames()
        self.notebook_data_pool = self.create_frame_for_data_pool()
        self.notebook_data_visual, self.spinbox\
            = self.create_frame_for_data_visual()
        self.create_frame_for_axes_visual()
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

    def create_frame_for_filenames(self) -> Treeview:
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

    def create_frame_for_data_pool(self) -> Notebook:
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
            command=lambda: self.clear_data_pool(),
            width=6
        )
        button.grid(row=1, column=1, **self.PADS)
        button['font'] = self.font_button
        return notebook

    def fill_data_visual_widgets(self, tab: Tab):
        label = tk.Label(tab, text='CSV ID: ')
        entry = ttk.Combobox(tab)
        label.grid(row=0, column=0, sticky=tk.W, **self.PADS)
        entry.grid(row=0, column=1, sticky=tk.W, **self.PADS)
        combobox_csv_idx = entry

        label = tk.Label(tab, text='Field X: ')
        entry = ttk.Combobox(tab)
        label.grid(row=1, column=0, sticky=tk.W, **self.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **self.PADS)
        combobox_field_x = entry

        label = tk.Label(tab, text='Field Y: ')
        entry = ttk.Combobox(tab)
        label.grid(row=2, column=0, sticky=tk.W, **self.PADS)
        entry.grid(row=2, column=1, sticky=tk.W, **self.PADS)
        combobox_field_y = entry

        label = tk.Label(tab, text='Label: ')
        entry = tk.Entry(tab)
        label.grid(row=3, column=0, sticky=tk.W, **self.PADS)
        entry.grid(row=3, column=1, sticky=tk.W, **self.PADS)

        widgets = {
            'csv_idx': combobox_csv_idx,
            'field_x': combobox_field_x,
            'field_y': combobox_field_y
        }
        tab.widgets = widgets

    def create_frame_for_data_visual(self) -> Tuple[Notebook, tk.Spinbox]:
        frame = tk.LabelFrame(self.root, text='Data Visualization')
        frame.grid(row=1, column=1, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = Notebook(frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        tab = notebook.create_new_tab('1')
        self.fill_data_visual_widgets(tab)

        label = tk.Label(frame, text='Numbers of datasets')
        label.grid(row=0, column=0, **self.PADS)

        spinbox = tk.Spinbox(
            frame, from_=1, to=20, width=3,
            command=lambda: self.change_number_of_dataset()
        )
        spinbox.grid(row=0, column=1, **self.PADS)
        return notebook, spinbox

    def create_frame_for_axes_visual(self):
        frame = tk.LabelFrame(self.root, text='Axes Visualization')
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
        self.treeview_filenames.clear_content()
        filenames = filedialog.askopenfilenames(
            title='Choose csv files',
            filetypes=[('csv files', '*.csv')]
        )
        self.filenames = {'CSV ID': [], 'CSV Path': []}
        for idx, filename in enumerate(filenames):
            self.filenames['CSV ID'].append(idx + 1)
            self.filenames['CSV Path'].append(filename)
        self.filenames = pd.DataFrame(self.filenames)
        self.treeview_filenames.insert_dataframe(self.filenames)
        self.treeview_filenames.adjust_column_width()

    def fill_widget_options(self, tab: Tab):
        values_csv_idx = list(self.data_pool.keys())
        tab.widgets['csv_idx'].config(values=values_csv_idx)
        tab.widgets['csv_idx'].current(0)

    def import_csv(self):
        try:
            if not self.treeview_filenames.get_children():
                raise Exception('No CSV file chosen.')
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)
        else:
            self.data_pool = {}
            self.notebook_data_pool.remove_tabs()
            for row_idx, row in self.filenames.iterrows():
                csv_idx = row['CSV ID']
                path = row['CSV Path']
                tab = self.notebook_data_pool.create_new_tab(csv_idx)
                csv_dataframe = pd.read_csv(path)
                self.data_pool[csv_idx] = csv_dataframe
                treeview = Treeview(tab, list(csv_dataframe.columns), 25)
                treeview.insert_dataframe(csv_dataframe)
                treeview.adjust_column_width()
            self.fill_widget_options(self.notebook_data_visual.tabs_['1'])

    def clear_data_pool(self):
        self.notebook_data_pool.remove_tabs()
        tab = self.notebook_data_pool.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=25)

    def change_number_of_dataset(self):
        exist_num = len(self.notebook_data_visual.tabs())
        tgt_num = int(self.spinbox.get())
        if tgt_num > exist_num:
            tabname = str(tgt_num)
            tab = self.notebook_data_visual.create_new_tab(tabname)
            self.fill_data_visual_widgets(tab)
            self.fill_widget_options(tab)
        elif tgt_num < exist_num:
            tabname = str(exist_num)
            tab_idx = self.notebook_data_visual.index('end') - 1
            self.notebook_data_visual.forget(tab_idx)
            self.notebook_data_visual.tabs_.pop(tabname)

    def draw(self):
        ...


if __name__ == '__main__':
    MyApp()
