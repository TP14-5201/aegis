from pathlib import Path
import os
import zipfile

from src.data.extractors.api_extractor import fetch_csv_from_url, fetch_excel_from_url, fetch_gdb_from_url, fetch_zip_from_url
from src.data.extractors.kaggle_extractor import fetch_json_from_kaggle, fetch_csv_from_kaggle
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
        (fetch_zip_from_url, settings.VICLGA_BOUNDARY_URL, settings.VICLGA_BOUNDARY_RAW_PATH, {}),
        (fetch_csv_from_url, settings.LGA_POPULATION_URL, settings.LGA_POPULATION_RAW_PATH, {"separator": settings.LGA_POPULATION_SEP}),
        (fetch_csv_from_url, settings.DIET_INDICATOR_URL, settings.DIET_INDICATOR_RAW_PATH, {"separator": settings.DIET_INDICATOR_SEP}),
        (fetch_csv_from_url, settings.HEALTH_OUTCOME_URL, settings.HEALTH_OUTCOME_RAW_PATH, {"separator": settings.HEALTH_OUTCOME_SEP}),
        (fetch_csv_from_url, settings.LOW_COST_DIET_URL, settings.LOW_COST_DIET_RAW_PATH, {"separator": settings.LOW_COST_DIET_SEP}),
        (fetch_csv_from_url, settings.LOW_COST_DIET_HEALTH_OUTCOME_URL, settings.LOW_COST_DIET_HEALTH_OUTCOME_RAW_PATH, {"separator": settings.LOW_COST_DIET_HEALTH_OUTCOME_SEP}),
        (fetch_csv_from_url, settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_URL, settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_RAW_PATH, {"separator": settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_SEP}),
        (fetch_csv_from_kaggle, settings.GROCERY_PRICES_DATASET, settings.GROCERY_PRICES_RAW_PATH, {"filename": settings.GROCERY_PRICES_DATASET_FILENAME, "output_dir": settings.RAW_DATA_DIR, "usecols": settings.GROCERY_PRICES_COLS, "separator": settings.GROCERY_PRICES_SEP}),
        (fetch_excel_from_url, settings.FOOD_FACTS_DATASET_URL, settings.FOOD_FACTS_RAW_PATH, {"sheet_name": settings.FOOD_FACTS_SHEET_NAME}),
        (fetch_csv_from_url, settings.FOOD_INACCESSIBILITY_REASONS_URL, settings.FOOD_INACCESSIBILITY_REASONS_RAW_PATH, {"separator": settings.FOOD_INACCESSIBILITY_REASONS_SEP})
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


if __name__ == "__main__":
    save_local_copy()