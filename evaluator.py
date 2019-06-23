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
from math import sqrt
import matplotlib.pyplot as plt


class Evaluator:
    '''Performs structural evaluations for the airfoil passed as argument.'''

    def __init__(self, airfoil):
        # Evaluator knows all geometrical info from evaluated airfoil
        self.airfoil = airfoil
        self.spar = airfoil.spar
        self.stringer = airfoil.stringer
        # Global dimensions
        self.chord = airfoil.chord
        self.semi_span = airfoil.semi_span

        # mass and area
        self.mass_total = float(airfoil.mass
                                + airfoil.spar.mass
                                + airfoil.stringer.mass)
        self.mass_dist = []
        # Coordinates
        self.x = airfoil.x
        self.z = airfoil.z
        # Lift
        self.lift_rectangular = []
        self.lift_elliptical = []
        self.lift_total = []
        # Drag
        self.drag = []
        # centroid
        self.centroid = []
        # Inertia terms:
        # I_x = self.I_[0]
        # I_z = self.I_[1]
        # I_xz = self.I_[2]
        self.I_ = []

    def info_print(self, round):
        '''
        Print all the component's evaluated data to the terminal.

        This function's output is piped to the 'save_data' function below.
        '''

        name = '    EVALUATOR DATA    '
        num_of_dashes = len(name)

        print(num_of_dashes * '-')
        print(name)
        print('Evaluating:', self.airfoil)
        print('Chord length:', self.chord)
        print('Semi-span:', self.semi_span)
        print('Total airfoil mass:', self.mass_total)
        print('Centroid location:\n', np.around(self.centroid, 3))
        print('Inertia terms:')
        print('I_x:\n', np.around(self.I_[0], 3))
        print('I_z:\n', np.around(self.I_[1], 3))
        print('I_xz:\n', np.around(self.I_[2], 3))
        print(num_of_dashes * '-')
        print('Rectangular lift:\n', np.around(self.lift_rectangular, round))
        print('Elliptical lift:\n', np.around(self.lift_elliptical, round))
        print('Combined lift:\n', np.around(self.lift_total, round))
        print('Distribution of mass:\n', np.around(self.mass_dist, round))
        print('Drag:\n', np.around(self.drag, round))
        return None

    def info_save(self, save_path, number):
        '''Save all the object's coordinates (must be full path).'''

        file_name = 'airfoil_{}_eval.txt'.format(number)
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
        '''Return the coordinates of the centroid.'''

        stringer_area = self.stringer.area
        caps_area = self.spar.cap_area

        caps_x = [value for spar in self.spar.x for value in spar]
        caps_z = [value for spar in self.spar.z for value in spar]
        stringers_x = self.stringer.x
        stringers_z = self.stringer.z

        denominator = float(len(caps_x) * caps_area
                            + len(stringers_x) * stringer_area)

        centroid_x = float(sum([x * caps_area for x in caps_x])
                           + sum([x * stringer_area for x in stringers_x]))
        centroid_x = centroid_x / denominator

        centroid_z = float(sum([z * caps_area for z in caps_z])
                           + sum([z * stringer_area for z in stringers_z]))
        centroid_z = centroid_z / denominator
        return(centroid_x, centroid_z)

    def get_inertia_terms(self):
        '''Obtain all inertia terms.'''

        stringer_area = self.stringer.area
        caps_area = self.spar.cap_area

        # Adds upper and lower components' coordinates to list
        x_stringers = self.stringer.x
        z_stringers = self.stringer.z
        x_spars = self.spar.x[:][0] + self.spar.x[:][1]
        z_spars = self.spar.z[:][0] + self.spar.z[:][1]
        stringer_count = range(len(x_stringers))
        spar_count = range(len(self.spar.x))

        # I_x is the sum of the contributions of the spar caps and stringers
        I_x = (sum([caps_area * (z_spars[i] - self.centroid[1]) ** 2
                    for i in spar_count])
               + sum([stringer_area * (z_stringers[i] - self.centroid[1]) ** 2
                      for i in stringer_count]))

        I_z = (sum([caps_area * (x_spars[i] - self.centroid[0]) ** 2
                    for i in spar_count])
               + sum([stringer_area * (x_stringers[i] - self.centroid[0]) ** 2
                      for i in stringer_count]))

        I_xz = (sum([caps_area * (x_spars[i] - self.centroid[0])
                     * (z_spars[i] - self.centroid[1])
                     for i in spar_count])
                + sum([stringer_area * (x_stringers[i] - self.centroid[0])
                       * (z_stringers[i] - self.centroid[1])
                       for i in stringer_count]))

        return(I_x, I_z, I_xz)

    def analysis(self):
        '''Perform all analysis calculations and store in class instance.'''

        self.drag = self.get_drag(10)

        self.lift_rectangular = self.get_lift_rectangular(1000)
        self.lift_elliptical = self.get_lift_elliptical(15)
        self.lift_total = self.get_lift_total()

        self.mass_dist = self.get_mass_distribution(self.mass_total)
        self.centroid = self.get_centroid()
        self.I_ = self.get_inertia_terms()
        return None


