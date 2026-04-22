import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, call

from src.data.loaders.data_loader import (
    _load_and_wrangle,
    load_emergency_services_dataset,
    load_food_insecurity_dataset,
    load_vic_boundaries_dataset,
    load_viclga_boundaries_dataset,
)
from src.core.config import settings


# ---------------------------------------------------------------------------
# Shared sample data
# ---------------------------------------------------------------------------

def make_sample_df(name_values: list[str] | None = None) -> pd.DataFrame:
    """Returns a minimal DataFrame for use as wrangler output stubs."""
    names = name_values or ["Service A", "Service B"]
    return pd.DataFrame({
        "name": names,
        "suburb": ["Melbourne"] * len(names),
        "source": ["test"] * len(names),
    })


MELBOURNE_DF = make_sample_df(["Zed Service", "Alpha Service"])
DATAGOV_DF   = make_sample_df(["Middle Service"])
VIC_DF       = pd.DataFrame({"vicgov_region": ["South East"], "geometry": ["POLYGON(...)"]})
LGA_DF       = pd.DataFrame({"lga_name": ["Melbourne"], "geometry": ["POLYGON(...)"]})

# ---------------------------------------------------------------------------
# Shared food insecurity fixtures
#
# load_food_insecurity_dataset now runs in three phases:
#   1. Read + wrangle the food insecurity Excel  → food_insecurity_df
#   2. _get_lga_service_counts: read the DataGov CSV via pd.read_csv,
#      run initial_cleaning_pipeline, split "lga" on "(", strip, groupby
#      → DataFrame with ["lga", "emergency_services_count"]
#   3. inner-join food_insecurity_df with lga_counts on subpopulation == lga
#
# Three DataFrames cover these phases in tests:
#   DATAGOV_RAW_DF   — returned by pd.read_csv inside _get_lga_service_counts
#   FOOD_WRANGLED_DF — returned by wrangle_food_insecurity (has "subpopulation")
# ---------------------------------------------------------------------------

# Raw DataGov CSV fed to _get_lga_service_counts.
# After split("(").str[0].str.strip():
#   "Melbourne (City)" -> "Melbourne"  (×2 → count 2)
#   "Yarra (City)"     -> "Yarra"      (×1 → count 1)
#   "No Parens"        -> "No Parens"  (×1 → count 1)
DATAGOV_RAW_DF = pd.DataFrame({
    "lga": [
        "Melbourne (City)",
        "Melbourne (City)",
        "Yarra (City)",
        "No Parens",
    ]
})

# Wrangled food insecurity DataFrame (output of wrangle_food_insecurity).
# "subpopulation" is the join key against "lga" in lga_counts.
# "No Match" has no corresponding LGA → dropped by the inner join → 2 rows remain.
FOOD_WRANGLED_DF = pd.DataFrame({
    "subpopulation": ["Melbourne", "Yarra", "No Match"],
    "indicator":     ["food insecurity"] * 3,
    "estimate_pct":  [10.0, 15.0, 5.0],
})


