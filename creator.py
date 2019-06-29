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

"""
The creator.py module contains class definitions for coordinates
and various components we add to an airfoil (spars, stringers, and ribs).

Classes:
    Airfoil: instantiated with class method to provide coordinates to heirs.
    Spar: inherits from Airfoil.
    Stringer: also inherits from Airfoil.

Functions:
    plot_geom(airfoil): generates a 2D plot of the airfoil & any components.
"""

import sys
import os.path
import numpy as np
from math import sin, cos, atan, sqrt
import bisect as bi
import matplotlib.pyplot as plt


class Airfoil:
    """
    This class represents a single NACA airfoil.

    Please note: the coordinates are saved as two lists
    for the x- and z-coordinates. The coordinates start at
    the leading edge, travel over the airfoil's upper edge,
    then loop back to the leading edge via the lower edge.

    This method was chosen for easier future exports
    to 3D CAD packages like SolidWorks, which can import such
    geometry as coordinates written in a CSV file.
    """

    # Defaults
    chord = 100
    semi_span = 200

    def __init__(self):
        # mass and area
        self.mass = float()
        self.area = float()
        # Component material
        self.material = str()
        # Coordinates
        self.x = []
        self.z = []

    @classmethod
    def from_dimensions(cls, chord, semi_span):
        cls.chord = chord
        cls.semi_span = semi_span
        return Airfoil()

    def __str__(self):
        return type(self).__name__

    def add_naca(self, naca_num):
        """
        This function generates geometry for a NACA number passed as argument.
        The nested functions perform the required steps to generate geometry,
        and can be called to solve the geometry y-coordinate for any 'x' input.
        Equation coefficients were retrieved from Wikipedia.org.

        Parameters:
        naca_num: 4-digit NACA wing

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
            Returns camber z-coordinate from 1 'x' along the airfoil chord.
            """
            z_c = float()
            if 0 <= x < p_c:
                z_c = (m / (p ** 2)) * (2 * p * (x / self.chord)
                                        - (x / self.chord) ** 2)
            elif p_c <= x <= self.chord:
                z_c = (m / ((1 - p) ** 2)) * ((1 - 2 * p)
                                              + 2 * p * (x / self.chord)
                                              - (x / self.chord) ** 2)
            return (z_c * self.chord)

        def get_thickness(x):
            """Returns thickness from 1 'x' along the airfoil chord."""
            x = 0 if x < 0 else x
            z_t = 5 * t * self.chord * (
                + 0.2969 * sqrt(x / self.chord)
                - 0.1260 * (x / self.chord)
                - 0.3516 * (x / self.chord) ** 2
                + 0.2843 * (x / self.chord) ** 3
                - 0.1015 * (x / self.chord) ** 4)
            return z_t

        def get_theta(x):
            dz_c = float()
            if 0 <= x < p_c:
                dz_c = ((2 * m) / p ** 2) * (p - x / self.chord)
            elif p_c <= x <= self.chord:
                dz_c = (2 * m) / ((1 - p) ** 2) * (p - x / self.chord)
            theta = atan(dz_c)
            return theta

        def get_upper_coord(x):
            x = x - get_thickness(x) * sin(get_theta(x))
            z = get_camber(x) + get_thickness(x) * cos(get_theta(x))
            return (x, z)

        def get_lower_coord(x):
            x = x + get_thickness(x) * sin(get_theta(x))
            z = get_camber(x) - get_thickness(x) * cos(get_theta(x))
            return (x, z)

        # Densify x-coordinates 10 times for first 1/4 chord length
        x_chord_25_percent = round(self.chord / 4)

        x_chord = [i / 10 for i in range(x_chord_25_percent * 10)]
        x_chord.extend(i for i in range(x_chord_25_percent, self.chord + 1))
        # Reversed list for our lower airfoil coordinate densification
        x_chord_rev = [i for i in range(self.chord, x_chord_25_percent, -1)]
        extend = [i / 10 for i in range(x_chord_25_percent * 10, -1, -1)]
        x_chord_rev.extend(extend)

        # Generate our airfoil geometry from previous sub-functions.
        self.x_c = []
        self.z_c = []
        for x in x_chord:
            self.x_c.append(x)
            self.z_c.append(get_camber(x))
            self.x.append(get_upper_coord(x)[0])
            self.z.append(get_upper_coord(x)[1])
        for x in x_chord_rev:
            self.x.append(get_lower_coord(x)[0])
            self.z.append(get_lower_coord(x)[1])
        return None

    def add_mass(self, mass):
        self.mass = mass

    def info_print(self, round):
        """
        Print all the component's coordinates to the terminal.

        This function's output is piped to the 'save_coord' function below.
        """

        name = '    CREATOR DATA    '
        num_of_dashes = len(name)

        print(num_of_dashes * '-')
        print(name)
        print('Component:', str(self))
        print('Chord length:', self.chord)
        print('Semi-span:', self.semi_span)
        print('Mass:', self.mass)
        print(num_of_dashes * '-')
        print('x-coordinates:\n', np.around(self.x, round))
        print('z-coordinates:\n', np.around(self.z, round))
        return None

    def info_save(self, save_path, number):
        """
        Save all the object's coordinates (must be full path).
        """

        file_name = '{}_{}.txt'.format(str(self).lower(), number)
        full_path = os.path.join(save_path, file_name)
        try:
            with open(full_path, 'w') as sys.stdout:
                self.info_print(6)
                # This line required to reset behavior of sys.stdout
                sys.stdout = sys.__stdout__
                print('Successfully wrote to file {}'.format(full_path))
        except IOError:
            print('Unable to write {} to specified directory.\n'
                  .format(file_name),
                  'Was the full path passed to the function?')
        return None


