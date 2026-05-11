import pandas as pd
from rapidfuzz import process, fuzz
from tqdm import tqdm

from .utils import initial_cleaning_pipeline, select_columns


def _filter_vic_state_only(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["state"]=="VIC"]


def _fill_null_retail_price(df: pd.DataFrame) -> pd.DataFrame:
    df["retail_price"] = df["retail_price"].fillna(df["unit_price"])
    return df


def _perform_ingredient_name_matching(price_df, ingredient_df):
    unique_ingredients = price_df['product_name'].unique()
    original_names = ingredient_df["product_name"].dropna().unique()
    name_lookup = {name.lower().strip(): name for name in original_names}
    ingredient_names = list(name_lookup.keys())   # match against lowercase

    mapping = {}
    total = len(unique_ingredients)

    for ing in tqdm(unique_ingredients, desc="Matching Prices"):
        match = process.extractOne(ing, ingredient_names, scorer=fuzz.WRatio)
        if match:
            mapping[ing] = {
                'matched_product_name': name_lookup[match[0]],  # store ORIGINAL casing
                'score': match[1]
            }

    return mapping
    

def _map_ingredients_to_price(mapping, price_df, ingredient_df):
    lookup_df = pd.DataFrame.from_dict(mapping, orient='index').reset_index()
    lookup_df.columns = ['product_name', 'matched_product_name', 'match_score']

    # Merge with original exploded recipes and ingredients
    price_df = price_df.merge(lookup_df, on='product_name', how='inner')
    price_df = price_df.merge(
        ingredient_df[['ingredient_code', "product_name"]], 
        left_on='matched_product_name', 
        right_on='product_name', 
        how='inner'
    )

    # Some ingredients might be duplicated so we need to drop them
    price_df = price_df.drop_duplicates(subset=["ingredient_code"], keep="first")

    return price_df
    

def wrangle_ingredient_price(price_df: pd.DataFrame, ingredient_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare price dataset."""
    price_df = initial_cleaning_pipeline(price_df)
    price_df = _filter_vic_state_only(price_df)
    price_df = _fill_null_retail_price(price_df)
    price_df = select_columns(price_df,  included_cols=["sub_category", "product_name", "retail_price"])
    price_df = price_df.drop_duplicates(subset=["sub_category", "product_name"])

    ingredient_to_price_map = _perform_ingredient_name_matching(price_df, ingredient_df)
    price_df = _map_ingredients_to_price(ingredient_to_price_map, price_df, ingredient_df)
    price_df = select_columns(price_df,  included_cols=["ingredient_code", "sub_category", "retail_price"])

    return price_df