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
