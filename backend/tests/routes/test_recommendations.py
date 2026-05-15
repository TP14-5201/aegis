import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from src.main import app, get_db


# ---------------------------------------------------------------------------
# Shared fixture data
# ---------------------------------------------------------------------------

def _base_ingredients() -> pd.DataFrame:
    return pd.DataFrame([
        {"ingredient_code": "A1", "product_name": "Chicken breast", "sub_category": "Poultry",
         "retail_price": 8.0, "nutriscore_grade": "a", "nova_score": 1,
         "final_health_score": 85.0, "protein_g": 20.0, "fibre_g": 0.0,
         "fat_g": 2.0, "sugars_g": 0.0, "rec_score": 0.75, "nutrient_badges": ["High protein"]},
        {"ingredient_code": "A2", "product_name": "Broccoli", "sub_category": "Vegetables",
         "retail_price": 4.0, "nutriscore_grade": "a", "nova_score": 1,
         "final_health_score": 90.0, "protein_g": 3.0, "fibre_g": 5.0,
         "fat_g": 0.3, "sugars_g": 1.5, "rec_score": 0.70, "nutrient_badges": ["High fibre", "Low fat"]},
        {"ingredient_code": "A3", "product_name": "Salmon fillet", "sub_category": "Seafood",
         "retail_price": 11.0, "nutriscore_grade": "b", "nova_score": 1,
         "final_health_score": 80.0, "protein_g": 22.0, "fibre_g": 0.0,
         "fat_g": 8.0, "sugars_g": 0.0, "rec_score": 0.65, "nutrient_badges": ["High protein"]},
        {"ingredient_code": "A4", "product_name": "Pork belly", "sub_category": "Pork",
         "retail_price": 9.0, "nutriscore_grade": "d", "nova_score": 3,
         "final_health_score": 30.0, "protein_g": 15.0, "fibre_g": 0.0,
         "fat_g": 25.0, "sugars_g": 0.0, "rec_score": 0.0, "nutrient_badges": []},
        {"ingredient_code": "A5", "product_name": "Cheddar cheese", "sub_category": "Cheese",
         "retail_price": 7.0, "nutriscore_grade": "c", "nova_score": 2,
         "final_health_score": 50.0, "protein_g": 10.0, "fibre_g": 0.0,
         "fat_g": 20.0, "sugars_g": 0.5, "rec_score": 0.0, "nutrient_badges": []},
    ])


def _empty_prefs():
    return {"preferred_sub_categories": [], "nutrient_priorities": [], "avoid_sub_categories": []}


def _fake_get_db():
    yield MagicMock()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _post(payload: dict, query: dict | None = None):
    app.dependency_overrides[get_db] = _fake_get_db
    client = TestClient(app)
    url = "/recommendations"
    if query:
        qs = "&".join(f"{k}={v}" for k, v in query.items())
        url = f"{url}?{qs}"
    resp = client.post(url, json=payload)
    app.dependency_overrides.clear()
    return resp


# ---------------------------------------------------------------------------
# Basic request — no description, no dietary_goal
# ---------------------------------------------------------------------------

class TestRecommendationsBasic:
    def test_returns_200(self):
        df = _base_ingredients()
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=df[df["rec_score"] > 0]):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": []})
        assert resp.status_code == 200

    def test_response_has_ingredients_and_bdpp(self):
        df = _base_ingredients()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": []})
        body = resp.json()
        assert "ingredients" in body
        assert "budget_per_dish_per_person" in body

    def test_zero_score_items_excluded(self):
        df = _base_ingredients()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": []})
        codes = [i["ingredient_code"] for i in resp.json()["ingredients"]]
        assert "A4" not in codes  # Pork, score=0
        assert "A5" not in codes  # Cheese, score=0

    def test_ingredient_has_required_fields(self):
        df = _base_ingredients()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": []})
        item = resp.json()["ingredients"][0]
        for field in ("ingredient_code", "product_name", "sub_category", "retail_price",
                      "health_score", "rec_score", "nutrient_badges"):
            assert field in item


# ---------------------------------------------------------------------------
# Dietary restriction veto
# ---------------------------------------------------------------------------

