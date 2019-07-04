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
The evaluator.py module contains a single Evaluator class,
which knows all the attributes of a specified Airfoil instance,
and contains functions to analyse the airfoil's geometrical
& structural properties.
"""

import sys
import os.path
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt


class Evaluator:
    """Performs structural evaluations for the airfoil passed as argument."""

    def __init__(self, airfoil):
        # Evaluator knows all geometrical info from evaluated airfoil
        self.airfoil = airfoil
        self.spar = airfoil.spar
        self.stringer = airfoil.stringer
        # Global dimensions
        self.chord = airfoil.chord
        self.semi_span = airfoil.semi_span
        # Mass & spanwise distribution
        self.mass_total = float(airfoil.mass
                                + airfoil.spar.mass
                                + airfoil.stringer.mass)
        self.mass_dist = []
        # Lift
        self.lift_rectangular = []
        self.lift_elliptical = []
        self.lift_total = []
        # Drag
        self.drag = []
        # centroid
        self.centroid = []
        # Inertia terms:
        self.I_ = {'x': 0, 'z': 0, 'xz': 0}

    def __str__(self):
        return type(self).__name__

    def info_print(self, round):
        """Print all the component's evaluated data to the terminal."""
        name = '    EVALUATOR DATA FOR {}    '.format(str(self).upper())
        num_of_dashes = len(name)
        print(num_of_dashes * '-')
        print(name)
        for k, v in self.__dict__.items():
            if type(v) != list:
                print('{}:\n'.format(k), v)
        print(num_of_dashes * '-')
        for k, v in self.__dict__.items():
            if type(v) == list:
                print('{}:\n'.format(k), np.around(v, round))
        return None

    def info_save(self, save_path, number):
        """Save all the object's coordinates (must be full path)."""
        file_name = 'airfoil_{}_eval.txt'.format(number)
        full_path = os.path.join(save_path, file_name)
        try:
            with open(full_path, 'w') as sys.stdout:
                self.info_print(6)
                # This line required to reset behavior of sys.stdout
                sys.stdout = sys.__stdout__
                print('Successfully wrote to file {}'.format(full_path))
        except IOError:
            print(
                'Unable to write {} to specified directory.\n'.format(
                    file_name), 'Was the full path passed to the function?')
        return None

    # All these functions take integer arguments and return lists.

    def get_lift_rectangular(self, lift):
        L_prime = [lift / (self.semi_span * 2) for x in range(self.semi_span)]
        return L_prime

    def get_lift_elliptical(self, L_0):
        L_prime = [
            L_0 / (self.semi_span * 2) * sqrt(1 - (y / self.semi_span)**2)
            for y in range(self.semi_span)
        ]
        return L_prime

    def get_lift_total(self):
        F_z = [(self.lift_rectangular[_] + self.lift_elliptical[_]) / 2
               for _ in range(len(self.lift_rectangular))]
        return F_z

    def get_mass_distribution(self, total_mass):
        F_z = [total_mass / self.semi_span for x in range(0, self.semi_span)]
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
        """Return the coordinates of the centroid."""
        stringer_area = self.stringer.area
        cap_area = self.spar.cap_area

        caps_x = [value for spar in self.spar.x for value in spar]
        caps_z = [value for spar in self.spar.z for value in spar]
        stringers_x = self.stringer.x
        stringers_z = self.stringer.z

        denominator = float(len(caps_x) * cap_area
                            + len(stringers_x) * stringer_area)

        centroid_x = float(sum([x * cap_area for x in caps_x])
                           + sum([x * stringer_area for x in stringers_x]))
        centroid_x = centroid_x / denominator

        centroid_z = float(sum([z * cap_area for z in caps_z])
                           + sum([z * stringer_area for z in stringers_z]))
        centroid_z = centroid_z / denominator

        return (centroid_x, centroid_z)

    def get_inertia_terms(self):
        """Obtain all inertia terms."""
        stringer_area = self.stringer.area
        cap_area = self.spar.cap_area

        # Adds upper and lower components' coordinates to list
        x_stringers = self.stringer.x
        z_stringers = self.stringer.z
        x_spars = self.spar.x[:][0] + self.spar.x[:][1]
        z_spars = self.spar.z[:][0] + self.spar.z[:][1]
        stringer_count = range(len(x_stringers))
        spar_count = range(len(self.spar.x))

        # I_x is the sum of the contributions of the spar caps and stringers
        # TODO: replace list indices with dictionary value
        I_x = sum([cap_area * (z_spars[i] - self.centroid[1])**2
                   for i in spar_count])
        I_x += sum([stringer_area * (z_stringers[i] - self.centroid[1])**2
                    for i in stringer_count])

        I_z = sum([cap_area * (x_spars[i] - self.centroid[0])**2
                   for i in spar_count])
        I_z += sum([stringer_area * (x_stringers[i] - self.centroid[0])**2
                    for i in stringer_count])

        I_xz = sum([cap_area * (x_spars[i] - self.centroid[0])
                    * (z_spars[i] - self.centroid[1])
                    for i in spar_count])
        I_xz += sum([stringer_area * (x_stringers[i] - self.centroid[0])
                     * (z_stringers[i] - self.centroid[1])
                     for i in stringer_count])
        return (I_x, I_z, I_xz)

    def get_dx(self, component):
        return [x - self.centroid[0] for x in component.x_start]

    def get_dz(self, component):
        return [x - self.centroid[1] for x in component.x_start]

    def get_dP(self, xDist, zDist, V_x, V_z, area):
        I_x = self.I_['x']
        I_z = self.I_['z']
        I_xz = self.I_['xz']
        denom = float(I_x * I_z - I_xz ** 2)
        z = float()
        for _ in range(len(xDist)):
            z += float(-area * xDist[_] * (I_x * V_x - I_xz * V_z)
                       / denom
                       - area * zDist[_] * (I_z * V_z - I_xz * V_x)
                       / denom)
        return z

    def analysis(self, V_x, V_z):
        """Perform all analysis calculations and store in class instance."""
        self.drag = self.get_drag(10)
        self.lift_rectangular = self.get_lift_rectangular(13.7)
        self.lift_elliptical = self.get_lift_elliptical(15)
        self.lift_total = self.get_lift_total()
        self.mass_dist = self.get_mass_distribution(self.mass_total)
        self.centroid = self.get_centroid()
        self.I_['x'] = self.get_inertia_terms()[0]
        self.I_['z'] = self.get_inertia_terms()[1]
        self.I_['xz'] = self.get_inertia_terms()[2]
        spar_dx = self.get_dx(self.spar)
        spar_dz = self.get_dz(self.spar)
        self.spar.dP_x = self.get_dP(spar_dx, spar_dz,
                                     V_x, 0, self.spar.cap_area)
        self.spar.dP_z = self.get_dP(spar_dx, spar_dz,
                                     0, V_z, self.spar.cap_area)
        return None


