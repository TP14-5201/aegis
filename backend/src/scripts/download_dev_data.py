import os

from src.data.extractors.support_services_extractor import fetch_csv_from_url
from src.core.config import settings
from src.core.logging import logger


def save_local_copy():
    df_melbourne = fetch_csv_from_url(settings.MELBOURNE_API_URL, settings.MELBOURNE_SEP)
    df_melbourne.to_csv("src/data/raw/melbourne_raw.csv", index=False)
    logger.info("Local dev file saved to src/data/raw/melbourne_raw.csv")

    df_datagov = fetch_csv_from_url(settings.OTHER_DATA_URL, settings.OTHER_SEP)
    df_datagov.to_csv("src/data/raw/datagov_raw.csv", index=False)
    logger.info("Local dev file saved to src/data/raw/datagov_raw.csv")

if __name__ == "__main__":
    if not os.path.exists("src/data/raw"):
        os.makedirs("src/data/raw")
    save_local_copy()