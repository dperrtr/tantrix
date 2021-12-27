"""

DavidPerruchoud (created on 26/12/2021)
"""
from itertools import product
from more_itertools import distinct_permutations

import numpy as np
from tqdm import tqdm


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
    perms = [list(simplified_pieces[:1]) +  list(perm) for perm in perms]
    print(f"Found a total of {len(perms)} possible distinct permutations.")

    for perm in tqdm(perms):
        possibilities = list(product([-1, 1], repeat=len(perm) - 1))
        for possibility in possibilities:
            raise NotImplementedError



