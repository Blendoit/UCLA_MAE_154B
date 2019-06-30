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
import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import numpy as np


root = tk.Tk()
root.wm_title('MAE 154B - Airfoil Design, Evaluation, Optimization')
# root.geometry('1000x400')

# # User inputs
# l_naca = ttk.Label(root, text='NACA Number')
# e_naca = ttk.Entry(root)
# l_chord = ttk.Label(root, text='Chord Length')
# e_chord = ttk.Entry(root)
# # Graph window

fig = Figure()
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# # Layout
# l_naca.grid(row=0, sticky='W')
# e_naca.grid(row=0, column=1)
# l_chord.grid(row=1, sticky='W')
# e_chord.grid(row=1, column=1)

root.mainloop()
