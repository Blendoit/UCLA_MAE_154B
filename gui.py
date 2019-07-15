# This file is part of Marius Peter's airfoil analysis package (this program).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from tools import creator, evaluator, generator
# import creator
# import evaluator
# import generator
import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


class MainWindow(tk.Frame):
    """Main editor window."""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        root = tk.Tk()
        root.wm_title('MAE 154B - Airfoil Design, Evaluation, Optimization')

        # self.button = tk.Button(self, text="Create new window",
        #                         command=self.create_window)
        # self.button.pack(side="top")
        frame_1 = ttk.Frame(root)
        l_naca, e_naca = new_field(frame_1, 'naca')
        l_chord, e_chord = new_field(frame_1, 'chord')
        l_semi_span, e_semi_span = new_field(frame_1, 'semi_span')
        af = generator.default_airfoil()
        # Graph window
        frame_2 = ttk.Frame(root)
        fig, ax = creator.plot_geom(af, False)
        plot = FigureCanvasTkAgg(fig, frame_2)
        # plot.draw()
        toolbar = NavigationToolbar2Tk(plot, frame_2)
        # toolbar.update()

        l_naca.grid(row=0, column=0)
        e_naca.grid(row=0, column=1, padx=4)
        # b_naca.grid(row=0, column=2)
        l_chord.grid(row=1, column=0)
        e_chord.grid(row=1, column=1, padx=4)
        l_semi_span.grid(row=2, column=0, padx=4)
        e_semi_span.grid(row=2, column=1, padx=4)
        frame_1.pack(side=tk.LEFT)
        # Graph window
        plot.get_tk_widget().pack(expand=1, fill=tk.BOTH)
        toolbar.pack()
        frame_2.pack(side=tk.LEFT)

    def create_window(self):
        self.counter += 1
        window = tk.Toplevel(self)
        window.wm_title("Window #%s" % self.counter)
        label = tk.Label(window, text="This is window #%s" % self.counter)
        label.pack(side="top", fill="both", expand=True, padx=100, pady=100)


def new_field(parent, name):
    """Add a new user input field."""

    label = ttk.Label(parent, text=name)
    entry = ttk.Entry(parent)
    return label, entry


def set_naca(name):
    naca_num = name.get()
    print(naca_num)


def set_chord(name):
    chord = name.get()
    print(chord)


def set_semi_span(name):
    semi_span = name.get()
    print(semi_span)


# plot.get_tk_widget().pack()
MainWindow().mainloop()
