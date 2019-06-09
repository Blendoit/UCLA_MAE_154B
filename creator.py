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
from math import sin, cos, tan, atan, sqrt, ceil
import bisect as bi
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

# This variable is required for main.py constant wing dimensions
# to be passed to inheriting classes (Airfoil, Spar, Stringer, Rib).
# This way, we don't have to redeclare our coordinates as parameters for
# our spars, stringers and ribs. This makes for more elegant code.
global parent


class Coordinates:
    """
    All airfoil components need the following:

    Parameters:
        * Component material
        * Coordinates relative to the chord & semi-span.

    Methods:
        * Print component coordinates
        * Save component coordinates to file specified in main.py

    So, all component classes inherit from class Coordinates.
    """

    def __init__(self, chord, semi_span):
        # Global dimensions
        self.chord = chord
        if chord < 10:
            self.chord = 10
        self.semi_span = semi_span
        # Component material
        self.material = str()
        # Upper coordinates
        self.x_u = []
        self.y_u = []
        # Lower coordinates
        self.x_l = []
        self.y_l = []
        # Coordinates x_u, y_u, x_l, y_l packed in single list
        self.coordinates = []
        global parent
        parent = self

    def print_coord(self, round):
        """
        Print all the component's coordinates to the terminal.

        This function's output is piped to the 'save_coord' function below.
        """
        print('============================')
        print('Component:', type(self).__name__)
        print('Chord length:', self.chord)
        print('Semi-span:', self.semi_span)
        print('============================')
        print('x_u the upper x-coordinates:',
              np.around(self.x_u, round),
              sep='\n')
        print('y_u the upper y-coordinates:',
              np.around(self.y_u, round),
              sep='\n')
        print('x_l the lower x-coordinates:',
              np.around(self.x_l, round),
              sep='\n')
        print('y_l the lower y-coordinates:',
              np.around(self.y_l, round),
              sep='\n')
        print('\n')
        return None

    def save_coord(self, save_dir_path):
        """
        Save all the object's coordinates (must be full path).
        """
        file_name = str(type(self).__name__)
        full_path = os.path.join(save_dir_path, file_name + '.txt')
        file = open(full_path, 'w')
        sys.stdout = file
        self.print_coord(4)
        return None


