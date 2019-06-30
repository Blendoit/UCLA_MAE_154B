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

import creator
import evaluator
import generator
import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


def main():
    root = tk.Tk()
    root.wm_title('MAE 154B - Airfoil Design, Evaluation, Optimization')
    # root.geometry('1000x400')

    # Object definition
    # User inputs
    frame_1 = ttk.Frame(root)
    l_naca = ttk.Label(frame_1, text='NACA Number')
    naca = tk.StringVar()
    e_naca = ttk.Entry(frame_1, textvariable=naca)
    l_chord = ttk.Label(frame_1, text='Chord Length')
    e_chord = ttk.Entry(frame_1)
    af = generator.default_airfoil()
    # Graph window
    frame_2 = ttk.Frame(root)
    fig, ax = creator.plot_geom(af, False)
    plot = FigureCanvasTkAgg(fig, frame_2)
    plot.draw()
    toolbar = NavigationToolbar2Tk(plot, frame_2)
    toolbar.update()

    # Layout
    # User input
    l_naca.grid(row=0, column=0)
    e_naca.grid(row=0, column=1, padx=4)
    l_chord.grid(row=1, column=0)
    e_chord.grid(row=1, column=1, padx=4)
    frame_1.pack(side=tk.LEFT)
    # Graph window
    plot.get_tk_widget().pack(fill=tk.BOTH)
    toolbar.pack()
    frame_2.pack(side=tk.LEFT)

    # plot.get_tk_widget().pack()

    root.mainloop()


if __name__ == '__main__':
    main()
