#
# File Name: Simples_Res.py
# By: Angel Martinez
#
# Last Modified: 04/25/2023
#
# Description:
# Creates a simple UI that can be use in resistance/resistivity data analysis from the outputted text file
# from LR-400 set up given columns in text file are in the form,
# "Temp(Cx)	Temp(Cryo)	R	VDP_Rs	Resistance_Range	Current"
#
#

import tkinter as tk
import tkinter.font
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def data_export(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    # extract x and y data
    x_data = []
    y_data = []
    for line in lines[1:]:  # skip the first two lines
        if len(line.strip().split('\t')) != 6:
            pass
        else:
            temp_cx, temp_cryo, r, vdp_rs, resistance_range, current = line.strip().split('\t')
            x_data.append(float(temp_cx))
            y_data.append(float(r))
    return x_data, y_data


def plot_data(x, y, sh=False):
    px = 1 / plt.rcParams['figure.dpi']
    fig, ax = plt.subplots(figsize=(575 * px, 390 * px))

    ax.set_title("Resistance vs Temp.")
    ax.set_xlabel("T(K)")
    ax.set_ylabel("Resistance(Ohms)")

    plt.scatter(x, y, s=1.5)

    if sh:
        plt.show()

    return fig, ax


class App:
    def __init__(self):
        # Create Windows
        self.window = tk.Tk()
        self.window.title("Resistivity Plot")

        # Create a variable for file name
        self.file = ""

        # Windows Setting
        self.window.geometry("925x425")
        self.window.resizable(width=False, height=False)

        self.w_font = tkinter.font.nametofont("TkDefaultFont")
        self.w_font.config(size=9)

        # Makes Canvas for chart
        self.figure0 = None
        self.figure_canvas = []

        # Stores the main data
        self.main_data = []

        # Create Frames
        self.top_left = tk.Frame(self.window, width=200, height=400)
        self.top_left.grid(row=0, column=0, padx=5, pady=5)

        self.top_right = tk.Frame(self.window, width=300, height=600)
        self.top_right.grid(row=0, column=1, padx=5, pady=5)

        self.main_frame = tk.Frame(self.top_left, width=200, height=200, highlightbackground="black",
                                   highlightthickness=1, borderwidth=2, relief="sunken")
        self.main_frame.grid(row=0, column=0)

        self.the_frame = tk.Frame(self.main_frame, width=200, height=20)
        self.the_frame.grid(row=1, column=0)

        self.folder_frame = tk.Frame(self.the_frame, width=200, height=20)
        self.folder_frame.grid(row=1, column=0)

        self.dropdown_frame = tk.Frame(self.main_frame, width=200, height=20)
        self.dropdown_frame.grid(row=2, column=0)

        # Creates Canvas frame
        self.canvas0 = tk.Canvas(self.top_right, width=580, height=400, borderwidth=2, relief="sunken")
        self.canvas0.grid(row=0, column=0)

        # Labels
        self.title = tk.Label(self.the_frame, text="Resistivity Plot", font=("Courier", 20, "bold"))
        self.title.grid(row=0, column=0)

        self.file = tk.Label(self.folder_frame, text=self.file, width=30)
        self.file.grid(row=0, column=1)

        # Button functions to change file
        def chg_file():
            self.figure0 = None

            path = askopenfilename()
            self.file.config(text=path[:36])

            if path is None:
                messagebox.showerror("Please choose a file.")
                pass

            x, y = data_export(path)

            self.main_data = [x, y]

            self.figure0, _ = plot_data(self.main_data[0], self.main_data[1])

            self.figure_canvas = FigureCanvasTkAgg(self.figure0, master=self.canvas0)
            self.figure_canvas.get_tk_widget().grid(row=0, padx=5, pady=10)

        def save_file():
            self.figure0 = None
            self.figure0, _ = plot_data(self.main_data[0], self.main_data[1], sh=True)

        # Creates Button
        self.folder = tk.Button(self.folder_frame, text="File: ", activebackground='#00ff00', command=chg_file)
        self.folder.grid(row=0, column=0, padx=10, pady=10)
        self.folder.config(width=9)

        self.save = tk.Button(self.folder_frame, text="Save", activebackground='#00ff00', command=save_file)
        self.save.grid(row=1, column=0, padx=10)
        self.save.config(width=9)

        self.window.mainloop()


App()
