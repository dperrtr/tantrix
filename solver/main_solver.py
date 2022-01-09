"""

DavidPerruchoud (created on 26/12/2021)
"""
from itertools import product, permutations
from more_itertools import distinct_permutations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from resources.hexagon import TantrixHex
from solver.hexagrid import HexaGrid, OccupiedCell


TILES = {1: 'rr----',
         2: 'r-r---',
         3: 'r--r--'}

# POSITION_OFFSET gives the offset in the grid of the tile adjacent tho the key edge
POSITION_OFFSET = {0: (-1, 0),
                   1: (-1, 1),
                   2: (0, 1),
                   3: (1, 0),
                   4: (1, -1),
                   5: (0, -1)}

mpl.use('TkAgg')
plt.ion()


def search_ring_permutations(tiles: list, tiles_order: tuple, tile_orientation: tuple, ring_color: str) -> [list, None]:
    """Once we defined a working anneal, we need to find the right sequence of pieces so that not only the main color
    works, but also all the other lines."""
    assert ring_color in 'rgby'
    assert len(tiles) == len(tiles_order) == len(tile_orientation) + 1
    pass
    # find all possible tiles' permutations
    tile_types = {k: [] for k in (1, 2, 3)}
    for tile in tiles:
        tile_types.get(tile.line_types.get(ring_color)).append(tile.back_number)
    tile_types_perms = {k: list(permutations(v)) for k, v in tile_types.items()}
    # we need to add the different orientations for the straight lines in the ring
    across_orientations = list(product([-1, 1], repeat=len(tile_types.get(3))))

    # iterate over each permutation of tiles
    for perm1, perm2, perm3, across_orient in product(
            tile_types_perms.get(1), tile_types_perms.get(2), tile_types_perms.get(3), across_orientations):

        # create a new grid, and place all tiles of that permutation
        grid = HexaGrid(len(pieces) * 2)

        # check if all the colors fit.


def solve(pieces: list, color: str, interactive_plot: bool = False):
    assert len(color) == 1 and color in 'rbyg'
    n_pieces = len(pieces)
    simplified_pieces = []
    for p in pieces:
        simplified_pieces.append(p.line_types.get(color))

    # the very first piece is fixed, and set as the starting point
    perms = list(distinct_permutations(simplified_pieces[1:]))
    perms = [tuple(simplified_pieces[:1]) + tuple(perm) for perm in perms]
    print(f"Found a total of {len(perms)} possible distinct permutations.")

    plt.figure(figsize=(10, 10))
    collapsed = False
    success = False

    debug_count = 0
    for perm in tqdm(perms):
        # get the possible orientations of each piece. 1 is the short curve CW, -1 is the long curve CW
        possibilities = list(product([-1, 1], repeat=len(perm) - 1))
        # TODO optimization: we can remove the additional possibility for straight tiles
        for possibility in possibilities:
            debug_count += 1

            # generate the grid
            grid = HexaGrid(len(pieces) * 2)

            # place the first tile
            grid.place_piece(*grid.mid,
                             piece=TantrixHex(edge_colors=TILES.get(perm[0]), back_color='y', back_number=1))

            # make variables to keep track of first and last tile positions, and exit
            first_tile_entry = 0
            last_tile_position = grid.mid
            last_tile_exit = (first_tile_entry + perm[0]) % 6

            success = False
            for next_tile, start in zip(perm[1:], possibility):
                collapsed = False
                next_tile_offset = POSITION_OFFSET.get(last_tile_exit)
                next_tile_position = (last_tile_position[0] + next_tile_offset[0],
                                      last_tile_position[1] + next_tile_offset[1])
                try:
                    new_tile = TantrixHex(edge_colors=TILES.get(next_tile), back_color='y',
                                          back_number=1)
                    entry = (last_tile_exit + 3) % 6
                    if start == 1:
                        new_tile.rotate(entry)
                        last_tile_exit = (entry + next_tile) % 6
                    elif start == -1:
                        rotation = (entry - next_tile) % 6
                        new_tile.rotate(rotation)
                        last_tile_exit = rotation

                    grid.place_piece(*next_tile_position,
                                     piece=new_tile)

                    last_tile_position = next_tile_position

                except OccupiedCell:
                    collapsed = True
                    # path collapsed
                    break

            if interactive_plot:
                plt.cla()
                grid.plot_grid()
                x_lim = ((grid.mid[0] - np.ceil(n_pieces / 5) * 1.5), (grid.mid[0] + n_pieces) * 1.5)
                x_span = np.diff(x_lim)[0]
                plt.xlim(x_lim)
                plt.ylim((-grid.mid[1] - n_pieces, -grid.mid[1] - n_pieces + x_span))
                plt.xticks([])
                plt.yticks([])
                plt.title(debug_count)
                plt.draw()
                plt.pause(1E-9)

            # FIXME: non-connex solution isn't valid
            if not collapsed and last_tile_position == (grid.mid[0] - 1, grid.mid[1]) and last_tile_exit == 3:
                # we found a working anneal. Now let's try all combination of pieces so that the other colors also match
                success = True
                print("Found a successful path!")
                plt.cla()
                grid.plot_grid()
                plt.xticks([])
                plt.yticks([])

                search_ring_permutations(pieces, perm, possibility, color)
                break
        if success:
            plt.ioff()
            plt.show()
            break


if __name__ == '__main__':
    from resources.data_loader import populate_tantrix_hexagons

    pieces = populate_tantrix_hexagons()

    solving_puzzle = 5
    assert 3 <= solving_puzzle <= 10
    interactive_plot_ = True
    solve(pieces[:solving_puzzle], pieces[solving_puzzle - 1].back_color, interactive_plot=interactive_plot_)

    # remaining optimization steps:
        # early stop path-finding if target is further than the number of pieces left
        # early stop path-finding if uses final cell early
        # early stop path-finding of corresponding paths if path collapsed