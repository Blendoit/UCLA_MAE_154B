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
import random

import time
start_time = time.time()

CHORD_LENGTH = 100
SEMI_SPAN = 200

POP_SIZE = 1
SAVE_PATH = 'C:/Users/blend/Desktop/python/airfoils'
# Where is my change?


def main():
    # Create coordinate system specific to airfoil dimensions.
    creator.Coordinates(CHORD_LENGTH, SEMI_SPAN)
    for airfoil_number in range(1, POP_SIZE + 1):
        foo = creator.Airfoil()
        foo.naca(2412)
        # foo.print_geometry(4)
        foo.spar = creator.Spar()
        foo.spar.add_spar(foo.coordinates, 'aluminium', 0.15)
        creator.plot(foo, foo.spar)
        # foo.save_values(airfoil_number, SAVE_PATH)

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
