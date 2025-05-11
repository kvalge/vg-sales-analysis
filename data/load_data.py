import os
import pandas as pd


def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'vgsales.csv')
    df = pd.read_csv(file_path)

    df = df.drop(columns=['Rank'])
    df = df.dropna()
    df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year
    df = df[df['Year'] <= 2016]

    df.columns = df.columns.str.replace('_', ' ')

    return df
