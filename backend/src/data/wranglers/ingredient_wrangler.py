import pandas as pd

from .utils import initial_cleaning_pipeline, select_columns, clean_na_values, rename_columns


def _remove_ingredients_with_null_codes(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["sku"].notnull()]


def _fill_null_retail_price(df: pd.DataFrame) -> pd.DataFrame:
    df["retail_price"] = df["retail_price"].fillna(df["unit_price"])
    return df


def _deduplicate_keeping_cheapest(df: pd.DataFrame) -> pd.DataFrame:
    """Keep one entry per product across all states, choosing the lowest retail price.

    Products appear once per state in the Kaggle dataset. We drop the state
    dimension entirely — AU supermarket prices are largely national — and keep
    the row with the lowest non-null retail price so the catalogue is as large
    as possible without duplicates.
    """
    df = df.copy()
    df["_sort_price"] = pd.to_numeric(df["retail_price"], errors="coerce").fillna(float("inf"))
    df = df.sort_values("_sort_price").drop(columns=["_sort_price"])
    return df.drop_duplicates(subset=["product_name"], keep="first").reset_index(drop=True)


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
    """Applies benefit tags based on sub_category."""
    INGREDIENT_METADATA = {
        "Vegetables":          {"benefits": ["Immunity", "Eye"]},
        "Fruit":               {"benefits": ["Immunity", "Energy"]},
        "Oils & vinegars":     {"benefits": ["Brain", "Energy"]},
        "Dairy":               {"benefits": ["Bones", "Teeth"]},
        "Milk":                {"benefits": ["Bones", "Teeth"]},
        "Cheese":              {"benefits": ["Bones", "Teeth", "Muscles"]},
        "Eggs":                {"benefits": ["Muscles", "Brain"]},
        "Seafood":             {"benefits": ["Brain", "Immunity"]},
        "Poultry":             {"benefits": ["Muscles", "Energy"]},
        "Beef & veal":         {"benefits": ["Muscles", "Energy", "Immunity"]},
        "Mince":               {"benefits": ["Muscles", "Energy"]},
        "Lamb":                {"benefits": ["Muscles", "Immunity"]},
        "Pork":                {"benefits": ["Muscles", "Energy"]},
        "Packaged Breads":     {"benefits": ["Energy"]},
        "Breakfast":           {"benefits": ["Energy", "Bones"]},
    }

    def get_benefits(cat):
        return INGREDIENT_METADATA.get(cat, {}).get("benefits", [])

    df["health_benefits"] = df["sub_category"].apply(get_benefits)
    return df


def wrangle_ingredient(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare ingredient dataset.

    Key pipeline decisions:
    - No state filter: the Kaggle dataset covers all AU states; prices are
      largely national, so we keep everything and deduplicate by product name
      keeping the cheapest price. This expands the catalogue ~5-8x vs VIC-only.
    - Price fill happens before dedup so the cheapest non-null price wins.
    """
    INGREDIENT_COLS = ["sku", "product_name", "sub_category", "retail_price"]
    INGREDIENT_MAPPING = {"sku": "ingredient_code"}

    df = initial_cleaning_pipeline(df)
    df = clean_na_values(df)
    df = _remove_ingredients_with_null_codes(df)
    df = _fill_null_retail_price(df)
    df = _deduplicate_keeping_cheapest(df)
    df = _filter_unhealthy_food_categories(df)
    df = _apply_health_and_dietary_tags(df)
    df = select_columns(df, included_cols=INGREDIENT_COLS)
    df = rename_columns(df, INGREDIENT_MAPPING)

    return df
