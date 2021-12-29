import os
from typing import List

import pandas as pd

from resources.hexagon import TantrixHex


def import_tantrix_data(filepath: str = None) -> pd.DataFrame:
    """Reads the CSV-file with the description of each Tantrix tile, and returns a dataframe."""
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), 'tantrix_pieces.csv')
    df = pd.read_csv(filepath, header=None, names=['back_number', 'back_color', 'edge_colors'])
    assert not df.edge_colors.duplicated().any()
    return df


def populate_tantrix_hexagons() -> List[TantrixHex]:
    """Reads the CSV-file with the description of each Tantrix tile, and returns a list of TantrixHex objects."""
    df = import_tantrix_data()
    hex_list = []
    for __, row in df.iterrows():
        hex_list.append(TantrixHex(edge_colors=row.edge_colors,
                                   back_color=row.back_color,
                                   back_number=row.back_number))
    return hex_list


if __name__ == '__main__':
    # make sure that there are no typos in the tile file. To do that, the CSV-file was manually written twice, and we
    # make sure we have the exact sames content in both of them.
    df_ = import_tantrix_data()
    verif_filepath = os.path.join(os.path.dirname(__file__), 'tantrix_pieces_verif.csv')
    df_verif = import_tantrix_data(verif_filepath)
    for idx in df_.index:
        if not df_.loc[idx].equals(df_verif.loc[idx]):
            print(idx)
    assert df_.equals(df_verif)