def plot_geom(evaluator):
    '''This function plots analysis results over the airfoil's geometry.'''

    # Plot chord
    x_chord = [0, evaluator.chord]
    y_chord = [0, 0]
    plt.plot(x_chord, y_chord, linewidth='1')
    # Plot quarter chord
    plt.plot(evaluator.chord / 4, 0, '.', color='g',
             markersize=24, label='Quarter-chord')
    # Plot airfoil surfaces
    plt.fill(evaluator.x, evaluator.z, color='b', linewidth='1', fill=False)

    # Plot spars
    try:
        for _ in range(len(evaluator.spar.x)):
            x = (evaluator.spar.x[_])
            y = (evaluator.spar.z[_])
            plt.plot(x, y, '-', color='b')
    except AttributeError:
        print('No spars to plot.')
    # Plot upper stringers
    try:
        for _ in range(0, len(evaluator.stringer.x)):
            x = evaluator.stringer.x[_]
            y = evaluator.stringer.z[_]
            plt.plot(x, y, '.', color='y', markersize=12)
    except AttributeError:
        print('No stringers to plot.')
    # # Plot lower stringers
    # for _ in range(0, len(evaluator.stringer.x)):
    #     x = evaluator.stringer.x[_]
    #     y = evaluator.stringer.z[_]
    #     plt.plot(x, y, '.', color='y', markersize=12)

    # Plot centroid
    x = evaluator.centroid[0]
    y = evaluator.centroid[1]
    plt.plot(x, y, '.', color='r', markersize=24, label='centroid')

    # Graph formatting
    plt.xlabel('X axis')
    plt.ylabel('Z axis')

    plot_bound = max(evaluator.x)
    plt.xlim(- 0.10 * plot_bound, 1.10 * plot_bound)
    plt.ylim(- (1.10 * plot_bound / 2), (1.10 * plot_bound / 2))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().legend()
    plt.grid(axis='both', linestyle=':', linewidth=1)
    plt.show()
    return None


def plot_lift(evaluator):
    x = range(evaluator.semi_span)
    y_1 = evaluator.lift_rectangular
    y_2 = evaluator.lift_elliptical
    y_3 = evaluator.lift_total
    plt.plot(x, y_1, '.', color='b', markersize=4,
             label='Rectangular lift')
    plt.plot(x, y_2, '.', color='g', markersize=4,
             label='Elliptical lift')
    plt.plot(x, y_3, '.', color='r', markersize=4, label='Total lift')

    # Graph formatting
    plt.xlabel('Semi-span location')
    plt.ylabel('Lift')

    plt.gca().legend()
    plt.grid(axis='both', linestyle=':', linewidth=1)
    plt.show()
    return None
