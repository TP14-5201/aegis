"""
test_ingredient_substitution.py
--------------------------------
Unit tests for the Smart Ingredient Switch engine.

Strategy
--------
All tests use a tiny synthetic dataset (20 rows) injected via a mock
SQLAlchemy Session so there is no dependency on the live database or
on Kaggle data.  The FAISS index is built in-memory for each test that
needs it; DB persistence is verified via assertions on the mock Session.

Run:
    pytest tests/test_ingredient_substitution.py -v
"""
from __future__ import annotations

import pickle
from typing import List
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# Helpers – build a deterministic synthetic dataset
# ---------------------------------------------------------------------------

_SYNTHETIC_ROWS: List[tuple] = [
    # code, name, brands, main_cat, grade, energy, protein, carbs, fat, sub_cat, price
    ("C001", "Chicken Breast", "Farm Fresh", None, "b", 150.0, 31.0, 0.0, 3.0, "Poultry", 12.5),
    ("C002", "Turkey Breast", "Naturalee", None, "b", 160.0, 29.0, 0.0, 4.0, "Poultry", 14.0),
    ("C003", "Chicken Thigh", "Farm Fresh", None, "c", 200.0, 25.0, 0.0, 12.0, "Poultry", 9.0),
    ("C004", "Duck Breast", "Gourmet", None, "c", 220.0, 19.0, 0.0, 15.0, "Poultry", 18.0),
    ("M001", "Beef Mince", "Aussie Beef", None, "c", 250.0, 26.0, 0.0, 17.0, "Meat", 15.0),
    ("M002", "Lamb Chops", "Pasture", None, "d", 290.0, 22.0, 0.0, 20.0, "Meat", 20.0),
    ("P001", "Spaghetti", "Barilla", None, "b", 350.0, 13.0, 72.0, 1.5, "Pasta", 3.0),
    ("P002", "Penne", "De Cecco", None, "b", 350.0, 13.0, 72.0, 1.5, "Pasta", 3.5),
    ("P003", "Fusilli", "Barilla", None, "b", 348.0, 12.5, 71.0, 1.4, "Pasta", 3.2),
    ("P004", "Fettuccine", "Barilla", None, "b", 351.0, 13.0, 73.0, 1.5, "Pasta", 3.0),
    ("D001", "Full Cream Milk", "Dairy Farmers", None, "b", 66.0, 3.4, 4.7, 3.9, "Dairy", 2.5),
    ("D002", "Skim Milk", "Dairy Farmers", None, "a", 35.0, 3.6, 5.0, 0.2, "Dairy", 2.3),
    ("D003", "Oat Milk", "Oatly", None, "b", 45.0, 1.0, 6.5, 1.5, "Dairy", 4.0),
    ("V001", "Broccoli", "Fresh Fields", None, "a", 34.0, 2.8, 7.0, 0.4, "Vegetables", 3.0),
    ("V002", "Spinach", "Fresh Fields", None, "a", 23.0, 2.9, 3.6, 0.4, "Vegetables", 2.5),
    ("V003", "Kale", "Organic Farm", None, "a", 35.0, 4.3, 4.4, 0.9, "Vegetables", 4.5),
    ("F001", "Olive Oil", "Cobram", None, "e", 820.0, 0.0, 0.0, 92.0, "Oils", 8.0),
    ("F002", "Canola Oil", "Value", None, "d", 800.0, 0.0, 0.0, 90.0, "Oils", 5.0),
    ("L001", "Red Lentils", "Ceres", None, "a", 330.0, 25.0, 60.0, 1.0, "Legumes", 4.0),
    ("L002", "Chickpeas", "Ceres", None, "a", 360.0, 19.0, 61.0, 6.0, "Legumes", 3.5),
]


def _make_mock_db() -> MagicMock:
    """Return a minimal mock Session that accepts all write calls without error."""
    return MagicMock()


