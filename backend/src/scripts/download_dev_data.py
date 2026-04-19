from pathlib import Path
import os

from src.data.extractors.support_services_extractor import fetch_csv_from_url, fetch_excel_from_url, fetch_gdb_from_url, fetch_zip_from_url
from src.core.config import settings
from src.core.logging import logger


def save_local_copy() -> None:
    """Downloads raw datasets and saves them locally based on source type."""
    
    # Check for raw data directory
    raw_dir = Path("src/data/raw")
    if not raw_dir.exists():
        logger.info(f"Creating directory: {raw_dir}")
        raw_dir.mkdir(parents=True, exist_ok=True)

    download_tasks = [
        (fetch_csv_from_url, settings.MELBOURNE_API_URL, settings.MELBOURNE_RAW_PATH, {"separator": settings.MELBOURNE_SEP}),
        (fetch_csv_from_url, settings.OTHER_DATA_URL, settings.DATAGOV_RAW_PATH, {"separator": settings.OTHER_SEP}),
        (fetch_excel_from_url, settings.FOOD_INSECURITY_URL, settings.FOOD_INSECURITY_RAW_PATH, {"sheet_name": settings.FOOD_INSECURITY_SHEET_NAME}),
        (fetch_gdb_from_url, settings.VICGOV_BOUNDARY_URL, settings.VICGOV_BOUNDARY_RAW_PATH, {}),
        (fetch_zip_from_url, settings.VICLGA_BOUNDARY_URL, settings.VICLGA_BOUNDARY_RAW_PATH, {}),
    ]

    # Download all necessary files
    for fetch_func, url, save_path, kwargs in download_tasks:
        try:
            df = fetch_func(url, **kwargs)
            if save_path.endswith(".xlsx"):
                df.to_excel(save_path, index=False)
            else:
                df.to_csv(save_path, index=False)
            logger.info(f"Local dev file saved to {save_path}")
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
