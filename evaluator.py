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


class Airfoil:
    '''Performs structural evaluations for the airfoil passed as argument.'''

    def __init__(self, airfoil):
        self.airfoil = airfoil
        # Global dimensions
        self.chord = airfoil.chord
        self.semi_span = airfoil.semi_span
        # mass and area
        self.mass_total = float()
        self.mass_dist = []

        self.lift_rectangular = []
        self.lift_elliptical = []
        self.lift = []

        self.drag = []

    def __str__(self):
        return type(self).__name__

    def print_info(self, round):
        """
        Print all the component's evaluated data to the terminal.

        This function's output is piped to the 'save_data' function below.
        """
        print('============================')
        print('       EVALUATOR DATA       ')
        print('Evaluating:', str(self.airfoil))
        print('Chord length:', self.chord)
        print('Semi-span:', self.semi_span)
        print('Total airfoil mass:', self.mass_total)
        print('============================')
        print('Rectangular lift:\n', np.around(self.lift_rectangular, round))
        print('Elliptical lift:\n', np.around(self.lift_elliptical, round))
        print('Combined lift:\n', np.around(self.lift, round))
        print('Distribution of mass:\n', np.around(self.mass_dist, round))
        print('Drag:\n', np.around(self.drag, round))
        return None

    def save_info(self, save_dir_path, number):
        """
        Save all the object's coordinates (must be full path).
        """

        file_name = '{}_{}.txt'.format(self, number)
        full_path = os.path.join(save_dir_path, file_name)
        try:
            with open(full_path, 'w') as sys.stdout:
                self.print_info(2)
                # This line required to reset behavior of sys.stdout
                sys.stdout = sys.__stdout__
                print('Successfully wrote to file {}'.format(full_path))
        except IOError:
            print('Unable to write {} to specified directory.\n'
                  .format(file_name),
                  'Was the full path passed to the function?')
        return None

    def get_mass_total(airfoil):
        total_mass = airfoil.mass + airfoil.spar.mass + airfoil.stringer.mass
        return total_mass

    # All these functions take integer arguments and return lists.

    def get_lift_rectangular(airfoil, lift):
        L_prime = [lift / (airfoil.semi_span * 2)
                   for x in range(airfoil.semi_span)]
        return L_prime

    def get_lift_elliptical(airfoil, L_0):
        L_prime = [L_0 * sqrt(1 - (y / airfoil.semi_span) ** 2)
                   for y in range(airfoil.semi_span)]
        return L_prime

    def get_lift(rectangular, elliptical):
        F_z = [(rectangular[_] + elliptical[_]) / 2
               for _ in range(len(rectangular))]
        return F_z

    def get_mass_distribution(airfoil, total_mass):
        F_z = [total_mass / airfoil.semi_span
               for x in range(0, airfoil.semi_span)]
        return F_z

    def get_drag(airfoil, drag):
        # Transform semi-span integer into list
        semi_span = [x for x in range(0, airfoil.semi_span)]

        # Drag increases after 80% of the semi_span
        cutoff = round(0.8 * airfoil.semi_span)

        # Drag increases by 25% after 80% of the semi_span
        F_x = [drag for x in semi_span[0:cutoff]]
        F_x.extend([1.25 * drag for x in semi_span[cutoff:]])
        return F_x

    def evaluate(self):
        self.drag = self.get_drag(self.airfoil, 10)

        self.lift_rectangular = self.get_lift_rectangular(10)
        self.lift_elliptical = self.get_lift_elliptical(15)
        self.lift = self.get_lift(self.lift_rectangular, self.lift_elliptical)

        self.mass_total = self.get_mass_total()
        self.mass_dist = self.get_mass_distribution(self.total_mass)
        return None

# def get_centroid(airfoil):
#     area = airfoil.stringer.area
#     top_stringers = airfoil.stringer
#     bottom_stringers =
#     nose_top_stringers =
#     nose_bottom_stringers =
#     for _ in airfoil.stringer[1]:
#         centroid.x +=

    # denominator
    # z_c =