def plot_geom(evaluator):
    """This function plots analysis results over the airfoil's geometry."""
    # Plot chord
    x_chord = [0, evaluator.chord]
    y_chord = [0, 0]
    plt.plot(x_chord, y_chord, linewidth='1')
    # Plot quarter chord
    plt.plot(evaluator.chord / 4, 0,
             '.', color='g', markersize=24, label='Quarter-chord')
    # Plot airfoil surfaces
    x = [0.98 * x for x in evaluator.airfoil.x]
    y = [0.98 * z for z in evaluator.airfoil.z]
    plt.fill(x, y, color='w', linewidth='1', fill=False)
    x = [1.02 * x for x in evaluator.airfoil.x]
    y = [1.02 * z for z in evaluator.airfoil.z]
    plt.fill(x, y, color='b', linewidth='1', fill=False)

    # Plot spars
    try:
        for _ in range(len(evaluator.spar.x)):
            x = (evaluator.spar.x[_])
            y = (evaluator.spar.z[_])
            plt.plot(x, y, '-', color='b')
    except AttributeError:
        print('No spars to plot.')
    # Plot stringers
    try:
        for _ in range(0, len(evaluator.stringer.x)):
            x = evaluator.stringer.x[_]
            y = evaluator.stringer.z[_]
            plt.plot(x, y, '.', color='y', markersize=12)
    except AttributeError:
        print('No stringers to plot.')

    # Plot centroid
    x = evaluator.centroid[0]
    y = evaluator.centroid[1]
    plt.plot(x, y, '.', color='r', markersize=24, label='centroid')

    # Graph formatting
    plt.xlabel('X axis')
    plt.ylabel('Z axis')

    plot_bound = max(evaluator.airfoil.x)
    plt.xlim(-0.10 * plot_bound, 1.10 * plot_bound)
    plt.ylim(-(1.10 * plot_bound / 2), (1.10 * plot_bound / 2))
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
    plt.plot(x, y_1, '.', color='b', markersize=4, label='Rectangular lift')
    plt.plot(x, y_2, '.', color='g', markersize=4, label='Elliptical lift')
    plt.plot(x, y_3, '.', color='r', markersize=4, label='Total lift')

    # Graph formatting
    plt.xlabel('Semi-span location')
    plt.ylabel('Lift')

    plt.gca().legend()
    plt.grid(axis='both', linestyle=':', linewidth=1)
    plt.show()
    return None
