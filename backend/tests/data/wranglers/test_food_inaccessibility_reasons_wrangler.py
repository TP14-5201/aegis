import pandas as pd

from src.data.wranglers.food_inaccessibility_reasons_wrangler import (
    _clean_lga_names,
    _filter_null_pid,
    _find_lga_pid,
    wrangle_food_inaccessibility_reasons,
)


def test_clean_lga_names_removes_parenthetical_suffix_and_whitespace():
    df = pd.DataFrame({"lga": ["Melbourne (C)", "  Ballarat  "]})

    result = _clean_lga_names(df)

    assert result["lga"].tolist() == ["Melbourne", "Ballarat"]


def test_find_lga_pid_maps_lga_names_from_boundary_dataframe():
    reason_df = pd.DataFrame({"lga": ["Melbourne", "Unknown"]})
    lga_df = pd.DataFrame(
        [{"lga_name": "Melbourne", "lga_pid": "LGA_MEL"}]
    )

    result = _find_lga_pid(reason_df, lga_df)

    assert result["lga_pid"].iloc[0] == "LGA_MEL"
    assert pd.isna(result["lga_pid"].iloc[1])


def test_filter_null_pid_removes_unmatched_lga_rows():
    df = pd.DataFrame({"lga_pid": ["LGA_MEL", None], "limited_variety": [1, 2]})

    result = _filter_null_pid(df)

    assert result["lga_pid"].tolist() == ["LGA_MEL"]


def test_wrangle_food_inaccessibility_reasons_returns_expected_columns_and_values():
    reason_df = pd.DataFrame(
        {
            "LGA": ["Melbourne (C)", "Unknown"],
            "Variety (%)": [10.0, 20.0],
            "Expensive (%)": [30.0, 40.0],
            "Quality (%)": [5.0, 6.0],
            "Transport (%)": [7.0, 8.0],
        }
    )
    lga_df = pd.DataFrame([{"lga_name": "Melbourne", "lga_pid": "LGA_MEL"}])

    result = wrangle_food_inaccessibility_reasons(reason_df, lga_df)

    assert list(result.columns) == [
        "lga_pid",
        "limited_variety",
        "too_expensive",
        "wrong_quality",
        "transport_gap",
    ]
    assert result.to_dict("records") == [
        {
            "lga_pid": "LGA_MEL",
            "limited_variety": 10.0,
            "too_expensive": 30.0,
            "wrong_quality": 5.0,
            "transport_gap": 7.0,
        }
    ]
