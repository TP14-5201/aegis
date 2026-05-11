import pandas as pd
import kagglehub
import os
import zipfile


def fetch_json_from_kaggle(dataset: str, filename: str, output_dir: str):
    """Fetches data from Kaggle and returns a pandas DataFrame."""
    path = kagglehub.dataset_download(dataset, path=filename, output_dir=output_dir)
    compression = "zip" if zipfile.is_zipfile(path) else None
    return pd.read_json(path, compression=compression)


def fetch_csv_from_kaggle(dataset: str, filename: str, output_dir: str, separator: str, usecols: list[str]):
    """Fetches data from Kaggle and returns a pandas DataFrame."""
    path = kagglehub.dataset_download(dataset, path=filename, output_dir=output_dir)
    compression = "zip" if zipfile.is_zipfile(path) else None
    return pd.read_csv(path, sep=separator, usecols=usecols, compression=compression)
