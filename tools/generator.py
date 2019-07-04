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
The generator.py module contains a single Population class,
which represents a collection of randomized airfoils.
"""

from tools import creator


def default_airfoil():
    """Generate the default airfoil."""
    airfoil = creator.Airfoil.from_dimensions(100, 200)
    airfoil.add_naca(2412)
    airfoil.add_mass(10)

    airfoil.spar = creator.Spar()
    airfoil.spar.add_coord(airfoil, 0.23)
    airfoil.spar.add_coord(airfoil, 0.57)
    airfoil.spar.add_spar_caps(0.3)
    airfoil.spar.add_mass(10)
    airfoil.spar.add_webs(0.4)

    airfoil.stringer = creator.Stringer()
    airfoil.stringer.add_coord(airfoil, 3, 6, 5, 4)
    airfoil.stringer.add_area(0.1)
    airfoil.stringer.add_mass(5)
    airfoil.stringer.add_webs(0.1)

    return airfoil


class Population(creator.Airfoil):
    """Collection of random airfoils."""

    def __init__(self, size):
        af = creator.Airfoil
        # print(af)
        self.size = size
        self.gen_number = 0  # incremented for every generation

    def mutate(self, prob_mt):
        """Randomly mutate the genes of prob_mt % of the population."""

    def crossover(self, prob_cx):
        """Combine the genes of prob_cx % of the population."""

    def reproduce(self, prob_rp):
        """Pass on the genes of the fittest prob_rp % of the population."""

    def fitness():
        """Rate the fitness of an individual on a relative scale (0-100)"""
