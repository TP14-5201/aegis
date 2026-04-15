from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Emergency service data: City of Melbourne API
    MELBOURNE_API_URL: str = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/free-and-cheap-support-services-with-opening-hours-public-transport-and-parking-/exports/csv"
    MELBOURNE_SEP: str = ";"

    # Emergency service data: Data Gov
    OTHER_DATA_URL: str = "https://data.gov.au/data/dataset/d667403f-2016-463f-bb0a-3087ae67c57f/resource/0e32d958-3796-4dca-8312-489ef7a610f6/download/emergency-relief-provider-outlets-october-2016.csv"
    OTHER_SEP: str = ","

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

    # Local file paths
    MELBOURNE_RAW_PATH: str = "src/data/raw/melbourne_raw.csv"
    DATAGOV_RAW_PATH: str = "src/data/raw/datagov_raw.csv"
    FOOD_INSECURITY_RAW_PATH: str = "src/data/raw/food_insecurity_raw.xlsx"


settings = Settings()
