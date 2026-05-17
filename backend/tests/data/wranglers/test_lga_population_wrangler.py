import pandas as pd

from src.data.wranglers.lga_population_wrangler import (
    filter_non_lga_population,
    filter_victorian_lga_population,
    wrangle_lga_population,
)


def test_filter_victorian_lga_population_keeps_only_victoria_rows():
    df = pd.DataFrame(
        {
            "state_and_territory_2021_name": ["Victoria", "New South Wales"],
            "lga": ["Melbourne", "Sydney"],
        }
    )

    result = filter_victorian_lga_population(df)

    assert result["lga"].tolist() == ["Melbourne"]


def test_filter_non_lga_population_removes_unincorporated_codes():
    df = pd.DataFrame(
        {
            "local_government_areas_2021_code": ["24600", "29499", "29799"],
            "lga": ["Melbourne", "No usual address", "Migratory"],
        }
    )

    result = filter_non_lga_population(df)

    assert result["local_government_areas_2021_code"].tolist() == ["24600"]


def test_wrangle_lga_population_filters_selects_and_renames_columns():
    df = pd.DataFrame(
        [
            {
                "State And Territory 2021 Name": "Victoria",
                "Local Government Areas 2021 Code": "24600",
                "Local Government Areas 2021 Name": "Melbourne",
                "Estimated Resident Population Persons No Data Year 2024": 180000,
                "Extra": "drop",
            },
            {
                "State And Territory 2021 Name": "Victoria",
                "Local Government Areas 2021 Code": "29499",
                "Local Government Areas 2021 Name": "No usual address",
                "Estimated Resident Population Persons No Data Year 2024": 1,
                "Extra": "drop",
            },
            {
                "State And Territory 2021 Name": "Tasmania",
                "Local Government Areas 2021 Code": "60010",
                "Local Government Areas 2021 Name": "Hobart",
                "Estimated Resident Population Persons No Data Year 2024": 100000,
                "Extra": "drop",
            },
        ]
    )

    result = wrangle_lga_population(df)

    assert list(result.columns) == ["lga_pid", "lga_name", "pop_2024_total"]
    assert result.to_dict("records") == [
        {"lga_pid": "24600", "lga_name": "Melbourne", "pop_2024_total": 180000}
    ]
