import pandas as pd
from rapidfuzz import process, fuzz
from tqdm import tqdm

from src.core.config import settings
from .utils import initial_cleaning_pipeline, clean_na_values, select_columns


def _clean_nutrition_header(df: pd.DataFrame) -> pd.DataFrame:
    # The column headers are on the 2nd row (index 1)
    df.columns = df.iloc[1]
    df = df.iloc[2:].reset_index(drop=True)
    # Replace the character \n in the column headers
    df.columns = [col.replace('\n', '') for col in df.columns]
    return df


def _perform_ingredient_name_matching(ingredient_df, nutrition_df):
    unique_ingredients = ingredient_df['product_name'].unique()
    original_names = nutrition_df["food_name"].dropna().unique()
    name_lookup = {name.lower().strip(): name for name in original_names}
    ingredient_names = list(name_lookup.keys())

    mapping = {}
    total = len(unique_ingredients)

    for ing in tqdm(unique_ingredients, desc="Matching Ingredient Nutrition Info"):
        match = process.extractOne(ing, ingredient_names, scorer=fuzz.WRatio)
        if match:
            mapping[ing] = {
                'matched_product_name': name_lookup[match[0]],
                'score': match[1]
            }

    return mapping
    

def _map_ingredients_to_price(mapping, ingredient_df, nutrition_df):
    lookup_df = pd.DataFrame.from_dict(mapping, orient='index').reset_index()
    lookup_df.columns = ['product_name', 'matched_product_name', 'match_score']

    # Merge with original exploded recipes and ingredients
    ingredient_nutrition_df = ingredient_df.merge(lookup_df, on='product_name', how='inner')
    ingredient_nutrition_df = ingredient_nutrition_df.merge(
        nutrition_df, 
        left_on='matched_product_name', 
        right_on='food_name', 
        how='inner'
    )

    return ingredient_nutrition_df
    

def wrangle_ingredient_nutrition(ingredient_df: pd.DataFrame, nutrition_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare nutrition dataset."""
    nutrition_df = _clean_nutrition_header(nutrition_df)
    nutrition_df = clean_na_values(nutrition_df)
    nutrition_df = initial_cleaning_pipeline(nutrition_df)
    ingredient_to_nutrition_map = _perform_ingredient_name_matching(ingredient_df, nutrition_df)
    ingredient_nutrition_df = _map_ingredients_to_price(ingredient_to_nutrition_map, ingredient_df, nutrition_df)
    ingredient_nutrition_df = select_columns(ingredient_nutrition_df,  included_cols=settings.FOOD_FACTS_COLS)

    return ingredient_nutrition_df