class Airfoil(Coordinates):
    """This class enables the creation of a single NACA airfoil."""

    def __init__(self):
        global parent
        # Run 'Coordinates' super class init method with same chord & 1/2 span.
        super().__init__(parent.chord, parent.semi_span)
        # NACA number
        self.naca_num = int()
        # Mean camber line
        self.x_c = []  # Contains only integers from 0 to self.chord
        self.y_c = []  # Contains floats
        # Thickness
        self.y_t = []
        # dy_c / d_x
        self.dy_c = []
        # Theta
        self.theta = []

    def naca(self, naca_num):
        """
        This function generates geometry for our chosen NACA airfoil shape.\
        The nested functions perform the required steps to generate geometry,\
        and can be called to solve the geometry y-coordinate for any 'x' input.\
        Equation coefficients were retrieved from Wikipedia.org.

        Parameters:
        naca_num: 4-digit NACA wing
        chord: wing chord length, in any unit

        Return:
        None
        """

        # Variables extracted from 'naca_num' argument passed to the function
        self.naca_num = naca_num
        m = int(str(naca_num)[0]) / 100
        p = int(str(naca_num)[1]) / 10
        t = int(str(naca_num)[2:]) / 100
        # x-coordinate of maximum camber
        p_c = p * self.chord

        def get_camber(x):
            """
            Returns 1 camber y-coordinate from 1 'x' along the airfoil chord.
            """
            x_c = x
            y_c = float()
            if 0 <= x < p_c:
                y_c = (m / (p**2)) * (2 * p * (x / self.chord) -
                                      (x / self.chord)**2)
            elif p_c <= x <= self.chord:
                y_c = (m /
                       ((1 - p)**2)) * ((1 - 2 * p) + 2 * p *
                                        (x / self.chord) - (x / self.chord)**2)
            else:
                print('x-coordinate for camber is out of bounds. '
                      'Check that 0 < x <= chord.')
            return (x_c, y_c * self.chord)

        def get_thickness(x):
            """
            Returns thickness from 1 'x' along the airfoil chord.
            """
            y_t = float()
            if 0 <= x <= self.chord:
                y_t = 5 * t * self.chord * (0.2969 * sqrt(x / self.chord) -
                                            0.1260 *
                                            (x / self.chord) - 0.3516 *
                                            (x / self.chord)**2 + 0.2843 *
                                            (x / self.chord)**3 - 0.1015 *
                                            (x / self.chord)**4)
            else:
                print('x-coordinate for thickness is out of bounds. '
                      'Check that 0 < x <= chord.')
            return y_t

        def get_dy_c(x):
            """
            Returns dy_c/dx from 1 'x' along the airfoil chord.
            """
            dy_c = float()
            if 0 <= x < p_c:
                dy_c = ((2 * m) / p**2) * (p - x / self.chord)
            elif p_c <= x <= self.chord:
                dy_c = (2 * m) / ((1 - p)**2) * (p - x / self.chord)
            return dy_c

        def get_theta(dy_c):
            theta = atan(dy_c)
            return theta

        def get_upper_coordinates(x):
            x_u = float()
            y_u = float()
            if 0 <= x < self.chord:
                x_u = x - self.y_t[x] * sin(self.theta[x])
                y_u = self.y_c[x] + self.y_t[x] * cos(self.theta[x])
            elif x == self.chord:
                x_u = x - self.y_t[x] * sin(self.theta[x])
                y_u = 0  # Make upper curve finish at y = 0
            return (x_u, y_u)

        def get_lower_coordinates(x):
            x_l = float()
            y_l = float()
            if 0 <= x < self.chord:
                x_l = (x + self.y_t[x] * sin(self.theta[x]))
                y_l = (self.y_c[x] - self.y_t[x] * cos(self.theta[x]))
            elif x == self.chord:
                x_l = (x + self.y_t[x] * sin(self.theta[x]))
                y_l = 0  # Make lower curve finish at y = 0
            return (x_l, y_l)

        # Generate all our wing geometries from previous sub-functions
        for x in range(0, self.chord + 1):
            self.x_c.append(get_camber(x)[0])
            self.y_c.append(get_camber(x)[1])
            self.y_t.append(get_thickness(x))
            self.dy_c.append(get_dy_c(x))
            self.theta.append(get_theta(self.dy_c[x]))
            self.x_u.append(get_upper_coordinates(x)[0])
            self.y_u.append(get_upper_coordinates(x)[1])
            self.x_l.append(get_lower_coordinates(x)[0])
            self.y_l.append(get_lower_coordinates(x)[1])

        self.coordinates.append(self.x_u)
        self.coordinates.append(self.y_u)
        self.coordinates.append(self.x_l)
        self.coordinates.append(self.y_l)

        return None


class Spar(Coordinates):
    """Contains a single spar's location and material."""
    global parent

    # Blendo

    def __init__(self):
        super().__init__(parent.chord, parent.semi_span)

    def add_spar(self, coordinates, material, spar_x):
        """
        Add a single spar at the % chord location given to function.

        Parameters:
        coordinates: provided by Airfoil.coordinates[x_u, y_u, x_l, y_l].
        material: spar's material. Assumes homogeneous material.
        spar_x: spar's location as a % of total chord length.

        Return:
        None
        """
        # Airfoil surface coordinates
        # unpacked from 'coordinates' (list of lists in 'Airfoil').
        x_u = coordinates[0]
        y_u = coordinates[1]
        x_l = coordinates[2]
        y_l = coordinates[3]
        # Scaled spar location with regards to chord
        loc = spar_x * self.chord
        # bisect_left: returns index of first value in x_u > loc.
        # This ensures that the spar coordinates intersect with airfoil surface.
        spar_x_u = bi.bisect_left(x_u, loc)  # index of spar's x_u
        spar_x_l = bi.bisect_left(x_l, loc)  # index of spar's x_l
        # These x and y coordinates are assigned to the spar, NOT airfoil.
        self.x_u.append(x_u[spar_x_u])
        self.y_u.append(y_u[spar_x_u])
        self.x_l.append(x_l[spar_x_l])
        self.y_l.append(y_l[spar_x_l])
        self.spar_material = material
        return None