def _run_food_loader(
    *,
    food_wrangled: pd.DataFrame | None = None,
    datagov_raw: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Runs load_food_insecurity_dataset() with all external calls mocked.

    food_wrangled — DataFrame returned by wrangle_food_insecurity
    datagov_raw   — DataFrame returned by pd.read_csv (DataGov file)

    initial_cleaning_pipeline is stubbed as an identity function so the
    raw datagov_raw DataFrame passes through unchanged.
    """
    food_wrangled = food_wrangled if food_wrangled is not None else FOOD_WRANGLED_DF
    datagov_raw   = datagov_raw   if datagov_raw   is not None else DATAGOV_RAW_DF

    with patch("src.data.loaders.data_loader.pd.read_excel", return_value=food_wrangled), \
         patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=food_wrangled), \
         patch("src.data.loaders.data_loader.pd.read_csv", return_value=datagov_raw), \
         patch("src.data.loaders.data_loader.initial_cleaning_pipeline", side_effect=lambda df: df):
        return load_food_insecurity_dataset()


# ---------------------------------------------------------------------------
# _load_and_wrangle (private helper — unit tested directly)
# ---------------------------------------------------------------------------

class TestLoadAndWrangle:
    def test_reads_csv_by_default(self):
        """Tests that pd.read_csv is used when is_excel=False (the default)."""
        mock_df = make_sample_df()
        mock_wrangler = MagicMock(return_value=mock_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=mock_df) as mock_read_csv, \
             patch("src.data.loaders.data_loader.pd.read_excel") as mock_read_excel:
            _load_and_wrangle("some/path.csv", mock_wrangler, "test")

        mock_read_csv.assert_called_once_with("some/path.csv")
        mock_read_excel.assert_not_called()

    def test_reads_excel_when_is_excel_true(self):
        """Tests that pd.read_excel is used when is_excel=True."""
        mock_df = make_sample_df()
        mock_wrangler = MagicMock(return_value=mock_df)

        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=mock_df) as mock_read_excel, \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv:
            _load_and_wrangle("some/path.xlsx", mock_wrangler, "test", is_excel=True)

        mock_read_excel.assert_called_once_with("some/path.xlsx", sheet_name=0)
        mock_read_csv.assert_not_called()

    def test_excel_reads_first_sheet_by_default(self):
        """Tests that Excel files are read with sheet_name=0 (the first sheet)."""
        mock_df = make_sample_df()
        mock_wrangler = MagicMock(return_value=mock_df)

        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=mock_df) as mock_read_excel:
            _load_and_wrangle("path.xlsx", mock_wrangler, "test", is_excel=True)

        _, kwargs = mock_read_excel.call_args
        assert kwargs.get("sheet_name") == 0

    def test_passes_dataframe_to_wrangler(self):
        """Tests that the DataFrame returned by read_csv/read_excel is passed to the wrangler."""
        raw_df = make_sample_df()
        wrangled_df = make_sample_df(["Wrangled"])
        mock_wrangler = MagicMock(return_value=wrangled_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df):
            _load_and_wrangle("path.csv", mock_wrangler, "test")

        mock_wrangler.assert_called_once_with(raw_df)

    def test_returns_wrangler_output(self):
        """Tests that the return value is the wrangler's output, not the raw DataFrame."""
        raw_df = make_sample_df()
        wrangled_df = make_sample_df(["Wrangled Result"])
        mock_wrangler = MagicMock(return_value=wrangled_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df):
            result = _load_and_wrangle("path.csv", mock_wrangler, "test")

        assert result is wrangled_df

    def test_logs_error_on_read_failure(self):
        """Tests that a read failure is logged at ERROR level with the label and path."""
        error = FileNotFoundError("No such file")

        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=error), \
             patch("src.data.loaders.data_loader.logger") as mock_logger:
            with pytest.raises(FileNotFoundError):
                _load_and_wrangle("missing.csv", MagicMock(), "Melbourne")

        mock_logger.error.assert_called_once_with(
            f"Failed to read Melbourne raw data from 'missing.csv': {error}"
        )

    def test_reraises_exception_after_logging(self):
        """Tests that exceptions are re-raised after logging — NOT swallowed."""
        error = FileNotFoundError("missing")

        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=error), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError, match="missing"):
                _load_and_wrangle("bad.csv", MagicMock(), "test")

    def test_logs_error_on_wrangler_failure(self):
        """Tests that a wrangler failure is also caught, logged, and re-raised."""
        raw_df = make_sample_df()
        error = ValueError("Wrangling failed")
        mock_wrangler = MagicMock(side_effect=error)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df), \
             patch("src.data.loaders.data_loader.logger") as mock_logger:
            with pytest.raises(ValueError):
                _load_and_wrangle("path.csv", mock_wrangler, "test label")

        mock_logger.error.assert_called_once_with(
            f"Failed to read test label raw data from 'path.csv': {error}"
        )

    def test_error_message_includes_path(self):
        """Tests that the logged error message contains the file path."""
        error = Exception("fail")

        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=error), \
             patch("src.data.loaders.data_loader.logger") as mock_logger:
            with pytest.raises(Exception):
                _load_and_wrangle("src/data/raw/specific.csv", MagicMock(), "label")

        logged_msg = mock_logger.error.call_args[0][0]
        assert "src/data/raw/specific.csv" in logged_msg

    def test_returns_dataframe(self):
        """Tests that the return value is a DataFrame."""
        raw_df = make_sample_df()
        mock_wrangler = MagicMock(return_value=raw_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df):
            result = _load_and_wrangle("path.csv", mock_wrangler, "test")

        assert isinstance(result, pd.DataFrame)


