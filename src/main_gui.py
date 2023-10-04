import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk
from typing import Dict, Sequence, TypedDict

import pandas as pd

import plotting
from custom_widgets import *


class AxisVisualWidgets(TypedDict):
    label: tk.Entry
    scale: ttk.Combobox
    assign_range: tk.IntVar
    min: tk.Entry
    max: tk.Entry


class FigureVisualWidgets(TypedDict):
    title: tk.Entry
    width: tk.DoubleVar
    height: tk.DoubleVar
    grid_visible: tk.IntVar
    legend_visible: tk.IntVar


class ConfigWidgets(TypedDict):
    csvnames: Treeview
    data_pool: Notebook
    data_visual: Notebook
    dataset_number: Spinbox
    figure_visual: FigureVisualWidgets
    axis_x: AxisVisualWidgets
    axis_y: AxisVisualWidgets


class App:
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
        self.config_values = plotting.get_initial_configuration()
        self.config_widgets = self.initialize_configuration_widgets()
        self.create_frame_for_filenames()
        self.create_frame_for_data_pool()
        self.create_frame_for_data_visual()
        self.create_frame_for_figure_visual()
        self.create_frame_for_axis_visual_x()
        self.create_frame_for_axis_visual_y()
        self.create_frame_for_plot()
        self.root.mainloop()

    def initialize_configuration_widgets(self) -> ConfigWidgets:
        config_widgets: ConfigWidgets = {
            'csvnames': None,
            'data_pool': None,
            'dataset_number': None,
            'data_visual': None,
            'figure_visual': FigureVisualWidgets(),
            'axis_x': AxisVisualWidgets(),
            'axis_y': AxisVisualWidgets()
        }
        return config_widgets

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
        frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, **App.PADS)
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
        button.grid(row=0, column=0, **App.PADS)
        button['font'] = self.font_button
        self.config_widgets['csvnames'] = treeview

    def create_frame_for_data_pool(self):
        frame = tk.LabelFrame(self.root, text='Review CSV data')
        frame.grid(row=1, column=0, rowspan=3, sticky=tk.NSEW, **App.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame['font'] = self.font_label

        notebook = Notebook(frame)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        tab = notebook.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=App.HEIGHT_DATAPOOL)

        button = tk.Button(
            frame,
            text='Import',
            command=lambda: self.import_csv(),
            width=6
        )
        button.grid(row=1, column=0, **App.PADS)
        button['font'] = self.font_button

        button = tk.Button(
            frame,
            text='Clear',
            command=lambda: self.clear_data_pool(),
            width=6
        )
        button.grid(row=1, column=1, **App.PADS)
        button['font'] = self.font_button
        self.config_widgets['data_pool'] = notebook

    def fill_data_visual_widgets(self, tab: Tab):
        label = tk.Label(tab, text='CSV ID: ')
        combobox = ttk.Combobox(tab, width=App.WIDTH_COMBOBOX)
        label.grid(row=0, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=0, column=1, sticky=tk.W, **App.PADS)
        combobox_csv_idx = combobox

        label = tk.Label(tab, text='Field X: ')
        combobox = ttk.Combobox(tab, width=App.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        combobox_field_x = combobox

        label = tk.Label(tab, text='Field Y: ')
        combobox = ttk.Combobox(tab, width=App.WIDTH_COMBOBOX)
        label.grid(row=2, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=2, column=1, sticky=tk.W, **App.PADS)
        combobox_field_y = combobox

        label = tk.Label(tab, text='Label: ')
        entry = tk.Entry(tab, width=App.WIDTH_ENTRY)
        label.grid(row=3, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=3, column=1, sticky=tk.W, **App.PADS)

        widgets = {
            'csv_idx': combobox_csv_idx,
            'field_x': combobox_field_x,
            'field_y': combobox_field_y,
            'label': entry
        }
        tab.widgets = widgets

    def create_frame_for_data_visual(self):
        frame = tk.LabelFrame(self.root, text='Data Visualization')
        frame.grid(row=1, column=1, sticky=tk.NSEW, **App.PADS)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = Notebook(frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        tab = notebook.create_new_tab('1')
        self.fill_data_visual_widgets(tab)

        label = tk.Label(frame, text='Numbers of datasets')
        label.grid(row=0, column=0, **App.PADS)

        spinbox = Spinbox(frame, from_=1, to=20, width=3)
        spinbox.grid(row=0, column=1, **App.PADS)
        spinbox.config(
            command=lambda: self.change_number_of_dataset()
        )
        self.config_widgets['data_visual'] = notebook
        self.config_widgets['dataset_number'] = spinbox

    def create_frame_for_figure_visual(self):
        widgets = self.config_widgets['figure_visual']
        frame = tk.LabelFrame(self.root, text='Figure Visualization')
        frame.grid(row=2, column=1, sticky=tk.NSEW, **App.PADS)

        label = tk.Label(frame, text='Title: ')
        entry = tk.Entry(frame, width=28)
        label.grid(row=0, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=0, column=1, columnspan=3, sticky=tk.W, **App.PADS)
        widgets['title'] = entry

        doublevar = tk.DoubleVar()
        label = tk.Label(frame, text='Width: ')
        entry = tk.Entry(frame, width=8, textvariable=doublevar)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        doublevar.set(4.8)
        widgets['width'] = doublevar

        doublevar = tk.DoubleVar()
        label = tk.Label(frame, text='Height: ')
        entry = tk.Entry(frame, width=8, textvariable=doublevar)
        label.grid(row=1, column=2, sticky=tk.W, **App.PADS)
        entry.grid(row=1, column=3, sticky=tk.W, **App.PADS)
        doublevar.set(2.4)
        widgets['height'] = doublevar

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            frame,
            text='Show grid',
            variable=intvar
        )
        checkbutton.grid(
            row=2, column=0, columnspan=4,
            sticky=tk.W, **App.PADS
        )
        intvar.set(True)
        widgets['grid_visible'] = intvar

        intvar = tk.IntVar()
        checkbutton = tk.Checkbutton(
            frame,
            text='Show legend',
            variable=intvar
        )
        checkbutton.grid(
            row=3, column=0, columnspan=4,
            sticky=tk.W, **App.PADS
        )
        intvar.set(True)
        widgets['legend_visible'] = intvar

    def create_frame_for_axis_visual_x(self):
        widgets = self.config_widgets['axis_x']
        frame = tk.LabelFrame(self.root, text='X-Axis Visualization')
        frame.grid(row=1, column=2, sticky=tk.NSEW, **App.PADS)

        label = tk.Label(frame, text='Label: ')
        entry = tk.Entry(frame, width=28)
        label.grid(row=0, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=0, column=1, sticky=tk.W, **App.PADS)
        widgets['label'] = entry

        label = tk.Label(frame, text='Scale: ')
        combobox = ttk.Combobox(frame, width=App.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        combobox.config(values=['linear', 'log'])
        combobox.current(0)
        widgets['scale'] = combobox

        subframe = tk.Frame(frame)
        subframe.grid(
            row=2, column=0, columnspan=2,
            sticky=tk.NSEW, **App.PADS
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
            sticky=tk.W, **App.PADS
        )
        widgets['assign_range'] = intvar

        label = tk.Label(subframe, text='Min: ')
        entry = tk.Entry(subframe, width=8)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        entry.config(state='disabled')
        widgets['min'] = entry

        label = tk.Label(subframe, text='Max: ')
        entry = tk.Entry(subframe, width=8)
        label.grid(row=2, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=2, column=1, sticky=tk.W, **App.PADS)
        entry.config(state='disabled')
        widgets['max'] = entry

    def create_frame_for_axis_visual_y(self):
        widgets = self.config_widgets['axis_y']
        frame = tk.LabelFrame(self.root, text='Y-Axis Visualization')
        frame.grid(row=2, column=2, sticky=tk.NSEW, **App.PADS)

        label = tk.Label(frame, text='Label: ')
        entry = tk.Entry(frame, width=28)
        label.grid(row=0, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=0, column=1, sticky=tk.W, **App.PADS)
        widgets['label'] = entry

        label = tk.Label(frame, text='Scale: ')
        combobox = ttk.Combobox(frame, width=App.WIDTH_COMBOBOX)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        combobox.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        combobox.config(values=['linear', 'log'])
        combobox.current(0)
        widgets['scale'] = combobox

        subframe = tk.Frame(frame)
        subframe.grid(
            row=2, column=0, columnspan=2,
            sticky=tk.NSEW, **App.PADS
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
            sticky=tk.W, **App.PADS
        )
        widgets['assign_range'] = intvar

        label = tk.Label(subframe, text='Min: ')
        entry = tk.Entry(subframe, width=8)
        label.grid(row=1, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=1, column=1, sticky=tk.W, **App.PADS)
        entry.config(state='disabled')
        widgets['min'] = entry

        label = tk.Label(subframe, text='Max: ')
        entry = tk.Entry(subframe, width=8)
        label.grid(row=2, column=0, sticky=tk.W, **App.PADS)
        entry.grid(row=2, column=1, sticky=tk.W, **App.PADS)
        entry.config(state='disabled')
        widgets['max'] = entry

    def create_frame_for_plot(self):
        frame = tk.LabelFrame(self.root, text='Plot Actions')
        frame.grid(row=3, column=1, columnspan=2, sticky=tk.NSEW, **App.PADS)
        frame.columnconfigure(0, weight=1)
        button = tk.Button(
            frame,
            text='Plot',
            command=lambda: self.plot(),
            width=6
        )
        button.grid(row=0, column=0, **App.PADS)
        button['font'] = self.font_button

    # actions
    def open_files(self):
        treeview = self.config_widgets['csvnames']
        treeview.clear_content()
        csvnames = filedialog.askopenfilenames(
            title='Choose csv files',
            filetypes=[('csv files', '*.csv')]
        )
        self.csvnames = pd.DataFrame(
            [[idx + 1, filename] for idx, filename in enumerate(csvnames)],
            columns=['CSV ID', 'CSV Path']
        )
        treeview.insert_dataframe(self.csvnames)
        treeview.adjust_column_width()

    def update_field_x_and_y(self, tab: Tab):
        csv_idx = int(tab.widgets['csv_idx'].get())
        columns = list(self.data_pool[csv_idx].columns)
        tab.widgets['field_x'].config(values=columns)
        tab.widgets['field_x'].current(0)
        tab.widgets['field_y'].config(values=columns)
        tab.widgets['field_y'].current(1)

    def initialize_tab_widgets(self, tab: Tab):
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
            if not self.config_widgets['csvnames'].get_children():
                raise Exception('No CSV file chosen.')
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)
        else:
            notebook = self.config_widgets['data_pool']
            self.data_pool: Dict[str, pd.DataFrame] = {}
            notebook.remove_all_tabs()
            for row in self.csvnames.itertuples():
                csv_idx, csv_path = row[1:]
                tab = notebook.create_new_tab(csv_idx)
                csv_dataframe = pd.read_csv(csv_path)
                self.data_pool[csv_idx] = csv_dataframe
                columns = list(csv_dataframe.columns)
                treeview = Treeview(tab, columns, App.HEIGHT_DATAPOOL)
                treeview.insert_dataframe(csv_dataframe)
                treeview.adjust_column_width()
            notebook = self.config_widgets['data_visual']
            self.initialize_tab_widgets(notebook.tabs_['1'])

    def clear_data_pool(self):
        notebook = self.config_widgets['data_pool']
        notebook.remove_all_tabs()
        tab = notebook.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=App.HEIGHT_DATAPOOL)

    def change_number_of_dataset(self):
        try:
            self.data_pool
        except AttributeError:
            self.config_widgets['dataset_number'].stringvar.set(1)
            msg = 'Please import data first.'
            tk.messagebox.showerror(title='Error', message=msg)
        else:
            exist_num = len(self.config_widgets['data_visual'].tabs())
            tgt_num = int(self.config_widgets['dataset_number'].get())
            notebook = self.config_widgets['data_visual']
            if tgt_num > exist_num:
                tabname = str(tgt_num)
                tab = notebook.create_new_tab(tabname)
                self.fill_data_visual_widgets(tab)
                self.initialize_tab_widgets(tab)
            elif tgt_num < exist_num:
                tabname = str(exist_num)
                notebook.remove_tab(tabname)

    def active_deactive_range(self):
        widgets = self.config_widgets['axis_x']
        if widgets['assign_range'].get():
            widgets['min'].config(state='normal')
            widgets['max'].config(state='normal')
        else:
            widgets['min'].config(state='disabled')
            widgets['max'].config(state='disabled')

        widgets = self.config_widgets['axis_y']
        if widgets['assign_range'].get():
            widgets['min'].config(state='normal')
            widgets['max'].config(state='normal')
        else:
            widgets['min'].config(state='disabled')
            widgets['max'].config(state='disabled')

    def collect_data_send(self) -> Sequence[pd.DataFrame]:
        data_send = []
        notebook = self.config_widgets['data_visual']
        for tab in notebook.tabs_.values():
            csv_idx = tab.widgets['csv_idx'].get()
            data_send.append(self.data_pool[int(csv_idx)])
        return data_send

    def collect_configurations_data(self):
        labels = self.config_values['data']['labels']
        fieldnames = self.config_values['data']['fieldnames']
        for tab in self.config_widgets['data_visual'].tabs_.values():
            labels.append(tab.widgets['label'].get())
            fieldnames.append({
                'x': tab.widgets['field_x'].get(),
                'y': tab.widgets['field_y'].get()
            })

    def collect_configurations_figure(self):
        widgets = self.config_widgets['figure_visual']
        values = self.config_values['figure']
        values['title'] = widgets['title'].get()
        values['size'] = [
            float(widgets['width'].get()),
            float(widgets['height'].get())
        ]
        values['grid_visible'] = widgets['grid_visible'].get()
        values['legend_visible'] = widgets['legend_visible'].get()

    def collect_configurations_axes(self):
        widgets = self.config_widgets['axis_x']
        values = self.config_values['axis_x']
        values['scale'] = widgets['scale'].get()
        values['label'] = widgets['label'].get()
        if widgets['assign_range'].get():
            values['lim'] = [
                float(widgets['min'].get()),
                float(widgets['max'].get())
            ]
        else:
            values['lim'] = None

        widgets = self.config_widgets['axis_y']
        values = self.config_values['axis_y']
        values['scale'] = widgets['scale'].get()
        values['label'] = widgets['label'].get()
        if widgets['assign_range'].get():
            values['lim'] = [
                float(widgets['min'].get()),
                float(widgets['max'].get())
            ]
        else:
            values['lim'] = None

    def plot(self):
        data_send = self.collect_data_send()
        self.collect_configurations_data()
        self.collect_configurations_figure()
        self.collect_configurations_axes()
        plotting.plot_by_app(self.config_values, data_send)


if __name__ == '__main__':
    App()