class TestDietaryVeto:
    def test_vegan_excludes_pork_and_cheese(self):
        df = _base_ingredients()
        df.loc[df["sub_category"].isin(["Pork", "Cheese"]), "rec_score"] = 0.0
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": ["vegan"]})
        cats = [i["sub_category"] for i in resp.json()["ingredients"]]
        assert "Pork" not in cats
        assert "Cheese" not in cats

    def test_halal_excludes_pork(self):
        df = _base_ingredients()
        df.loc[df["sub_category"] == "Pork", "rec_score"] = 0.0
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": ["halal"]})
        cats = [i["sub_category"] for i in resp.json()["ingredients"]]
        assert "Pork" not in cats


# ---------------------------------------------------------------------------
# Description / dietary_goal preference path
# ---------------------------------------------------------------------------

class TestPreferencePath:
    def _prefs_df(self) -> pd.DataFrame:
        df = _base_ingredients()
        df["preference_alignment"] = 0.3
        df["final_score"] = df["rec_score"] * 0.7 + 0.3 * 0.3
        return df

    def test_description_triggers_preference_path(self):
        df = self._prefs_df()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.personalisation_service.extract_preferences", return_value=_empty_prefs()), \
             patch("src.services.recommendation_service.score_ingredients_with_preferences", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": [],
                          "description": "I love seafood"})
        assert resp.status_code == 200

    def test_dietary_goal_only_triggers_preference_path(self):
        df = self._prefs_df()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.personalisation_service.extract_preferences", return_value=_empty_prefs()), \
             patch("src.services.recommendation_service.score_ingredients_with_preferences", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": [],
                          "dietary_goal": "Muscle gain"})
        assert resp.status_code == 200

    def test_description_and_goal_combined(self):
        df = self._prefs_df()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        captured = {}
        def fake_extract(text):
            captured["text"] = text
            return _empty_prefs()
        with patch("src.services.personalisation_service.extract_preferences", side_effect=fake_extract), \
             patch("src.services.recommendation_service.score_ingredients_with_preferences", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": [],
                   "description": "I love seafood", "dietary_goal": "More protein"})
        assert "I love seafood" in captured["text"]
        assert "More protein" in captured["text"]

    def test_no_description_no_goal_uses_base_path(self):
        df = _base_ingredients()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df) as mock_score, \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": []})
        mock_score.assert_called_once()


# ---------------------------------------------------------------------------
# bag_size query param
# ---------------------------------------------------------------------------

class TestBagSize:
    def test_bag_size_passed_to_select_bag(self):
        df = _base_ingredients()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        captured = {}
        def fake_select_bag(scored, bag_size, max_per_category, score_col):
            captured["bag_size"] = bag_size
            return viable
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", side_effect=fake_select_bag):
            _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": []}, query={"bag_size": 7})
        assert captured["bag_size"] == 7

    def test_default_bag_size_is_15(self):
        df = _base_ingredients()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        captured = {}
        def fake_select_bag(scored, bag_size, max_per_category, score_col):
            captured["bag_size"] = bag_size
            return viable
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", side_effect=fake_select_bag):
            _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": []})
        assert captured["bag_size"] == 15


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_viable_returns_empty_ingredients(self):
        df = _base_ingredients()
        df["rec_score"] = 0.0
        empty = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=empty):
            resp = _post({"budget": 5, "people": 2, "days": 5, "dietary_needs": []})
        assert resp.status_code == 200
        assert resp.json()["ingredients"] == []

    def test_whitespace_only_description_uses_base_path(self):
        df = _base_ingredients()
        viable = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df) as mock_score, \
             patch("src.services.recommendation_service.select_bag", return_value=viable):
            resp = _post({"budget": 60, "people": 2, "days": 5, "dietary_needs": [],
                          "description": "   "})
        assert resp.status_code == 200
        mock_score.assert_called_once()

    def test_budget_zero_returns_200(self):
        df = _base_ingredients()
        df["rec_score"] = 0.0
        empty = df[df["rec_score"] > 0].reset_index(drop=True)
        with patch("src.services.recommendation_service.score_ingredients", return_value=df), \
             patch("src.services.recommendation_service.select_bag", return_value=empty):
            resp = _post({"budget": 0, "people": 2, "days": 5, "dietary_needs": []})
        assert resp.status_code == 200
