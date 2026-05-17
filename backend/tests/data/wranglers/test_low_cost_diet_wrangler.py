import pandas as pd

from src.data.wranglers.low_cost_diet_wrangler import (
    fill_health_outcome_na_values,
    wrangle_low_cost_diet,
)


def test_fill_health_outcome_na_values_fills_missing_stats_from_category_remainder():
    df = pd.DataFrame(
        [
            {"category": "A", "indicator_response": "Yes", "relied_lowcost_yes_95ci_ul": "60", "relied_lowcost_no_pct": 35.0},
            {"category": "A", "indicator_response": "No", "relied_lowcost_yes_95ci_ul": None, "relied_lowcost_no_pct": None},
        ]
    )

    result = fill_health_outcome_na_values(df)

    assert result["relied_lowcost_yes_95ci_ul"].dtype == float
    assert result["relied_lowcost_yes_95ci_ul"].iloc[1] == 40.0
    assert result["relied_lowcost_no_pct"].iloc[1] == 65.0


def test_wrangle_low_cost_diet_cleans_names_na_values_and_fills_missing_values():
    df = pd.DataFrame(
        [
            {"Category": " A ", "Indicator Response": "Yes", "Relied Lowcost Yes 95ci Ul": "70", "Relied Lowcost No Pct": 45.0},
            {"Category": "A", "Indicator Response": "No", "Relied Lowcost Yes 95ci Ul": None, "Relied Lowcost No Pct": None},
        ]
    )

    result = wrangle_low_cost_diet(df)

    assert list(result.columns) == [
        "category",
        "indicator_response",
        "relied_lowcost_yes_95ci_ul",
        "relied_lowcost_no_pct",
    ]
    assert result["category"].iloc[0] == "A"
    assert result["relied_lowcost_no_pct"].iloc[1] == 55.0
