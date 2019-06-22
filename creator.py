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


import sys
import os.path
import numpy as np
from math import sin, cos, atan, sqrt
import bisect as bi
import matplotlib.pyplot as plt


# This variable is required for main.py constant wing dimensions
# to be passed to inheriting classes (Airfoil, Spar, Stringer, Rib).
# This way, we don't have to redeclare our coordinates as parameters for
# our spars, stringers and ribs. This makes for more elegant code.
global parent


class Coordinates:
    '''
    All airfoil components need the following:

    Parameters:
        * Component material
        * Coordinates relative to the chord & semi-span

    Methods:
        * Print component coordinates
        * Save component coordinates to file specified in main.py

    So, all component classes inherit from class Coordinates.
    '''

    def __init__(self, chord, semi_span):
        # Global dimensions
        self.chord = chord if chord > 10 else 10
        self.semi_span = semi_span
        # mass and area
        self.mass = float()
        self.area = float()
        # Component material
        self.material = str()
        # Upper coordinates
        self.x_u = []
        self.z_u = []
        # Lower coordinates
        self.x_l = []
        self.z_l = []
        # Coordinates x_u, z_u, x_l, z_l packed in single list
        self.coord = []

        # The airfoil components know the Coordinates instance's coords
        global parent
        parent = self

    def __str__(self):
        return type(self).__name__

    def print_info(self, round):
        '''
        Print all the component's coordinates to the terminal.

        This function's output is piped to the 'save_coord' function below.
        '''
        print(20 * '-')
        print('    CREATOR DATA    ')
        print('Component:', str(self))
        print('Chord length:', self.chord)
        print('Semi-span:', self.semi_span)
        print('Mass:', self.mass)
        print(20 * '-')
        print('x_u the upper x-coordinates:\n', np.around(self.x_u, round))
        print('z_u the upper z-coordinates:\n', np.around(self.z_u, round))
        print('x_l the lower x-coordinates:\n', np.around(self.x_l, round))
        print('z_l the lower z-coordinates:\n', np.around(self.z_l, round))
        return None

    def save_info(self, save_dir_path, number):
        '''
        Save all the object's coordinates (must be full path).
        '''

        file_name = '{}_{}.txt'.format(str(self).lower(), number)
        full_path = os.path.join(save_dir_path, file_name)
        try:
            with open(full_path, 'w') as sys.stdout:
                self.print_info(6)
                # This line required to reset behavior of sys.stdout
                sys.stdout = sys.__stdout__
                print('Successfully wrote to file {}'.format(full_path))
        except IOError:
            print('Unable to write {} to specified directory.\n'
                  .format(file_name),
                  'Was the full path passed to the function?')
        return None

    def pack_info(self):
        self.coord.append(self.x_u)
        self.coord.append(self.z_u)
        self.coord.append(self.x_l)
        self.coord.append(self.z_l)
        return None


