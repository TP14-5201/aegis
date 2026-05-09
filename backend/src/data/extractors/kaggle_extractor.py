import pandas as pd
import kagglehub
import os


def fetch_json_from_kaggle(dataset: str, filename: str, output_dir: str):
    """Fetches data from Kaggle and returns a pandas DataFrame."""
    kagglehub.dataset_download(dataset, path=filename, output_dir=output_dir)
    df = pd.read_json(os.path.join(output_dir, filename), compression="zip")
    return df


def fetch_csv_from_kaggle(dataset: str, filename: str, output_dir: str, separator: str, usecols: list[str]):
    """Fetches data from Kaggle and returns a pandas DataFrame."""
    kagglehub.dataset_download(dataset, path=filename, output_dir=output_dir)
    return pd.read_csv(os.path.join(output_dir, filename), sep=separator, usecols=usecols, compression="zip")
