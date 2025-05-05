import os
import pandas as pd

def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'vgsales.csv')
    df = pd.read_csv(file_path)
    return df
