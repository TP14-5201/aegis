import requests
import pandas as pd
import io

from src.core.logging import logger


def fetch_csv_from_url(url: str, separator: str = ","):
    """
    Generic function to fetch and parse CSVs with any separator.
    """
    logger.info(f"Fetching CSV from {url}")
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), sep=separator)
