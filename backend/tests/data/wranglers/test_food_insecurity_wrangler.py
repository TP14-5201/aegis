import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch

from src.data.wranglers.food_insecurity_wrangler import (
    filter_by_phu,
    filter_by_gender,
    filter_by_estimate_type,
    filter_by_indicator_category,
    clean_subpopulation,
    impute_estimate,
    filter_records,
    add_vic_region_code,
    wrangle_food_insecurity,
)


# ---------------------------------------------------------------------------
# Shared constants & helpers
# ---------------------------------------------------------------------------

# A valid Victorian PHU region that passes filter_by_phu.
VALID_REGION = "LGAs of South East PHU"

# All regions defined in settings.SELECTED_REGIONS — kept local so tests are
# self-contained and don't break when settings change.
ALL_REGIONS = [
    "LGAs of Ovens-Murray PHU",
    "LGAs of Grampians Wimmera Southern Mallee PHU",
    "LGAs of North Eastern PHU",
    "LGAs of Gippsland PHU",
    "LGAs of South East PHU",
    "LGAs of Goulburn Valley PHU",
    "LGAs of Western PHU",
    "LGAs of Loddon Mallee PHU",
    "LGAs of Barwon South-West PHU",
]

# The region code mapping as defined in add_vic_region_code.
REGION_CODES = {
    "LGAs of Barwon South-West PHU": 10,
    "LGAs of North Eastern PHU": 11,
    "LGAs of Gippsland PHU": 12,
    "LGAs of Grampians Wimmera Southern Mallee PHU": 13,
    "LGAs of Goulburn Valley PHU": 14,
    "LGAs of Ovens-Murray PHU": 14,
    "LGAs of Loddon Mallee PHU": 15,
    "LGAs of Western PHU": 16,
    "LGAs of South East PHU": 17,
}


def make_filter_df(**overrides) -> pd.DataFrame:
    """
    Minimal single-row DataFrame with post-standardised column names,
    suitable for testing individual filter and transform functions.
    All defaults pass every filter.
    """
    row = {
        "stratified_by": VALID_REGION,
        "gender": "Women",
        "estimate_type": "Crude",
        "indicator_category": "Yes",
        "indicator": "Food insecurity",
        "subpopulation": "Total (18+ years)",
        "estimate_pct": 12.5,
    }
    row.update(overrides)
    return pd.DataFrame([row])