# ---------------------------------------------------------------------------
# load_emergency_services_dataset
# ---------------------------------------------------------------------------

class TestLoadEmergencyServicesDataset:
    def _run(self, mel_df=None, gov_df=None):
        """Runs load_emergency_services_dataset with both wranglers mocked."""
        mel_df = mel_df if mel_df is not None else MELBOURNE_DF
        gov_df = gov_df if gov_df is not None else DATAGOV_DF

        with patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_melbourne", return_value=mel_df), \
             patch("src.data.loaders.data_loader.wrangle_datagov", return_value=gov_df):
            mock_read_csv.side_effect = [mel_df, gov_df]
            return load_emergency_services_dataset()

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        result = self._run()
        assert isinstance(result, pd.DataFrame)

    def test_reads_melbourne_from_correct_path(self):
        """Tests that the Melbourne raw CSV is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_melbourne", return_value=MELBOURNE_DF), \
             patch("src.data.loaders.data_loader.wrangle_datagov", return_value=DATAGOV_DF):
            mock_read_csv.side_effect = [MELBOURNE_DF, DATAGOV_DF]
            load_emergency_services_dataset()

        paths_called = [c.args[0] for c in mock_read_csv.call_args_list]
        assert settings.MELBOURNE_RAW_PATH in paths_called

    def test_reads_datagov_from_correct_path(self):
        """Tests that the DataGov raw CSV is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_melbourne", return_value=MELBOURNE_DF), \
             patch("src.data.loaders.data_loader.wrangle_datagov", return_value=DATAGOV_DF):
            mock_read_csv.side_effect = [MELBOURNE_DF, DATAGOV_DF]
            load_emergency_services_dataset()

        paths_called = [c.args[0] for c in mock_read_csv.call_args_list]
        assert settings.DATAGOV_RAW_PATH in paths_called

    def test_combines_both_datasets(self):
        """Tests that both Melbourne and DataGov rows appear in the output."""
        mel_df = make_sample_df(["Zed Service"])
        gov_df = make_sample_df(["Alpha Service"])
        result = self._run(mel_df=mel_df, gov_df=gov_df)
        assert "Zed Service" in result["name"].values
        assert "Alpha Service" in result["name"].values

    def test_combined_row_count_is_sum_of_both_sources(self):
        """Tests that the combined DataFrame has rows from both sources."""
        mel_df = make_sample_df(["A", "B"])
        gov_df = make_sample_df(["C", "D", "E"])
        result = self._run(mel_df=mel_df, gov_df=gov_df)
        assert len(result) == 5

    def test_output_is_sorted_by_name_ascending(self):
        """Tests that the combined result is sorted alphabetically by 'name'."""
        mel_df = make_sample_df(["Zed Service", "Middle Service"])
        gov_df = make_sample_df(["Alpha Service"])
        result = self._run(mel_df=mel_df, gov_df=gov_df)
        names = list(result["name"])
        assert names == sorted(names)

    def test_output_index_is_reset_after_concat(self):
        """Tests that the output has a clean 0..N integer index (ignore_index=True)."""
        mel_df = make_sample_df(["A", "B"])
        gov_df = make_sample_df(["C"])
        result = self._run(mel_df=mel_df, gov_df=gov_df)
        assert list(result.index) == list(range(len(result)))

    def test_propagates_exception_from_melbourne_load(self):
        """Tests that a failure loading the Melbourne dataset propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_emergency_services_dataset()

    def test_propagates_exception_from_datagov_load(self):
        """Tests that a failure loading the DataGov dataset propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_melbourne", return_value=MELBOURNE_DF), \
             patch("src.data.loaders.data_loader.logger"):
            mock_read_csv.side_effect = [MELBOURNE_DF, FileNotFoundError("missing")]
            with pytest.raises(FileNotFoundError):
                load_emergency_services_dataset()


