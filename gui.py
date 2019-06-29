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

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np


def main():
    root = tk.Tk()
    root.title('MAE 154B - Airfoil Design, Evaluation, Optimization')
    root.geometry('1000x400')

    frame = ttk.Frame(root).grid(row=0, column=0)
    ttk.Label(frame, text='NACA Number').grid(row=0, sticky='W')
    ttk.Entry(frame).grid(row=0, column=1)
    ttk.Label(frame, text='Chord Length').grid(row=1, sticky='W')
    ttk.Entry(frame).grid(row=1, column=1)

    # Create airfoil instance
    creator.Coordinates(68, 200)
    af = creator.Airfoil()
    af.add_naca(2412)
    af.add_mass(10)

    af.spar = creator.Spar()
    af.spar.add_coord(af, 0.20)
    af.spar.add_coord(af, 0.65)
    af.spar.add_spar_caps(0.03)
    af.spar.add_mass(0.04)
    af.spar.add_webs(0.02)

    af.stringer = creator.Stringer()
    af.stringer.add_coord(af, 3, 6, 5, 4)
    af.stringer.add_area(0.1)
    af.stringer.add_mass(0.02)
    af.stringer.add_webs(0.03)

    frame = ttk.Frame(root).grid(row=0, column=1)

    fig = plt.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(af.x, af.z)

    canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
    # canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1)

    # toolbar = NavigationToolbar2Tk(canvas, master)
    # toolbar.update()
    # canvas.get_tk_widget().grid(row=0, column=1)

    root.mainloop()
    return None


if __name__ == '__main__':
    main()
