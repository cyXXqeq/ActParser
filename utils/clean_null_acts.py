import pandas as pd


def clean_df(df: pd.DataFrame):
    indexes = []
    for index, row in df.loc[:, df.columns != 'Скважина'].iterrows():
        if set(row.tolist()) != {'н/д', 'н/д или п/д'}:
            indexes.append(index)
    return df.iloc[indexes].reset_index(drop=True)
