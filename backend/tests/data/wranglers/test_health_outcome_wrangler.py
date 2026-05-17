import pandas as pd

from src.data.wranglers.health_outcome_wrangler import (
    fill_health_outcome_na_values,
    wrangle_health_outcome,
)


def test_fill_health_outcome_na_values_fills_positive_missing_remainder():
    df = pd.DataFrame(
        [
            {
                "category": "A",
                "health_outcome": "One",
                "insecure_hunger_pct": 40.0,
                "insecure_hunger_95ci_ul": "60",
                "food_secure_pct": 25.0,
            },
            {
                "category": "A",
                "health_outcome": "Two",
                "insecure_hunger_pct": None,
                "insecure_hunger_95ci_ul": "20",
                "food_secure_pct": None,
            },
        ]
    )

    result = fill_health_outcome_na_values(df)

    assert result["insecure_hunger_pct"].iloc[1] == 60.0
    assert result["food_secure_pct"].iloc[1] == 75.0
    assert result["insecure_hunger_95ci_ul"].dtype == float


def test_fill_health_outcome_na_values_fills_zero_when_remainder_not_positive():
    df = pd.DataFrame(
        [
            {"category": "A", "health_outcome": "One", "insecure_hunger_95ci_ul": "120", "food_secure_pct": 110.0},
            {"category": "A", "health_outcome": "Two", "insecure_hunger_95ci_ul": "10", "food_secure_pct": None},
        ]
    )

    result = fill_health_outcome_na_values(df)

    assert result["food_secure_pct"].iloc[1] == 0


def test_wrangle_health_outcome_cleans_columns_na_values_and_fills_missing_stats():
    df = pd.DataFrame(
        [
            {"Category": " A ", "Health Outcome": "One", "Insecure Hunger 95ci Ul": "60", "Food Secure Pct": 30.0},
            {"Category": "A", "Health Outcome": "Two", "Insecure Hunger 95ci Ul": "20", "Food Secure Pct": None},
        ]
    )

    result = wrangle_health_outcome(df)

    assert list(result.columns) == [
        "category",
        "health_outcome",
        "insecure_hunger_95ci_ul",
        "food_secure_pct",
    ]
    assert result["category"].iloc[0] == "A"
    assert result["food_secure_pct"].iloc[1] == 70.0