class Airfoil(Coordinates):
    '''This class enables the creation of a single NACA airfoil.'''

    def __init__(self):
        global parent
        # Run 'Coordinates' super class init method with same chord & 1/2 span.
        super().__init__(parent.chord, parent.semi_span)
        # NACA number
        self.naca_num = int()
        # Mean camber line
        self.x_c = []
        self.y_c = []

    def add_naca(self, naca_num):
        '''
        This function generates geometry for our chosen NACA airfoil shape.
        The nested functions perform the required steps to generate geometry,
        and can be called to solve the geometry y-coordinate for any 'x' input.
        Equation coefficients were retrieved from Wikipedia.org.

        Parameters:
        naca_num: 4-digit NACA wing

        Return:
        None
        '''

        # Variables extracted from 'naca_num' argument passed to the function
        self.naca_num = naca_num
        m = int(str(naca_num)[0]) / 100
        p = int(str(naca_num)[1]) / 10
        t = int(str(naca_num)[2:]) / 100
        # x-coordinate of maximum camber
        p_c = p * self.chord

        def get_camber(x):
            '''
            Returns camber y-coordinate from 1 'x' along the airfoil chord.
            '''
            y_c = float()
            if 0 <= x < p_c:
                y_c = (m / (p ** 2)) * (2 * p * (x / self.chord)
                                        - (x / self.chord) ** 2)
            elif p_c <= x <= self.chord:
                y_c = (m / ((1 - p) ** 2)) * ((1 - 2 * p)
                                              + 2 * p * (x / self.chord)
                                              - (x / self.chord) ** 2)
            return (y_c * self.chord)

        def get_thickness(x):
            '''
            Returns thickness from 1 'x' along the airfoil chord.
            '''
            y_t = 5 * t * self.chord * (
                + 0.2969 * sqrt(x / self.chord)
                - 0.1260 * (x / self.chord)
                - 0.3516 * (x / self.chord) ** 2
                + 0.2843 * (x / self.chord) ** 3
                - 0.1015 * (x / self.chord) ** 4)
            return y_t

        def get_theta(x):
            dy_c = float()
            if 0 <= x < p_c:
                dy_c = ((2 * m) / p ** 2) * (p - x / self.chord)
            elif p_c <= x <= self.chord:
                dy_c = (2 * m) / ((1 - p) ** 2) * (p - x / self.chord)
            theta = atan(dy_c)
            return theta

        def get_upper_coord(x):
            x_u = x - get_thickness(x) * sin(get_theta(x))
            z_u = get_camber(x) + get_thickness(x) * cos(get_theta(x))
            return (x_u, z_u)

        def get_lower_coord(x):
            x_l = x + get_thickness(x) * sin(get_theta(x))
            z_l = get_camber(x) - get_thickness(x) * cos(get_theta(x))
            return (x_l, z_l)

        # Densify x-coordinates 10 times for first 1/4 chord length
        x_chord_25_percent = round(self.chord / 4)
        x_chord = [x / 10 for x in range(x_chord_25_percent * 10)]
        x_chord.extend([x for x in range(x_chord_25_percent, self.chord + 1)])

        # Generate our airfoil geometry from previous sub-functions.
        for x in x_chord:
            self.x_c.append(x)
            self.y_c.append(get_camber(x))
            self.x_u.append(get_upper_coord(x)[0])
            self.z_u.append(get_upper_coord(x)[1])
            self.x_l.append(get_lower_coord(x)[0])
            self.z_l.append(get_lower_coord(x)[1])

        super().pack_info()
        return None

    def add_mass(self, mass):
        self.mass = mass

    def print_info(self, round):
        super().print_info(round)
        print('x_c the camber x-coordinates:\n', np.around(self.x_u, round))
        print('z_c the camber z-coordinates:\n', np.around(self.x_u, round))
        return None


class Spar(Coordinates):
    '''Contains a single spar's location.'''
    global parent

    def __init__(self):
        super().__init__(parent.chord, parent.semi_span)

    def add_coord(self, airfoil_coord, spar_x):
        '''
        Add a single spar at the % chord location given to function.

        Parameters:
        coordinates: provided by Airfoil.coordinates[x_u, z_u, x_l, z_l].
        material: spar's material. Assumes homogeneous material.
        spar_x: spar's location as a % of total chord length.

        Return:
        None
        '''
        # Airfoil surface coordinates
        # unpacked from 'coordinates' (list of lists in 'Coordinates').
        x_u = airfoil_coord[0]
        z_u = airfoil_coord[1]
        x_l = airfoil_coord[2]
        z_l = airfoil_coord[3]
        # Scaled spar location with regards to chord
        loc = spar_x * self.chord
        # bisect_left: returns index of first value in x_u > loc.
        # Ensures that the spar coordinates intersect with airfoil surface.
        spar_x_u = bi.bisect_left(x_u, loc)  # index of spar's x_u
        spar_x_l = bi.bisect_left(x_l, loc)  # index of spar's x_l
        # These x and y coordinates are assigned to the spar, NOT airfoil.
        self.x_u.append(x_u[spar_x_u])
        self.z_u.append(z_u[spar_x_u])
        self.x_l.append(x_l[spar_x_l])
        self.z_l.append(z_l[spar_x_l])

        super().pack_info()
        return None

    def add_mass(self, mass):
        self.mass = len(self.x_u) * mass


