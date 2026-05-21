import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from src.services.recommendation_service import (
    _dietary_vetoed,
    _load_ingredients_df,
    _compute_rec_score,
    _compute_nutrient_badges,
    warm_percentiles,
    select_bag,
    score_ingredients,
    score_ingredients_with_preferences,
)
from src.services import recommendation_service


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(**kwargs) -> pd.Series:
    defaults = {
        "ingredient_code": "0001",
        "product_name": "Test Item",
        "sub_category": "Vegetables",
        "retail_price": 5.0,
        "nutriscore_grade": "b",
        "nova_score": 1,
        "final_health_score": 70.0,
        "protein_g": 5.0,
        "fibre_g": 2.0,
        "fat_g": 1.0,
        "sugars_g": 2.0,
    }
    defaults.update(kwargs)
    return pd.Series(defaults)


def _make_df(rows: list[dict]) -> pd.DataFrame:
    full_rows = [_make_row(**r) for r in rows]
    return pd.DataFrame(full_rows).reset_index(drop=True)


def _make_scored_df(rows: list[dict]) -> pd.DataFrame:
    """DataFrame already containing rec_score column."""
    df = _make_df(rows)
    df["rec_score"] = [r.get("rec_score", 0.5) for r in rows]
    df["nutrient_badges"] = [[] for _ in rows]
    return df.sort_values("rec_score", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# _dietary_vetoed
# ---------------------------------------------------------------------------

class TestDietaryVetoed:
    def test_seafood_vetoed_for_vegetarian(self):
        assert _dietary_vetoed("Seafood", ["vegetarian"]) is True

    def test_vegetables_not_vetoed_for_vegetarian(self):
        assert _dietary_vetoed("Vegetables", ["vegetarian"]) is False

    def test_pork_vetoed_for_halal(self):
        assert _dietary_vetoed("Pork", ["halal"]) is True

    def test_vegetables_not_vetoed_for_halal(self):
        assert _dietary_vetoed("Vegetables", ["halal"]) is False

    def test_cheese_vetoed_for_vegan(self):
        assert _dietary_vetoed("Cheese", ["vegan"]) is True

    def test_eggs_vetoed_for_vegan(self):
        assert _dietary_vetoed("Eggs", ["vegan"]) is True

    def test_cheese_vetoed_for_dairy_free(self):
        assert _dietary_vetoed("Cheese", ["dairy-free"]) is True

    def test_milk_not_vetoed_for_halal(self):
        assert _dietary_vetoed("Milk", ["halal"]) is False

    def test_no_dietary_needs_never_vetoes(self):
        assert _dietary_vetoed("Pork", []) is False

    def test_case_insensitive_need(self):
        assert _dietary_vetoed("Pork", ["Halal"]) is True

    def test_unknown_need_never_vetoes(self):
        assert _dietary_vetoed("Beef & veal", ["keto"]) is False

    def test_multiple_needs_any_match_vetoes(self):
        assert _dietary_vetoed("Pork", ["vegetarian", "halal"]) is True


# ---------------------------------------------------------------------------
# _compute_rec_score
# ---------------------------------------------------------------------------

class TestComputeRecScore:
    def test_price_above_cap_returns_zero(self):
        row = _make_row(retail_price=20.0)
        assert _compute_rec_score(row, price_cap=10.0, cat_median_prices={}, dietary_needs=[]) == 0.0

    def test_vetoed_sub_category_returns_zero(self):
        row = _make_row(sub_category="Pork", retail_price=5.0)
        assert _compute_rec_score(row, price_cap=20.0, cat_median_prices={}, dietary_needs=["halal"]) == 0.0

    def test_valid_item_returns_positive_score(self):
        row = _make_row(retail_price=5.0, sub_category="Vegetables")
        score = _compute_rec_score(row, price_cap=20.0, cat_median_prices={"Vegetables": 8.0}, dietary_needs=[])
        assert 0.0 < score <= 1.0

    def test_score_capped_at_one(self):
        row = _make_row(retail_price=0.01, protein_g=30.0, fibre_g=10.0, nutriscore_grade="a", nova_score=1)
        score = _compute_rec_score(row, price_cap=100.0, cat_median_prices={}, dietary_needs=[])
        assert score <= 1.0

    def test_missing_nutriscore_uses_default(self):
        row = _make_row(nutriscore_grade=None, retail_price=5.0)
        score = _compute_rec_score(row, price_cap=20.0, cat_median_prices={}, dietary_needs=[])
        assert score > 0.0

    def test_missing_nova_uses_default(self):
        row = _make_row(nova_score=None, retail_price=5.0)
        score = _compute_rec_score(row, price_cap=20.0, cat_median_prices={}, dietary_needs=[])
        assert score > 0.0

    def test_cheaper_item_scores_higher_affordability(self):
        cheap = _make_row(retail_price=3.0, sub_category="Fruit")
        pricey = _make_row(retail_price=9.0, sub_category="Fruit")
        cap = 12.0
        medians = {"Fruit": 6.0}
        assert _compute_rec_score(cheap, cap, medians, []) > _compute_rec_score(pricey, cap, medians, [])

    def test_invalid_nova_score_uses_default_deduction(self):
        row = _make_row(nova_score="not-a-number", retail_price=5.0)
        score = _compute_rec_score(row, price_cap=20.0, cat_median_prices={}, dietary_needs=[])
        assert score > 0.0


# ---------------------------------------------------------------------------
# _compute_nutrient_badges
# ---------------------------------------------------------------------------

class TestComputeNutrientBadges:
    def test_high_protein_badge(self):
        row = _make_row(protein_g=15.0)
        assert "High protein" in _compute_nutrient_badges(row)

    def test_no_high_protein_below_threshold(self):
        row = _make_row(protein_g=5.0)
        assert "High protein" not in _compute_nutrient_badges(row)

    def test_high_fibre_badge(self):
        row = _make_row(fibre_g=5.0)
        assert "High fibre" in _compute_nutrient_badges(row)

    def test_low_fat_badge(self):
        row = _make_row(fat_g=1.0)
        assert "Low fat" in _compute_nutrient_badges(row)

    def test_no_low_fat_above_threshold(self):
        row = _make_row(fat_g=10.0)
        assert "Low fat" not in _compute_nutrient_badges(row)

    def test_low_sugar_badge(self):
        row = _make_row(sugars_g=2.0)
        assert "Low sugar" in _compute_nutrient_badges(row)

    def test_multiple_badges(self):
        row = _make_row(protein_g=15.0, fat_g=1.0)
        badges = _compute_nutrient_badges(row)
        assert "High protein" in badges
        assert "Low fat" in badges

    def test_no_badges_for_average_item(self):
        row = _make_row(protein_g=5.0, fibre_g=1.0, fat_g=8.0, sugars_g=10.0)
        assert _compute_nutrient_badges(row) == []


# ---------------------------------------------------------------------------
# select_bag
# ---------------------------------------------------------------------------

class TestSelectBag:
    def _scored(self, entries: list[tuple[str, float]]) -> pd.DataFrame:
        rows = [
            {"sub_category": cat, "rec_score": score, "ingredient_code": f"code_{i}",
             "product_name": f"Item {i}", "retail_price": 5.0, "nutriscore_grade": "b",
             "nova_score": 1, "final_health_score": 70.0, "protein_g": 5.0,
             "fibre_g": 2.0, "fat_g": 1.0, "sugars_g": 2.0, "nutrient_badges": []}
            for i, (cat, score) in enumerate(entries)
        ]
        df = pd.DataFrame(rows)
        return df.sort_values("rec_score", ascending=False).reset_index(drop=True)

    def test_max_per_category_respected(self):
        entries = [("Vegetables", 0.9), ("Vegetables", 0.8), ("Vegetables", 0.7), ("Vegetables", 0.6)]
        result = select_bag(self._scored(entries), bag_size=10, max_per_category=3)
        assert (result["sub_category"] == "Vegetables").sum() <= 3

    def test_bag_size_respected(self):
        entries = [(f"Cat{i % 5}", 1.0 - i * 0.01) for i in range(20)]
        result = select_bag(self._scored(entries), bag_size=5, max_per_category=3)
        assert len(result) <= 5

    def test_score_order_preserved(self):
        entries = [("A", 0.9), ("B", 0.8), ("A", 0.7), ("C", 0.6)]
        result = select_bag(self._scored(entries), bag_size=10, max_per_category=3)
        scores = result["rec_score"].tolist()
        assert scores == sorted(scores, reverse=True)

    def test_empty_df_returns_empty(self):
        df = pd.DataFrame(columns=["sub_category", "rec_score", "ingredient_code",
                                    "product_name", "retail_price"])
        result = select_bag(df, bag_size=10)
        assert len(result) == 0

    def test_fewer_items_than_bag_size(self):
        entries = [("A", 0.9), ("B", 0.8)]
        result = select_bag(self._scored(entries), bag_size=15, max_per_category=3)
        assert len(result) == 2

    def test_high_scoring_category_gets_more_slots(self):
        entries = [("Seafood", 0.95), ("Seafood", 0.90), ("Seafood", 0.85),
                   ("Eggs", 0.40), ("Fruit", 0.30)]
        result = select_bag(self._scored(entries), bag_size=5, max_per_category=3)
        assert (result["sub_category"] == "Seafood").sum() == 3


# ---------------------------------------------------------------------------
# score_ingredients — uses mock DB via patching _load_ingredients_df
# ---------------------------------------------------------------------------

def _make_ingredients_df() -> pd.DataFrame:
    return pd.DataFrame([
        {"ingredient_code": "A1", "product_name": "Chicken breast", "sub_category": "Poultry",
         "retail_price": 8.0, "nutriscore_grade": "a", "nova_score": 1,
         "final_health_score": 85.0, "protein_g": 20.0, "fibre_g": 0.0, "fat_g": 2.0, "sugars_g": 0.0},
        {"ingredient_code": "A2", "product_name": "Pork belly", "sub_category": "Pork",
         "retail_price": 10.0, "nutriscore_grade": "d", "nova_score": 3,
         "final_health_score": 30.0, "protein_g": 15.0, "fibre_g": 0.0, "fat_g": 25.0, "sugars_g": 0.0},
        {"ingredient_code": "A3", "product_name": "Broccoli", "sub_category": "Vegetables",
         "retail_price": 4.0, "nutriscore_grade": "a", "nova_score": 1,
         "final_health_score": 90.0, "protein_g": 3.0, "fibre_g": 5.0, "fat_g": 0.3, "sugars_g": 1.5},
        {"ingredient_code": "A4", "product_name": "Expensive wagyu", "sub_category": "Beef & veal",
         "retail_price": 100.0, "nutriscore_grade": "b", "nova_score": 1,
         "final_health_score": 60.0, "protein_g": 25.0, "fibre_g": 0.0, "fat_g": 20.0, "sugars_g": 0.0},
    ])


class TestWarmPercentilesAndLoadIngredients:
    def test_warm_percentiles_populates_cache_and_logs(self):
        df = _make_ingredients_df()

        with patch("src.services.recommendation_service._load_ingredients_df", return_value=df), \
             patch("src.services.recommendation_service.logger") as mock_logger:
            warm_percentiles(MagicMock())

        assert recommendation_service._PERCENTILES["protein_g"]["p25"] == pytest.approx(df["protein_g"].quantile(0.25))
        assert recommendation_service._PERCENTILES["total_sugars_g"]["p75"] == pytest.approx(df["sugars_g"].quantile(0.75))
        mock_logger.info.assert_called_once()

    def test_load_ingredients_df_builds_dataframe_and_filters_missing_or_non_positive_prices(self):
        rows = [
            ("A1", "Apple", "Fruit", 2.0, 0.20, "100G", 0.25, "a", 1, 90.0, 0.3, 2.4, 0.1, 10.0),
            ("A2", "Free sample", "Fruit", 0.0, 0.10, "100G", 0.12, "b", 1, 80.0, 1.0, 1.0, 1.0, 1.0),
            ("A3", "Missing price", "Fruit", None, None, None, None, "c", 1, 70.0, 1.0, 1.0, 1.0, 1.0),
        ]
        query = MagicMock()
        query.outerjoin.return_value = query
        query.all.return_value = rows
        db = MagicMock()
        db.query.return_value = query

        result = _load_ingredients_df(db)

        assert list(result["ingredient_code"]) == ["A1"]
        assert list(result.columns) == [
            "ingredient_code",
            "product_name",
            "sub_category",
            "retail_price",
            "unit_price",
            "unit_price_unit",
            "unit_price_adjusted",
            "nutriscore_grade",
            "nova_score",
            "final_health_score",
            "protein_g",
            "fibre_g",
            "fat_g",
            "sugars_g",
        ]


class TestScoreIngredients:
    def test_all_prices_within_budget_cap(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()):
            db = MagicMock()
            result = score_ingredients(db, budget=60.0, people=2, days=5, dietary_needs=[])
        viable = result[result["rec_score"] > 0]
        assert all(viable["retail_price"] <= 60.0 / 5.0)

    def test_sorted_descending_by_rec_score(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()):
            db = MagicMock()
            result = score_ingredients(db, budget=60.0, people=2, days=5, dietary_needs=[])
        scores = result["rec_score"].tolist()
        assert scores == sorted(scores, reverse=True)

    def test_expensive_item_has_zero_score(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()):
            db = MagicMock()
            result = score_ingredients(db, budget=60.0, people=2, days=5, dietary_needs=[])
        wagyu = result[result["ingredient_code"] == "A4"]
        assert wagyu.iloc[0]["rec_score"] == 0.0

    def test_vegan_vetos_pork(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()):
            db = MagicMock()
            result = score_ingredients(db, budget=60.0, people=2, days=5, dietary_needs=["vegan"])
        pork = result[result["sub_category"] == "Pork"]
        assert all(pork["rec_score"] == 0.0)

    def test_nutrient_badges_column_present(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()):
            db = MagicMock()
            result = score_ingredients(db, budget=60.0, people=2, days=5, dietary_needs=[])
        assert "nutrient_badges" in result.columns


# ---------------------------------------------------------------------------
# score_ingredients_with_preferences
# ---------------------------------------------------------------------------

class TestScoreIngredientsWithPreferences:
    def _prefs(self, **kwargs):
        base = {"preferred_sub_categories": [], "nutrient_priorities": [], "avoid_sub_categories": []}
        base.update(kwargs)
        return base

    def test_avoid_sub_category_hard_filtered(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()), \
             patch("src.services.recommendation_service._sub_engine") as mock_engine:
            mock_engine.find_similar_to_text.return_value = {}
            db = MagicMock()
            result = score_ingredients_with_preferences(
                db, budget=60.0, people=2, days=5, dietary_needs=[],
                preferences=self._prefs(avoid_sub_categories=["Pork"]),
            )
        assert "Pork" not in result["sub_category"].values

    def test_preferred_sub_category_boosts_final_score(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()), \
             patch("src.services.recommendation_service._sub_engine") as mock_engine:
            mock_engine.find_similar_to_text.return_value = {}
            db = MagicMock()
            result = score_ingredients_with_preferences(
                db, budget=60.0, people=2, days=5, dietary_needs=[],
                preferences=self._prefs(preferred_sub_categories=["Vegetables"]),
            )
        veg = result[result["sub_category"] == "Vegetables"]
        if not veg.empty and veg.iloc[0]["rec_score"] > 0:
            assert veg.iloc[0]["preference_alignment"] > 0.0

    def test_no_preferences_final_score_equals_rec_score(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()), \
             patch("src.services.recommendation_service._sub_engine") as mock_engine:
            mock_engine.find_similar_to_text.return_value = {}
            db = MagicMock()
            result = score_ingredients_with_preferences(
                db, budget=60.0, people=2, days=5, dietary_needs=[],
                preferences=self._prefs(),
            )
        assert "final_score" in result.columns
        pd.testing.assert_series_equal(
            result["final_score"].round(6), result["rec_score"].round(6), check_names=False
        )

    def test_faiss_similarity_contributes_to_final_score(self):
        sim_map = {"A3": 0.9, "A1": 0.2}  # broccoli gets high FAISS score
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()), \
             patch("src.services.recommendation_service._sub_engine") as mock_engine:
            mock_engine.find_similar_to_text.return_value = sim_map
            db = MagicMock()
            result = score_ingredients_with_preferences(
                db, budget=60.0, people=2, days=5, dietary_needs=[],
                preferences=self._prefs(),
                description="I love vegetables",
            )
        broccoli = result[result["ingredient_code"] == "A3"].iloc[0]
        assert broccoli["preference_alignment"] > 0.0

    def test_sorted_descending_by_final_score(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()), \
             patch("src.services.recommendation_service._sub_engine") as mock_engine:
            mock_engine.find_similar_to_text.return_value = {}
            db = MagicMock()
            result = score_ingredients_with_preferences(
                db, budget=60.0, people=2, days=5, dietary_needs=[],
                preferences=self._prefs(),
            )
        scores = result["final_score"].tolist()
        assert scores == sorted(scores, reverse=True)

    def test_nutrient_priority_boosts_alignment_for_threshold_matches(self):
        with patch("src.services.recommendation_service._load_ingredients_df", return_value=_make_ingredients_df()), \
             patch("src.services.recommendation_service._sub_engine") as mock_engine:
            mock_engine.find_similar_to_text.return_value = {}
            result = score_ingredients_with_preferences(
                MagicMock(),
                budget=60.0,
                people=2,
                days=5,
                dietary_needs=[],
                preferences=self._prefs(nutrient_priorities=["protein_g", "unknown_priority"]),
            )

        chicken = result[result["ingredient_code"] == "A1"].iloc[0]
        assert chicken["preference_alignment"] == pytest.approx(0.2)


