from unittest.mock import patch
from types import SimpleNamespace

import pandas as pd

from src.data.wranglers import nutrition_wrangler
from src.data.wranglers.nutrition_wrangler import (
    _clean_nutrition_header,
    _map_ingredients_to_price,
    _perform_ingredient_name_matching,
    wrangle_ingredient_nutrition,
)


def test_clean_nutrition_header_uses_second_row_as_headers_and_removes_newlines():
    df = pd.DataFrame(
        [
            ["metadata", "metadata"],
            ["Food\nName", "Protein\n(g)"],
            ["Apple", 0.3],
        ]
    )

    result = _clean_nutrition_header(df)

    assert list(result.columns) == ["FoodName", "Protein(g)"]
    assert result.to_dict("records") == [{"FoodName": "Apple", "Protein(g)": 0.3}]


def test_perform_ingredient_name_matching_returns_best_original_nutrition_names():
    ingredient_df = pd.DataFrame({"product_name": ["red apple", "banana"]})
    nutrition_df = pd.DataFrame({"food_name": ["Red Apple Raw", "Banana ripe", None]})

    result = _perform_ingredient_name_matching(ingredient_df, nutrition_df)

    assert result["red apple"]["matched_product_name"] == "Red Apple Raw"
    assert result["banana"]["matched_product_name"] == "Banana ripe"
    assert result["red apple"]["score"] > 0


def test_perform_ingredient_name_matching_skips_when_no_match_returned():
    ingredient_df = pd.DataFrame({"product_name": ["Mystery"]})
    nutrition_df = pd.DataFrame({"food_name": ["Known"]})

    with patch("src.data.wranglers.nutrition_wrangler.process.extractOne", return_value=None):
        result = _perform_ingredient_name_matching(ingredient_df, nutrition_df)

    assert result == {}


def test_map_ingredients_to_price_merges_mapping_ingredients_and_nutrition_rows():
    mapping = {"Apple": {"matched_product_name": "Apple raw", "score": 95.0}}
    ingredient_df = pd.DataFrame(
        [{"ingredient_code": "A1", "product_name": "Apple", "retail_price": 1.5}]
    )
    nutrition_df = pd.DataFrame(
        [{"food_name": "Apple raw", "protein_g": 0.3}]
    )

    result = _map_ingredients_to_price(mapping, ingredient_df, nutrition_df)

    assert result.to_dict("records") == [
        {
            "ingredient_code": "A1",
            "product_name": "Apple",
            "retail_price": 1.5,
            "matched_product_name": "Apple raw",
            "match_score": 95.0,
            "food_name": "Apple raw",
            "protein_g": 0.3,
        }
    ]


def test_wrangle_ingredient_nutrition_runs_full_pipeline_and_selects_food_fact_columns(monkeypatch):
    ingredient_df = pd.DataFrame(
        [{"ingredient_code": "A1", "product_name": "Apple", "retail_price": 1.5}]
    )
    nutrition_df = pd.DataFrame(
        [
            ["metadata", "metadata"],
            ["Food Name", "Protein G"],
            ["Apple raw", 0.3],
        ]
    )
    monkeypatch.setattr(
        nutrition_wrangler,
        "settings",
        SimpleNamespace(FOOD_FACTS_COLS=["ingredient_code", "product_name", "food_name", "protein_g"]),
    )

    result = wrangle_ingredient_nutrition(ingredient_df, nutrition_df)

    assert list(result.columns) == ["ingredient_code", "product_name", "food_name", "protein_g"]
    assert result.iloc[0]["ingredient_code"] == "A1"
    assert result.iloc[0]["food_name"] == "Apple raw"
