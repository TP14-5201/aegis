import os

from src.data.extractors.support_services_extractor import fetch_csv_from_url
from src.core.config import settings
from src.core.logging import logger


def save_local_copy() -> None:
    """Downloads raw CSVs from their source URLs and saves them locally.

    Creates the raw data directory if it doesn't already exist.
    The function has no return value; callers should read the saved files
    directly via the paths defined in settings.
    """
    if not os.path.exists("src/data/raw"):
        logger.info("Raw data directory does not exist. Creating raw data directory...")
        os.makedirs("src/data/raw")

    df_melbourne = fetch_csv_from_url(settings.MELBOURNE_API_URL, settings.MELBOURNE_SEP)
    df_melbourne.to_csv(settings.MELBOURNE_RAW_PATH, index=False)
    logger.info(f"Local dev file saved to {settings.MELBOURNE_RAW_PATH}")

    df_datagov = fetch_csv_from_url(settings.OTHER_DATA_URL, settings.OTHER_SEP)
    df_datagov.to_csv(settings.DATAGOV_RAW_PATH, index=False)
    logger.info(f"Local dev file saved to {settings.DATAGOV_RAW_PATH}")
