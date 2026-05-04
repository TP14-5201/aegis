import pandas as pd
import pytest

from src.data.wranglers.ingredient_nutrients_wrangler import (
    coerce_amount,
    wrangle_ingredient_nutrients,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_nutrients_df(**overrides) -> pd.DataFrame:
    row = {
        "ingredient_name": "Beef Mince",
        "nutrient_name": "protein",
        "amount_per_100g": "26.0",
        "unit": "g",
        "usda_fdc_id": "174032",
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# coerce_amount
# ---------------------------------------------------------------------------

class TestCoerceAmount:
    def test_string_float_is_coerced(self):
        df = make_nutrients_df(amount_per_100g="26.5")
        result = coerce_amount(df)
        assert abs(result["amount_per_100g"].iloc[0] - 26.5) < 0.01

    def test_non_parseable_yields_nan(self):
        df = make_nutrients_df(amount_per_100g="trace")
        result = coerce_amount(df)
        assert pd.isna(result["amount_per_100g"].iloc[0])


# ---------------------------------------------------------------------------
# wrangle_ingredient_nutrients (integration)
# ---------------------------------------------------------------------------

class TestWrangleIngredientNutrients:
    def test_returns_dataframe(self):
        df = make_nutrients_df()
        result = wrangle_ingredient_nutrients(df)
        assert isinstance(result, pd.DataFrame)

    def test_empty_dataframe_returns_empty_with_schema(self):
        df = pd.DataFrame(columns=["ingredient_name", "nutrient_name", "amount_per_100g", "unit"])
        result = wrangle_ingredient_nutrients(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert "ingredient_name" in result.columns

    def test_all_na_rows_treated_as_empty(self):
        df = pd.DataFrame([{"ingredient_name": None, "nutrient_name": None, "amount_per_100g": None, "unit": None}])
        result = wrangle_ingredient_nutrients(df)
        assert len(result) == 0

    def test_has_required_columns(self):
        df = make_nutrients_df()
        result = wrangle_ingredient_nutrients(df)
        for col in ["ingredient_name", "nutrient_name", "amount_per_100g", "unit"]:
            assert col in result.columns

    def test_amount_is_numeric(self):
        df = make_nutrients_df(amount_per_100g="26.0")
        result = wrangle_ingredient_nutrients(df)
        assert result["amount_per_100g"].iloc[0] == 26.0

    def test_multiple_nutrients_per_ingredient(self):
        rows = [
            {"ingredient_name": "Beef Mince", "nutrient_name": "protein", "amount_per_100g": "26.0", "unit": "g", "usda_fdc_id": "174032"},
            {"ingredient_name": "Beef Mince", "nutrient_name": "iron", "amount_per_100g": "2.6", "unit": "mg", "usda_fdc_id": "174032"},
        ]
        df = pd.DataFrame(rows)
        result = wrangle_ingredient_nutrients(df)
        assert len(result) == 2
