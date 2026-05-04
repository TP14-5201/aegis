import pandas as pd
import pytest

from src.data.wranglers.dish_ingredients_wrangler import (
    coerce_quantity,
    coerce_is_optional,
    wrangle_dish_ingredients,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_dish_ingredients_df(**overrides) -> pd.DataFrame:
    row = {
        "dish_name": "Spaghetti Bolognese",
        "ingredient_name": "Beef Mince",
        "quantity_g": "125",
        "is_optional": "False",
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# coerce_quantity
# ---------------------------------------------------------------------------

class TestCoerceQuantity:
    def test_string_float_is_coerced(self):
        df = make_dish_ingredients_df(quantity_g="125.5")
        result = coerce_quantity(df)
        assert abs(result["quantity_g"].iloc[0] - 125.5) < 0.01

    def test_non_parseable_yields_nan(self):
        df = make_dish_ingredients_df(quantity_g="abc")
        result = coerce_quantity(df)
        assert pd.isna(result["quantity_g"].iloc[0])


# ---------------------------------------------------------------------------
# coerce_is_optional
# ---------------------------------------------------------------------------

class TestCoerceIsOptional:
    def test_false_string(self):
        df = make_dish_ingredients_df(is_optional="False")
        result = coerce_is_optional(df)
        assert result["is_optional"].iloc[0] == False

    def test_true_string(self):
        df = make_dish_ingredients_df(is_optional="True")
        result = coerce_is_optional(df)
        assert result["is_optional"].iloc[0] == True

    def test_case_insensitive(self):
        df = make_dish_ingredients_df(is_optional="TRUE")
        result = coerce_is_optional(df)
        assert result["is_optional"].iloc[0] == True

    def test_unknown_value_defaults_false(self):
        df = make_dish_ingredients_df(is_optional="maybe")
        result = coerce_is_optional(df)
        assert result["is_optional"].iloc[0] is False


# ---------------------------------------------------------------------------
# wrangle_dish_ingredients (integration)
# ---------------------------------------------------------------------------

class TestWrangleDishIngredients:
    def test_returns_dataframe(self):
        df = make_dish_ingredients_df()
        result = wrangle_dish_ingredients(df)
        assert isinstance(result, pd.DataFrame)

    def test_preserves_name_columns(self):
        df = make_dish_ingredients_df()
        result = wrangle_dish_ingredients(df)
        assert "dish_name" in result.columns
        assert "ingredient_name" in result.columns

    def test_quantity_is_numeric(self):
        df = make_dish_ingredients_df(quantity_g="200")
        result = wrangle_dish_ingredients(df)
        assert result["quantity_g"].iloc[0] == 200.0

    def test_is_optional_is_bool(self):
        df = make_dish_ingredients_df(is_optional="True")
        result = wrangle_dish_ingredients(df)
        assert result["is_optional"].iloc[0] == True

    def test_multiple_rows(self):
        rows = [
            {"dish_name": "Dish A", "ingredient_name": "Beef Mince", "quantity_g": "100", "is_optional": "False"},
            {"dish_name": "Dish A", "ingredient_name": "Spaghetti", "quantity_g": "80", "is_optional": "False"},
        ]
        df = pd.DataFrame(rows)
        result = wrangle_dish_ingredients(df)
        assert len(result) == 2
