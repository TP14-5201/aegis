import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ### Emergency Services Dataset ###
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
    ### END OF Emergency Services Dataset ###

    ### Victoria Geographical & Demographical Dataset ###
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
    VICLGA_BOUNDARY_URL: str = "https://data.gov.au/data/dataset/bdf92691-c6fe-42b9-a0e2-a4cd716fa811/resource/95079e79-37d0-43c7-9f80-10eda1b0d05f/download/vic_lga_gda2020.zip"

    # LGA Population
    LGA_POPULATION_URL: str = "https://stg-arcgisazurecdataprodap1.az.arcgis.com/exportfiles-1032-2313/LGA_pop_ppl_DbR_Nov25_-3329894466674715511.csv?sv=2025-05-05&st=2026-04-26T05%3A23%3A40Z&se=2026-04-26T06%3A28%3A40Z&sr=c&sp=r&sig=BFbMCTHXPxxhEjQcfHASaDF8JKJBqgvlLmpv6cKhrdo%3D"
    LGA_POPULATION_SEP: str = ","
    ### END OF Victoria Geographical & Demographical Dataset ###

    ### Victorian Population Health Survey (VPHS) 2014 Data ###
    # VPHS 2014 Diet Indicator
    DIET_INDICATOR_URL: str = "https://www.dropbox.com/scl/fi/iummecvcrqg59y4k9tv49/vphs_2014_food_insecurity_diet_indicators_table_a1_18.csv?rlkey=xejidbj7sr68j8v05cm3k3qjx&st=vc1c5ba4&dl=1"
    DIET_INDICATOR_SEP: str = ","
    # VPHS 2014 Health Outcome
    HEALTH_OUTCOME_URL: str = "https://www.dropbox.com/scl/fi/64qdk5b6v4kfphul99urn/vphs_2014_food_insecurity_health_outcomes_table_a1_19.csv?rlkey=3h4ds9jlma1wmg4g8hnjn9bxf&st=n8ymhkpc&dl=1"
    HEALTH_OUTCOME_SEP: str = ","
    # VPHS 2014 Parents Low Cost Diet Table
    LOW_COST_DIET_URL: str = "https://www.dropbox.com/scl/fi/lvt872810o0napqs4dbcs/vphs_2014_parents_low_cost_diet_table_a1_27_raw.csv?rlkey=enfc1sm8svisjggl4o9qzfjyz&st=g676xyrx&dl=1"
    LOW_COST_DIET_SEP: str = ","
    ### END OF Victorian Population Health Survey (VPHS) 2014 Data ###

    ### Local file paths ###
    RAW_DATA_DIR: str = "src/data/raw"

    MELBOURNE_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "melbourne_raw.csv")
    DATAGOV_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "datagov_raw.csv")
    FOOD_INSECURITY_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "food_insecurity_raw.xlsx")
    
    VICLGA_BOUNDARY_RAW_ZIP_PATH: str = os.path.join(RAW_DATA_DIR, "viclga_boundary_raw.zip")
    VICLGA_BOUNDARY_RAW_UNZIP_PATH: str = os.path.join(RAW_DATA_DIR, "viclga_boundary_raw")
    VICLGA_BOUNDARY_RAW_PATH: str = os.path.join(VICLGA_BOUNDARY_RAW_UNZIP_PATH, "vic_lga.csv")

    LGA_POPULATION_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "abs_population_raw.csv")

    DIET_INDICATOR_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "vphs_2014_food_insecurity_diet_indicators_table_a1_18_raw.csv")
    HEALTH_OUTCOME_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "vphs_2014_food_insecurity_health_outcomes_table_a1_19_raw.csv")
    LOW_COST_DIET_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "vphs_2014_parents_low_cost_diet_table_a1_27_raw.csv")
    ### END OF Local file paths ###

settings = Settings()
