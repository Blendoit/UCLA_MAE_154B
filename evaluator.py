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
        print(self.airfoil)
        # Global dimensions
        self.chord = airfoil.chord
        self.semi_span = airfoil.semi_span
        # mass and area
        self.mass_total = float(airfoil.mass
                                + airfoil.spar.mass
                                + airfoil.stringer.mass)
        self.mass_dist = []

        self.lift_rectangular = []
        self.lift_elliptical = []
        self.lift = []

        self.drag = []

    def print_info(self, round):
        '''
        Print all the component's evaluated data to the terminal.

        This function's output is piped to the 'save_data' function below.
        '''

        print(22 * '-')
        print('    EVALUATOR DATA    ')
        print('Evaluating:', self.airfoil)
        print('Chord length:', self.chord)
        print('Semi-span:', self.semi_span)
        print('Total airfoil mass:', self.mass_total)
        print('Centroid location:', np.around(self.centroid, round + 1))
        print(22 * '-')
        print('Rectangular lift:\n', np.around(self.lift_rectangular, round))
        print('Elliptical lift:\n', np.around(self.lift_elliptical, round))
        print('Combined lift:\n', np.around(self.lift, round))
        print('Distribution of mass:\n', np.around(self.mass_dist, round))
        print('Drag:\n', np.around(self.drag, round))
        return None

    def save_info(self, save_dir_path, number):
        '''Save all the object's coordinates (must be full path).'''

        file_name = 'airfoil_{}_eval.txt'.format(number)
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

    # def get_mass_total(airfoil):
    #     total_mass = airfoil.mass + airfoil.spar.mass + airfoil.stringer.mass
    #     return total_mass

    # All these functions take integer arguments and return lists.

    def get_lift_rectangular(self, lift):
        L_prime = [lift / (self.semi_span * 2)
                   for x in range(self.semi_span)]
        return L_prime

    def get_lift_elliptical(self, L_0):
        L_prime = [L_0 * sqrt(1 - (y / self.semi_span) ** 2)
                   for y in range(self.semi_span)]
        return L_prime

    def get_lift_total(self):
        F_z = [(self.lift_rectangular[_] + self.lift_elliptical[_]) / 2
               for _ in range(len(self.lift_rectangular))]
        return F_z

    def get_mass_distribution(self, total_mass):
        F_z = [total_mass / self.semi_span
               for x in range(0, self.semi_span)]
        return F_z

    def get_drag(self, drag):
        # Transform semi-span integer into list
        semi_span = [x for x in range(0, self.semi_span)]

        # Drag increases after 80% of the semi_span
        cutoff = round(0.8 * self.semi_span)

        # Drag increases by 25% after 80% of the semi_span
        F_x = [drag for x in semi_span[0:cutoff]]
        F_x.extend([1.25 * drag for x in semi_span[cutoff:]])
        return F_x

    def get_centroid(self):
        area = self.airfoil.stringer.area
        x_stringers = self.airfoil.stringer.x_u + self.airfoil.stringer.x_l
        x_centroid = sum([x * area for x in x_stringers]) / \
            (len(x_stringers) * area)

        z_stringers = self.airfoil.stringer.z_u + self.airfoil.stringer.z_l
        z_centroid = sum([x * area for x in z_stringers]) / \
            (len(x_stringers) * area)
        return(x_centroid, z_centroid)

    def analysis(self):
        '''Perform all analysis calculations and store in class instance.'''

        self.drag = self.get_drag(10)

        self.lift_rectangular = self.get_lift_rectangular(10)
        self.lift_elliptical = self.get_lift_elliptical(15)
        self.lift = self.get_lift_total()

        self.mass_dist = self.get_mass_distribution(self.mass_total)
        self.centroid = self.get_centroid()
        return None

    # denominator
    # z_c =
