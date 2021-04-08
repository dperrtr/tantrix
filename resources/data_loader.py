import pandas as pd
import os


def populate_tantrix_hexagons() -> pd.DataFrame:
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tantrix_pieces.csv')
    df = pd.read_csv(filepath, header=None, names=['back_number', 'back_color', 'edge_colors'])
    return df


if __name__ == '__main__':
    populate_tantrix_hexagons()