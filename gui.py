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


import tkinter as tk
from tkinter import ttk


class Input:
    '''User inputs.'''

    def __init__(self, master):
        ttk.Frame(master).grid(row=0, column=0)
        ttk.Label(master, text='NACA Number').grid(row=0, sticky='W')
        ttk.Label(master, text='Chord Length').grid(row=1, sticky='W')
        ttk.Entry(master).grid(row=0, column=1)
        ttk.Entry(master).grid(row=1, column=1)


class Graph:
    '''Graph airfoil.'''

    def __init__(self, master):
        ttk.Frame(master).grid(row=0, column=1)


def main():
    root = tk.Tk()
    root.title('MAE 154B - Airfoil Design, Evaluation, Optimization')
    root.geometry('1000x400')

    Input(root)
    Graph(root)
    root.mainloop()
    return None


if __name__ == '__main__':
    main()
