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

import creator  # Create geometry
import evaluator  # Evaluate geometry
import generator  # Iteratevely evaluate instances of geometry
import random

import time
start_time = time.time()

CHORD_LENGTH = 100
SEMI_SPAN = 200

POP_SIZE = 1
SAVE_PATH = 'C:/Users/blend/github/UCLA_MAE_154B/save'


def main():
    # Create coordinate system specific to our airfoil dimensions.
    creator.Coordinates(CHORD_LENGTH, SEMI_SPAN)

    # Interate through all wings in population.
    for _ in range(1, POP_SIZE + 1):
        # Create airfoil instance
        af = creator.Airfoil()
        # Define NACA airfoil coordinates
        af.add_naca(2412)
        af.print_coord(2)

        # Create spar instance
        af.spar = creator.Spar()
        # Define the spar coordinates, stored in single spar object
        af.spar.add(af.coord, 0.15)
        af.spar.add(af.coord, 0.55)
        af.spar.print_coord(2)

        # Create stringer instance
        af.stringer = creator.Stringer()
        # Define the stringer coordinates from their amount
        af.stringer.add(af.coord, af.spar.coord, 4, 7, 5, 6)
        # Print coordinates of af.stringer to terminal
        af.stringer.print_coord(2)

        # Plot components with matplotlib
        creator.plot(af, af.spar, af.stringer)

        # Save component coordinates
        af.save_coord(SAVE_PATH, _)
        af.spar.save_coord(SAVE_PATH, _)
        af.stringer.save_coord(SAVE_PATH, _)

    # Print final execution time
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
