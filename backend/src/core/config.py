import os
from typing import Any

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


    ### "Learn More" Page Dataset ###
    # Food insecurity data: VAHI (Victorian Population Health Survey)
    FOOD_INSECURITY_URL: str = "https://www.dropbox.com/scl/fi/8dj6f9knai1pvc2kuxbq8/food_insecurity_data.xlsx?rlkey=jxyaf0viyy84fnev3t3m0atod&st=7vc78ayw&dl=1"
    FOOD_INSECURITY_SHEET_NAME: Any = 0
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
    VICLGA_BOUNDARY_URL: str = "https://www.dropbox.com/scl/fi/hjjai65eudy2rl81fb85x/vic_lga_gda2020.zip?rlkey=ygjk3mmq5y5dfv69y5kukpr5h&st=dptdfzsz&dl=1"

    # LGA Population
    LGA_POPULATION_URL: str = "https://www.dropbox.com/scl/fi/ebycjxbqe4k609nl7tr5r/abs_population_raw.csv?rlkey=acffuxvapuwtae1asrfyeivaz&st=msgf6ui9&dl=1"
    LGA_POPULATION_SEP: str = ","


    # VPHS 2014 Diet Indicator
    DIET_INDICATOR_URL: str = "https://www.dropbox.com/scl/fi/iummecvcrqg59y4k9tv49/vphs_2014_food_insecurity_diet_indicators_table_a1_18.csv?rlkey=xejidbj7sr68j8v05cm3k3qjx&st=vc1c5ba4&dl=1"
    DIET_INDICATOR_SEP: str = ","
    
    # VPHS 2014 Health Outcome
    HEALTH_OUTCOME_URL: str = "https://www.dropbox.com/scl/fi/64qdk5b6v4kfphul99urn/vphs_2014_food_insecurity_health_outcomes_table_a1_19.csv?rlkey=3h4ds9jlma1wmg4g8hnjn9bxf&st=n8ymhkpc&dl=1"
    HEALTH_OUTCOME_SEP: str = ","
    
    # VPHS 2014 Parents Low Cost Diet Table
    LOW_COST_DIET_URL: str = "https://www.dropbox.com/scl/fi/lvt872810o0napqs4dbcs/vphs_2014_parents_low_cost_diet_table_a1_27_raw.csv?rlkey=enfc1sm8svisjggl4o9qzfjyz&st=g676xyrx&dl=1"
    LOW_COST_DIET_SEP: str = ","
    
    # VPHS 2014 Parents Low Cost Diet Health Outcomes Table
    LOW_COST_DIET_HEALTH_OUTCOME_URL: str = "https://www.dropbox.com/scl/fi/bs2lvwfe2nluwf7q371ha/vphs_2014_parents_low_cost_health_outcomes_table_a1_28_raw.csv?rlkey=iq25f7umbf3r60oe962mzzt6i&st=q3bqhlgh&dl=1"
    LOW_COST_DIET_HEALTH_OUTCOME_SEP: str = ","

    # Recommended Macronutrients Intake Data (Appendix 3: Macro and micronutrient goals)
    RECOMMENDED_MACRONUTRIENTS_INTAKE_URL: str = "https://www.dropbox.com/scl/fi/aok0u8f41q2wrisy00gmk/recommended_macronutrients.csv?rlkey=qwgcap8nvtftwrjc4joywuwrx&st=dkpxc39u&dl=1"
    RECOMMENDED_MACRONUTRIENTS_INTAKE_SEP: str = ","

    # VAHI Food Inaccessibility Reasons (Table A1-30: Reasons why people were not always able to access healthy food, by local government area in metropolitan Victoria)
    FOOD_INACCESSIBILITY_REASONS_URL: str = "https://www.dropbox.com/scl/fi/86w1h845uj5e3wo9ofule/food_inaccessibility_reasons.csv?rlkey=ygaxs6wxgjec9xgs7zoepuehb&st=782e6nzg&dl=1"
    FOOD_INACCESSIBILITY_REASONS_SEP: str = ","
    ### END OF "Learn More" Page Dataset ###

    # "Get Food" Page Food & Ingredient Recommendation
    GROCERY_PRICES_DATASET: str = "thedevastator/grocery-product-prices-for-australian-states"
    GROCERY_PRICES_DATASET_FILENAME: str = "Australia_Grocery_2022Sep.csv"
    GROCERY_PRICES_SEP: str = ","
    GROCERY_PRICES_COLS: list[str] = [
        "Sku",
        "state",
        "Product_Name",
        "Sub_category",
        "Retail_price",
        "unit_price",
        "unit_price_unit"
    ]

    FOOD_FACTS_DATASET_URL: str = "https://www.foodstandards.gov.au/sites/default/files/2025-12/AFCD%20Release%203%20-%20Nutrient%20profiles.xlsx"
    FOOD_FACTS_SHEET_NAME: Any = 1
    FOOD_FACTS_COLS: list[str] = [
        # Main ingredient info
        'ingredient_code',
        'protein_g',
        'fat_total_g',   
        'total_dietary_fibre_g',   
        'total_sugars_g',       
        'available_carbohydrate_without_sugar_alcohols_g',             
        'sodium_na_mg'
    ]

    ### END OF "Get Food" Page Food & Ingredient Recommendation ###


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
    LOW_COST_DIET_HEALTH_OUTCOME_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "vphs_2014_parents_low_cost_health_outcomes_table_a1_28_raw.csv")
    RECOMMENDED_MACRONUTRIENTS_INTAKE_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "recommended_macronutrients_raw.csv")
    FOOD_INACCESSIBILITY_REASONS_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "food_inaccessibility_reasons_raw.csv")
    
    GROCERY_PRICES_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "grocery_prices.csv")
    FOOD_FACTS_RAW_PATH: str = os.path.join(RAW_DATA_DIR, "nutrient_profiles.xlsx")
    ### END OF Local file paths ###

settings = Settings()
