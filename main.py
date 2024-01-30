import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from create_potential import *
from create_plots import *
from solve import *


class Home():
    def __init__(self, root):
        self.root = root
        WIDTH = 1280
        HEIGHT = 700

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg='#f2f2f2')  # Light gray background
        self.canvas.pack()

        Menu(self.root, self.canvas)


class Menu():
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        #Initializations
        self.var_labels = []
        self.case = 0
        self.current_graph = plt.figure()
        plt.xlim([0, 5])
        plt.ylim([0, 5])
        plt.grid(visible=True)
        self.dz = 0.1 * (nm)
        self.V = []
        self.z_mw = []
        self.button_width = 15
        self.button_height = 2

        #Simulation label
        self.sim_title_text = tk.StringVar(self.canvas, value="Simulation")
        self.sim_title_label = tk.Label(self.canvas, textvariable=self.sim_title_text, font=("Helvetica", 16, "bold"))
        self.sim_title_label.place(x=1280 - 300, y=47, anchor='center')  # Centered title

       
        entry_font = ("Helvetica", 12)
        label_font = ("Helvetica", 12, "bold")
        #Mass label-entry
        self.mass_label = tk.Label(self.canvas, text="Mass/Electron_mass:", font=label_font)
        self.mass_label.place(x=1280 - 510, y=60)
        self.mass = tk.StringVar()
        self.mass_entry = tk.Entry(self.canvas, textvariable=self.mass, font=entry_font)
        self.mass_entry.place(x=1280 - 300, y=60)

        #Range label-entry
        self.range_label = tk.Label(self.canvas, text="Range(nm):", font=label_font)
        self.range_label.place(x=1280 - 510, y=90)
        self.range = tk.StringVar()
        self.range_entry = tk.Entry(self.canvas, textvariable=self.range, font=entry_font)
        self.range_entry.place(x=1280 - 300, y=90)

        self.vars = [self.mass, self.range]

        # Buttons
        button_font = ("Helvetica", 12)
        button_bg = '#66c2ff'

        self.qwB = tk.Button(self.canvas, text='Finite Quantum Well', width=self.button_width,
                             height=self.button_height,
                             bg=button_bg, command=lambda: [self.sim_title('Finite Quantum Well'), self.qw_event(1)])
        self.qw = self.canvas.create_window(1280 - 70, 15, window=self.qwB)

        self.hosciB = tk.Button(self.canvas, text='Harmonic Oscillator', width=self.button_width,
                                height=self.button_height,
                                bg=button_bg, command=lambda: [self.sim_title('Harmonic Oscillator'), self.hp_event()])
        self.hosci = self.canvas.create_window(1280 - 200, 15, window=self.hosciB)

        self.ptB = tk.Button(self.canvas, text='Poshl-Teller', width=self.button_width, height=self.button_height,
                             bg=button_bg, command=lambda: [self.sim_title('Poshl-Teller'), self.pt_event()])
        self.pt = self.canvas.create_window(1280 - 330, 15, window=self.ptB)

        self.mwB = tk.Button(self.canvas, text='Multiple Wells', width=self.button_width, height=self.button_height,
                             bg=button_bg, command=lambda: [self.sim_title('Multiple Wells'), self.qw_event(4)])
        self.mw = self.canvas.create_window(1280 - 460, 15, window=self.mwB)

        self.runB = tk.Button(self.canvas, text='RUN', width=self.button_width, height=self.button_height,
                              bg=button_bg, command=lambda: self.run())
        self.runw = self.canvas.create_window(1280 - 250, 600, window=self.runB)

        # Create a frame to embed the plot
        self.plot_frame = ttk.Frame(self.canvas)
        self.plot_frame.place(x=0, y=0, relwidth=0.6, relheight=1)

        self.canvas_fig = FigureCanvasTkAgg(self.current_graph, master=self.plot_frame)
        self.w = NavigationToolbar2TkAgg(self.canvas_fig, self.plot_frame)

        self.canvas_fig_widget = self.canvas_fig.get_tk_widget()
        self.canvas_fig_widget.pack(fill=tk.BOTH, expand=True)
    #Changing the title of each case
    def sim_title(self, text):
        self.sim_title_text.set(text)
    #Reseting the variables
    def clear(self):
        for i in self.var_labels:
            i.destroy()

        self.var_labels = []
        self.vars[2:] = []
    #Harmonic potential 
    def hp_event(self):
        self.clear()
        self.case = 2
        self.omega = tk.StringVar()
        self.omega_label = tk.Label(self.canvas, text="Angular Frequency(rad/s):", font=("Helvetica", 12, "bold"))
        self.omega_label.place(x=1280 - 510, y=120)
        self.omega_entry = tk.Entry(self.canvas, textvariable=self.omega, font=("Helvetica", 12))
        self.omega_entry.place(x=1280 - 300, y=120)
        self.n = tk.StringVar()
        self.n_label = tk.Label(self.canvas, text="Number of eigenstates:", font=("Helvetica", 12, "bold"))
        self.n_label.place(x=1280 - 510, y=150)
        self.n_entry = tk.Entry(self.canvas, textvariable=self.n, font=("Helvetica", 12))
        self.n_entry.place(x=1280 - 300, y=150)
        self.vars.extend([self.omega, self.n])
        self.var_labels.extend([self.omega_label, self.omega_entry, self.n_label, self.n_entry])
    #Poschl-Teller potential 
    def pt_event(self):
        self.clear()
        self.case = 3
        self.lmb = tk.StringVar()
        self.lmb_label = tk.Label(self.canvas, text="Lamda:", font=("Helvetica", 12, "bold"))
        self.lmb_label.place(x=1280 - 510, y=120)
        self.lmb_entry = tk.Entry(self.canvas, textvariable=self.lmb, font=("Helvetica", 12))
        self.lmb_entry.place(x=1280 - 300, y=120)
        self.a = tk.StringVar()
        self.a_label = tk.Label(self.canvas, text="Alpha:", font=("Helvetica", 12, "bold"))
        self.a_label.place(x=1280 - 510, y=150)
        self.a_entry = tk.Entry(self.canvas, textvariable=self.a, font=("Helvetica", 12))
        self.a_entry.place(x=1280 - 300, y=150)
        self.n = tk.StringVar()
        self.n_label = tk.Label(self.canvas, text="Number of eigenstates:", font=("Helvetica", 12, "bold"))
        self.n_label.place(x=1280 - 510, y=180)
        self.n_entry = tk.Entry(self.canvas, textvariable=self.n, font=("Helvetica", 12))
        self.n_entry.place(x=1280 - 300, y=180)
        self.vars.extend([self.lmb,self.a,self.n])
        self.var_labels.extend([self.lmb_label, self.lmb_entry,self.a_entry,self.n_entry])
    #Well potential
    def qw_event(self, n):
        self.clear()
        self.case = n
        self.vmax = tk.StringVar()
        self.Vmax_label = tk.Label(self.canvas, text="Vmax(eV):", font=("Helvetica", 12, "bold"))
        self.Vmax_label.place(x=1280 - 510, y=120)
        self.Vmax_entry = tk.Entry(self.canvas, textvariable=self.vmax, font=("Helvetica", 12))
        self.Vmax_entry.place(x=1280 - 300, y=120)

        self.Vmin_label = tk.Label(self.canvas, text="Vmin(eV):", font=("Helvetica", 12, "bold"))
        self.Vmin_label.place(x=1280 - 510, y=150)
        self.vmin = tk.StringVar()
        self.Vmin_entry = tk.Entry(self.canvas, textvariable=self.vmin, font=("Helvetica", 12))
        self.Vmin_entry.place(x=1280 - 300, y=150)

        self.width_label = tk.Label(self.canvas, text="Width(nm):", font=("Helvetica", 12, "bold"))
        self.width_label.place(x=1280 - 510, y=180)
        self.width = tk.StringVar()
        self.width_entry = tk.Entry(self.canvas, textvariable=self.width, font=("Helvetica", 12))
        self.width_entry.place(x=1280 - 300, y=180)
        self.var_labels.extend(
            [self.Vmax_label, self.Vmin_label, self.width_label, self.Vmax_entry, self.Vmin_entry, self.width_entry])
        self.vars.extend([self.vmax, self.vmin, self.width])

        if self.case == 4:
            self.n = tk.StringVar()
            self.n_label = tk.Label(self.canvas, text="Number of wells:", font=("Helvetica", 12, "bold"))
            self.n_label.place(x=1280 - 510, y=210)
            self.n_entry = tk.Entry(self.canvas, textvariable=self.n, font=("Helvetica", 12))
            self.n_entry.place(x=1280 - 300, y=210)
            self.var_labels.extend([self.n_label,self.n_entry])
            self.vars.append(self.n)
    #Getting data from the entries
    def getData(self, vars):
        data_list = []
        for i in vars:
            data_list.append(float(i.get()))
        return data_list
    #Updating plot
    def update_plot(self):
        # Destroy existing widgets
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create and pack new widgets
        self.canvas_fig = FigureCanvasTkAgg(self.current_graph, master=self.plot_frame)
        self.w = NavigationToolbar2TkAgg(self.canvas_fig, self.plot_frame)
        self.canvas_fig_widget = self.canvas_fig.get_tk_widget()
        self.canvas_fig_widget.pack(fill=tk.BOTH, expand=True)


    #Calling the corresponding functions to solve each case
    def run(self):

    
            standard = [float(self.vars[0].get()), np.arange(-int(self.vars[1].get()) * (nm) / 2,
                                                                 int(self.vars[1].get()) * (nm) / 2 + self.dz, self.dz)]
            data = self.getData(self.vars[2:])


            if self.case == 1:

                self.V = create_qw(standard[1], data[2] * (nm), data[0] * (eV), data[1] * (eV))
                s = solve(standard[1] , self.V, standard[0] * mass_e * (kg), self.dz)
                self.current_graph = plot_qw(s, standard[1], self.V)

            elif self.case == 2:

                self.V = create_hp(standard[1] * (nm), standard[0] * mass_e * (kg), data[0])
                s = solve(standard[1] * (nm), self.V, standard[0] * mass_e * (kg), self.dz)
                self.current_graph = plot_hp(s, standard[1], self.V, int(data[1]))
            elif self.case == 3:


                self.V = create_pt(standard[1]/(nm), data[0], data[1],standard[0] * mass_e * (kg))
                s = solve(standard[1] , self.V, standard[0] * mass_e * (kg), self.dz)
                self.current_graph = plot_pt(s, standard[1] , self.V,int(data[2]))
            elif self.case == 4:

                self.V = create_multi_wells(standard[1], data[2] * (nm), data[0] * (eV), data[1] * (eV), int(data[3]))
                s = solve(standard[1] , self.V, standard[0] * mass_e * (kg), self.dz)
                self.current_graph = plot_qw(s, standard[1], self.V)
            else:
                pass
            self.update_plot()
        


#Main
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1280x700')
    root.resizable(False, False)
    root.title('Schrödinger')

    m = Home(root)
    root.mainloop()
