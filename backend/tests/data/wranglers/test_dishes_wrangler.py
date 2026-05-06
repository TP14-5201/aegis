import pandas as pd
import pytest

from src.data.wranglers.dishes_wrangler import (
    parse_dietary_flags,
    coerce_base_servings,
    wrangle_dishes,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_dishes_df(**overrides) -> pd.DataFrame:
    row = {
        "name": "Test Dish",
        "cuisine": "Italian",
        "dietary_flags": '["Vegetarian"]',
        "base_servings": "4",
        "description": "A test dish",
        "source": "manual",
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# parse_dietary_flags
# ---------------------------------------------------------------------------

class TestParseDietaryFlags:
    def test_parses_json_string_list(self):
        df = make_dishes_df(dietary_flags='["Vegetarian", "Gluten-free"]')
        result = parse_dietary_flags(df)
        assert result["dietary_flags"].iloc[0] == ["Vegetarian", "Gluten-free"]

    def test_empty_list_string(self):
        df = make_dishes_df(dietary_flags="[]")
        result = parse_dietary_flags(df)
        assert result["dietary_flags"].iloc[0] == []

    def test_none_value_returns_empty_list(self):
        df = make_dishes_df(dietary_flags=None)
        result = parse_dietary_flags(df)
        assert result["dietary_flags"].iloc[0] == []

    def test_already_list_passthrough(self):
        df = make_dishes_df()
        df["dietary_flags"] = [["Vegan"]]
        result = parse_dietary_flags(df)
        assert result["dietary_flags"].iloc[0] == ["Vegan"]

    def test_invalid_json_returns_empty_list(self):
        df = make_dishes_df(dietary_flags="not-valid-json")
        result = parse_dietary_flags(df)
        assert result["dietary_flags"].iloc[0] == []


# ---------------------------------------------------------------------------
# coerce_base_servings
# ---------------------------------------------------------------------------

class TestCoerceBaseServings:
    def test_string_int_is_coerced(self):
        df = make_dishes_df(base_servings="4")
        result = coerce_base_servings(df)
        assert result["base_servings"].iloc[0] == 4
        assert result["base_servings"].dtype == int

    def test_non_parseable_defaults_to_4(self):
        df = make_dishes_df(base_servings="abc")
        result = coerce_base_servings(df)
        assert result["base_servings"].iloc[0] == 4

    def test_none_defaults_to_4(self):
        df = make_dishes_df(base_servings=None)
        result = coerce_base_servings(df)
        assert result["base_servings"].iloc[0] == 4


# ---------------------------------------------------------------------------
# wrangle_dishes (integration)
# ---------------------------------------------------------------------------

class TestWrangleDishes:
    def test_returns_dataframe(self):
        df = make_dishes_df()
        result = wrangle_dishes(df)
        assert isinstance(result, pd.DataFrame)

    def test_has_required_columns(self):
        df = make_dishes_df()
        result = wrangle_dishes(df)
        assert "name" in result.columns
        assert "cuisine" in result.columns
        assert "dietary_flags" in result.columns
        assert "base_servings" in result.columns
        assert "source" in result.columns

    def test_dietary_flags_is_list(self):
        df = make_dishes_df(dietary_flags='["Vegan"]')
        result = wrangle_dishes(df)
        assert isinstance(result["dietary_flags"].iloc[0], list)

    def test_multiple_rows(self):
        rows = [
            {"name": "Dish A", "cuisine": "Italian", "dietary_flags": "[]", "base_servings": "4", "description": "", "source": "manual"},
            {"name": "Dish B", "cuisine": "Indian", "dietary_flags": '["Vegan"]', "base_servings": "2", "description": "", "source": "manual"},
        ]
        df = pd.DataFrame(rows)
        result = wrangle_dishes(df)
        assert len(result) == 2

    def test_adds_source_if_missing(self):
        df = make_dishes_df()
        df = df.drop(columns=["source"])
        result = wrangle_dishes(df)
        assert result["source"].iloc[0] == "yummly"
