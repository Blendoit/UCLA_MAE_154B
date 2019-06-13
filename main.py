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

# masss
AIRFOIL_MASS = 100  # lbs
SPAR_MASS = 10  # lbs
STRINGER_MASS = 5  # lbs

POP_SIZE = 1
SAVE_PATH = 'C:/Users/blend/github/UCLA_MAE_154B/save'


def main():
    # Create coordinate system specific to our airfoil dimensions.
    creator.Coordinates(CHORD_LENGTH, SEMI_SPAN)

    # Interate through all wings in population.
    for _ in range(1, POP_SIZE + 1):

        # Create airfoil instance
        af = creator.Airfoil()
        # Define NACA airfoil coordinates and mass
        af.add_naca(2412)
        af.add_mass(AIRFOIL_MASS)
        af.print_info(2)

        # Create spar instance
        af.spar = creator.Spar()
        # Define the spar coordinates and mass, stored in single spar object
        af.spar.add_coord(af.coord, 0.15)
        af.spar.add_coord(af.coord, 0.55)
        af.spar.add_mass(SPAR_MASS)
        af.spar.print_info(2)

        # Create stringer instance
        af.stringer = creator.Stringer()
        # Compute the stringer coordinates from their quantity in each zone
        af.stringer.add_coord(af.coord, af.spar.coord, 4, 7, 5, 6)
        af.stringer.add_mass(STRINGER_MASS)
        af.stringer.print_info(2)

        # Plot components with matplotlib
        # creator.plot(af, af.spar, af.stringer)

        # Save component info
        af.save_info(SAVE_PATH, _)
        af.spar.save_info(SAVE_PATH, _)
        af.stringer.save_info(SAVE_PATH, _)

    # Print final execution time
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