class Spar(Airfoil):
    """Contains a single spar's location."""

    def __init__(self):
        super().__init__()
        self.x_start = []
        self.x_end = []
        self.thickness = float()
        self.z_start = []
        self.z_end = []

    def add_coord(self, airfoil, x_loc_percent):
        """
        Add a single spar at the % chord location given to function.

        Parameters:
        airfoil: gives the spar access to airfoil's coordinates.
        x_loc_percent: spar's location as a % of total chord length.

        Return:
        None
        """

        # Scaled spar location with regards to chord
        loc = x_loc_percent * self.chord
        # bi.bisect_left: returns index of first value in airfoil.x > loc
        # This ensures that spar geom intersects with airfoil geom.
        # Spar upper coordinates
        spar_x = bi.bisect_left(airfoil.x, loc) - 1
        x = [airfoil.x[spar_x]]
        z = [airfoil.z[spar_x]]
        # Spar lower coordinates
        spar_x = bi.bisect_left(airfoil.x[::-1], loc) - 1
        x += [airfoil.x[-spar_x]]
        z += [airfoil.z[-spar_x]]
        self.x.append(x)
        self.z.append(z)
        return None

    def add_spar_caps(self, spar_cap_area):
        self.cap_area = spar_cap_area
        return None

    def add_mass(self, mass):
        self.mass = len(self.x) * mass
        return None

    def add_webs(self, thickness):
        """Add webs to spars."""
        for _ in range(len(self.x)):
            self.x_start.append(self.x[_][0])
            self.x_end.append(self.x[_][1])
            self.z_start.append(self.z[_][0])
            self.z_end.append(self.z[_][1])
        self.thickness = thickness
        return None


