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


def main():
    root = tk.Tk()
    root.title('MAE 154B - Airfoil Design, Evaluation, Optimization')
    root.geometry('1000x400')

    frame = ttk.Frame(root).grid(row=0, column=0)
    ttk.Label(frame, text='NACA Number').grid(row=0, sticky='W')
    ttk.Entry(frame).grid(row=0, column=1)
    ttk.Label(frame, text='Chord Length').grid(row=1, sticky='W')
    ttk.Entry(frame).grid(row=1, column=1)

    root.mainloop()
    return None


if __name__ == '__main__':
    main()
