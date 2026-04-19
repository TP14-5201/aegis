import requests
import pandas as pd
import io
import geopandas as gpd
import zipfile

from src.core.logging import logger
from src.core.config import settings


def fetch_csv_from_url(url: str, separator: str = ","):
    """
    Generic function to fetch and parse CSVs with any separator.
    """
    logger.info(f"Fetching CSV from {url}")
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), sep=separator)


def fetch_excel_from_url(url: str, sheet_name: str = 0):
    """
    Generic function to fetch and parse an Excel file.
    """
    logger.info(f"Fetching Excel from {url}")
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_excel(io.BytesIO(response.content), sheet_name=sheet_name)


def fetch_gdb_from_url(url: str):
    """
    Generic function to fetch and parse a GDB file.
    """
    logger.info(f"Fetching GDB from {url}")
    response = requests.get(url)
    response.raise_for_status()
    return gpd.read_file(io.BytesIO(response.content))


def fetch_zip_from_url(url: str):
    """
    Generic function to fetch and parse a ZIP file.
    """
    logger.info(f"Fetching ZIP from {url}")
    response = requests.get(url)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH)
    return gpd.read_file(f"{settings.VICLGA_BOUNDARY_RAW_UNZIP_PATH}/VIC_LGA_GDA2020/vic_lga.shp")
