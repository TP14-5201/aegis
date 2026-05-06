import json
import pandas as pd
import pytest

from src.data.wranglers.ingredients_wrangler import (
    compute_price_per_100g,
    add_nullable_usda_columns,
    wrangle_ingredients,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_ingredients_df(**overrides) -> pd.DataFrame:
    row = {
        "name": "Beef Mince",
        "category": "protein",
        "pack_size_g": "500",
        "pack_price_aud": "7.50",
        "supermarket": "Coles",
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# compute_price_per_100g
# ---------------------------------------------------------------------------

class TestComputePricePer100g:
    def test_basic_calculation(self):
        df = make_ingredients_df(pack_size_g="500", pack_price_aud="7.50")
        df["pack_grams"] = df["pack_size_g"].astype(float)
        df["price_aud"] = df["pack_price_aud"].astype(float)
        result = compute_price_per_100g(df)
        assert abs(result["price_per_100g"].iloc[0] - 1.5) < 0.01

    def test_string_inputs_are_coerced(self):
        df = make_ingredients_df(pack_size_g="1000", pack_price_aud="5.00")
        df["pack_grams"] = df["pack_size_g"]
        df["price_aud"] = df["pack_price_aud"]
        result = compute_price_per_100g(df)
        assert abs(result["price_per_100g"].iloc[0] - 0.5) < 0.01

    def test_zero_pack_size_yields_nan(self):
        df = make_ingredients_df(pack_size_g="0", pack_price_aud="5.00")
        df["pack_grams"] = df["pack_size_g"]
        df["price_aud"] = df["pack_price_aud"]
        result = compute_price_per_100g(df)
        assert pd.isna(result["price_per_100g"].iloc[0])


# ---------------------------------------------------------------------------
# add_nullable_usda_columns
# ---------------------------------------------------------------------------

class TestAddNullableUsdaColumns:
    def test_adds_benefit_tags_column(self):
        df = make_ingredients_df()
        result = add_nullable_usda_columns(df)
        assert "benefit_tags" in result.columns
        assert result["benefit_tags"].iloc[0] is None

    def test_converts_existing_benefit_tag(self):
        df = make_ingredients_df()
        df["benefit_tag"] = "Muscles"
        result = add_nullable_usda_columns(df)
        assert "benefit_tag" not in result.columns
        assert json.loads(result["benefit_tags"].iloc[0]) == ["Muscles"]


# ---------------------------------------------------------------------------
# wrangle_ingredients (integration)
# ---------------------------------------------------------------------------

class TestWrangleIngredients:
    def test_returns_dataframe(self):
        df = make_ingredients_df()
        result = wrangle_ingredients(df)
        assert isinstance(result, pd.DataFrame)

    def test_has_price_per_100g(self):
        df = make_ingredients_df(pack_size_g="500", pack_price_aud="7.50")
        result = wrangle_ingredients(df)
        assert "price_per_100g" in result.columns
        assert abs(result["price_per_100g"].iloc[0] - 1.5) < 0.01

    def test_has_nullable_usda_columns(self):
        df = make_ingredients_df()
        result = wrangle_ingredients(df)
        assert "benefit_tags" in result.columns

    def test_adds_source_if_missing(self):
        df = make_ingredients_df()
        result = wrangle_ingredients(df)
        assert "source" in result.columns
        assert result["source"].iloc[0] == "open_food_facts"

    def test_multiple_rows(self):
        rows = [
            {"name": "Beef Mince", "category": "protein", "pack_size_g": "500", "pack_price_aud": "7.50", "supermarket": "Coles"},
            {"name": "Chicken Breast", "category": "protein", "pack_size_g": "600", "pack_price_aud": "9.00", "supermarket": "Woolworths"},
        ]
        df = pd.DataFrame(rows)
        result = wrangle_ingredients(df)
        assert len(result) == 2
