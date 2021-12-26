import pandas as pd
import os


def populate_tantrix_hexagons(filepath: str = None) -> pd.DataFrame:
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), 'tantrix_pieces.csv')
    df = pd.read_csv(filepath, header=None, names=['back_number', 'back_color', 'edge_colors'])
    assert not df.edge_colors.duplicated().any()
    return df


if __name__ == '__main__':
    df = populate_tantrix_hexagons()
    verif_filepath = os.path.join(os.path.dirname(__file__), 'tantrix_pieces_verif.csv')
    df_verif = populate_tantrix_hexagons(verif_filepath)
    for idx in df.index:
        if not df.loc[idx].equals(df_verif.loc[idx]):
            print(idx)
    assert df.equals(df_verif)
