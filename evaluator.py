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

# F_z =


def get_centroid(airfoil):
    area = airfoil.stringer.area
    numerator = float()
    for _ in airfoil.stringer.x_u:
        numerator += _ * area
    for _ in airfoil.stringer.x_l:
        numerator += _ * area
    # denominator
    # z_c =


def get_total_mass(self, *component):
    total_mass = float()
    for _ in component:
        total_mass += _.mass
    return total_mass