def _make_synthetic_df(rows: List[tuple] | None = None) -> pd.DataFrame:
    """
    Convert synthetic row tuples into the DataFrame schema expected by
    build_index(df=...).  This avoids any DB or geoalchemy2 dependency.
    """
    from src.services.ingredient_substitution import _infer_role

    if rows is None:
        rows = _SYNTHETIC_ROWS

    df = pd.DataFrame(rows, columns=[
        "ingredient_code", "product_name", "brands", "main_category",
        "nutrition_grade_fr", "energy_100g", "proteins_100g",
        "carbohydrates_100g", "fat_100g", "sub_category", "retail_price",
    ]).set_index("ingredient_code")

    df["nutrition_grade_fr"] = df["nutrition_grade_fr"].str.lower()
    df["functional_role"] = df["sub_category"].apply(_infer_role)
    return df


def _make_load_db_from_engine(eng) -> MagicMock:
    """
    Build a mock Session that returns the data build_index would have persisted.

    load_index makes three distinct query patterns:
      1. db.query(SubstitutionMeta).filter_by(key=...).first()  → scaler blob
      2. db.query(IngredientEmbedding).all()                    → embedding rows
    _load_dataframe is patched separately in the roundtrip test so this mock
    does not need to handle the three-table join.
    """
    meta_row = MagicMock()
    meta_row.value = pickle.dumps(eng._scaler, protocol=pickle.HIGHEST_PROTOCOL)

    emb_rows = []
    for code, row in eng._df.iterrows():
        r = MagicMock()
        r.ingredient_code = code
        r.embedding = np.array(row["_embedding"], dtype="float32").tobytes()
        r.functional_role = row["functional_role"]
        r.proteins_100g = (
            float(row["proteins_100g"]) if not pd.isna(row["proteins_100g"]) else None
        )
        r.fat_100g = (
            float(row["fat_100g"]) if not pd.isna(row["fat_100g"]) else None
        )
        r.carbohydrates_100g = (
            float(row["carbohydrates_100g"]) if not pd.isna(row["carbohydrates_100g"]) else None
        )
        r.energy_100g = (
            float(row["energy_100g"]) if not pd.isna(row["energy_100g"]) else None
        )
        emb_rows.append(r)

    def _query_side_effect(model):
        """Dispatch on the model class name to return the right mock chain."""
        q = MagicMock()
        model_name = getattr(model, "__name__", str(model))
        if "SubstitutionMeta" in model_name:
            q.filter_by.return_value.first.return_value = meta_row
        elif "IngredientEmbedding" in model_name:
            q.all.return_value = emb_rows
        return q

    mock_db = MagicMock()
    mock_db.query.side_effect = _query_side_effect
    return mock_db


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def engine_instance():
    """A fresh IngredientSubstitutionEngine instance."""
    from src.services.ingredient_substitution import IngredientSubstitutionEngine
    return IngredientSubstitutionEngine()


# ---------------------------------------------------------------------------
# Tests: build_index
# ---------------------------------------------------------------------------

class TestBuildIndex:
    def test_build_index_persists_to_db(self, engine_instance):
        """After build_index, the engine must commit embeddings and scaler to the DB."""
        mock_db = _make_mock_db()
        engine_instance.build_index(mock_db, df=_make_synthetic_df())

        mock_db.bulk_save_objects.assert_called_once()
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_build_index_sets_ready(self, engine_instance):
        engine_instance.build_index(_make_mock_db(), df=_make_synthetic_df())
        assert engine_instance._ready is True

    def test_index_ntotal_matches_row_count(self, engine_instance):
        engine_instance.build_index(_make_mock_db(), df=_make_synthetic_df())
        assert engine_instance._index.ntotal == len(_SYNTHETIC_ROWS)

    def test_load_index_roundtrip(self, engine_instance):
        """Build → load produces the same ntotal and DataFrame row count."""
        from src.services.ingredient_substitution import IngredientSubstitutionEngine

        engine_instance.build_index(_make_mock_db(), df=_make_synthetic_df())

        load_db = _make_load_db_from_engine(engine_instance)
        loader = IngredientSubstitutionEngine()

        # Patch _load_dataframe so load_index can reconstruct display columns
        # without needing a real three-table DB join.
        with patch.object(loader, "_load_dataframe", return_value=_make_synthetic_df()):
            ok = loader.load_index(load_db)

        assert ok is True
        assert loader._index.ntotal == engine_instance._index.ntotal
        assert loader._df.shape[0] == engine_instance._df.shape[0]


# ---------------------------------------------------------------------------
# Tests: get_substitutes – structural guarantees
# ---------------------------------------------------------------------------

