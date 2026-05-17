import sys
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd

sys.modules.setdefault("kagglehub", SimpleNamespace(dataset_download=None))

from src.data.extractors.kaggle_extractor import fetch_csv_from_kaggle, fetch_json_from_kaggle


def test_fetch_json_from_kaggle_downloads_and_reads_plain_json():
    with patch("src.data.extractors.kaggle_extractor.kagglehub.dataset_download", return_value="data.json") as mock_download, \
         patch("src.data.extractors.kaggle_extractor.zipfile.is_zipfile", return_value=False), \
         patch("src.data.extractors.kaggle_extractor.pd.read_json", return_value=pd.DataFrame()) as mock_read_json:
        fetch_json_from_kaggle("owner/dataset", "file.json", "out")

    mock_download.assert_called_once_with("owner/dataset", path="file.json", output_dir="out")
    mock_read_json.assert_called_once_with("data.json", compression=None)


def test_fetch_json_from_kaggle_uses_zip_compression_when_download_is_zip():
    with patch("src.data.extractors.kaggle_extractor.kagglehub.dataset_download", return_value="data.zip"), \
         patch("src.data.extractors.kaggle_extractor.zipfile.is_zipfile", return_value=True), \
         patch("src.data.extractors.kaggle_extractor.pd.read_json", return_value=pd.DataFrame()) as mock_read_json:
        fetch_json_from_kaggle("owner/dataset", "file.json", "out")

    mock_read_json.assert_called_once_with("data.zip", compression="zip")


def test_fetch_csv_from_kaggle_downloads_and_reads_csv_with_options():
    with patch("src.data.extractors.kaggle_extractor.kagglehub.dataset_download", return_value="data.csv") as mock_download, \
         patch("src.data.extractors.kaggle_extractor.zipfile.is_zipfile", return_value=False), \
         patch("src.data.extractors.kaggle_extractor.pd.read_csv", return_value=pd.DataFrame()) as mock_read_csv:
        fetch_csv_from_kaggle("owner/dataset", "file.csv", "out", ";", ["name"])

    mock_download.assert_called_once_with("owner/dataset", path="file.csv", output_dir="out")
    mock_read_csv.assert_called_once_with("data.csv", sep=";", usecols=["name"], compression=None)


def test_fetch_csv_from_kaggle_uses_zip_compression_when_download_is_zip():
    with patch("src.data.extractors.kaggle_extractor.kagglehub.dataset_download", return_value="data.zip"), \
         patch("src.data.extractors.kaggle_extractor.zipfile.is_zipfile", return_value=True), \
         patch("src.data.extractors.kaggle_extractor.pd.read_csv", return_value=pd.DataFrame()) as mock_read_csv:
        fetch_csv_from_kaggle("owner/dataset", "file.csv", "out", ",", ["name"])

    mock_read_csv.assert_called_once_with("data.zip", sep=",", usecols=["name"], compression="zip")