class Stringer():
    """Contains the coordinates of stringer(s) location and material."""

    def __init__(self):
        # Stringer attributes
        self.stringer_x_u = []
        self.stringer_y_u = []
        self.stringer_x_l = []
        self.stringer_y_l = []
        self.stringer_mat = []

    def add_stringers(self, material, *density):
        """
        Add stringers to the wing from their distribution density between spars.
        First half of density[] concerns stringer distribution on

        Parameters:
        material: stringer material
        *density:

        """

        # Find interval between leading edge and first upper stringer,
        # from density parameter den_u_1.
        interval = self.spar_x_u[0] / (den_u_1 * self.spar_x_u[0])
        # initialise first self.stringer_x_u at first interval.
        x = interval
        # Add upper stringers until first spar.
        while x < self.spar_x_u[0]:
            # Index of the first value of self.x_u > x
            x_u = bi.bisect_left(self.x_u, x)
            self.stringer_x_u.append(self.x_u[x_u])
            self.stringer_y_u.append(self.y_u[x_u])
            x += interval

        # Find interval between leading edge and first lower stringer,
        # from density parameter den_l_1.
        interval = self.spar_x_u[0] / (den_l_1 * self.spar_x_u[0])
        # initialise first self.stringer_x_l at first interval.
        x = interval
        # Add lower stringers until first spar.
        while x < self.spar_x_l[0]:
            # Index of the first value of self.x_l > x
            x_u = bi.bisect_left(self.x_l, x)
            self.stringer_x_l.append(self.x_l[x_u])
            self.stringer_y_l.append(self.y_l[x_u])
            x += interval
        return None


def plot(airfoil, spar):
    """This function plots the elements passed as arguments."""

    print('Plotting airfoil.')
    # Plot chord
    x_chord = [0, airfoil.chord]
    y_chord = [0, 0]
    plt.plot(x_chord, y_chord, linewidth='1')
    # Plot mean camber line
    plt.plot(airfoil.x_c,
             airfoil.y_c,
             '-.',
             color='r',
             linewidth='2',
             label='mean camber line')
    # Plot upper surface
    plt.plot(airfoil.x_u, airfoil.y_u, '', color='b', linewidth='1')
    # Plot lower surface
    plt.plot(airfoil.x_l, airfoil.y_l, '', color='b', linewidth='1')
    # Plot spars
    try:
        for _ in range(0, len(spar.x_u)):
            x = (spar.spar_x_u[_], spar.spar_x_l[_])
            y = (spar.spar_y_u[_], spar.spar_y_l[_])
            plt.plot(x, y, '.-', color='b', label='spar')
            plt.legend()
    except:
        print('Did not plot spars. Were they added?')
    # Plot stringers
    # if len(self.spar_x) != 0:
    #     for _ in range(0, len(self.stringer_x)):
    #         x = (self.stringer_x[_], self.stringer_x[_])
    #         y = (self.stringer_y_u[_], self.stringer_y_l[_])
    #         plt.scatter(x, y, color='y', linewidth='1',
    # else:
    #     print('Unable to plot stringers. Were they created?')
    # Graph formatting
    plt.gcf().set_size_inches(9, 2.2)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    # plt.gcf().set_size_inches(self.chord, max(self.y_u) - min(self.y_l))
    plt.grid(axis='both', linestyle=':', linewidth=1)
    plt.show()
    return None


def main():
    return None


if __name__ == '__main__':
    main()