def make_full_raw_df(**overrides) -> pd.DataFrame:
    """
    Single-row DataFrame that matches the raw Excel schema (pre-pipeline).
    The estimate column is named '%' as it arrives from the data source;
    initial_cleaning_pipeline will standardise it to an empty string ''.
    Used exclusively for wrangle_food_insecurity integration tests.
    """
    row = {
        "stratified_by": VALID_REGION,
        "gender": "Women",
        "estimate_type": "Crude",
        "indicator_category": "Yes",
        "indicator": "Food insecurity",
        "subpopulation": "Total (18+ years)",
        "%": 12.5,
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# filter_by_phu
# ---------------------------------------------------------------------------

class TestFilterByPhu:
    def test_keeps_rows_with_valid_region(self):
        """Tests that a row whose region is in SELECTED_REGIONS is kept."""
        df = make_filter_df(stratified_by=VALID_REGION)
        result = filter_by_phu(df)
        assert len(result) == 1

    def test_removes_rows_with_unknown_region(self):
        """Tests that a row whose region is not in SELECTED_REGIONS is removed."""
        df = make_filter_df(stratified_by="LGAs of Unknown PHU")
        result = filter_by_phu(df)
        assert len(result) == 0

    def test_keeps_all_valid_regions(self):
        """Tests that every region in SELECTED_REGIONS passes the filter."""
        df = pd.DataFrame([make_filter_df(stratified_by=r).iloc[0] for r in ALL_REGIONS])
        result = filter_by_phu(df)
        assert len(result) == len(ALL_REGIONS)

    def test_filters_mixed_rows(self):
        """Tests that only rows with valid regions survive a mixed DataFrame."""
        df = pd.DataFrame([
            make_filter_df(stratified_by=VALID_REGION).iloc[0],
            make_filter_df(stratified_by="LGAs of Unknown PHU").iloc[0],
        ])
        result = filter_by_phu(df)
        assert len(result) == 1
        assert result["stratified_by"].iloc[0] == VALID_REGION

    def test_nan_region_is_excluded(self):
        """Tests that a NaN stratified_by value is excluded."""
        df = make_filter_df(stratified_by=np.nan)
        result = filter_by_phu(df)
        assert len(result) == 0

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_filter_df()
        assert isinstance(filter_by_phu(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# filter_by_gender
# ---------------------------------------------------------------------------

class TestFilterByGender:
    def test_keeps_men(self):
        """Tests that rows with gender 'Men' are kept."""
        df = make_filter_df(gender="Men")
        result = filter_by_gender(df)
        assert len(result) == 1

    def test_keeps_women(self):
        """Tests that rows with gender 'Women' are kept."""
        df = make_filter_df(gender="Women")
        result = filter_by_gender(df)
        assert len(result) == 1

    def test_removes_persons(self):
        """Tests that 'Persons' (aggregate gender) is excluded."""
        df = make_filter_df(gender="Persons")
        result = filter_by_gender(df)
        assert len(result) == 0

    def test_removes_unknown_gender(self):
        """Tests that an unrecognised gender value is excluded."""
        df = make_filter_df(gender="Non-binary")
        result = filter_by_gender(df)
        assert len(result) == 0

    def test_removes_nan_gender(self):
        """Tests that a NaN gender value is excluded."""
        df = make_filter_df(gender=np.nan)
        result = filter_by_gender(df)
        assert len(result) == 0

    def test_filters_mixed_genders(self):
        """Tests that only Men and Women survive a mixed DataFrame."""
        df = pd.DataFrame([
            make_filter_df(gender="Men").iloc[0],
            make_filter_df(gender="Persons").iloc[0],
            make_filter_df(gender="Women").iloc[0],
        ])
        result = filter_by_gender(df)
        assert len(result) == 2
        assert set(result["gender"].tolist()) == {"Men", "Women"}

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_filter_df()
        assert isinstance(filter_by_gender(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# filter_by_estimate_type
# ---------------------------------------------------------------------------

class TestFilterByEstimateType:
    def test_keeps_crude_estimate_type(self):
        """Tests that 'Crude' estimate type rows are kept."""
        df = make_filter_df(estimate_type="Crude")
        result = filter_by_estimate_type(df)
        assert len(result) == 1

    def test_removes_age_standardised(self):
        """Tests that 'Age-standardised' estimate type is excluded."""
        df = make_filter_df(estimate_type="Age-standardised")
        result = filter_by_estimate_type(df)
        assert len(result) == 0

    def test_removes_nan_estimate_type(self):
        """Tests that a NaN estimate type is excluded."""
        df = make_filter_df(estimate_type=np.nan)
        result = filter_by_estimate_type(df)
        assert len(result) == 0

    def test_is_case_sensitive(self):
        """Tests that the match is case-sensitive ('crude' != 'Crude')."""
        df = make_filter_df(estimate_type="crude")
        result = filter_by_estimate_type(df)
        assert len(result) == 0

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_filter_df()
        assert isinstance(filter_by_estimate_type(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# filter_by_indicator_category
# ---------------------------------------------------------------------------

class TestFilterByIndicatorCategory:
    def test_keeps_yes(self):
        """Tests that 'Yes' indicator_category rows are kept."""
        df = make_filter_df(indicator_category="Yes")
        result = filter_by_indicator_category(df)
        assert len(result) == 1

    def test_keeps_yes_definitely(self):
        """Tests that 'Yes, definitely' indicator_category rows are kept."""
        df = make_filter_df(indicator_category="Yes, definitely")
        result = filter_by_indicator_category(df)
        assert len(result) == 1

    def test_removes_no(self):
        """Tests that 'No' indicator_category rows are excluded."""
        df = make_filter_df(indicator_category="No")
        result = filter_by_indicator_category(df)
        assert len(result) == 0

    def test_removes_nan_indicator_category(self):
        """Tests that a NaN indicator_category is excluded."""
        df = make_filter_df(indicator_category=np.nan)
        result = filter_by_indicator_category(df)
        assert len(result) == 0

    def test_removes_yes_sometimes(self):
        """Tests that 'Yes, sometimes' (partial agreement) is excluded."""
        df = make_filter_df(indicator_category="Yes, sometimes")
        result = filter_by_indicator_category(df)
        assert len(result) == 0

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_filter_df()
        assert isinstance(filter_by_indicator_category(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# clean_subpopulation
# ---------------------------------------------------------------------------

class TestCleanSubpopulation:
    def test_strips_parenthetical_age_range(self):
        """Tests that the parenthetical part (e.g. '(18+ years)') is removed."""
        df = make_filter_df(subpopulation="Total (18+ years)")
        result = clean_subpopulation(df)
        assert result["subpopulation"].iloc[0] == "Total"

    def test_strips_trailing_whitespace_after_split(self):
        """Tests that no trailing space remains after the parenthetical is removed."""
        df = make_filter_df(subpopulation="Low income (< $600/week)")
        result = clean_subpopulation(df)
        assert not result["subpopulation"].iloc[0].endswith(" ")

    def test_value_without_parentheses_is_unchanged(self):
        """Tests that a subpopulation with no parenthetical is returned as-is."""
        df = make_filter_df(subpopulation="Total")
        result = clean_subpopulation(df)
        assert result["subpopulation"].iloc[0] == "Total"

    def test_multiple_parenthetical_groups_only_first_split_used(self):
        """Tests that only the first '(' is used as the split point."""
        df = make_filter_df(subpopulation="Group A (label) (extra)")
        result = clean_subpopulation(df)
        # str.split('(').str[0] takes everything before the first '('
        assert result["subpopulation"].iloc[0] == "Group A"

    def test_handles_multiple_rows(self):
        """Tests that cleaning is applied correctly across multiple rows."""
        df = pd.DataFrame({
            "subpopulation": ["Total (18+ years)", "Low income (< $600/week)", "Total"]
        })
        result = clean_subpopulation(df)
        assert result["subpopulation"].tolist() == ["Total", "Low income", "Total"]

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_filter_df()
        assert isinstance(clean_subpopulation(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# impute_estimate
# ---------------------------------------------------------------------------

class TestImputeEstimate:
    def test_fills_nan_with_zero(self):
        """Tests that NaN estimate_pct values are replaced with 0."""
        df = pd.DataFrame({"estimate_pct": [np.nan]})
        result = impute_estimate(df)
        assert result["estimate_pct"].iloc[0] == 0

    def test_does_not_alter_existing_values(self):
        """Tests that non-NaN estimate_pct values are preserved."""
        df = pd.DataFrame({"estimate_pct": [12.5, 0.0, 99.9]})
        result = impute_estimate(df)
        assert result["estimate_pct"].tolist() == [12.5, 0.0, 99.9]

    def test_mixed_nan_and_valid_values(self):
        """Tests that only NaN values are replaced when mixed with valid values."""
        df = pd.DataFrame({"estimate_pct": [np.nan, 10.0, np.nan, 5.5]})
        result = impute_estimate(df)
        assert result["estimate_pct"].tolist() == [0, 10.0, 0, 5.5]

    def test_zero_estimate_is_not_changed(self):
        """Tests that an existing 0 value is not altered by the imputation."""
        df = pd.DataFrame({"estimate_pct": [0.0]})
        result = impute_estimate(df)
        assert result["estimate_pct"].iloc[0] == 0.0

    def test_result_column_is_numeric(self):
        """Tests that estimate_pct remains a numeric dtype after imputation."""
        df = pd.DataFrame({"estimate_pct": [np.nan, 5.0]})
        result = impute_estimate(df)
        assert pd.api.types.is_numeric_dtype(result["estimate_pct"])

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"estimate_pct": [1.0]})
        assert isinstance(impute_estimate(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# filter_records (combined filter pipeline)
# ---------------------------------------------------------------------------

class TestFilterRecords:
    def test_keeps_row_passing_all_filters(self):
        """Tests that a row satisfying all four filters is kept."""
        df = make_filter_df()
        result = filter_records(df)
        assert len(result) == 1

    def test_removes_row_failing_phu_filter(self):
        """Tests that a row with an invalid PHU is removed."""
        df = make_filter_df(stratified_by="Unknown PHU")
        result = filter_records(df)
        assert len(result) == 0

    def test_removes_row_failing_gender_filter(self):
        """Tests that a row with 'Persons' gender is removed."""
        df = make_filter_df(gender="Persons")
        result = filter_records(df)
        assert len(result) == 0

    def test_removes_row_failing_estimate_type_filter(self):
        """Tests that a non-Crude estimate type is removed."""
        df = make_filter_df(estimate_type="Age-standardised")
        result = filter_records(df)
        assert len(result) == 0

    def test_removes_row_failing_indicator_category_filter(self):
        """Tests that a 'No' indicator_category is removed."""
        df = make_filter_df(indicator_category="No")
        result = filter_records(df)
        assert len(result) == 0

    def test_all_filters_must_pass_simultaneously(self):
        """Tests that a row failing even one filter is removed entirely."""
        # Valid in PHU, gender, estimate_type, but fails indicator_category
        df = make_filter_df(indicator_category="No")
        result = filter_records(df)
        assert len(result) == 0

    def test_filters_mixed_dataframe(self):
        """Tests that only fully-valid rows survive a mixed DataFrame."""
        df = pd.DataFrame([
            make_filter_df().iloc[0],                                             # passes all
            make_filter_df(gender="Persons").iloc[0],                             # fails gender
            make_filter_df(estimate_type="Age-standardised").iloc[0],             # fails estimate
            make_filter_df(stratified_by="Unknown PHU").iloc[0],                  # fails PHU
            make_filter_df(indicator_category="No").iloc[0],                      # fails category
            make_filter_df(gender="Men", indicator_category="Yes, definitely").iloc[0],  # passes all
        ])
        result = filter_records(df)
        assert len(result) == 2

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_filter_df()
        assert isinstance(filter_records(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# add_vic_region_code
# ---------------------------------------------------------------------------

class TestAddVicRegionCode:
    def test_adds_vic_region_code_column(self):
        """Tests that a 'vic_region_code' column is added."""
        df = pd.DataFrame({"region": [VALID_REGION]})
        result = add_vic_region_code(df)
        assert "vic_region_code" in result.columns

    @pytest.mark.parametrize("region,expected_code", [
        ("LGAs of Barwon South-West PHU", 10),
        ("LGAs of North Eastern PHU", 11),
        ("LGAs of Gippsland PHU", 12),
        ("LGAs of Grampians Wimmera Southern Mallee PHU", 13),
        ("LGAs of Goulburn Valley PHU", 14),
        ("LGAs of Loddon Mallee PHU", 15),
        ("LGAs of Western PHU", 16),
        ("LGAs of South East PHU", 17),
    ])
    def test_correct_code_for_each_region(self, region, expected_code):
        """Tests that each region maps to its expected region code."""
        df = pd.DataFrame({"region": [region]})
        result = add_vic_region_code(df)
        assert result["vic_region_code"].iloc[0] == expected_code

    def test_ovens_murray_and_goulburn_valley_share_code_14(self):
        """Documents the known duplicate: both Ovens-Murray and Goulburn Valley map to
        code 14. This is likely a copy-paste bug in the REGION_CODES dict — each other
        region has a unique code. A future fix should assign Ovens-Murray a distinct code.
        """
        df = pd.DataFrame({"region": [
            "LGAs of Ovens-Murray PHU",
            "LGAs of Goulburn Valley PHU",
        ]})
        result = add_vic_region_code(df)
        assert result["vic_region_code"].iloc[0] == 14
        assert result["vic_region_code"].iloc[1] == 14

    def test_unknown_region_produces_nan_code(self):
        """Tests that an unrecognised region yields NaN (not an error) via dict.map."""
        df = pd.DataFrame({"region": ["LGAs of Unknown PHU"]})
        result = add_vic_region_code(df)
        assert pd.isna(result["vic_region_code"].iloc[0])

    def test_all_known_regions_produce_non_nan_codes(self):
        """Tests that every region in REGION_CODES produces a valid (non-NaN) code."""
        df = pd.DataFrame({"region": list(REGION_CODES.keys())})
        result = add_vic_region_code(df)
        assert result["vic_region_code"].notna().all()

    def test_existing_columns_are_preserved(self):
        """Tests that columns other than vic_region_code are unchanged."""
        df = pd.DataFrame({"region": [VALID_REGION], "gender": ["Women"]})
        result = add_vic_region_code(df)
        assert "gender" in result.columns
        assert result["gender"].iloc[0] == "Women"

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"region": [VALID_REGION]})
        assert isinstance(add_vic_region_code(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# wrangle_food_insecurity (integration)
# NOTE: wrangle_food_insecurity uses rename_columns and select_columns but
# does NOT import them from .utils — this will raise NameError at runtime.
# The integration tests below document this bug: they will fail until the
# imports are added:
#   from .utils import initial_cleaning_pipeline, rename_columns, select_columns
# ---------------------------------------------------------------------------

class TestWrangleFoodInsecurity:
    def test_returns_dataframe(self):
        """Tests that the pipeline returns a DataFrame."""
        df = make_full_raw_df()
        result = wrangle_food_insecurity(df)
        assert isinstance(result, pd.DataFrame)

    def test_output_has_expected_columns(self):
        """Tests that the output contains all required schema columns."""
        df = make_full_raw_df()
        result = wrangle_food_insecurity(df)
        expected_cols = [
            "gender", "indicator", "indicator_category",
            "region", "subpopulation", "estimate_pct", "vic_region_code",
        ]
        for col in expected_cols:
            assert col in result.columns, f"Missing column: {col}"

    def test_stratified_by_renamed_to_region(self):
        """Tests that 'stratified_by' is renamed to 'region' end-to-end."""
        df = make_full_raw_df()
        result = wrangle_food_insecurity(df)
        assert "region" in result.columns
        assert "stratified_by" not in result.columns

    def test_percent_column_renamed_to_estimate_pct(self):
        """Tests that the '%' raw column (standardised to '' by initial_cleaning_pipeline)
        is renamed to 'estimate_pct' by the pipeline."""
        df = make_full_raw_df(**{"%": 15.0})
        result = wrangle_food_insecurity(df)
        assert "estimate_pct" in result.columns
        assert result["estimate_pct"].iloc[0] == 15.0

    def test_filters_out_non_vic_regions(self):
        """Tests that rows with out-of-scope regions are removed end-to-end."""
        df = pd.DataFrame([
            make_full_raw_df(stratified_by=VALID_REGION).iloc[0],
            make_full_raw_df(stratified_by="LGAs of Unknown PHU").iloc[0],
        ])
        result = wrangle_food_insecurity(df)
        assert len(result) == 1

    def test_filters_out_persons_gender(self):
        """Tests that rows with 'Persons' gender are removed end-to-end."""
        df = pd.DataFrame([
            make_full_raw_df(gender="Women").iloc[0],
            make_full_raw_df(gender="Persons").iloc[0],
        ])
        result = wrangle_food_insecurity(df)
        assert len(result) == 1
        assert result["gender"].iloc[0] == "Women"

    def test_filters_out_non_crude_estimate_types(self):
        """Tests that non-Crude estimate type rows are removed end-to-end."""
        df = pd.DataFrame([
            make_full_raw_df(estimate_type="Crude").iloc[0],
            make_full_raw_df(estimate_type="Age-standardised").iloc[0],
        ])
        result = wrangle_food_insecurity(df)
        assert len(result) == 1

    def test_filters_out_non_yes_indicator_categories(self):
        """Tests that rows with 'No' indicator_category are removed end-to-end."""
        df = pd.DataFrame([
            make_full_raw_df(indicator_category="Yes").iloc[0],
            make_full_raw_df(indicator_category="No").iloc[0],
        ])
        result = wrangle_food_insecurity(df)
        assert len(result) == 1

    def test_subpopulation_is_cleaned(self):
        """Tests that the parenthetical age range is stripped end-to-end."""
        df = make_full_raw_df(subpopulation="Total (18+ years)")
        result = wrangle_food_insecurity(df)
        assert result["subpopulation"].iloc[0] == "Total"

    def test_nan_estimate_pct_is_imputed_to_zero(self):
        """Tests that a NaN estimate value is imputed to 0 end-to-end."""
        df = make_full_raw_df(**{"%": np.nan})
        result = wrangle_food_insecurity(df)
        assert result["estimate_pct"].iloc[0] == 0

    def test_vic_region_code_is_added(self):
        """Tests that vic_region_code is present and correct end-to-end."""
        df = make_full_raw_df(stratified_by="LGAs of South East PHU")
        result = wrangle_food_insecurity(df)
        assert "vic_region_code" in result.columns
        assert result["vic_region_code"].iloc[0] == 17

    def test_does_not_mutate_input(self):
        """Tests that the original input DataFrame is not modified by the pipeline."""
        df = make_full_raw_df()
        original_columns = list(df.columns)
        original_value = df["stratified_by"].iloc[0]
        wrangle_food_insecurity(df)
        assert list(df.columns) == original_columns
        assert df["stratified_by"].iloc[0] == original_value

    def test_empty_dataframe_after_filtering_returns_empty(self):
        """Tests that filtering all rows returns an empty DataFrame (not an error)."""
        df = make_full_raw_df(gender="Persons")  # will be filtered out
        result = wrangle_food_insecurity(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0