"""

DavidPerruchoud (created on 26/12/2021)
"""
from itertools import product
from more_itertools import distinct_permutations

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from resources.hexagon import TantrixHex
from solver.hexagrid import HexaGrid, OccupiedCell


TILES = {1: 'rr----',
         2: 'r-r---',
         3: 'r--r--'}
POSITION_OFFSET = {0: (-1, 0),
                   1: (-1, 1),
                   2: (0, 1),
                   3: (1, 0),
                   4: (1, -1),
                   5: (0, -1)}


def solve(pieces: list, color: str):
    assert len(color) == 1 and color in 'rby'
    simplified_pieces = []
    for p in pieces:
        dist = np.diff(np.where(np.array(list(p.edge_colors)) == color))[0][0]
        if dist == 3:
            simplified_pieces.append(3)  # across
        elif dist in (2, 4):
            simplified_pieces.append(2)  # curve
        elif dist in (1, 5):
            simplified_pieces.append(1)  # direct
        else:
            raise ValueError

    # the very first piece is fixed, and set as the starting point
    perms = list(distinct_permutations(simplified_pieces[1:]))
    perms = [list(simplified_pieces[:1]) + list(perm) for perm in perms]
    print(f"Found a total of {len(perms)} possible distinct permutations.")

    plt.figure(figsize=(10, 10))

    debug_count = 0
    for perm in tqdm(perms):
        possibilities = list(product([-1, 1], repeat=len(perm) - 1))
        for possibility in possibilities:
            debug_count += 1

            # generate the grid
            grid = HexaGrid(len(pieces) * 2)

            # place the first tile
            grid.place_piece(*grid.mid,
                             piece=TantrixHex(edge_colors=TILES.get(perm[0]), back_color='y', back_number=1))

            # make variables to keep track of first and last tile positions, and exit
            first_tile_position = grid.mid
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

            plt.close()
            grid.plot_grid()
            plt.title(debug_count)
            plt.show()

            if not collapsed and last_tile_position == (grid.mid[0] - 1, grid.mid[1]) and last_tile_exit == 3:
                success = True
                print("Found a successful path!")
                grid.plot_grid()
                break
        if success:
            break


if __name__ == '__main__':
    from resources.data_loader import populate_tantrix_hexagons
    from solver.hexagrid import HexaGrid

    pieces = populate_tantrix_hexagons()

    solving_puzzle = 4
    assert 3 <= solving_puzzle <= 10
    solve(pieces[:solving_puzzle], pieces[solving_puzzle - 1].back_color)
