import pandas as pd


def read_data(file_path: str) -> pd.DataFrame:
    """
    Read the dataset from the csv file
    :return: None
    """
    df = pd.read_csv(file_path)
    return df
