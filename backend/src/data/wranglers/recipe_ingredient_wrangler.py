import ast
import re

import pandas as pd
from rapidfuzz import process, fuzz
from tqdm import tqdm

from .utils import initial_cleaning_pipeline, select_columns, rename_columns


def _explode_ingredients(df: pd.DataFrame) -> pd.DataFrame:
    df['ingredients'] = df['ingredients'].apply(ast.literal_eval)
    df = df.explode('ingredients').reset_index(drop=True)
    df['ingredients'] = df['ingredients'].str.strip()

    return df


def _perform_ingredient_name_matching(cuisine_df, ingredient_df):
    unique_ingredients = cuisine_df['ingredients'].unique()
    original_names = ingredient_df["product_name"].dropna().unique()
    name_lookup = {name.lower().strip(): name for name in original_names}
    ingredient_names = list(name_lookup.keys())   # match against lowercase

    mapping = {}
    total = len(unique_ingredients)

    for ing in tqdm(unique_ingredients, desc="Matching Ingredients"):
        match = process.extractOne(ing, ingredient_names, scorer=fuzz.WRatio)
        if match:
            mapping[ing] = {
                'matched_product_name': name_lookup[match[0]],  # store ORIGINAL casing
                'score': match[1]
            }

    return mapping


def _map_ingredients_to_recipe(mapping, cuisine_df, ingredient_df):
    lookup_df = pd.DataFrame.from_dict(mapping, orient='index').reset_index()
    lookup_df.columns = ['ingredients', 'matched_product_name', 'match_score']

    # Merge with original exploded recipes and ingredients
    recipe_df = cuisine_df.merge(lookup_df, on='ingredients', how='left')
    recipe_df = recipe_df.merge(
        ingredient_df[['ingredient_code', "product_name"]], 
        left_on='matched_product_name', 
        right_on='product_name', 
        how='left'
    )

    # Some ingredients might be duplicated so we need to drop them
    recipe_df = recipe_df.drop_duplicates(subset=["id", "ingredients", "product_name"], keep="first")

    return recipe_df


def _remove_null_ingredients(recipe_df: pd.DataFrame) -> pd.DataFrame:
    return recipe_df[recipe_df['ingredient_code'].notna()]
    

def wrangle_recipe_ingredient(recipe_with_ingredients_df: pd.DataFrame, recipe_df: pd.DataFrame, ingredient_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare recipe dataset."""
    recipe_with_ingredients_df["id"] = recipe_with_ingredients_df["id"].astype(str)
    recipe_with_ingredients_df = initial_cleaning_pipeline(recipe_with_ingredients_df)
    recipe_with_ingredients_df = _explode_ingredients(recipe_with_ingredients_df)
    recipe_df = recipe_df.merge(recipe_with_ingredients_df, left_on='recipe_id', right_on='id', how='left')

    recipe_ingredient_mapping = _perform_ingredient_name_matching(recipe_df, ingredient_df)
    recipe_df = _map_ingredients_to_recipe(recipe_ingredient_mapping, recipe_df, ingredient_df)
    recipe_df = _remove_null_ingredients(recipe_df)
    
    recipe_df = select_columns(recipe_df, ["recipe_id", "ingredient_code"])
    recipe_df = recipe_df.drop_duplicates(subset=["recipe_id", "ingredient_code"], keep="first")

    return recipe_df