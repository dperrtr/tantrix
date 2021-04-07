from math import sqrt

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
        self.angles = None
        self.midpoints = None

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

        # TODO populate the midpoints

    def plot_hexagon(self):
        plt.figure()
        for a in self.angles:
            plt.scatter(*a, c='k')
        plt.show()


if __name__ == '__main__':
    hexagon = Hexagon(ri=2, center=(0, 5))
    hexagon.plot_hexagon()
