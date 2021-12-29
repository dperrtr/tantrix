import pandas as pd


class TantrixHex:
    """Representation of a Tantrix tile. Mostly, it is defined by the sequence of colors on the edges of its front side.
    It is represented vertically, meaning that two angles are pointed up and down, and two edges are vertical.
    Rotation status is encoded in the edge colors, with the the first color in the list corresponding to the
    North-East (NE) edge. In such, rotating the tile by one tick simply corresponds to moving the last color of the list
    at the beginning of the list.
    Each tile also has a number and color, which refers to how many tiles are in the puzzle, and what color must the
    ring be. Those two attribute are barely used (if any).
    """
    def __init__(self, edge_colors: str, back_color: str, back_number: int):
        # sanity check
        assert 1 <= back_number <= 30
        assert back_color in 'rby'
        assert isinstance(edge_colors, str)
        assert len(edge_colors) == 6
        char_counts = pd.Series(iter(edge_colors)).value_counts()
        assert len(char_counts) == 3
        assert (char_counts == 2).all()

        self.edge_colors = edge_colors
        self.back_color = back_color
        self.back_number = back_number

    def rotate(self, cw_steps: int):
        """Rotate the tile by x steps, clockwise"""
        cw_steps = cw_steps % 6
        self.edge_colors = self.edge_colors[(6 - cw_steps):] + self.edge_colors[:(6 - cw_steps)]


if __name__ == '__main__':
    from resources.data_loader import populate_tantrix_hexagons
    from solver.hexagrid import HexaGrid

    pieces = populate_tantrix_hexagons()

    grid = HexaGrid(5)

    pieces[0].rotate(4)
    pieces[1].rotate(5)
    pieces[2].rotate(4)

    grid.place_piece(2, 2, pieces[0])
    grid.place_piece(1, 3, pieces[1])
    grid.place_piece(1, 2, pieces[2])

    grid.plot_grid()
