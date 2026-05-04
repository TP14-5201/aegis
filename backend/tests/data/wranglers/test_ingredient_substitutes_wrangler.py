import pandas as pd
import pytest

from src.data.wranglers.ingredient_substitutes_wrangler import (
    coerce_similarity_score,
    wrangle_ingredient_substitutes,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_substitutes_df(**overrides) -> pd.DataFrame:
    row = {
        "ingredient_name": "Beef Mince",
        "substitute_name": "Lentils (red dry)",
        "similarity_score": "0.75",
        "reason": "Similar protein content lower cost",
        "source": "manual",
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# coerce_similarity_score
# ---------------------------------------------------------------------------

class TestCoerceSimilarityScore:
    def test_string_float_is_coerced(self):
        df = make_substitutes_df(similarity_score="0.75")
        result = coerce_similarity_score(df)
        assert abs(result["similarity_score"].iloc[0] - 0.75) < 0.01

    def test_score_above_1_clamped(self):
        df = make_substitutes_df(similarity_score="1.5")
        result = coerce_similarity_score(df)
        assert result["similarity_score"].iloc[0] == 1.0

    def test_score_below_0_clamped(self):
        df = make_substitutes_df(similarity_score="-0.5")
        result = coerce_similarity_score(df)
        assert result["similarity_score"].iloc[0] == 0.0

    def test_non_parseable_yields_nan(self):
        df = make_substitutes_df(similarity_score="high")
        result = coerce_similarity_score(df)
        assert pd.isna(result["similarity_score"].iloc[0])


# ---------------------------------------------------------------------------
# wrangle_ingredient_substitutes (integration)
# ---------------------------------------------------------------------------

class TestWrangleIngredientSubstitutes:
    def test_returns_dataframe(self):
        df = make_substitutes_df()
        result = wrangle_ingredient_substitutes(df)
        assert isinstance(result, pd.DataFrame)

    def test_empty_dataframe_returns_empty_with_schema(self):
        df = pd.DataFrame(columns=["ingredient_name", "substitute_name", "similarity_score", "reason", "source"])
        result = wrangle_ingredient_substitutes(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_preserves_name_columns(self):
        df = make_substitutes_df()
        result = wrangle_ingredient_substitutes(df)
        assert "ingredient_name" in result.columns
        assert "substitute_name" in result.columns

    def test_similarity_score_is_numeric(self):
        df = make_substitutes_df(similarity_score="0.80")
        result = wrangle_ingredient_substitutes(df)
        assert abs(result["similarity_score"].iloc[0] - 0.80) < 0.01

    def test_adds_source_if_missing(self):
        df = make_substitutes_df()
        df = df.drop(columns=["source"])
        result = wrangle_ingredient_substitutes(df)
        assert result["source"].iloc[0] == "manual"

    def test_multiple_substitutes(self):
        rows = [
            {"ingredient_name": "Beef Mince", "substitute_name": "Lentils (red dry)", "similarity_score": "0.75", "reason": "Plant-based", "source": "manual"},
            {"ingredient_name": "Beef Mince", "substitute_name": "Canned Beans (mixed)", "similarity_score": "0.70", "reason": "Budget friendly", "source": "manual"},
        ]
        df = pd.DataFrame(rows)
        result = wrangle_ingredient_substitutes(df)
        assert len(result) == 2
