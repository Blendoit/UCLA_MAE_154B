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
import generator  # Iteratevely evaluate instances of geometry and optimize
import random

import time
start_time = time.time()

# Airfoil dimensions
NACA_NUM = 2412
CHORD_LENGTH = 100
SEMI_SPAN = 40

# Airfoil thickness
T_UPPER = 0.1
T_LOWER = 0.1

# Component masses
AIRFOIL_MASS = 10  # lbs
SPAR_MASS = 10  # lbs
STRINGER_MASS = 5  # lbs

# Area
SPAR_CAP_AREA = 0.3  # sqin
STRINGER_AREA = 0.1  # sqin

# Amount of stringers
TOP_STRINGERS = 6
BOTTOM_STRINGERS = 4
NOSE_TOP_STRINGERS = 3
NOSE_BOTTOM_STRINGERS = 6

# population information & save path
POP_SIZE = 1
SAVE_PATH = 'C:/Users/blend/github/UCLA_MAE_154B/save'


def main():
    '''
    Create an airfoil;
    Evaluate an airfoil;
    Generate a population of airfoils & optimize.
    '''

    # Create coordinate system specific to our airfoil dimensions.
    # TODO: imperial + metric unit setting
    creator.Coordinates(CHORD_LENGTH, SEMI_SPAN)

    # Interate through all wings in population, creating and evaluating them.
    for _ in range(1, POP_SIZE + 1):

        # Create airfoil instance
        af = creator.Airfoil()
        # Define NACA airfoil coordinates and mass
        af.add_naca(NACA_NUM)
        af.add_mass(AIRFOIL_MASS)
        # af.info_print(2)
        af.info_save(SAVE_PATH, _)

        # Create spar instance
        af.spar = creator.Spar()
        # Define the spar coordinates and mass, stored in single spar object
        af.spar.add_coord(af, 0.20)
        af.spar.add_coord(af, 0.65)
        # Automatically adds spar caps for all spars previously defined
        af.spar.add_spar_caps(SPAR_CAP_AREA)
        af.spar.add_mass(SPAR_MASS)
        # af.spar.info_print(2)
        af.spar.info_save(SAVE_PATH, _)

        # Create stringer instance
        af.stringer = creator.Stringer()
        # Compute the stringer coordinates from their quantity in each zone
        af.stringer.add_coord(af,
                              NOSE_TOP_STRINGERS,
                              TOP_STRINGERS,
                              NOSE_BOTTOM_STRINGERS,
                              BOTTOM_STRINGERS)
        af.stringer.add_area(STRINGER_AREA)
        af.stringer.add_mass(STRINGER_MASS)
        # af.stringer.info_print(2)
        af.stringer.info_save(SAVE_PATH, _)

        # Plot components with matplotlib
        creator.plot_geom(af)

        # Evaluator object contains airfoil analysis results.
        eval = evaluator.Evaluator(af)
        # The analysis is performed in the evaluator.py module.
        eval.analysis()
        # eval.info_print(2)
        eval.info_save(SAVE_PATH, _)
        evaluator.plot_geom(eval)
        # evaluator.plot_lift(eval)

    # Print final execution time
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
