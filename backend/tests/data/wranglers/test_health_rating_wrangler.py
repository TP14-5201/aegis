import pandas as pd
import pytest

from src.data.wranglers.health_rating_wrangler import (
    _points,
    _grade,
    _score_to_100,
    compute_nutriscore,
    wrangle_ingredient_health_ratings,
)

_NUTRITION_COLS = [
    "ingredient_code",
    "protein_g",
    "fat_total_g",
    "total_dietary_fibre_g",
    "total_sugars_g",
    "available_carbohydrate_without_sugar_alcohols_g",
    "sodium_na_mg",
]


def _make_ingredient_df(*codes):
    return pd.DataFrame({"ingredient_code": list(codes)})


def _make_nutrition_df(*rows):
    return pd.DataFrame(rows, columns=_NUTRITION_COLS)


# ---------------------------------------------------------------------------
# _points
# ---------------------------------------------------------------------------

class TestPoints:
    def test_returns_zero_when_below_first_threshold(self):
        assert _points(0.5, [1, 2, 3]) == 0

    def test_returns_middle_index_when_between_thresholds(self):
        assert _points(1.5, [1, 2, 3]) == 1

    def test_returns_len_thresholds_when_above_all(self):
        assert _points(10.0, [1, 2, 3]) == 3

    def test_empty_thresholds_returns_zero(self):
        assert _points(5.0, []) == 0

    def test_value_exactly_equal_to_threshold_is_included(self):
        assert _points(2.0, [1, 2, 3]) == 1


# ---------------------------------------------------------------------------
# _grade
# ---------------------------------------------------------------------------

class TestGrade:
    def test_grade_a_for_low_score(self):
        assert _grade(-5) == "A"

    def test_grade_a_at_boundary(self):
        assert _grade(-1) == "A"

    def test_grade_b(self):
        assert _grade(0) == "B"

    def test_grade_b_at_boundary(self):
        assert _grade(2) == "B"

    def test_grade_c(self):
        assert _grade(5) == "C"

    def test_grade_d(self):
        assert _grade(15) == "D"

    def test_grade_e_for_high_score(self):
        assert _grade(19) == "E"

    def test_grade_e_well_above_threshold(self):
        assert _grade(40) == "E"


# ---------------------------------------------------------------------------
# _score_to_100
# ---------------------------------------------------------------------------

class TestScoreTo100:
    def test_min_raw_gives_100(self):
        assert _score_to_100(-10) == 100.0

    def test_max_raw_gives_0(self):
        assert _score_to_100(40) == 0.0

    def test_midpoint(self):
        assert _score_to_100(15) == 50.0

    def test_clamps_below_min(self):
        assert _score_to_100(-20) == 100.0

    def test_clamps_above_max(self):
        assert _score_to_100(50) == 0.0

    def test_zero_raw(self):
        assert _score_to_100(0) == 80.0


# ---------------------------------------------------------------------------
# compute_nutriscore
# ---------------------------------------------------------------------------

class TestComputeNutriscore:
    def test_returns_dict_with_expected_keys(self):
        result = compute_nutriscore(protein_g=5, fat_total_g=2, fibre_g=1,
                                    sugars_g=4, sodium_mg=100, carb_g=20)
        assert set(result.keys()) == {"nutriscore_grade", "nutriscore_score", "final_health_score"}

    def test_all_zeros_does_not_raise(self):
        result = compute_nutriscore(protein_g=0, fat_total_g=0, fibre_g=0,
                                    sugars_g=0, sodium_mg=0, carb_g=0)
        assert result["nutriscore_grade"] == "B"
        assert result["final_health_score"] == 80.0

    def test_healthy_values_give_grade_a(self):
        result = compute_nutriscore(protein_g=10, fat_total_g=5, fibre_g=3,
                                    sugars_g=5, sodium_mg=200, carb_g=20)
        assert result["nutriscore_grade"] == "A"

    def test_high_sugar_fat_gives_grade_e(self):
        result = compute_nutriscore(protein_g=1, fat_total_g=30, fibre_g=0,
                                    sugars_g=40, sodium_mg=800, carb_g=60)
        assert result["nutriscore_grade"] == "E"

    def test_negative_inputs_do_not_crash(self):
        result = compute_nutriscore(protein_g=-1, fat_total_g=-2, fibre_g=-1,
                                    sugars_g=-5, sodium_mg=-10, carb_g=-3)
        assert "nutriscore_grade" in result


# ---------------------------------------------------------------------------
# wrangle_ingredient_health_ratings
# ---------------------------------------------------------------------------

class TestWrangleIngredientHealthRatings:
    def test_returns_dataframe(self):
        ingredient_df = _make_ingredient_df("A001")
        nutrition_df = _make_nutrition_df(["A001", 5.0, 2.0, 3.0, 4.0, 20.0, 100.0])
        result = wrangle_ingredient_health_ratings(ingredient_df, nutrition_df)
        assert isinstance(result, pd.DataFrame)

    def test_expected_columns_present(self):
        ingredient_df = _make_ingredient_df("A001")
        nutrition_df = _make_nutrition_df(["A001", 5.0, 2.0, 3.0, 4.0, 20.0, 100.0])
        result = wrangle_ingredient_health_ratings(ingredient_df, nutrition_df)
        for col in ("ingredient_code", "nutriscore_grade", "nova_score", "final_health_score"):
            assert col in result.columns

    def test_one_row_per_ingredient(self):
        ingredient_df = _make_ingredient_df("A001", "A002")
        nutrition_df = _make_nutrition_df(
            ["A001", 5.0, 2.0, 3.0, 4.0, 20.0, 100.0],
            ["A002", 10.0, 1.0, 4.0, 2.0, 15.0, 80.0],
        )
        result = wrangle_ingredient_health_ratings(ingredient_df, nutrition_df)
        assert len(result) == 2

    def test_empty_ingredient_df_returns_empty(self):
        ingredient_df = pd.DataFrame({"ingredient_code": pd.Series([], dtype=str)})
        nutrition_df = _make_nutrition_df(["A001", 5.0, 2.0, 3.0, 4.0, 20.0, 100.0])
        result = wrangle_ingredient_health_ratings(ingredient_df, nutrition_df)
        assert result.empty

    def test_empty_nutrition_df_uses_zero_defaults(self):
        ingredient_df = _make_ingredient_df("A001")
        nutrition_df = pd.DataFrame(columns=_NUTRITION_COLS)
        result = wrangle_ingredient_health_ratings(ingredient_df, nutrition_df)
        assert len(result) == 1
        assert result.iloc[0]["nutriscore_grade"] == "B"