# ---------------------------------------------------------------------------
# select_bag — additional edge cases
# ---------------------------------------------------------------------------

class TestSelectBagEdgeCases:
    def _scored(self, entries):
        rows = [
            {"sub_category": cat, "rec_score": score, "ingredient_code": f"code_{i}",
             "product_name": f"Item {i}", "retail_price": 5.0, "nutriscore_grade": "b",
             "nova_score": 1, "final_health_score": 70.0, "protein_g": 5.0,
             "fibre_g": 2.0, "fat_g": 1.0, "sugars_g": 2.0, "nutrient_badges": []}
            for i, (cat, score) in enumerate(entries)
        ]
        df = pd.DataFrame(rows)
        return df.sort_values("rec_score", ascending=False).reset_index(drop=True)

    def test_stops_exactly_at_bag_size(self):
        entries = [(f"Cat{i}", 1.0 - i * 0.01) for i in range(10)]
        result = select_bag(self._scored(entries), bag_size=5, max_per_category=3)
        assert len(result) == 5

    def test_none_sub_category_treated_as_empty_string(self):
        entries = [(None, 0.9), (None, 0.8), (None, 0.7), (None, 0.6)]
        result = select_bag(self._scored(entries), bag_size=10, max_per_category=3)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# score_ingredients — budget-zero edge case
# ---------------------------------------------------------------------------

class TestScoreIngredientsEdgeCases:
    def test_budget_zero_gives_all_zero_scores(self):
        with patch("src.services.recommendation_service._load_ingredients_df",
                   return_value=_make_ingredients_df()):
            db = MagicMock()
            result = score_ingredients(db, budget=0.0, people=2, days=5, dietary_needs=[])
        assert (result["rec_score"] == 0.0).all()
