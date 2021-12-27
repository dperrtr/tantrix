from math import sqrt

import pandas as pd
import matplotlib.pyplot as plt


class Hexagon:
    def __init__(self, rc: float = None, ri: float = None, center: tuple = (0, 0),
                 is_vertical: bool = True):
        assert rc is None or ri is None, "Hexagon must be instantiated with either 'ri' or 'rc', but not both."
        if rc is None and ri is None:
            rc = 1  # default rc if neither rc or ri is provided
        if rc is not None:
            self.rc = rc  # circumradius
            self.ri = sqrt(3) / 2 * rc  # inradius
        else:
            self.rc = 2 / sqrt(3) * ri
            self.ri = ri
        if not isinstance(center, tuple) or len(center) != 2 or not all([isinstance(i, (float, int)) for i in center]):
            raise ValueError("Invalid value for init argument 'center'.")
        self.center = center
        self.is_vertical = is_vertical  # a vertical hexagon is oriented in a way to have two vertical edges
        self.angles = None  # 6-tuple tuple, giving the XY position of each angle (north first)
        self.midpoints = None  # 6-tuple tuple, giving the XY position of each midpoing (north-east first)

        self._populate_angles_and_midpoints()

    def _populate_angles_and_midpoints(self):
        """Uses the instance attribute to generate the hexagon's angles and midpoints."""
        if not self.is_vertical:
            raise NotImplementedError("The logics for non-vertical hexagon isn't implemented yet.")

        # both angles and midpoints are arranged from midday clockwise
        self.angles = ((self.center[0], self.center[1] + self.rc),  # A0 (north)
                       (self.center[0] + self.ri, self.center[1] + (self.rc / 2)),  # A1 (north-east)
                       (self.center[0] + self.ri, self.center[1] - (self.rc / 2)),  # A2 (south-east)
                       (self.center[0], self.center[1] - self.rc),  # A3 (south)
                       (self.center[0] - self.ri, self.center[1] - (self.rc / 2)),  # A4 (south-west)
                       (self.center[0] - self.ri, self.center[1] + (self.rc / 2))  # A5 (north-west)
                       )
        self.midpoints = ((self._find_midpoint(*self.angles[0:2])),  # M1 (north-east)
                          (self._find_midpoint(*self.angles[1:3])),  # M2 (east)
                          (self._find_midpoint(*self.angles[2:4])),  # M3 (south-east)
                          (self._find_midpoint(*self.angles[3:5])),  # M4 (south-west)
                          (self._find_midpoint(*self.angles[4:6])),  # M5 (west)
                          (self._find_midpoint(self.angles[-1], self.angles[0])),  # M6 (north-west)
                          )

    @staticmethod
    def _find_midpoint(p1: tuple, p2: tuple) -> tuple:
        return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

    def plot_hexagon(self):
        # plot the edges
        for p1, p2 in zip(self.angles[:-1], self.angles[1:]):
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k')
        # add the last edge to close the loop
        p1 = self.angles[-1]
        p2 = self.angles[0]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k')

        # scatter the midpoints
        for midpoint in self.midpoints:
            plt.scatter(*midpoint, c='k')


class TantrixHex(Hexagon):
    def __init__(self, edge_colors: str, back_color: str, back_number: int, **kwargs):
        # sanity check
        assert 1 <= back_number <= 30
        assert back_color in 'rby'
        assert isinstance(edge_colors, str)
        assert len(edge_colors) == 6
        char_counts = pd.Series(iter(edge_colors)).value_counts()
        assert len(char_counts) == 3
        assert (char_counts == 2).all()

        super().__init__(**kwargs)

        self.edge_colors = edge_colors
        self.back_color = back_color,
        self.back_number = back_number

    def plot_hexagon(self):
        super().plot_hexagon()
        # we need to  find the midpoints with the same colors:
        path_dict = {}
        for idx, c in enumerate(self.edge_colors):
            if c in path_dict.keys():
                path_dict.get(c).append(idx)
            else:
                path_dict[c] = [idx, ]

        for c, indices in path_dict.items():
            p1 = self.midpoints[indices[0]]
            p2 = self.midpoints[indices[1]]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c=c, lw=5)
        # for midpoint, ec in zip(self.midpoints, self.edge_colors):
        #     plt.scatter(*midpoint, c=ec)

    def rotate(self, cw_steps: int):

        self.edge_colors = self.edge_colors[(6 - cw_steps):] + self.edge_colors[:(6 - cw_steps)]


if __name__ == '__main__':
    from resources.data_loader import import_tantrix_data, populate_tantrix_hexagons
    from resources.common_constants import CommonConstants
    from solver.main_solver import solve

    rc, ri = CommonConstants.RC, CommonConstants.RI

    pieces = populate_tantrix_hexagons()

    solve(pieces[:4], 'r')
    print()



    # df = import_tantrix_data()
    # pieces = []
    # centers = [(0, 0), (2 * ri, 0), (ri, (rc / 2) + rc)]
    # for (__, row), center in zip(df.iterrows(), centers):
    #     pieces.append(TantrixHex(ri=ri, center=center,
    #                              edge_colors=row.edge_colors, back_color=row.back_color, back_number=row.back_number))
    # pieces[0].rotate(4)
    # pieces[1].rotate(5)
    # pieces[2].rotate(4)
    #
    # plt.figure()
    # for th in pieces:
    #     th.plot_hexagon()
    # plt.show()
