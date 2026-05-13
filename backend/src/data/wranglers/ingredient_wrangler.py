import pandas as pd

from .utils import initial_cleaning_pipeline, select_columns, clean_na_values, rename_columns


def _remove_ingredients_with_null_codes(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["sku"].notnull()]


def _remove_duplicate_product_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(subset=['product_name'])


def _filter_vic_state_only(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["state"]=="VIC"]


def _fill_null_retail_price(df: pd.DataFrame) -> pd.DataFrame:
    df["retail_price"] = df["retail_price"].fillna(df["unit_price"])
    return df


def _filter_unhealthy_food_categories(df: pd.DataFrame) -> pd.DataFrame:
    unhealthy_food_categories = [
        'Energy drinks',
        'Coffee',
        'Coffee Drinks',
        'Tea',
        'Tea Drinks',
        'Soft drinks',
        'Confectionery',
        'Packaged Cakes & Sweet Treats',
        'Jams, honey & spreads',
        'Chips, crackers & snacks',
        'Sports drinks',
        'Sauces',
    ]
    return df[~df["sub_category"].isin(unhealthy_food_categories)]


def _apply_health_and_dietary_tags(df: pd.DataFrame) -> pd.DataFrame:
    """Applies benefit icons and allergen tags based on sub_category."""
    INGREDIENT_METADATA = {
        "Vegetables": {"benefits": ["Immunity", "Eye"]},
        "Fruit": {"benefits": ["Immunity", "Energy"]},
        "Oils & vinegars": {"benefits": ["Brain", "Energy"]},
        "Dairy": {"benefits": ["Bones", "Teeth"]},
        "Milk": {"benefits": ["Bones", "Teeth"]},
        "Cheese": {"benefits": ["Bones", "Teeth", "Muscles"]},
        "Eggs": {"benefits": ["Muscles", "Brain"]},
        "Seafood": {"benefits": ["Brain", "Immunity"]},
        "Poultry": {"benefits": ["Muscles", "Energy"]},
        "Beef & veal": {"benefits": ["Muscles", "Energy", "Immunity"]},
        "Mince": {"benefits": ["Muscles", "Energy"]},
        "Lamb": {"benefits": ["Muscles", "Immunity"]},
        "Pork": {"benefits": ["Muscles", "Energy"]},
        "Packaged Breads": {"benefits": ["Energy"]},
        "Breakfast": {"benefits": ["Energy", "Bones"]},
        "Tea": {"benefits": ["Brain", "Immunity"]},
        "Jams, honey & spreads": {"benefits": ["Energy"]},
        "Sports drinks": {"benefits": ["Energy"]}
    }
    
    def get_meta(cat, key):
        return INGREDIENT_METADATA.get(cat, {}).get(key, [])

    df["health_benefits"] = df["sub_category"].apply(lambda x: get_meta(x, "benefits"))
    
    return df


def wrangle_ingredient(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare ingredient dataset."""
    INGREDIENT_COLS = [
        'sku',
        'product_name',
        'sub_category',
        'retail_price',
    ]
        
    INGREDIENT_MAPPING = {"sku": "ingredient_code"}

    df = initial_cleaning_pipeline(df)
    df = clean_na_values(df)
    df = _remove_ingredients_with_null_codes(df)
    df = _remove_duplicate_product_names(df)
    df = _filter_vic_state_only(df)
    df = _fill_null_retail_price(df)
    df = _filter_unhealthy_food_categories(df)
    df = _apply_health_and_dietary_tags(df)
    df = select_columns(df, included_cols=INGREDIENT_COLS)
    df = rename_columns(df, INGREDIENT_MAPPING)

    return df