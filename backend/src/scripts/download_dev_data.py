import os
import pandas as pd

from src.data.extractors.support_services_extractor import fetch_csv_from_url
from src.core.config import settings
from src.core.logging import logger


def save_local_copy() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not os.path.exists("src/data/raw"):
        logger.info(f"Raw data directory {settings.MELBOURNE_RAW_PATH} does not exist. Creating raw data directory...")
        os.makedirs("src/data/raw")

    df_melbourne = fetch_csv_from_url(settings.MELBOURNE_API_URL, settings.MELBOURNE_SEP)
    df_melbourne.to_csv(settings.MELBOURNE_RAW_PATH, index=False)
    logger.info(f"Local dev file saved to {settings.MELBOURNE_RAW_PATH}")

    df_datagov = fetch_csv_from_url(settings.OTHER_DATA_URL, settings.OTHER_SEP)
    df_datagov.to_csv(settings.DATAGOV_RAW_PATH, index=False)
    logger.info(f"Local dev file saved to {settings.DATAGOV_RAW_PATH}")

