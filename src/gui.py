import tkinter as tk
from tkinter import font
from tkinter import ttk

import kernel


class MyApp:
    PADS = {
        'padx': 5, 'pady': 5,
        'ipadx': 1, 'ipady': 1,
    }
    ROOT_MINSIZE = {
        'width': 400, 'height': 400
    }

    def __init__(self):
        self.root = self.initial_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_btn = font.Font(family='Helvetica', size=10)
        self.treeview_filenames = self.create_directory_frame()
        self.notebook_data = self.create_data_frame()
        self.create_curve_frame()
        self.create_axes_frame()
        self.root.mainloop()

    def initial_main_window(self) -> tk.Tk:
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

    def create_directory_frame(self) -> ttk.Treeview:
        frame = tk.LabelFrame(self.root, text='Choose csv files')
        frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, **self.PADS)
        frame['font'] = self.font_label

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
        button.grid(row=0, column=0, **self.PADS)
        button['font'] = self.font_btn
        return treeview

    def create_data_frame(self):
        frame = tk.LabelFrame(self.root, text='Review data')
        frame.grid(row=1, column=0, sticky=tk.NSEW, **self.PADS)
        frame['font'] = self.font_label

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook = ttk.Notebook(frame)
        notebook.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        kernel.initial_tabs_with_treeview(notebook)

        import_btn = tk.Button(
            frame,
            text='Import',
            command=lambda: kernel.import_csv(
                self.treeview_filenames,
                notebook
            ),
            width=6
        )
        import_btn.grid(row=1, column=0, **self.PADS)
        import_btn['font'] = self.font_btn

        clear_btn = tk.Button(
            frame,
            text='Clear',
            command=lambda: kernel.initial_tabs_with_treeview(notebook),
            width=6
        )
        clear_btn.grid(row=1, column=1, **self.PADS)
        clear_btn['font'] = self.font_btn
        return notebook

    def create_curve_frame(self):
        frame = tk.LabelFrame(self.root, text='Curve settings')
        frame.grid(row=1, column=1, sticky=tk.NSEW, **self.PADS)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        notebook_curve = ttk.Notebook(frame)
        notebook_curve.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        kernel.initial_tabs_with_frame(notebook_curve)

        label = tk.Label(frame, text='Curve numbers')
        label.grid(row=0, column=0, **self.PADS)

        spinbox = tk.Spinbox(
            frame, from_=1, to=20, width=3,
            command=lambda: kernel.create_curve_tab(
                self.notebook_data,
                notebook_curve,
                spinbox
            )
        )
        spinbox.grid(row=0, column=1, **self.PADS)

    def create_axes_frame(self):
        frame = tk.LabelFrame(self.root, text='Axes settings')
        frame.grid(row=1, column=2, sticky=tk.NSEW, **self.PADS)
        button = tk.Button(
            frame,
            text='Draw',
            command=lambda: kernel.draw(),
            width=6
        )
        button.grid(row=0, column=0, **self.PADS)
        button['font'] = self.font_btn


if __name__ == '__main__':
    MyApp()
