import json
import re

import pandas as pd

from .utils import initial_cleaning_pipeline, add_source_column, clean_na_values

# Filler words stripped before picking "top" ingredients for name generation
_NAME_STOPWORDS = {
    "fresh", "dried", "ground", "chopped", "diced", "minced", "sliced",
    "grated", "peeled", "crushed", "cooked", "raw", "frozen", "canned",
    "large", "small", "medium", "extra", "optional", "and", "or", "to",
    "taste", "a", "the", "of", "with", "salt", "pepper", "water", "oil",
    "olive", "vegetable", "butter", "flour", "sugar", "eggs", "egg",
    "baking", "powder", "soda", "vanilla", "sauce",
}

# Cuisine → display label used in the generated name
_CUISINE_LABELS: dict[str, str] = {
    "italian":       "Italian",
    "mexican":       "Mexican",
    "chinese":       "Chinese",
    "indian":        "Indian",
    "french":        "French",
    "greek":         "Greek",
    "thai":          "Thai",
    "japanese":      "Japanese",
    "vietnamese":    "Vietnamese",
    "mediterranean": "Mediterranean",
    "southern_us":   "Southern US",
    "cajun_creole":  "Cajun",
    "british":       "British",
    "irish":         "Irish",
    "spanish":       "Spanish",
    "moroccan":      "Moroccan",
    "brazilian":     "Brazilian",
    "filipino":      "Filipino",
    "jamaican":      "Jamaican",
    "russian":       "Russian",
    "korean":        "Korean",
    "british":       "British",
}

_QTY_RE = re.compile(
    r"^\s*[\d/½¼¾⅓⅔]+\s*(cup|c\.|tbsp|tsp|tablespoon|teaspoon|oz|lb|g|kg|ml|l|pound|ounce|clove|head|bunch|slice|can|jar|pkg|package|medium|large|small|piece|pinch|dash|handful)s?\s*",
    re.IGNORECASE,
)


def _top_ingredients(ingredients_json: str, n: int = 2) -> list[str]:
    """Returns up to n display-ready ingredient tokens from a JSON ingredient list."""
    try:
        items = json.loads(ingredients_json) if isinstance(ingredients_json, str) else ingredients_json
    except (json.JSONDecodeError, TypeError):
        return []
    tokens = []
    for item in items:
        item = _QTY_RE.sub("", str(item)).strip()
        words = [w for w in item.lower().split() if w not in _NAME_STOPWORDS and len(w) > 2]
        if words:
            tokens.append(words[0].title())
        if len(tokens) == n:
            break
    return tokens


def generate_dish_name(df: pd.DataFrame) -> pd.DataFrame:
    """Builds a readable dish name from cuisine + top ingredients.

    Yummly data has no recipe names — "Italian Recipe 22213" is not display-ready.
    We produce names like "Italian Chicken & Tomato" or "Greek Lamb & Lemon" instead.
    Falls back to the existing name column if it already has real values.
    """
    has_real_names = (
        "name" in df.columns
        and not df["name"].isna().all()
        and not df["name"].str.match(r"^\w+ Recipe \d+$", na=True).all()
    )
    if has_real_names:
        return df

    def _build(row):
        cuisine_raw = str(row.get("cuisine", "")).lower()
        cuisine_label = _CUISINE_LABELS.get(cuisine_raw, cuisine_raw.replace("_", " ").title() or "Mixed")
        ing_col = "ingredients" if "ingredients" in row.index else None
        top = _top_ingredients(row[ing_col]) if ing_col else []
        if top:
            return f"{cuisine_label} {' & '.join(top)}"
        row_id = str(int(row["id"])) if "id" in row.index else str(row.name)
        return f"{cuisine_label} Dish {row_id}"

    df["name"] = df.apply(_build, axis=1)
    return df


def parse_dietary_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Parses dietary_flags from a CSV string representation into a Python list."""
    def _parse(val):
        if pd.isna(val) or str(val).strip() == "":
            return []
        if isinstance(val, list):
            return val
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return []

    df["dietary_flags"] = df["dietary_flags"].apply(_parse)
    return df


def coerce_base_servings(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures base_servings is an integer, defaulting to 4 on parse failure."""
    df["base_servings"] = pd.to_numeric(df["base_servings"], errors="coerce").fillna(4).astype(int)
    return df


def wrangle_dishes(df: pd.DataFrame) -> pd.DataFrame:
    df = initial_cleaning_pipeline(df)
    df = generate_dish_name(df)
    if "dietary_flags" not in df.columns:
        df["dietary_flags"] = None
    df = parse_dietary_flags(df)
    if "base_servings" not in df.columns:
        df["base_servings"] = 4
    df = coerce_base_servings(df)
    if "source" not in df.columns:
        df = add_source_column(df, "yummly")
    df = clean_na_values(df)
    return df