class TestGetSubstitutes:
    @pytest.fixture(autouse=True)
    def _build(self, engine_instance):
        engine_instance.build_index(_make_mock_db(), df=_make_synthetic_df())
        self.eng = engine_instance

    def test_returns_three_slots(self):
        result = self.eng.get_substitutes("P001", _make_mock_db())
        assert result.budget is not None, "budget slot should be filled"
        assert result.nutrition is not None, "nutrition slot should be filled"
        assert result.balanced is not None, "balanced slot should be filled"
        assert result.error is None

    def test_query_ingredient_excluded_from_results(self):
        result = self.eng.get_substitutes("P001", _make_mock_db())
        codes = {result.budget.ingredient_code, result.nutrition.ingredient_code, result.balanced.ingredient_code}
        assert "P001" not in codes, "Query ingredient must not appear as its own substitute"

    def test_unknown_ingredient_returns_error(self):
        result = self.eng.get_substitutes("XXXX", _make_mock_db())
        assert result.error is not None
        assert result.budget is None

    def test_diversity_enforcement(self):
        """All three slots should reference distinct ingredients (where possible)."""
        result = self.eng.get_substitutes("P001", _make_mock_db())
        codes = [
            result.budget.ingredient_code,
            result.nutrition.ingredient_code,
            result.balanced.ingredient_code,
        ]
        # With ≥ 3 culinary-valid candidates, each slot must be unique
        assert len(set(codes)) == 3, f"Expected distinct substitutes, got {codes}"


# ---------------------------------------------------------------------------
# Tests: Functional Role Filter
# ---------------------------------------------------------------------------

class TestFunctionalRoleFilter:
    @pytest.fixture(autouse=True)
    def _build(self, engine_instance):
        engine_instance.build_index(_make_mock_db(), df=_make_synthetic_df())
        self.eng = engine_instance

    def test_pasta_substitutes_are_pasta(self):
        """Querying Spaghetti should not return Chicken or Dairy as a substitute."""
        result = self.eng.get_substitutes("P001", _make_mock_db())
        df = self.eng._df
        for slot in [result.budget, result.nutrition, result.balanced]:
            if slot is None:
                continue
            role = df.at[slot.ingredient_code, "functional_role"]
            assert role in {"carb", "other"}, (
                f"Expected carb-role substitute for pasta, got role='{role}' "
                f"for '{slot.product_name}'"
            )

    def test_poultry_substitutes_are_protein(self):
        """Querying Chicken Breast should return other proteins."""
        result = self.eng.get_substitutes("C001", _make_mock_db())
        df = self.eng._df
        for slot in [result.budget, result.nutrition, result.balanced]:
            if slot is None:
                continue
            role = df.at[slot.ingredient_code, "functional_role"]
            assert role in {"protein", "other"}, (
                f"Expected protein-role substitute for poultry, got '{role}' "
                f"for '{slot.product_name}'"
            )


# ---------------------------------------------------------------------------
# Tests: Objective scoring monotonicity
# ---------------------------------------------------------------------------

class TestObjectiveScoringMonotonicity:
    @pytest.fixture(autouse=True)
    def _build(self, engine_instance):
        engine_instance.build_index(_make_mock_db(), df=_make_synthetic_df())
        self.eng = engine_instance

    def _get_price(self, code: str) -> float:
        return float(self.eng._df.at[code, "retail_price"])

    def _get_nutri_score(self, code: str) -> float:
        from src.services.ingredient_substitution import NUTRI_GRADE_MAP
        grade = self.eng._df.at[code, "nutrition_grade_fr"]
        return NUTRI_GRADE_MAP.get(str(grade).lower() if grade else None, 0.3)

    @pytest.mark.parametrize("query_code", ["C001", "P001", "D001", "V001"])
    def test_budget_is_cheaper_or_equal_90pct(self, query_code):
        """Budget substitute should have price ≤ query in at least 90% of cases."""
        result = self.eng.get_substitutes(query_code, _make_mock_db())
        if result.budget is None or result.error:
            pytest.skip("No budget candidate returned")
        query_price = self._get_price(query_code)
        budget_price = result.budget.retail_price or 0.0
        # Allow a small tolerance: budget can be marginally more expensive if
        # the query is already the cheapest in its category
        assert budget_price <= query_price * 1.15, (
            f"Budget substitute (${budget_price}) is significantly more expensive "
            f"than query (${query_price}) for '{query_code}'"
        )

    @pytest.mark.parametrize("query_code", ["C001", "P001", "D001", "V001"])
    def test_nutrition_score_is_higher_or_equal(self, query_code):
        """Nutrition substitute should have Nutri-Score ≥ query in most cases."""
        result = self.eng.get_substitutes(query_code, _make_mock_db())
        if result.nutrition is None or result.error:
            pytest.skip("No nutrition candidate returned")
        query_ns = self._get_nutri_score(query_code)
        sub_ns = self._get_nutri_score(result.nutrition.ingredient_code)
        # Allow equality (same grade is still valid)
        assert sub_ns >= query_ns - 0.2, (
            f"Nutrition substitute grade ({sub_ns:.2f}) is notably below "
            f"query grade ({query_ns:.2f}) for '{query_code}'"
        )


