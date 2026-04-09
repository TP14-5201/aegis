import pandas as pd

from src.data.extractors.support_services_extractor import fetch_csv_from_url
from src.core.config import settings
from src.data.wranglers.melbourne_wrangler import wrangle_melbourne


if __name__ == "__main__":
    # df_melbourne = fetch_csv_from_url(settings.MELBOURNE_API_URL, settings.MELBOURNE_SEP)
    # df_datagov = fetch_csv_from_url(settings.OTHER_DATA_URL, settings.OTHER_SEP)

    df_melbourne = pd.read_csv("src/data/raw/melbourne_raw.csv")
    df_melbourne = wrangle_melbourne(df_melbourne)

    df_datagov = pd.read_csv("src/data/raw/datagov_raw.csv")