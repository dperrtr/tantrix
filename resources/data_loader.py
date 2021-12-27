import os
from typing import List

import pandas as pd

from resources.hexagon import TantrixHex


def import_tantrix_data(filepath: str = None) -> pd.DataFrame:
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), 'tantrix_pieces.csv')
    df = pd.read_csv(filepath, header=None, names=['back_number', 'back_color', 'edge_colors'])
    assert not df.edge_colors.duplicated().any()
    return df


def populate_tantrix_hexagons() -> List[TantrixHex]:
    df = import_tantrix_data()
    hex_list = []
    for __, row in df.iterrows():
        hex_list.append(TantrixHex(edge_colors=row.edge_colors,
                                   back_color=row.back_color,
                                   back_number=row.back_number))
    return hex_list


if __name__ == '__main__':
    df = import_tantrix_data()
    verif_filepath = os.path.join(os.path.dirname(__file__), 'tantrix_pieces_verif.csv')
    df_verif = import_tantrix_data(verif_filepath)
    for idx in df.index:
        if not df.loc[idx].equals(df_verif.loc[idx]):
            print(idx)
    assert df.equals(df_verif)
