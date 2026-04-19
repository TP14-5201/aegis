import requests
import pandas as pd
import io
import geopandas as gpd
import zipfile

from src.core.logging import logger
from src.core.config import settings


def _download_content(url: str, as_bytes: bool = True):
    """Internal helper to handle networking logic and errors."""
    logger.info(f"Fetching data from {url}")
    response = requests.get(url, timeout=30) # Added timeout for safety
    response.raise_for_status()
    return response.content if as_bytes else response.text


def fetch_csv_from_url(url: str, separator: str = ","):
    content = _download_content(url, as_bytes=False)
    return pd.read_csv(io.StringIO(content), sep=separator)


def fetch_excel_from_url(url: str, sheet_name: str = 0):
    content = _download_content(url)
    return pd.read_excel(io.BytesIO(content), sheet_name=sheet_name)


def fetch_gdb_from_url(url: str):
    content = _download_content(url)
    return gpd.read_file(io.BytesIO(content))


def fetch_zip_from_url(url: str):
    content = _download_content(url)
    with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
        zip_ref.extractall(settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH)
    
    path = f"{settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH}/VIC_LGA_GDA2020/vic_lga.shp"
    return gpd.read_file(path)