import pandas as pd

from .utils import initial_cleaning_pipeline, select_columns, clean_na_values, rename_columns


def _remove_ingredients_with_null_codes(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["code"].notnull()]


def _remove_duplicate_product_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(subset=['product_name'])


def wrangle_ingredient(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    """Clean and prepare price dataset."""
    if mode == "general":
        MAIN_INGREDIENT_COLS = [
            'code',
            'product_name',
        ]
    else:
        MAIN_INGREDIENT_COLS = [
            'code',
            'nutrition_grade_fr',
            'energy_100g',
            'proteins_100g',
            'carbohydrates_100g',
            'fat_100g'
        ]
        
    MAIN_INGREDIENT_MAPPING = {"code": "ingredient_code"}

    df = initial_cleaning_pipeline(df)
    df = clean_na_values(df)
    df = _remove_ingredients_with_null_codes(df)
    df = _remove_duplicate_product_names(df)
    df = select_columns(df, included_cols=MAIN_INGREDIENT_COLS)
    df = rename_columns(df, cols_rename_map=MAIN_INGREDIENT_MAPPING)
    
    return df