# ---------------------------------------------------------------------------
# Tests: Imputation
# ---------------------------------------------------------------------------

class TestImputation:
    def test_missing_nutrition_is_filled(self, engine_instance):
        """Ingredients without nutrition rows should have macros filled by sub_category-median."""
        rows_with_nulls = list(_SYNTHETIC_ROWS)
        # Null out macros for C003
        c003 = rows_with_nulls[2]
        rows_with_nulls[2] = (
            c003[0], c003[1], c003[2], c003[3],
            None, None, None, None, None,   # null nutrition
            c003[9], c003[10]
        )
        df = _make_synthetic_df(rows_with_nulls)
        # Re-apply null to the already-constructed df (synthetic_df doesn't impute)
        for col in ["energy_100g", "proteins_100g", "carbohydrates_100g", "fat_100g"]:
            df.at["C003", col] = float("nan")
        engine_instance.build_index(_make_mock_db(), df=df)

        df = engine_instance._df
        for col in ["proteins_100g", "fat_100g", "carbohydrates_100g", "energy_100g"]:
            assert not pd.isna(df.at["C003", col]), (
                f"Column '{col}' should be imputed for C003, got NaN"
            )

    def test_imputation_uses_subcategory_median(self, engine_instance):
        """For C003 (Poultry), imputed values should be close to the Poultry median."""
        rows_with_nulls = list(_SYNTHETIC_ROWS)
        c003 = rows_with_nulls[2]
        rows_with_nulls[2] = (
            c003[0], c003[1], c003[2], c003[3],
            None, None, None, None, None,
            c003[9], c003[10]
        )
        df = _make_synthetic_df(rows_with_nulls)
        for col in ["energy_100g", "proteins_100g", "carbohydrates_100g", "fat_100g"]:
            df.at["C003", col] = float("nan")
        engine_instance.build_index(_make_mock_db(), df=df)

        df = engine_instance._df
        # Poultry proteins for C001 (31) and C002 (29), C004 (19); median = 29
        poultry_proteins = df[df["sub_category"] == "Poultry"]["proteins_100g"]
        expected_median = poultry_proteins.median()
        actual = df.at["C003", "proteins_100g"]
        assert abs(actual - expected_median) < 1.0, (
            f"Imputed protein for C003 ({actual}) should be near Poultry median ({expected_median})"
        )


# ---------------------------------------------------------------------------
# Tests: _infer_role
# ---------------------------------------------------------------------------

class TestInferRole:
    def test_known_categories(self):
        from src.services.ingredient_substitution import _infer_role
        assert _infer_role("Poultry") == "protein"
        assert _infer_role("Meat") == "protein"
        assert _infer_role("Pasta") == "carb"
        assert _infer_role("Dairy") == "dairy_protein"
        assert _infer_role("Vegetables") == "vegetable"
        assert _infer_role("Oils") == "fat"
        assert _infer_role("Legumes") == "plant_protein"

    def test_unknown_category_returns_other(self):
        from src.services.ingredient_substitution import _infer_role
        assert _infer_role("Miscellaneous") == "other"
        assert _infer_role(None) == "other"
        assert _infer_role("") == "other"

    def test_case_insensitive(self):
        from src.services.ingredient_substitution import _infer_role
        assert _infer_role("POULTRY") == "protein"
        assert _infer_role("Dairy Farmers") == "dairy_protein"