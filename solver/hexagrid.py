"""

DavidPerruchoud (created on 29/12/2021)
"""
from itertools import product
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from resources.hexagon import TantrixHex
from resources.common_constants import CommonConstants


sns.set_theme('talk')


class OccupiedCell(Exception):
    """Exception to be raised if we attempt to place a tile on a cell of the grid already occupied."""
    pass


class HexaCell:
    """Represents one cell of the grid. It can be occupied by a tile. If that's the case, its 'edge_colors' and
    'lines' attributes are updated accordingly"""
    int2card = ['NW', 'NE', 'E', 'SE', 'SW', 'W']  # 0 -> 5
    card2int = {'NW': 0, 'NE': 1, 'E': 2, 'SE': 3, 'SW': 4, 'W': 5}

    def __init__(self, edge_colors: str = None):
        """
            0   1           NW NE
          5       2       W       E
            4   3           SW SE

        edge_colors can also represent a piece with a single line, in which case the missing lines must be replaced
        with '-'.
        """
        if edge_colors is None:
            self.occupied = False
            self.edge_colors = None
            self.lines = dict()  # dict of color: (entry side, exit side), e.g. 'r': (0, 2)
        else:
            self.occupied = True
            self.edge_colors = edge_colors
            self.lines = dict()
            self._populate_lines(edge_colors)

    def __str__(self):
        if self.occupied:
            indices = []
            colors = []
            for color, idx in self.lines.items():
                indices.extend(idx)
                colors.extend([color, color])
            ser = pd.Series(data=colors, index=indices).sort_index()
            return f"""
                        {ser.loc[0]}   {ser.loc[1]}
                      {ser.loc[5]}       {ser.loc[2]}
                        {ser.loc[4]}   {ser.loc[3]}
                    """
        return "Cell is unoccupied."

    def __repr__(self):
        if self.occupied:
            return f"HexaCell(edge_colors='{self.edge_colors}')"
        else:
            return "HexaCell()"

    def place_piece(self, piece: TantrixHex):
        """Place a new tile on the cell."""
        if self.occupied:
            raise OccupiedCell

        self.occupied = True
        self.edge_colors = piece.edge_colors
        self._populate_lines(self.edge_colors)

    def _populate_lines(self, edge_colors: str):
        """Populate the 'lines' attribute according to the placed tile."""
        color_list = np.array(list(edge_colors))
        for c in np.unique(color_list):
            if c == '-':
                # we ignore those lines
                continue
            self.lines[c] = list(np.where(color_list == c)[0])


class HexaGrid:
    """Represents the playing area. Builds a X-by-Y grid of hexagonal cells, which can be filled with tiles. This keeps
    track of the position of all placed tiles."""
    def __init__(self, grid_size: int = 50):
        self.x_size = grid_size
        self.y_size = grid_size
        self.grid = np.empty((self.x_size, self.y_size), dtype=HexaCell)
        self.mid = (int(grid_size / 2), int(grid_size / 2))
        self.occupied_cells = []

        self.populate_grid()

    def populate_grid(self):
        """Populate the grid with unoccuped HexaCells"""
        for x, y in product(range(self.x_size), range(self.y_size)):
            self.grid[x, y] = HexaCell()

    def get_cell(self, x: int, y: int) -> HexaCell:
        """Returns a cell of the Grid."""
        return self.grid[x, y]

    def place_piece(self, x: int, y: int, piece: TantrixHex):
        """Place a tile in one of the cells."""
        self.get_cell(x, y).place_piece(piece)
        self.occupied_cells.append((x, y))

    def plot_grid(self):
        """Plots the state of the grid."""
        # limit the grid size to the minimum necessary:
        min_x, max_x = np.min([v[0] for v in self.occupied_cells]), np.max([v[0] for v in self.occupied_cells]) + 1
        min_y, max_y = np.min([v[1] for v in self.occupied_cells]), np.max([v[1] for v in self.occupied_cells]) + 1

        x_gap = min_x
        y_gap = min_y

        plotted_grid = self.grid[min_x:max_x, min_y:max_y]

        # plot the base grid in grey
        for x, y in product(range(plotted_grid.shape[0]), range(plotted_grid.shape[1])):
            center_x = (2 * y + x) * CommonConstants.RI
            center_y = -1.5 * x * CommonConstants.RC
            self.plot_hex_pattern(center_x, center_y)

        # plot the placed tiles
        for x, y in self.occupied_cells:
            new_x = x - x_gap
            new_y = y - y_gap
            center_x = (2 * new_y + new_x) * CommonConstants.RI
            center_y = -1.5 * new_x * CommonConstants.RC
            # plot the border in black
            self.plot_hex_pattern(center_x, center_y, c='k')

            # plot the color lines
            tile = plotted_grid[new_x, new_y]
            self.plot_hex_lines(tile, center_x, center_y)

        # make the figure square
        xlim = plt.xlim()
        x_dist = xlim[1] - xlim[0]
        ylim = plt.ylim()
        y_dist = ylim[1] - ylim[0]
        max_dist = np.max([x_dist, y_dist])

        plt.xlim((xlim[0], xlim[0] + max_dist))
        plt.ylim((ylim[0], ylim[0] + max_dist))

    @staticmethod
    def get_unit_vertices(rc, ri) -> list:
        """Get the position of the vertices of a HexaCell, with respect to its center. """
        # TODO compute this only once if performance issues
        return [(-ri, (rc / 2)),  # NW
                (0, rc),  # N
                (0 + ri, (rc / 2)),  # NE
                (0 + ri, -(rc / 2)),  # SE
                (0, -rc),  # S
                (-ri, -(rc / 2)),  # SW
                ]

    def plot_hex_pattern(self, mid_x: float, mid_y: float, rc: float = None, c: str = 'gray'):
        """Plots the edges of a single HexaCell."""
        if rc is None:
            rc = CommonConstants.RC
            ri = CommonConstants.RI
        else:
            ri = sqrt(3) / 2 * rc

        vertices = self.get_unit_vertices(rc, ri)
        vertices = [(mid_x + p[0], mid_y + p[1]) for p in vertices]
        # duplicate the first vertex a the end of the list, to simplify plotting
        vertices = vertices + [vertices[0], ]

        for p1, p2 in zip(vertices[:-1], vertices[1:]):
            plt.plot((p1[0], p2[0]), (p1[1], p2[1]), color=c)

    def plot_hex_lines(self, tile: HexaCell, mid_x: float, mid_y: float, rc: float = None):
        """Plots the colored lines of a HexaCell."""
        if rc is None:
            rc = CommonConstants.RC
            ri = CommonConstants.RI
        else:
            ri = sqrt(3) / 2 * rc

        vertices = self.get_unit_vertices(rc, ri)
        vertices = [(mid_x + p[0], mid_y + p[1]) for p in vertices]
        # duplicate the first vertex a the end of the list, to simplify plotting
        vertices = vertices + [vertices[0], ]

        # compute the position of the midpoint
        midpoints = []
        for v1, v2 in zip(vertices[:-1], vertices[1:]):
            midpoints.append(((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2))

        for c, points in tile.lines.items():
            if c == '-':
                # we ignore those other lines
                continue
            entry = midpoints[points[0]]
            exit_ = midpoints[points[1]]
            plt.plot((entry[0], exit_[0]), (entry[1], exit_[1]), color=c, lw=6)


if __name__ == '__main__':
    from resources.data_loader import populate_tantrix_hexagons
    from solver.main_solver import solve

    pieces = populate_tantrix_hexagons()

    solve(pieces[:5], 'r')
    print()