# ---------------------------------------------------------------------------
# load_food_insecurity_dataset
#
# CHANGED BEHAVIOUR — this function now:
#   1. Reads + wrangles the food insecurity Excel (unchanged)
#   2. Reads the DataGov CSV via pd.read_csv (NEW — _get_lga_service_counts)
#   3. Applies initial_cleaning_pipeline to the DataGov DF (NEW)
#   4. Strips parenthetical suffixes from "lga" values (NEW)
#   5. Counts services per LGA (NEW)
#   6. Inner-joins food_insecurity_df with lga_counts on subpopulation == lga (NEW)
#
# BUGS IN IMPLEMENTATION:
#   - Dead code: `return food_insecurity_df` after `return pd.merge(...)` is
#     unreachable — leftover from before the feature was added; should be removed.
#   - `filter_victoria_services` is imported but never used.
#
# PATCHING NOTE:
#   pd.read_csv is now called inside _get_lga_service_counts, so any test
#   that previously asserted mock_csv.assert_not_called() was wrong and has
#   been corrected.
# ---------------------------------------------------------------------------

class TestLoadFoodInsecurityDataset:

    # --- Return type & output structure --------------------------------------

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        result = _run_food_loader()
        assert isinstance(result, pd.DataFrame)

    def test_result_contains_food_insecurity_columns(self):
        """Tests that food insecurity columns (indicator, estimate_pct) survive the merge."""
        result = _run_food_loader()
        assert "indicator" in result.columns
        assert "estimate_pct" in result.columns

    def test_result_contains_emergency_services_count_column(self):
        """Tests that the lga_counts column is present after the merge."""
        result = _run_food_loader()
        assert "emergency_services_count" in result.columns

    def test_result_contains_lga_column(self):
        """Tests that the 'lga' column from lga_counts is present in the merged output."""
        result = _run_food_loader()
        assert "lga" in result.columns

    # --- Food insecurity Excel read ------------------------------------------

    def test_reads_food_insecurity_from_correct_excel_path(self):
        """Tests that pd.read_excel is called with the configured food insecurity path."""
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_WRANGLED_DF) as mock_excel, \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_WRANGLED_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv", return_value=DATAGOV_RAW_DF), \
             patch("src.data.loaders.data_loader.initial_cleaning_pipeline", side_effect=lambda df: df):
            load_food_insecurity_dataset()

        mock_excel.assert_called_once_with(settings.FOOD_INSECURITY_RAW_PATH, sheet_name=0)

    def test_uses_excel_reader_for_food_insecurity_file(self):
        """Tests that pd.read_excel is called exactly once for the food insecurity file.

        NOTE: pd.read_csv IS also called (for the DataGov file in _get_lga_service_counts).
        The old test incorrectly asserted read_csv was never called — that was
        only true before this feature was added.
        """
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_WRANGLED_DF) as mock_excel, \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_WRANGLED_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv", return_value=DATAGOV_RAW_DF), \
             patch("src.data.loaders.data_loader.initial_cleaning_pipeline", side_effect=lambda df: df):
            load_food_insecurity_dataset()

        mock_excel.assert_called_once()

    def test_passes_raw_excel_df_to_food_insecurity_wrangler(self):
        """Tests that the DataFrame read from Excel is passed to wrangle_food_insecurity."""
        raw_excel_df = FOOD_WRANGLED_DF.copy()
        mock_wrangler = MagicMock(return_value=FOOD_WRANGLED_DF)

        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=raw_excel_df), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", mock_wrangler), \
             patch("src.data.loaders.data_loader.pd.read_csv", return_value=DATAGOV_RAW_DF), \
             patch("src.data.loaders.data_loader.initial_cleaning_pipeline", side_effect=lambda df: df):
            load_food_insecurity_dataset()

        mock_wrangler.assert_called_once_with(raw_excel_df)

    # --- DataGov LGA counts (_get_lga_service_counts) -----------------------

    def test_reads_datagov_csv_for_lga_counts(self):
        """Tests that pd.read_csv is called with the DataGov path inside _get_lga_service_counts."""
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_WRANGLED_DF), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_WRANGLED_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv", return_value=DATAGOV_RAW_DF) as mock_csv, \
             patch("src.data.loaders.data_loader.initial_cleaning_pipeline", side_effect=lambda df: df):
            load_food_insecurity_dataset()

        mock_csv.assert_called_once_with(settings.DATAGOV_RAW_PATH)

    def test_applies_initial_cleaning_pipeline_to_datagov_csv(self):
        """Tests that initial_cleaning_pipeline is called on the raw DataGov DataFrame."""
        mock_pipeline = MagicMock(return_value=DATAGOV_RAW_DF)

        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_WRANGLED_DF), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_WRANGLED_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv", return_value=DATAGOV_RAW_DF), \
             patch("src.data.loaders.data_loader.initial_cleaning_pipeline", mock_pipeline):
            load_food_insecurity_dataset()

        mock_pipeline.assert_called_once_with(DATAGOV_RAW_DF)

    def test_lga_parenthetical_suffix_is_stripped_before_counting(self):
        """Tests that 'Melbourne (City)' is reduced to 'Melbourne' so it can match
        food insecurity subpopulation values which have no parenthetical."""
        datagov_raw = pd.DataFrame({
            "lga": ["Melbourne (City)", "Melbourne (City)", "Yarra (City)"]
        })
        food_wrangled = pd.DataFrame({
            "subpopulation": ["Melbourne", "Yarra"],
            "indicator":     ["food", "food"],
            "estimate_pct":  [10.0, 15.0],
        })
        result = _run_food_loader(food_wrangled=food_wrangled, datagov_raw=datagov_raw)
        assert "Melbourne" in result["lga"].values
        assert not any("(" in str(v) for v in result["lga"].values)

    def test_lga_counts_aggregate_correctly(self):
        """Tests that emergency_services_count reflects the correct per-LGA frequency."""
        datagov_raw = pd.DataFrame({
            "lga": ["Melbourne (City)", "Melbourne (City)", "Yarra (City)"]
        })
        food_wrangled = pd.DataFrame({
            "subpopulation": ["Melbourne", "Yarra"],
            "indicator":     ["food", "food"],
            "estimate_pct":  [10.0, 15.0],
        })
        result = _run_food_loader(food_wrangled=food_wrangled, datagov_raw=datagov_raw)

        mel_count = result.loc[result["lga"] == "Melbourne", "emergency_services_count"].iloc[0]
        yar_count = result.loc[result["lga"] == "Yarra", "emergency_services_count"].iloc[0]
        assert mel_count == 2
        assert yar_count == 1

    def test_lga_name_with_no_parentheses_passes_through_unchanged(self):
        """Tests that an LGA name without parentheses is left unmodified."""
        datagov_raw = pd.DataFrame({"lga": ["No Parens"]})
        food_wrangled = pd.DataFrame({
            "subpopulation": ["No Parens"],
            "indicator":     ["food"],
            "estimate_pct":  [5.0],
        })
        result = _run_food_loader(food_wrangled=food_wrangled, datagov_raw=datagov_raw)
        assert "No Parens" in result["lga"].values

    # --- Merge behaviour -----------------------------------------------------

    def test_inner_join_drops_unmatched_food_insecurity_rows(self):
        """Tests that subpopulations with no matching LGA are excluded from the result.

        FOOD_WRANGLED_DF has 'No Match' which has no LGA counterpart in
        DATAGOV_RAW_DF — the inner join must drop it.
        """
        result = _run_food_loader()
        assert "No Match" not in result["subpopulation"].values

    def test_inner_join_retains_matched_rows(self):
        """Tests that subpopulations that do have a matching LGA are kept."""
        result = _run_food_loader()
        assert "Melbourne" in result["subpopulation"].values
        assert "Yarra" in result["subpopulation"].values

    def test_merged_row_count_equals_number_of_matched_subpopulations(self):
        """Tests that output row count equals matched pairs (3 food rows, 2 match → 2)."""
        result = _run_food_loader()
        assert len(result) == 2

    def test_empty_result_when_no_subpopulations_match_any_lga(self):
        """Tests that a completely non-overlapping join produces an empty DataFrame."""
        food_wrangled = pd.DataFrame({
            "subpopulation": ["No Match A", "No Match B"],
            "indicator":     ["food", "food"],
            "estimate_pct":  [1.0, 2.0],
        })
        result = _run_food_loader(food_wrangled=food_wrangled, datagov_raw=DATAGOV_RAW_DF)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_result_is_merged_not_just_wrangled_food_df(self):
        """Tests that the output is the merged DataFrame — not the raw wrangler output.

        This also documents the dead code bug: `return food_insecurity_df` after
        `return pd.merge(...)` is unreachable. The merge return always executes
        first, so the second return is dead code that should be removed.
        """
        result = _run_food_loader()
        # The merged result contains columns from both sides of the join
        assert "emergency_services_count" in result.columns   # only from lga_counts
        assert "estimate_pct" in result.columns               # only from food_insecurity_df

    # --- Error propagation ---------------------------------------------------

    def test_propagates_exception_on_missing_food_insecurity_file(self):
        """Tests that a FileNotFoundError on the Excel read propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_excel", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_food_insecurity_dataset()

    def test_propagates_exception_on_missing_datagov_csv(self):
        """Tests that a FileNotFoundError inside _get_lga_service_counts propagates up.

        _get_lga_service_counts has no try/except of its own — exceptions
        bubble through load_food_insecurity_dataset to the caller.
        """
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_WRANGLED_DF), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_WRANGLED_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_food_insecurity_dataset()


# ---------------------------------------------------------------------------
# load_vic_boundaries_dataset
# ---------------------------------------------------------------------------

class TestLoadVicBoundariesDataset:
    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF):
            result = load_vic_boundaries_dataset()
        assert isinstance(result, pd.DataFrame)

    def test_reads_from_correct_path(self):
        """Tests that the VIC boundaries CSV is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=VIC_DF) as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF):
            load_vic_boundaries_dataset()

        mock_read_csv.assert_called_once_with(settings.VICGOV_BOUNDARY_RAW_PATH)

    def test_uses_csv_reader_not_excel(self):
        """Tests that pd.read_csv is used (is_excel defaults to False)."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.pd.read_excel") as mock_excel, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF):
            load_vic_boundaries_dataset()

        mock_excel.assert_not_called()

    def test_passes_result_through_vic_boundaries_wrangler(self):
        """Tests that the raw DataFrame is passed to wrangle_vic_boundaries."""
        raw_df = VIC_DF.copy()
        wrangled_df = VIC_DF.copy()
        mock_wrangler = MagicMock(return_value=wrangled_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df), \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", mock_wrangler):
            result = load_vic_boundaries_dataset()

        mock_wrangler.assert_called_once_with(raw_df)
        assert result is wrangled_df

    def test_propagates_exception_on_missing_file(self):
        """Tests that a FileNotFoundError propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_vic_boundaries_dataset()


