import pandas as pd
from rapidfuzz import process, fuzz
from tqdm import tqdm

from .utils import initial_cleaning_pipeline, select_columns


def _filter_vic_state_only(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["state"]=="VIC"]


def _fill_null_retail_price(df: pd.DataFrame) -> pd.DataFrame:
    df["retail_price"] = df["retail_price"].fillna(df["unit_price"])
    return df


def _filter_unhealthy_food_categories(df: pd.DataFrame) -> pd.DataFrame:
    unhealthy_food_categories = [
        'Soft drinks', 
        'Sport drinks', 
        'Packaged Cakes & Sweet Treats', 
        'Sports drink', 
        'Confectionery', 
        'Sauces', 
        'Energy drinks', 
        'Coffee', 
        'Coffee Drinks', 
        'Chips, crackers & snacks', 
        'Tea Drinks'
        ]
    return df[~df["sub_category"].isin(unhealthy_food_categories)]


def _apply_health_and_dietary_tags(df: pd.DataFrame) -> pd.DataFrame:
    """Applies benefit icons and allergen tags based on sub_category."""
    INGREDIENT_METADATA = {
        "Vegetables": {"benefits": ["Immunity", "Eye"], "tags": ["Vegan", "Vegetarian", "Gluten-free", "Dairy-free", "Halal"]},
        "Fruit": {"benefits": ["Immunity", "Energy"], "tags": ["Vegan", "Vegetarian", "Gluten-free", "Dairy-free", "Halal"]},
        "Oils & vinegars": {"benefits": ["Brain", "Energy"], "tags": ["Vegan", "Vegetarian", "Gluten-free", "Dairy-free", "Halal"]},
        "Dairy": {"benefits": ["Bones", "Teeth"], "tags": ["Vegetarian", "Gluten-free", "Halal"]},
        "Milk": {"benefits": ["Bones", "Teeth"], "tags": ["Vegetarian", "Gluten-free", "Halal"]},
        "Cheese": {"benefits": ["Bones", "Teeth", "Muscles"], "tags": ["Vegetarian", "Gluten-free", "Halal"]},
        "Eggs": {"benefits": ["Muscles", "Brain"], "tags": ["Vegetarian", "Gluten-free", "Dairy-free", "Halal"]},
        "Seafood": {"benefits": ["Brain", "Immunity"], "tags": ["Gluten-free", "Dairy-free", "Halal"]},
        "Poultry": {"benefits": ["Muscles", "Energy"], "tags": ["Gluten-free", "Dairy-free", "Halal"]},
        "Beef & veal": {"benefits": ["Muscles", "Energy", "Immunity"], "tags": ["Gluten-free", "Dairy-free", "Halal"]},
        "Mince": {"benefits": ["Muscles", "Energy"], "tags": ["Gluten-free", "Dairy-free", "Halal"]},
        "Lamb": {"benefits": ["Muscles", "Immunity"], "tags": ["Gluten-free", "Dairy-free", "Halal"]},
        "Pork": {"benefits": ["Muscles", "Energy"], "tags": ["Gluten-free", "Dairy-free"]},
        "Packaged Breads": {"benefits": ["Energy"], "tags": ["Vegan", "Vegetarian", "Dairy-free", "Halal"]},
        "Breakfast": {"benefits": ["Energy", "Bones"], "tags": ["Vegetarian", "Halal"]},
        "Tea": {"benefits": ["Brain", "Immunity"], "tags": ["Vegan", "Vegetarian", "Gluten-free", "Dairy-free", "Halal"]},
        "Jams, honey & spreads": {"benefits": ["Energy"], "tags": ["Vegetarian", "Gluten-free", "Halal"]},
        "Sports drinks": {"benefits": ["Energy"], "tags": ["Vegan", "Vegetarian", "Gluten-free", "Dairy-free", "Halal"]}
    }
    
    def get_meta(cat, key):
        return INGREDIENT_METADATA.get(cat, {}).get(key, [])

    df["health_benefits"] = df["sub_category"].apply(lambda x: get_meta(x, "benefits"))
    df["dietary_tags"] = df["sub_category"].apply(lambda x: get_meta(x, "tags"))
    
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
    price_df = _filter_unhealthy_food_categories(price_df)
    price_df = _apply_health_and_dietary_tags(price_df)
    price_df = price_df.drop_duplicates(subset=["sub_category", "product_name"])

    ingredient_to_price_map = _perform_ingredient_name_matching(price_df, ingredient_df)
    price_df = _map_ingredients_to_price(ingredient_to_price_map, price_df, ingredient_df)
    price_df = select_columns(price_df,  included_cols=["ingredient_code", "sub_category", "retail_price", "health_benefits", "dietary_tags"])

    return price_df