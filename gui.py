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


def make_airfoil():
    """Create airfoil instance."""

    airfoil = creator.Airfoil.from_dimensions(100, 200)
    airfoil.add_naca(2412)
    airfoil.add_mass(10)

    airfoil.spar = creator.Spar()
    airfoil.spar.add_coord(airfoil, 0.23)
    airfoil.spar.add_coord(airfoil, 0.57)
    airfoil.spar.add_spar_caps(0.3)
    airfoil.spar.add_mass(10)
    airfoil.spar.add_webs(0.4)

    airfoil.stringer = creator.Stringer()
    airfoil.stringer.add_coord(airfoil,
                               3,
                               6,
                               5,
                               4)
    airfoil.stringer.add_area(0.1)
    airfoil.stringer.add_mass(5)
    airfoil.stringer.add_webs(0.1)
    return airfoil


def main():
    root = tk.Tk()
    root.wm_title('MAE 154B - Airfoil Design, Evaluation, Optimization')
    # root.geometry('1000x400')

    # # User inputs
    l_naca = ttk.Label(root, text='NACA Number')
    e_naca = ttk.Entry(root)
    l_chord = ttk.Label(root, text='Chord Length')
    e_chord = ttk.Entry(root)
    af = make_airfoil()

    # # Graph window
    fig, ax = creator.plot_geom(af, False)

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # # Layout
    l_naca.pack()
    e_naca.pack()
    l_chord.pack()
    e_chord.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
