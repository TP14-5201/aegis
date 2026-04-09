from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Source 1: Melbourne API
    MELBOURNE_API_URL: str = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/free-and-cheap-support-services-with-opening-hours-public-transport-and-parking-/exports/csv"
    MELBOURNE_SEP: str = ";"

    # Source 2: Data Gov
    OTHER_DATA_URL: str = "https://data.gov.au/data/dataset/d667403f-2016-463f-bb0a-3087ae67c57f/resource/0e32d958-3796-4dca-8312-489ef7a610f6/download/emergency-relief-provider-outlets-october-2016.csv"
    OTHER_SEP: str = ","

settings = Settings()