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

from math import sin, cos, atan, sqrt

# All of these functions take integer arguments and return lists.


def get_total_mass(*component):
    total_mass = float()
    for _ in component:
        total_mass += _.mass
    return total_mass


def get_lift_rectangular(lift, semi_span):
    L_prime = lift / (semi_span * 2)
    return L_prime


def get_lift_elliptical(L_0, y, semi_span):
    L_prime = L_0 * sqrt(1 - (y / semi_span) ** 2)
    return L_prime


def get_lift(rectangular, elliptical):
    F_z = (rectangular + elliptical) / 2
    return F_z


def get_mass_distribution(airfoil, total_mass):
    F_z = [total_mass / airfoil.semi_span
           for x in range(0, airfoil.semi_span)]
    return F_z


def get_drag(airfoil, drag):
    # Transform semi-span integer into list
    semi_span = [x for x in range(0, airfoil.semi_span)]
    cutoff = round(0.8 * airfoil.semi_span)

    F_x = [drag for x in semi_span[0:cutoff]]
    F_x.extend([1.25 * drag for x in semi_span[cutoff:]])
    # for x in semi_span[cutoff:]:
    #     drag_distribution.append(1.25 * drag)
    return F_x


def get_centroid(airfoil):
    area = airfoil.stringer.area
    numerator = float()
    for _ in airfoil.stringer.x_u:
        numerator += _ * area
    for _ in airfoil.stringer.x_l:
        numerator += _ * area
    # denominator
    # z_c =
