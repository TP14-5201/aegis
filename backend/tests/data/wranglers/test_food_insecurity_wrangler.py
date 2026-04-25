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
    add_region_ids,
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

# Local copy of the PHU → vicgov_region mapping defined in the wrangler module.
# Used in add_region_ids tests so they are self-contained.
_PHU_TO_VICGOV_REGION = {
    "LGAs of Barwon South-West PHU":                  "BARWON SOUTH WEST",
    "LGAs of Gippsland PHU":                          "GIPPSLAND",
    "LGAs of Grampians Wimmera Southern Mallee PHU":  "GRAMPIANS",
    "LGAs of Goulburn Valley PHU":                    "HUME",
    "LGAs of Ovens-Murray PHU":                       "HUME",
    "LGAs of Loddon Mallee PHU":                      "LODDON MALLEE",
    "LGAs of North Eastern PHU":                      "EASTERN METROPOLITAN",
    "LGAs of South East PHU":                         "SOUTHERN METROPOLITAN",
    "LGAs of Western PHU":                            "NORTHERN AND WESTERN METROPOLITAN",
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


def make_vic_boundaries_df(rows: list[dict] | None = None) -> pd.DataFrame:
    """
    Minimal vic_boundaries DataFrame for add_region_ids and integration tests.
    vicgov_region is title-cased as it arrives from vic_boundaries_wrangler;
    add_region_ids uppercases it internally for the case-insensitive lookup.

    VALID_REGION ('LGAs of South East PHU') maps to 'SOUTHERN METROPOLITAN'.
    """
    if rows is None:
        rows = [{"vicgov_region": "Southern Metropolitan", "ufi": "UFI_001"}]
    return pd.DataFrame(rows)


def make_viclga_boundaries_df(rows: list[dict] | None = None) -> pd.DataFrame:
    """
    Minimal viclga_boundaries DataFrame for add_region_ids and integration tests.
    lga_name must match the cleaned subpopulation value (parentheticals stripped).

    The default 'Total' matches make_full_raw_df's subpopulation 'Total (18+ years)'
    after clean_subpopulation runs.
    """
    if rows is None:
        rows = [{"lga_name": "Total", "lga_pid": "LGA_PID_001"}]
    return pd.DataFrame(rows)


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
# add_region_ids
# ---------------------------------------------------------------------------

class TestAddRegionIds:
    """Tests for add_region_ids(df, vic_boundaries, viclga_boundaries).

    add_region_ids enriches the food insecurity DataFrame with two foreign keys:
    - ufi:     resolved via _PHU_TO_VICGOV_REGION → vicgov_region (case-insensitive)
               → ufi from vic_boundaries.
    - lga_pid: resolved by matching subpopulation against lga_name in
               viclga_boundaries.

    The input df uses the post-pipeline column names (region, subpopulation)
    as the function runs after rename_columns in the pipeline.
    """

    def _make_df(self, region=VALID_REGION, subpopulation="Total") -> pd.DataFrame:
        """Minimal post-rename DataFrame for add_region_ids unit tests."""
        return pd.DataFrame([{"region": region, "subpopulation": subpopulation}])

    # --- Return type ---------------------------------------------------------

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = self._make_df()
        result = add_region_ids(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert isinstance(result, pd.DataFrame)

    # --- ufi column ----------------------------------------------------------

    def test_adds_ufi_column(self):
        """Tests that a 'ufi' column is added to the DataFrame."""
        df = self._make_df()
        result = add_region_ids(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert "ufi" in result.columns

    def test_correct_ufi_resolved_for_known_region(self):
        """Tests that a known PHU region resolves to the correct ufi."""
        vic_boundaries = pd.DataFrame([
            {"vicgov_region": "Southern Metropolitan", "ufi": "UFI_SOUTH_EAST"},
        ])
        df = self._make_df(region="LGAs of South East PHU")
        result = add_region_ids(df, vic_boundaries, make_viclga_boundaries_df())
        assert result["ufi"].iloc[0] == "UFI_SOUTH_EAST"

    def test_vicgov_region_lookup_is_case_insensitive(self):
        """Tests that vicgov_region matching works regardless of case in vic_boundaries.

        The wrangler title-cases vicgov_region; _PHU_TO_VICGOV_REGION stores uppercase.
        add_region_ids uppercases vic_boundaries values before matching, so both
        'Southern Metropolitan' and 'SOUTHERN METROPOLITAN' should resolve correctly.
        """
        for case in ("Southern Metropolitan", "SOUTHERN METROPOLITAN", "southern metropolitan"):
            vic_boundaries = pd.DataFrame([{"vicgov_region": case, "ufi": "UFI_CASE_TEST"}])
            df = self._make_df(region="LGAs of South East PHU")
            result = add_region_ids(df, vic_boundaries, make_viclga_boundaries_df())
            assert result["ufi"].iloc[0] == "UFI_CASE_TEST", f"Failed for vicgov_region='{case}'"

    def test_two_phu_regions_sharing_vicgov_get_same_ufi(self):
        """Tests that Ovens-Murray and Goulburn Valley both resolve to the HUME ufi.

        Both PHU regions map to the same vicgov_region ('HUME'), so both should
        receive the same ufi value.
        """
        vic_boundaries = pd.DataFrame([{"vicgov_region": "Hume", "ufi": "UFI_HUME"}])
        df = pd.DataFrame([
            {"region": "LGAs of Ovens-Murray PHU",    "subpopulation": "Total"},
            {"region": "LGAs of Goulburn Valley PHU", "subpopulation": "Total"},
        ])
        result = add_region_ids(df, vic_boundaries, make_viclga_boundaries_df())
        assert result["ufi"].iloc[0] == "UFI_HUME"
        assert result["ufi"].iloc[1] == "UFI_HUME"

    def test_unknown_region_produces_nan_ufi(self):
        """Tests that a region absent from _PHU_TO_VICGOV_REGION yields NaN ufi."""
        df = self._make_df(region="LGAs of Unknown PHU")
        result = add_region_ids(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert pd.isna(result["ufi"].iloc[0])

    def test_all_known_phu_regions_resolve_non_nan_ufi(self):
        """Tests that every region in _PHU_TO_VICGOV_REGION resolves to a non-NaN ufi."""
        # Build a vic_boundaries with one row per unique vicgov_region
        unique_vicgov = list({v for v in _PHU_TO_VICGOV_REGION.values()})
        vic_boundaries = pd.DataFrame([
            {"vicgov_region": vg, "ufi": f"UFI_{i}"} for i, vg in enumerate(unique_vicgov)
        ])
        df = pd.DataFrame([{"region": phu, "subpopulation": "Total"} for phu in _PHU_TO_VICGOV_REGION])
        result = add_region_ids(df, vic_boundaries, make_viclga_boundaries_df())
        assert result["ufi"].notna().all(), "Some PHU regions failed to resolve a ufi"

    # --- lga_pid column ------------------------------------------------------

    def test_adds_lga_pid_column(self):
        """Tests that a 'lga_pid' column is added to the DataFrame."""
        df = self._make_df()
        result = add_region_ids(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert "lga_pid" in result.columns

    def test_correct_lga_pid_resolved_for_known_subpopulation(self):
        """Tests that a subpopulation matching a lga_name resolves the correct lga_pid."""
        viclga_boundaries = pd.DataFrame([{"lga_name": "Melbourne", "lga_pid": "LGA_MEL"}])
        df = self._make_df(subpopulation="Melbourne")
        result = add_region_ids(df, make_vic_boundaries_df(), viclga_boundaries)
        assert result["lga_pid"].iloc[0] == "LGA_MEL"

    def test_unknown_subpopulation_produces_nan_lga_pid(self):
        """Tests that a subpopulation with no matching lga_name yields NaN lga_pid."""
        df = self._make_df(subpopulation="Unknown LGA")
        result = add_region_ids(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert pd.isna(result["lga_pid"].iloc[0])

    def test_handles_duplicate_lga_name_columns_in_viclga_boundaries(self):
        """Tests that duplicate lga_name columns in viclga_boundaries are handled correctly.

        The function drops duplicated columns keeping the last occurrence, so the
        lookup uses the final lga_name column (the cleaned abb_name value).
        """
        viclga_boundaries = pd.DataFrame(
            [["Melbourne (orig)", "Melbourne", "LGA_MEL"]],
            columns=["lga_name", "lga_name", "lga_pid"],
        )
        df = self._make_df(subpopulation="Melbourne")
        result = add_region_ids(df, make_vic_boundaries_df(), viclga_boundaries)
        assert result["lga_pid"].iloc[0] == "LGA_MEL"

    def test_multiple_rows_resolved_independently(self):
        """Tests that ufi and lga_pid are resolved correctly for each row."""
        vic_boundaries = pd.DataFrame([
            {"vicgov_region": "Southern Metropolitan", "ufi": "UFI_SE"},
            {"vicgov_region": "Gippsland",             "ufi": "UFI_GL"},
        ])
        viclga_boundaries = pd.DataFrame([
            {"lga_name": "Melbourne", "lga_pid": "LGA_MEL"},
            {"lga_name": "Ballarat",  "lga_pid": "LGA_BAL"},
        ])
        df = pd.DataFrame([
            {"region": "LGAs of South East PHU", "subpopulation": "Melbourne"},
            {"region": "LGAs of Gippsland PHU",  "subpopulation": "Ballarat"},
        ])
        result = add_region_ids(df, vic_boundaries, viclga_boundaries)
        assert result["ufi"].iloc[0] == "UFI_SE"
        assert result["ufi"].iloc[1] == "UFI_GL"
        assert result["lga_pid"].iloc[0] == "LGA_MEL"
        assert result["lga_pid"].iloc[1] == "LGA_BAL"

    # --- Column preservation -------------------------------------------------

    def test_existing_columns_are_preserved(self):
        """Tests that columns other than ufi and lga_pid are untouched."""
        df = pd.DataFrame([{
            "region": VALID_REGION,
            "subpopulation": "Total",
            "gender": "Women",
            "estimate_pct": 12.5,
        }])
        result = add_region_ids(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert result["gender"].iloc[0] == "Women"
        assert result["estimate_pct"].iloc[0] == 12.5


# ---------------------------------------------------------------------------
# wrangle_food_insecurity (integration)
# ---------------------------------------------------------------------------

class TestWrangleFoodInsecurity:
    def test_returns_dataframe(self):
        """Tests that the pipeline returns a DataFrame."""
        df = make_full_raw_df()
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert isinstance(result, pd.DataFrame)

    def test_output_has_expected_columns(self):
        """Tests that the output contains all required schema columns."""
        df = make_full_raw_df()
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        expected_cols = [
            "gender", "indicator", "indicator_category",
            "region", "subpopulation", "estimate_pct", "ufi", "lga_pid",
        ]
        for col in expected_cols:
            assert col in result.columns, f"Missing column: {col}"

    def test_stratified_by_renamed_to_region(self):
        """Tests that 'stratified_by' is renamed to 'region' end-to-end."""
        df = make_full_raw_df()
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert "region" in result.columns
        assert "stratified_by" not in result.columns

    def test_percent_column_renamed_to_estimate_pct(self):
        """Tests that the '%' raw column (standardised to '' by initial_cleaning_pipeline)
        is renamed to 'estimate_pct' by the pipeline."""
        df = make_full_raw_df(**{"%": 15.0})
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert "estimate_pct" in result.columns
        assert result["estimate_pct"].iloc[0] == 15.0

    def test_filters_out_non_vic_regions(self):
        """Tests that rows with out-of-scope regions are removed end-to-end."""
        df = pd.DataFrame([
            make_full_raw_df(stratified_by=VALID_REGION).iloc[0],
            make_full_raw_df(stratified_by="LGAs of Unknown PHU").iloc[0],
        ])
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert len(result) == 1

    def test_filters_out_persons_gender(self):
        """Tests that rows with 'Persons' gender are removed end-to-end."""
        df = pd.DataFrame([
            make_full_raw_df(gender="Women").iloc[0],
            make_full_raw_df(gender="Persons").iloc[0],
        ])
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert len(result) == 1
        assert result["gender"].iloc[0] == "Women"

    def test_filters_out_non_crude_estimate_types(self):
        """Tests that non-Crude estimate type rows are removed end-to-end."""
        df = pd.DataFrame([
            make_full_raw_df(estimate_type="Crude").iloc[0],
            make_full_raw_df(estimate_type="Age-standardised").iloc[0],
        ])
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert len(result) == 1

    def test_filters_out_non_yes_indicator_categories(self):
        """Tests that rows with 'No' indicator_category are removed end-to-end."""
        df = pd.DataFrame([
            make_full_raw_df(indicator_category="Yes").iloc[0],
            make_full_raw_df(indicator_category="No").iloc[0],
        ])
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert len(result) == 1

    def test_subpopulation_is_cleaned(self):
        """Tests that the parenthetical age range is stripped end-to-end."""
        df = make_full_raw_df(subpopulation="Total (18+ years)")
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert result["subpopulation"].iloc[0] == "Total"

    def test_nan_estimate_pct_is_imputed_to_zero(self):
        """Tests that a NaN estimate value is imputed to 0 end-to-end."""
        df = make_full_raw_df(**{"%": np.nan})
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert result["estimate_pct"].iloc[0] == 0

    def test_ufi_is_resolved_end_to_end(self):
        """Tests that ufi is correctly enriched from vic_boundaries end-to-end.

        VALID_REGION ('LGAs of South East PHU') maps to 'SOUTHERN METROPOLITAN',
        which should resolve to the ufi supplied in vic_boundaries.
        """
        vic_boundaries = pd.DataFrame([
            {"vicgov_region": "Southern Metropolitan", "ufi": "UFI_EXPECTED"},
        ])
        df = make_full_raw_df(stratified_by=VALID_REGION)
        result = wrangle_food_insecurity(df, vic_boundaries, make_viclga_boundaries_df())
        assert "ufi" in result.columns
        assert result["ufi"].iloc[0] == "UFI_EXPECTED"

    def test_lga_pid_is_resolved_end_to_end(self):
        """Tests that lga_pid is correctly enriched from viclga_boundaries end-to-end.

        subpopulation 'Total (18+ years)' is cleaned to 'Total' by clean_subpopulation,
        which must then match lga_name in viclga_boundaries.
        """
        viclga_boundaries = pd.DataFrame([
            {"lga_name": "Total", "lga_pid": "LGA_EXPECTED"},
        ])
        df = make_full_raw_df(subpopulation="Total (18+ years)")
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), viclga_boundaries)
        assert "lga_pid" in result.columns
        assert result["lga_pid"].iloc[0] == "LGA_EXPECTED"

    def test_does_not_mutate_input(self):
        """Tests that the original input DataFrame is not modified by the pipeline."""
        df = make_full_raw_df()
        original_columns = list(df.columns)
        original_value = df["stratified_by"].iloc[0]
        wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert list(df.columns) == original_columns
        assert df["stratified_by"].iloc[0] == original_value

    def test_empty_dataframe_after_filtering_returns_empty(self):
        """Tests that filtering all rows returns an empty DataFrame (not an error)."""
        df = make_full_raw_df(gender="Persons")  # will be filtered out
        result = wrangle_food_insecurity(df, make_vic_boundaries_df(), make_viclga_boundaries_df())
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0