# ---------------------------------------------------------------------------
# load_viclga_boundaries_dataset
# ---------------------------------------------------------------------------

class TestLoadViclgaBoundariesDataset:
    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF):
            result = load_viclga_boundaries_dataset()
        assert isinstance(result, pd.DataFrame)

    def test_reads_from_correct_path(self):
        """Tests that the VIC LGA boundaries CSV is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=LGA_DF) as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF):
            load_viclga_boundaries_dataset()

        mock_read_csv.assert_called_once_with(settings.VICLGA_BOUNDARY_RAW_PATH)

    def test_uses_csv_reader_not_excel(self):
        """Tests that pd.read_csv is used (is_excel defaults to False)."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.pd.read_excel") as mock_excel, \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF):
            load_viclga_boundaries_dataset()

        mock_excel.assert_not_called()

    def test_passes_result_through_viclga_boundaries_wrangler(self):
        """Tests that the raw DataFrame is passed to wrangle_viclga_boundaries."""
        raw_df = LGA_DF.copy()
        wrangled_df = LGA_DF.copy()
        mock_wrangler = MagicMock(return_value=wrangled_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", mock_wrangler):
            result = load_viclga_boundaries_dataset()

        mock_wrangler.assert_called_once_with(raw_df)
        assert result is wrangled_df

    def test_propagates_exception_on_missing_file(self):
        """Tests that a FileNotFoundError propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_viclga_boundaries_dataset()

    def test_viclga_path_differs_from_vic_path(self):
        """Documents that VICLGA_BOUNDARY_RAW_PATH and VICGOV_BOUNDARY_RAW_PATH are
        distinct settings — the two boundary loaders must NOT share the same path."""
        assert settings.VICLGA_BOUNDARY_RAW_PATH != settings.VICGOV_BOUNDARY_RAW_PATH