class Stringer(Airfoil):
    """Contains the coordinates of all stringers."""

    def __init__(self):
        super().__init__()
        self.x_start = []
        self.x_end = []
        self.thickness = float()
        self.z_start = []
        self.z_end = []
        self.area = float()

    def add_coord(self, airfoil,
                  stringer_u_1, stringer_u_2,
                  stringer_l_1, stringer_l_2):
        """
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
        """

        # Find distance between leading edge and first upper stringer
        interval = airfoil.spar.x[0][0] / (stringer_u_1 + 1)
        # initialise first self.stringer_x at first interval
        x = interval
        # Add upper stringers from leading edge until first spar.
        for _ in range(0, stringer_u_1):
            # Index of the first value of airfoil.x > x
            i = bi.bisect_left(airfoil.x, x)
            self.x.append(airfoil.x[i])
            self.z.append(airfoil.z[i])
            x += interval
        # Add upper stringers from first spar until last spar
        # TODO: stringer placement if only one spar is created
        interval = (airfoil.spar.x[-1][0]
                    - airfoil.spar.x[0][0]) / (stringer_u_2 + 1)
        x = interval + airfoil.spar.x[0][0]
        for _ in range(0, stringer_u_2):
            i = bi.bisect_left(airfoil.x, x)
            self.x.append(airfoil.x[i])
            self.z.append(airfoil.z[i])
            x += interval

        # Find distance between leading edge and first lower stringer
        interval = airfoil.spar.x[0][1] / (stringer_l_1 + 1)
        x = interval
        # Add lower stringers from leading edge until first spar.
        for _ in range(0, stringer_l_1):
            i = bi.bisect_left(airfoil.x[::-1], x)
            self.x.append(airfoil.x[-i])
            self.z.append(airfoil.z[-i])
            x += interval
        # Add lower stringers from first spar until last spar
        interval = (airfoil.spar.x[-1][1]
                    - airfoil.spar.x[0][1]) / (stringer_l_2 + 1)
        x = interval + airfoil.spar.x[0][1]
        for _ in range(0, stringer_l_2):
            i = bi.bisect_left(airfoil.x[::-1], x)
            self.x.append(airfoil.x[-i])
            self.z.append(airfoil.z[-i])
            x += interval
        return None

    def add_area(self, area):
        self.area = area
        return None

    def add_mass(self, mass):
        self.mass = len(self.x) * mass + len(self.x) * mass
        return None

    def add_webs(self, thickness):
        """Add webs to stringers."""
        for _ in range(len(self.x) // 2):
            self.x_start.append(self.x[_])
            self.x_end.append(self.x[_ + 1])
            self.z_start.append(self.z[_])
            self.z_end.append(self.z[_ + 1])
        self.thickness = thickness
        return None

    def info_print(self, round):
        super().info_print(round)
        print('Stringer Area:\n', np.around(self.area, round))
        return None


def plot_geom(airfoil):
    """This function plots the airfoil's + sub-components' geometry."""

    # Plot chord
    x_chord = [0, airfoil.chord]
    y_chord = [0, 0]
    plt.plot(x_chord, y_chord, linewidth='1')
    # Plot quarter chord
    plt.plot(airfoil.chord / 4, 0, '.', color='g',
             markersize=24, label='Quarter-chord')
    # Plot mean camber line
    plt.plot(airfoil.x_c, airfoil.z_c, '-.', color='r', linewidth='2',
             label='Mean camber line')
    # Plot airfoil surfaces
    plt.fill(airfoil.x, airfoil.z, color='b', linewidth='1', fill=False)

    # Plot spars
    try:
        for _ in range(len(airfoil.spar.x)):
            x = (airfoil.spar.x[_])
            y = (airfoil.spar.z[_])
            plt.plot(x, y, '-', color='b')
    except AttributeError:
        print('No spars to plot.')
    # Plot stringers
    try:
        for _ in range(0, len(airfoil.stringer.x)):
            x = airfoil.stringer.x[_]
            y = airfoil.stringer.z[_]
            plt.plot(x, y, '.', color='y', markersize=12)
    except AttributeError:
        print('No stringers to plot.')

    # Graph formatting
    plt.xlabel('X axis')
    plt.ylabel('Z axis')
    plot_bound = max(airfoil.x)
    plt.xlim(- 0.10 * plot_bound, 1.10 * plot_bound)
    plt.ylim(- (1.10 * plot_bound / 2), (1.10 * plot_bound / 2))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().legend()
    plt.grid(axis='both', linestyle=':', linewidth=1)
    plt.show()
    return None


def main():
    return None


if __name__ == '__main__':
    main()
