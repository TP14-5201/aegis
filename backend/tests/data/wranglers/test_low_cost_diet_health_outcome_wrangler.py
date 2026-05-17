import pandas as pd

from src.data.wranglers.low_cost_diet_health_outcome_wrangler import (
    fill_health_outcome_na_values,
    wrangle_low_cost_diet_health_outcome,
)


def test_fill_health_outcome_na_values_casts_ci_columns_and_fills_remainders():
    df = pd.DataFrame(
        [
            {
                "category": "A",
                "health_outcome": "One",
                "relied_lowcost_yes_95ci_ul": "60",
                "relied_lowcost_no_95ci_ul": "70",
                "relied_lowcost_yes_pct": 40.0,
            },
            {
                "category": "A",
                "health_outcome": "Two",
                "relied_lowcost_yes_95ci_ul": None,
                "relied_lowcost_no_95ci_ul": None,
                "relied_lowcost_yes_pct": None,
            },
        ]
    )

    result = fill_health_outcome_na_values(df)

    assert result["relied_lowcost_yes_95ci_ul"].dtype == float
    assert result["relied_lowcost_no_95ci_ul"].dtype == float
    assert result["relied_lowcost_yes_95ci_ul"].iloc[1] == 40.0
    assert result["relied_lowcost_no_95ci_ul"].iloc[1] == 30.0
    assert result["relied_lowcost_yes_pct"].iloc[1] == 60.0


def test_wrangle_low_cost_diet_health_outcome_cleans_and_fills_missing_values():
    df = pd.DataFrame(
        [
            {
                "Category": " A ",
                "Health Outcome": "One",
                "Relied Lowcost Yes 95ci Ul": "80",
                "Relied Lowcost No 95ci Ul": "75",
                "Relied Lowcost Yes Pct": 55.0,
            },
            {
                "Category": "A",
                "Health Outcome": "Two",
                "Relied Lowcost Yes 95ci Ul": None,
                "Relied Lowcost No 95ci Ul": None,
                "Relied Lowcost Yes Pct": None,
            },
        ]
    )

    result = wrangle_low_cost_diet_health_outcome(df)

    assert result["category"].iloc[0] == "A"
    assert result["relied_lowcost_yes_95ci_ul"].iloc[1] == 20.0
    assert result["relied_lowcost_no_95ci_ul"].iloc[1] == 25.0
    assert result["relied_lowcost_yes_pct"].iloc[1] == 45.0
