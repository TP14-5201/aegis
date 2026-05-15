import pandas as pd
import pytest

from src.data.wranglers.ingredient_wrangler import (
    _remove_ingredients_with_null_codes,
    _fill_null_retail_price,
    _deduplicate_keeping_cheapest,
    _filter_unhealthy_food_categories,
    _apply_health_and_dietary_tags,
    wrangle_ingredient,
)


def _make_ingredient_df(**overrides):
    row = {
        "sku": "A001",
        "product_name": "Broccoli",
        "sub_category": "Vegetables",
        "retail_price": 2.99,
        "unit_price": 2.99,
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# _remove_ingredients_with_null_codes
# ---------------------------------------------------------------------------

class TestRemoveIngredientsWithNullCodes:
    def test_removes_null_sku_rows(self):
        df = pd.DataFrame({"sku": ["A001", None, "A002"]})
        result = _remove_ingredients_with_null_codes(df)
        assert len(result) == 2
        assert result["sku"].notna().all()

    def test_returns_empty_when_all_null(self):
        df = pd.DataFrame({"sku": [None, None]})
        result = _remove_ingredients_with_null_codes(df)
        assert result.empty

    def test_keeps_all_rows_when_none_null(self):
        df = pd.DataFrame({"sku": ["A001", "A002", "A003"]})
        result = _remove_ingredients_with_null_codes(df)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# _fill_null_retail_price
# ---------------------------------------------------------------------------

class TestFillNullRetailPrice:
    def test_fills_null_retail_price_from_unit_price(self):
        df = pd.DataFrame({"retail_price": [5.99, None], "unit_price": [5.99, 2.99]})
        result = _fill_null_retail_price(df)
        assert result["retail_price"].iloc[1] == 2.99

    def test_non_null_retail_price_unchanged(self):
        df = pd.DataFrame({"retail_price": [3.49], "unit_price": [9.99]})
        result = _fill_null_retail_price(df)
        assert result["retail_price"].iloc[0] == 3.49

    def test_remains_null_when_both_prices_null(self):
        df = pd.DataFrame({"retail_price": [None], "unit_price": [None]})
        result = _fill_null_retail_price(df)
        assert pd.isna(result["retail_price"].iloc[0])


# ---------------------------------------------------------------------------
# _deduplicate_keeping_cheapest
# ---------------------------------------------------------------------------

class TestDeduplicateKeepingCheapest:
    def test_keeps_cheapest_duplicate(self):
        df = pd.DataFrame({
            "product_name": ["Milk", "Milk"],
            "retail_price": [3.99, 2.49],
        })
        result = _deduplicate_keeping_cheapest(df)
        assert len(result) == 1
        assert result.iloc[0]["retail_price"] == 2.49

    def test_no_duplicates_unchanged(self):
        df = pd.DataFrame({
            "product_name": ["Milk", "Bread"],
            "retail_price": [3.99, 2.49],
        })
        result = _deduplicate_keeping_cheapest(df)
        assert len(result) == 2

    def test_handles_unparseable_price(self):
        df = pd.DataFrame({
            "product_name": ["Cheese", "Cheese"],
            "retail_price": ["not-a-price", 4.99],
        })
        result = _deduplicate_keeping_cheapest(df)
        assert len(result) == 1
        assert result.iloc[0]["retail_price"] == 4.99

    def test_empty_dataframe_returns_empty(self):
        df = pd.DataFrame({"product_name": [], "retail_price": []})
        result = _deduplicate_keeping_cheapest(df)
        assert result.empty


# ---------------------------------------------------------------------------
# _filter_unhealthy_food_categories
# ---------------------------------------------------------------------------

class TestFilterUnhealthyFoodCategories:
    def test_removes_unhealthy_categories(self):
        df = pd.DataFrame({"sub_category": ["Vegetables", "Coffee", "Fruit", "Soft drinks"]})
        result = _filter_unhealthy_food_categories(df)
        assert set(result["sub_category"].tolist()) == {"Vegetables", "Fruit"}

    def test_all_unhealthy_returns_empty(self):
        df = pd.DataFrame({"sub_category": ["Coffee", "Tea", "Energy drinks"]})
        result = _filter_unhealthy_food_categories(df)
        assert result.empty

    def test_null_subcategory_row_is_kept(self):
        df = pd.DataFrame({"sub_category": [None, "Coffee"]})
        result = _filter_unhealthy_food_categories(df)
        assert len(result) == 1
        assert pd.isna(result.iloc[0]["sub_category"])

    def test_healthy_categories_all_kept(self):
        df = pd.DataFrame({"sub_category": ["Vegetables", "Seafood", "Dairy"]})
        result = _filter_unhealthy_food_categories(df)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# _apply_health_and_dietary_tags
# ---------------------------------------------------------------------------

class TestApplyHealthAndDietaryTags:
    def test_known_category_gets_benefits(self):
        df = pd.DataFrame({"sub_category": ["Vegetables"]})
        result = _apply_health_and_dietary_tags(df)
        assert "health_benefits" in result.columns
        assert result.iloc[0]["health_benefits"] == ["Immunity", "Eye"]

    def test_unknown_category_gets_empty_list(self):
        df = pd.DataFrame({"sub_category": ["Unknown Category"]})
        result = _apply_health_and_dietary_tags(df)
        assert result.iloc[0]["health_benefits"] == []

    def test_null_category_gets_empty_list(self):
        df = pd.DataFrame({"sub_category": [None]})
        result = _apply_health_and_dietary_tags(df)
        assert result.iloc[0]["health_benefits"] == []


# ---------------------------------------------------------------------------
# wrangle_ingredient
# ---------------------------------------------------------------------------

class TestWrangleIngredient:
    def test_pipeline_returns_expected_columns(self):
        df = _make_ingredient_df()
        result = wrangle_ingredient(df)
        assert set(result.columns) == {"ingredient_code", "product_name", "sub_category", "retail_price"}

    def test_sku_renamed_to_ingredient_code(self):
        df = _make_ingredient_df(sku="X999")
        result = wrangle_ingredient(df)
        assert "ingredient_code" in result.columns
        assert result.iloc[0]["ingredient_code"] == "X999"

    def test_unhealthy_category_filtered_out(self):
        df = pd.DataFrame([
            {"sku": "A001", "product_name": "Cola", "sub_category": "Soft drinks",
             "retail_price": 1.99, "unit_price": 1.99},
            {"sku": "A002", "product_name": "Broccoli", "sub_category": "Vegetables",
             "retail_price": 2.99, "unit_price": 2.99},
        ])
        result = wrangle_ingredient(df)
        assert "Soft drinks" not in result["sub_category"].values
        assert "Vegetables" in result["sub_category"].values

    def test_empty_input_returns_empty(self):
        df = pd.DataFrame(columns=["sku", "product_name", "sub_category", "retail_price", "unit_price"])
        result = wrangle_ingredient(df)
        assert result.empty
