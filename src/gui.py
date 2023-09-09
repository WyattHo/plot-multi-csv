import tkinter as tk
from tkinter import font
from tkinter import ttk

from kernel import TreeviewTools, NotebookTools, MyAppAction


class MyApp:
    PADS = {
        'padx': 5, 'pady': 5,
        'ipadx': 1, 'ipady': 1,
    }
    ROOT_MINSIZE = {
        'width': 400, 'height': 400
    }

    def __init__(self):
        self.root = self.initialize_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_btn = font.Font(family='Helvetica', size=10)
        self.treeview_csv_names = self.create_frame_for_csv_names()
        self.notebook_csv_data = self.create_frame_for_csv_data()
        self.notebook_curve_settings = self.create_frame_for_curve_settings()
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

    def create_frame_for_csv_names(self) -> ttk.Treeview:
        frame = tk.LabelFrame(self.root, text='Choose CSV files')
        frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame['font'] = self.font_label

        subframe = tk.Frame(frame)
        subframe.grid(row=0, column=0, sticky=tk.NSEW)
        columns = ('CSV ID', 'CSV Path')
        treeview = TreeviewTools.create_treeview(subframe, columns, 5)

        subframe = tk.Frame(frame)
        subframe.grid(row=0, column=1)
        button = tk.Button(
            subframe,
            text='Choose',
            command=lambda: MyAppAction.open_files(treeview),
            width=6
        )
        button.grid(row=0, column=0, **self.PADS)
        button['font'] = self.font_btn
        return treeview

    def create_frame_for_csv_data(self):
        frame = tk.LabelFrame(self.root, text='Review CSV data')
        frame.grid(row=1, column=0, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame['font'] = self.font_label

        notebook = ttk.Notebook(frame)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        tab = NotebookTools.create_new_tab(notebook, tabname='1')
        TreeviewTools.create_treeview(tab, columns=('',), height=25)

        button = tk.Button(
            frame,
            text='Import',
            command=lambda: MyAppAction.import_csv(
                self.treeview_csv_names,
                notebook
            ),
            width=6
        )
        button.grid(row=1, column=0, **self.PADS)
        button['font'] = self.font_btn

        button = tk.Button(
            frame,
            text='Clear',
            command=lambda: MyAppAction.clear_csv_data_notebook(notebook),
            width=6
        )
        button.grid(row=1, column=1, **self.PADS)
        button['font'] = self.font_btn
        return notebook

    def create_frame_for_curve_settings(self):
        frame = tk.LabelFrame(self.root, text='Curve settings')
        frame.grid(row=1, column=1, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = ttk.Notebook(frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        NotebookTools.initialize_notebook_for_curve_settings(
            notebook, MyApp.PADS)

        label = tk.Label(frame, text='Curve numbers')
        label.grid(row=0, column=0, **self.PADS)

        spinbox = tk.Spinbox(
            frame, from_=1, to=20, width=3,
            command=lambda: MyAppAction.adjust_curve_settings_tabs(
                self.notebook_csv_data,
                notebook,
                spinbox,
                MyApp.PADS
            )
        )
        spinbox.grid(row=0, column=1, **self.PADS)
        return notebook

    def create_frame_for_axes_settings(self):
        frame = tk.LabelFrame(self.root, text='Axes settings')
        frame.grid(row=1, column=2, sticky=tk.NSEW, **self.PADS)
        button = tk.Button(
            frame,
            text='Draw',
            command=lambda: MyAppAction.draw(),
            width=6
        )
        button.grid(row=0, column=0, **self.PADS)
        button['font'] = self.font_btn


if __name__ == '__main__':
    MyApp()
