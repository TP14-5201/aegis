import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Emergency service data: City of Melbourne API
    MELBOURNE_API_URL: str = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/free-and-cheap-support-services-with-opening-hours-public-transport-and-parking-/exports/csv"
    MELBOURNE_SEP: str = ";"

    # Emergency service data: Data Gov
    OTHER_DATA_URL: str = "https://data.gov.au/data/dataset/d667403f-2016-463f-bb0a-3087ae67c57f/resource/0e32d958-3796-4dca-8312-489ef7a610f6/download/emergency-relief-provider-outlets-october-2016.csv"
    OTHER_SEP: str = ","

    # Emergency services columns
    EMERGENCY_INCLUDED_COLS: list[str] = [
        "name",
        "description",
        "target_audience",
        "address",
        "suburb",
        "primary_phone",
        "phone_display",
        "email",
        "website",
        "social_media",
        "opening_hours",
        "cost",
        "tram_routes",
        "bus_routes",
        "nearest_train_station",
        "categories",
        "longitude",
        "latitude"
    ]

    # Food insecurity data: VAHI (Victorian Population Health Survey)
    FOOD_INSECURITY_URL: str = "https://www.dropbox.com/scl/fi/8dj6f9knai1pvc2kuxbq8/food_insecurity_data.xlsx?rlkey=jxyaf0viyy84fnev3t3m0atod&st=7vc78ayw&dl=1"
    FOOD_INSECURITY_SHEET_NAME: any = 0
    SELECTED_REGIONS: list[str] = [
        'LGAs of Ovens-Murray PHU',
        'LGAs of Grampians Wimmera Southern Mallee PHU',
        'LGAs of North Eastern PHU',
        'LGAs of Gippsland PHU',
        'LGAs of South East PHU',
        'LGAs of Goulburn Valley PHU',
        'LGAs of Western PHU',
        'LGAs of Loddon Mallee PHU',
        'LGAs of Barwon South-West PHU'
    ]

    # Regional Victorian GDB boundaries
    VICGOV_BOUNDARY_URL: str = "https://www.dropbox.com/scl/fo/qr05jgmxcdbdn0boev1w7/ANUNe4e7aGOSzulbbzNLqX4?rlkey=8sna6zqjt5xrw52pf2jv37r0c&st=c3sn5k9r&dl=1"
    VICLGA_BOUNDARY_URL: str = "https://data.gov.au/data/dataset/bdf92691-c6fe-42b9-a0e2-a4cd716fa811/resource/95079e79-37d0-43c7-9f80-10eda1b0d05f/download/vic_lga_gda2020.zip"


    # Local file paths
    RAW_DATA_DIR: str = "src/data/raw"

    MELBOURNE_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "melbourne_raw.csv")
    DATAGOV_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "datagov_raw.csv")
    FOOD_INSECURITY_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "food_insecurity_raw.xlsx")
    VICGOV_BOUNDARY_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "vicgov_boundary_raw.csv")
    
    VICLGA_BOUNDARY_RAW_ZIP_PATH: str = os.path.join(RAW_DATA_DIR, "viclga_boundary_raw.zip")
    VICLGA_BOUNDARY_RAW_UNZIP_PATH: str = os.path.join(RAW_DATA_DIR, "viclga_boundary_raw")
    VICLGA_BOUNDARY_RAW_PATH: str = os.path.join(VICLGA_BOUNDARY_RAW_UNZIP_PATH, "vic_lga.csv")

settings = Settings()
