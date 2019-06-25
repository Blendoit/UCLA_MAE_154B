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

import creator


class Population:
    '''Collection of random airfoils.'''

    def __init__(self, size):
        self.size = size
        self.gen_number = 0  # incremented for every generation

    def mutate(self, prob_mt):
        '''Randomly mutate the genes of prob_mt % of the population.'''

    def crossover(self, prob_cx):
        '''Combine the genes of prob_cx % of the population.'''

    def reproduce(self, prob_rp):
        '''Pass on the genes of the fittest prob_rp % of the population.'''

    def fitness():
        '''Rate the fitness of an individual on a relative scale (0-100)'''
