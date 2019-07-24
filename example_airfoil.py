"""This example illustrates the usage of creator, evaluator and generator.

All the steps of airfoil creation & evaluation are detailed here;
however, the generator.py module contains certain presets (default airfoils).

Create an airfoil;
Evaluate an airfoil;
Generate a population of airfoils & optimize.
"""

from tools import creator, evaluator, generator

import time
start_time = time.time()

# Airfoil dimensions
NACA_NUM = 2412
CHORD_LENGTH = 68  # inches
SEMI_SPAN = 150  # inches

# Thicknesses
SPAR_THICKNESS = 0.4
SKIN_THICKNESS = 0.1

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
NOSE_BOTTOM_STRINGERS = 5

SAVE_PATH = 'C:/Users/blend/github/UCLA_MAE_154B/save'


# Create airfoil instance
af = creator.Airfoil.from_dimensions(CHORD_LENGTH, SEMI_SPAN)
af.add_naca(NACA_NUM)
af.add_mass(AIRFOIL_MASS)
af.info_print(2)
af.info_save(SAVE_PATH, 'foo_name')

# Create spar instance
af.spar = creator.Spar()
# All spar coordinates are stored in single Spar object
af.spar.add_coord(af, 0.23)
af.spar.add_coord(af, 0.57)
# Automatically adds spar caps for each spar previously defined
af.spar.add_spar_caps(SPAR_CAP_AREA)
af.spar.add_mass(SPAR_MASS)
af.spar.add_webs(SPAR_THICKNESS)
af.spar.info_print(2)
af.spar.info_save(SAVE_PATH, 'foo_name')

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
af.stringer.add_webs(SKIN_THICKNESS)
af.stringer.info_print(2)
af.stringer.info_save(SAVE_PATH, 'foo_name')

# Plot components with matplotlib
creator.plot_geom(af, True)

# Evaluator object contains airfoil analysis results.
eval = evaluator.Evaluator(af)
# The analysis is performed in the evaluator.py module.
eval.analysis(1, 1)
eval.info_print(2)
eval.info_save(SAVE_PATH, 'foo_name')
# evaluator.plot_geom(eval)
evaluator.plot_lift(eval)

pop = generator.Population(10)

print(help(creator))
print(help(evaluator))
print(help(generator))

# Print final execution time
print("--- %s seconds ---" % (time.time() - start_time))
