import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk
from typing import Dict, Sequence

import pandas as pd

import plotting
from custom_widgets import *


class MyApp:
    PADS = {
        'padx': 5, 'pady': 5,
        'ipadx': 1, 'ipady': 1,
    }
    ROOT_MINSIZE = {
        'width': 400, 'height': 400
    }
    HEIGHT_DATAPOOL = 25
    WIDTH_COMBOBOX = 12
    WIDTH_ENTRY = 14

    # typesetting
    def __init__(self):
        self.root = self.initialize_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_button = font.Font(family='Helvetica', size=10)
        self.config = plotting.get_initial_configuration()
        self.create_frame_for_filenames()
        self.create_frame_for_data_pool()
        self.create_frame_for_data_visual()
        self.create_frame_for_figure_visual()
        self.create_frame_for_x_axis_visual()
        self.create_frame_for_y_axis_visual()
        self.create_frame_for_plot()
        self.root.mainloop()

    def initialize_main_window(self) -> tk.Tk:
        root = tk.Tk()
        root.title('PlotCSV')
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)
        root.rowconfigure(2, weight=5)
        root.state('zoomed')
        root.minsize(**self.ROOT_MINSIZE)
        root.configure()
        return root

    def create_frame_for_filenames(self):
        frame = tk.LabelFrame(self.root, text='Choose CSV files')
        frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, **MyApp.PADS)
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
        button.grid(row=0, column=0, **MyApp.PADS)
        button['font'] = self.font_button
        self.treeview_filenames = treeview

    def create_frame_for_data_pool(self):
        frame = tk.LabelFrame(self.root, text='Review CSV data')
        frame.grid(row=1, column=0, rowspan=3, sticky=tk.NSEW, **MyApp.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame['font'] = self.font_label

        notebook = Notebook(frame)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        tab = notebook.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=MyApp.HEIGHT_DATAPOOL)

        button = tk.Button(
            frame,
            text='Import',
            command=lambda: self.import_csv(),
            width=6
        )
        button.grid(row=1, column=0, **MyApp.PADS)
        button['font'] = self.font_button

        button = tk.Button(
            frame,
            text='Clear',
            command=lambda: self.clear_data_pool(),
            width=6
        )
        button.grid(row=1, column=1, **MyApp.PADS)
        button['font'] = self.font_button
        self.notebook_data_pool = notebook

    def fill_data_visual_widgets(self, tab: Tab):
        label = tk.Label(tab, text='CSV ID: ')
        entry = ttk.Combobox(tab, width=MyApp.WIDTH_COMBOBOX)
        label.grid(row=0, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=0, column=1, sticky=tk.W, **MyApp.PADS)
        combobox_csv_idx = entry

        label = tk.Label(tab, text='Field X: ')
        entry = ttk.Combobox(tab, width=MyApp.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **MyApp.PADS)
        combobox_field_x = entry

        label = tk.Label(tab, text='Field Y: ')
        entry = ttk.Combobox(tab, width=MyApp.WIDTH_COMBOBOX)
        label.grid(row=2, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=2, column=1, sticky=tk.W, **MyApp.PADS)
        combobox_field_y = entry

        label = tk.Label(tab, text='Label: ')
        entry = tk.Entry(tab, width=MyApp.WIDTH_ENTRY)
        label.grid(row=3, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=3, column=1, sticky=tk.W, **MyApp.PADS)

        widgets = {
            'csv_idx': combobox_csv_idx,
            'field_x': combobox_field_x,
            'field_y': combobox_field_y,
            'label': entry
        }
        tab.widgets = widgets

    def create_frame_for_data_visual(self):
        frame = tk.LabelFrame(self.root, text='Data Visualization')
        frame.grid(row=1, column=1, sticky=tk.NSEW, **MyApp.PADS)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = Notebook(frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        tab = notebook.create_new_tab('1')
        self.fill_data_visual_widgets(tab)

        label = tk.Label(frame, text='Numbers of datasets')
        label.grid(row=0, column=0, **MyApp.PADS)

        spinbox = Spinbox(frame, from_=1, to=20, width=3)
        spinbox.grid(row=0, column=1, **MyApp.PADS)
        spinbox.config(
            command=lambda: self.change_number_of_dataset()
        )
        self.notebook_data_visual = notebook
        self.spinbox_dataset = spinbox

    def create_frame_for_figure_visual(self):
        self.figure_visual_widgets = {}
        frame = tk.LabelFrame(self.root, text='Figure Visualization')
        frame.grid(row=2, column=1, sticky=tk.NSEW, **MyApp.PADS)

        label = tk.Label(frame, text='Title: ')
        entry = tk.Entry(frame, width=28)
        label.grid(row=0, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=0, column=1, columnspan=3, sticky=tk.W, **MyApp.PADS)
        self.figure_visual_widgets['title'] = entry

        doublevar = tk.DoubleVar()
        label = tk.Label(frame, text='Width: ')
        entry = tk.Entry(frame, width=8, textvariable=doublevar)
        label.grid(row=1, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **MyApp.PADS)
        doublevar.set(4.8)
        self.figure_visual_widgets['width'] = doublevar

        doublevar = tk.DoubleVar()
        label = tk.Label(frame, text='Height: ')
        entry = tk.Entry(frame, width=8, textvariable=doublevar)
        label.grid(row=1, column=2, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=1, column=3, sticky=tk.W, **MyApp.PADS)
        doublevar.set(2.4)
        self.figure_visual_widgets['height'] = doublevar

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            frame,
            text='Show grid',
            variable=intvar
        )
        checkbutton.grid(
            row=2, column=0, columnspan=4,
            sticky=tk.W, **MyApp.PADS
        )
        intvar.set(True)
        self.figure_visual_widgets['show_grid'] = intvar

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            frame,
            text='Show legend',
            variable=intvar
        )
        checkbutton.grid(
            row=3, column=0, columnspan=4,
            sticky=tk.W, **MyApp.PADS
        )
        intvar.set(True)
        self.figure_visual_widgets['legend_visible'] = intvar

    def create_frame_for_x_axis_visual(self):
        self.x_axis_visual_widgets = {}
        frame = tk.LabelFrame(self.root, text='X-Axis Visualization')
        frame.grid(row=1, column=2, sticky=tk.NSEW, **MyApp.PADS)

        label = tk.Label(frame, text='Label: ')
        entry = tk.Entry(frame, width=28)
        label.grid(row=0, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=0, column=1, sticky=tk.W, **MyApp.PADS)
        self.x_axis_visual_widgets['label'] = entry

        label = tk.Label(frame, text='Scale: ')
        entry = ttk.Combobox(frame, width=MyApp.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **MyApp.PADS)
        entry.config(values=['linear', 'log'])
        entry.current(0)
        self.x_axis_visual_widgets['scale'] = entry

        subframe = tk.Frame(frame)
        subframe.grid(
            row=2, column=0, columnspan=2,
            sticky=tk.NSEW, **MyApp.PADS
        )

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            subframe,
            text='Assign range',
            variable=intvar,
            command=self.active_deactive_range
        )
        checkbutton.grid(
            row=0, column=0,
            columnspan=2,
            sticky=tk.W, **MyApp.PADS
        )
        self.x_axis_visual_widgets['assign_range'] = intvar

        label = tk.Label(subframe, text='Min: ')
        entry = tk.Entry(subframe, width=8)
        label.grid(row=1, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **MyApp.PADS)
        entry.config(state='disabled')
        self.x_axis_visual_widgets['min'] = entry

        label = tk.Label(subframe, text='Max: ')
        entry = tk.Entry(subframe, width=8)
        label.grid(row=2, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=2, column=1, sticky=tk.W, **MyApp.PADS)
        entry.config(state='disabled')
        self.x_axis_visual_widgets['max'] = entry

    def create_frame_for_y_axis_visual(self):
        self.y_axis_visual_widgets = {}
        frame = tk.LabelFrame(self.root, text='Y-Axis Visualization')
        frame.grid(row=2, column=2, sticky=tk.NSEW, **MyApp.PADS)

        label = tk.Label(frame, text='Label: ')
        entry = tk.Entry(frame, width=28)
        label.grid(row=0, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=0, column=1, sticky=tk.W, **MyApp.PADS)
        self.y_axis_visual_widgets['label'] = entry

        label = tk.Label(frame, text='Scale: ')
        entry = ttk.Combobox(frame, width=MyApp.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **MyApp.PADS)
        entry.config(values=['linear', 'log'])
        entry.current(0)
        self.y_axis_visual_widgets['scale'] = entry

        subframe = tk.Frame(frame)
        subframe.grid(
            row=2, column=0, columnspan=2,
            sticky=tk.NSEW, **MyApp.PADS
        )

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            subframe,
            text='Assign range',
            variable=intvar,
            command=self.active_deactive_range
        )
        checkbutton.grid(
            row=0, column=0,
            columnspan=2,
            sticky=tk.W, **MyApp.PADS
        )
        self.y_axis_visual_widgets['assign_range'] = intvar

        label = tk.Label(subframe, text='Min: ')
        entry = tk.Entry(subframe, width=8)
        label.grid(row=1, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **MyApp.PADS)
        entry.config(state='disabled')
        self.y_axis_visual_widgets['min'] = entry

        label = tk.Label(subframe, text='Max: ')
        entry = tk.Entry(subframe, width=8)
        label.grid(row=2, column=0, sticky=tk.W, **MyApp.PADS)
        entry.grid(row=2, column=1, sticky=tk.W, **MyApp.PADS)
        entry.config(state='disabled')
        self.y_axis_visual_widgets['max'] = entry

    def create_frame_for_plot(self):
        frame = tk.LabelFrame(self.root, text='Plot Actions')
        frame.grid(row=3, column=1, columnspan=2, sticky=tk.NSEW, **MyApp.PADS)
        frame.columnconfigure(0, weight=1)
        button = tk.Button(
            frame,
            text='Plot',
            command=lambda: self.plot(),
            width=6
        )
        button.grid(row=0, column=0, **MyApp.PADS)
        button['font'] = self.font_button

    # actions
    def open_files(self):
        self.treeview_filenames.clear_content()
        filenames = filedialog.askopenfilenames(
            title='Choose csv files',
            filetypes=[('csv files', '*.csv')]
        )
        self.filenames = pd.DataFrame(
            [[idx + 1, filename] for idx, filename in enumerate(filenames)],
            columns=['CSV ID', 'CSV Path']
        )
        self.treeview_filenames.insert_dataframe(self.filenames)
        self.treeview_filenames.adjust_column_width()

    def update_field_x_and_y(self, tab: Tab):
        csv_idx = int(tab.widgets['csv_idx'].get())
        columns = list(self.data_pool[csv_idx].columns)
        tab.widgets['field_x'].config(values=columns)
        tab.widgets['field_x'].current(0)
        tab.widgets['field_y'].config(values=columns)
        tab.widgets['field_y'].current(1)

    def initialize_csv_indices(self, tab: Tab):
        values_csv_idx = list(self.data_pool.keys())
        tab.widgets['csv_idx'].config(values=values_csv_idx)
        tab.widgets['csv_idx'].current(0)
        self.update_field_x_and_y(tab)
        tab.widgets['csv_idx'].bind(
            '<<ComboboxSelected>>',
            lambda event: self.update_field_x_and_y(tab)
        )

    def import_csv(self):
        try:
            if not self.treeview_filenames.get_children():
                raise Exception('No CSV file chosen.')
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)
        else:
            self.data_pool: Dict[str, pd.DataFrame] = {}
            self.notebook_data_pool.remove_all_tabs()
            for row in self.filenames.itertuples():
                csv_idx, csv_path = row[1:]
                tab = self.notebook_data_pool.create_new_tab(csv_idx)
                csv_dataframe = pd.read_csv(csv_path)
                self.data_pool[csv_idx] = csv_dataframe
                columns = list(csv_dataframe.columns)
                treeview = Treeview(tab, columns, MyApp.HEIGHT_DATAPOOL)
                treeview.insert_dataframe(csv_dataframe)
                treeview.adjust_column_width()
            self.initialize_csv_indices(self.notebook_data_visual.tabs_['1'])

    def clear_data_pool(self):
        self.notebook_data_pool.remove_all_tabs()
        tab = self.notebook_data_pool.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=MyApp.HEIGHT_DATAPOOL)

    def change_number_of_dataset(self):
        try:
            self.data_pool
        except AttributeError:
            self.spinbox_dataset.stringvar.set(1)
            msg = 'Please import data first.'
            tk.messagebox.showerror(title='Error', message=msg)
        else:
            exist_num = len(self.notebook_data_visual.tabs())
            tgt_num = int(self.spinbox_dataset.get())
            if tgt_num > exist_num:
                tabname = str(tgt_num)
                tab = self.notebook_data_visual.create_new_tab(tabname)
                self.fill_data_visual_widgets(tab)
                self.initialize_csv_indices(tab)
            elif tgt_num < exist_num:
                tabname = str(exist_num)
                self.notebook_data_visual.remove_tab(tabname)

    def active_deactive_range(self):
        if self.x_axis_visual_widgets['assign_range'].get():
            self.x_axis_visual_widgets['min'].config(state='normal')
            self.x_axis_visual_widgets['max'].config(state='normal')
        else:
            self.x_axis_visual_widgets['min'].config(state='disabled')
            self.x_axis_visual_widgets['max'].config(state='disabled')
        if self.y_axis_visual_widgets['assign_range'].get():
            self.y_axis_visual_widgets['min'].config(state='normal')
            self.y_axis_visual_widgets['max'].config(state='normal')
        else:
            self.y_axis_visual_widgets['min'].config(state='disabled')
            self.y_axis_visual_widgets['max'].config(state='disabled')

    def collect_data_send(self) -> Sequence[pd.DataFrame]:
        data_send = []
        for tab in self.notebook_data_visual.tabs_.values():
            csv_idx = tab.widgets['csv_idx'].get()
            data_send.append(self.data_pool[int(csv_idx)])
        return data_send

    def collect_configurations_data(self):
        labels = self.config['data']['labels']
        fieldnames = self.config['data']['fieldnames']
        for tab in self.notebook_data_visual.tabs_.values():
            labels.append(tab.widgets['label'].get())
            fieldnames.append({
                'x': tab.widgets['field_x'].get(),
                'y': tab.widgets['field_y'].get()
            })

    def collect_configurations_figure(self):
        widgets = self.figure_visual_widgets
        self.config['figure']['title'] = widgets['title'].get()
        self.config['figure']['size'] = [
            float(widgets['width'].get()),
            float(widgets['height'].get())
        ]
        self.config['figure']['grid_visible'] = widgets['show_grid'].get()
        self.config['figure']['legend_visible'] = widgets['legend_visible'].get()

    def collect_configurations_axes(self):
        self.config['axis_x']['scale'] = 'linear'
        self.config['axis_x']['lim'] = None
        self.config['axis_y']['scale'] = 'linear'
        self.config['axis_y']['lim'] = None

    def plot(self):
        data_send = self.collect_data_send()
        self.collect_configurations_data()
        self.collect_configurations_figure()
        self.collect_configurations_axes()
        plotting.plot_by_app(self.config, data_send)


if __name__ == '__main__':
    MyApp()
