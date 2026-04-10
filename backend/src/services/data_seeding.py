import os
import pandas as pd

from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models import Base, SupportService

from src.core.config import settings
from src.core.logging import logger
from src.scripts.download_dev_data import save_local_copy
from src.data.wranglers.melbourne_wrangler import wrangle_melbourne
from src.data.wranglers.datagov_wrangler import wrangle_datagov


def seed_support_services(db: Session, df: pd.DataFrame):
    logger.info(f"Starting database seed with {len(df)} records...")
    
    records = df.to_dict(orient='records')
    try:
        # Clear existing data to avoid duplicates if re-running
        db.query(SupportService).delete() 
        service_objects = [SupportService(**data) for data in records]        
        db.bulk_save_objects(service_objects)
        db.commit()
        
        logger.info(f"Database seeding completed successfully! Inserted {len(service_objects)} records.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise e


def load_dataset():
    """Download (if needed), load, wrangle, and combine datasets."""
    if not os.path.exists(settings.MELBOURNE_RAW_PATH) and not os.path.exists(settings.DATAGOV_RAW_PATH):
        logger.info("Raw data files not found. Downloading from source...")
        save_local_copy()
    else:
        logger.info("Raw data files found. Loading from local files...")
    
    df_melbourne = pd.read_csv(settings.MELBOURNE_RAW_PATH)
    df_datagov = pd.read_csv(settings.DATAGOV_RAW_PATH)
        

    df_melbourne = wrangle_melbourne(df_melbourne)
    df_datagov = wrangle_datagov(df_datagov)
    df_final = pd.concat([df_melbourne, df_datagov], ignore_index=True).sort_values(by="name")

    return df_final


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    df_final = load_dataset()
    db = SessionLocal()
    try:
        seed_support_services(db, df_final)
    finally:
        db.close()