class Stringer(Coordinates):
    '''Contains the coordinates of all stringers.'''
    global parent

    def __init__(self):
        super().__init__(parent.chord, parent.semi_span)
        self.area = float()

    def add_coord(self, airfoil_coord, spar_coord,
                  stringer_u_1, stringer_u_2, stringer_l_1, stringer_l_2):
        '''
        Add equally distributed stringers to four airfoil locations
        (upper nose, lower nose, upper surface, lower surface).

        Parameters:
        airfoil_coord: packed airfoil coordinates
        spar_coord: packed spar coordinates
        stringer_u_1: upper nose number of stringers
        stringer_u_2: upper surface number of stringers
        stringer_l_1: lower nose number of stringers
        stringer_l_2: lower surface number of stringers

        Returns:
        None
        '''

        # Airfoil surface coordinates
        # unpacked from 'coordinates' (list of lists in 'Coordinates').
        airfoil_x_u = airfoil_coord[0]
        airfoil_z_u = airfoil_coord[1]
        airfoil_x_l = airfoil_coord[2]
        airfoil_z_l = airfoil_coord[3]
        # Spar coordinates
        # unpacked from 'coordinates' (list of lists in 'Coordinates').
        spar_x_u = spar_coord[0]
        spar_z_u = spar_coord[1]
        spar_x_l = spar_coord[2]
        spar_z_l = spar_coord[3]

        # Find distance between leading edge and first upper stringer
        interval = spar_x_u[0] / (stringer_u_1 + 1)
        # initialise first self.stringer_x_u at first interval
        x = interval
        # Add upper stringers from leading edge until first spar.
        for _ in range(0, stringer_u_1):
            # Index of the first value of airfoil_x_u > x
            index = bi.bisect_left(airfoil_x_u, x)
            self.x_u.append(airfoil_x_u[index])
            self.z_u.append(airfoil_z_u[index])
            x += interval
        # Add upper stringers from first spar until last spar
        interval = (spar_x_u[-1] - spar_x_u[0]) / (stringer_u_2 + 1)
        x = interval + spar_x_u[0]
        for _ in range(0, stringer_u_2):
            index = bi.bisect_left(airfoil_x_u, x)
            self.x_u.append(airfoil_x_u[index])
            self.z_u.append(airfoil_z_u[index])
            x += interval

        # Find distance between leading edge and first lower stringer
        interval = spar_x_l[0] / (stringer_l_1 + 1)
        x = interval
        # Add lower stringers from leading edge until first spar.
        for _ in range(0, stringer_l_1):
            index = bi.bisect_left(airfoil_x_l, x)
            self.x_l.append(airfoil_x_l[index])
            self.z_l.append(airfoil_z_l[index])
            x += interval
        # Add lower stringers from first spar until last spar
        interval = (spar_x_l[-1] - spar_x_l[0]) / (stringer_l_2 + 1)
        x = interval + spar_x_l[0]
        for _ in range(0, stringer_l_2):
            index = bi.bisect_left(airfoil_x_l, x)
            self.x_l.append(airfoil_x_l[index])
            self.z_l.append(airfoil_z_l[index])
            x += interval
        super().pack_info()
        return None

    def add_area(self, area):
        self.area = area
        return None

    def add_mass(self, mass):
        self.mass = len(self.x_u) * mass + len(self.x_l) * mass
        return None

    def print_info(self, round):
        super().print_info(round)
        print('Stringer Area:\n', np.around(self.area, round))
        return None


def plot(airfoil, spar, stringer):
    '''This function plots the elements passed as arguments.'''

    # Plot chord
    x_chord = [0, airfoil.chord]
    y_chord = [0, 0]
    plt.plot(x_chord, y_chord, linewidth='1')
    # Plot quarter chord
    plt.plot(airfoil.chord / 4, 0, '.', color='g')
    # Plot mean camber line
    plt.plot(airfoil.x_c, airfoil.y_c,
             '-.', color='r', linewidth='2',
             label='mean camber line')
    # Plot upper surface
    plt.plot(airfoil.x_u, airfoil.z_u,
             '', color='b', linewidth='1')
    # Plot lower surface
    plt.plot(airfoil.x_l, airfoil.z_l,
             '', color='b', linewidth='1')

    # Plot spars
    for _ in range(0, len(spar.x_u)):
        x = (spar.x_u[_], spar.x_l[_])
        y = (spar.z_u[_], spar.z_l[_])
        plt.plot(x, y, '.-', color='b')

    # Plot stringers
    # Upper stringers
    for _ in range(0, len(stringer.x_u)):
        x = stringer.x_u[_]
        y = stringer.z_u[_]
        plt.plot(x, y, '.', color='y')
    # Lower stringers
    for _ in range(0, len(stringer.x_l)):
        x = stringer.x_l[_]
        y = stringer.z_l[_]
        plt.plot(x, y, '.', color='y')

    # Graph formatting
    plt.xlabel('X axis')
    plt.ylabel('Z axis')

    plot_bound = airfoil.x_u[-1]
    plt.xlim(- 0.10 * plot_bound, 1.10 * plot_bound)
    plt.ylim(- (1.10 * plot_bound / 2), (1.10 * plot_bound / 2))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(axis='both', linestyle=':', linewidth=1)
    plt.show()
    return None


def main():
    return None


if __name__ == '__main__':
    main()
