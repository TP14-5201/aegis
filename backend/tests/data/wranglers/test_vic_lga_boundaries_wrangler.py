import pytest
import numpy as np
import pandas as pd

from src.data.wranglers.vic_lga_boundaries_wrangler import (
    clean_lga_names,
    take_latest_lga_boundaries,
    wrangle_viclga_boundaries,
)


# ---------------------------------------------------------------------------
# Shared constants & helpers
# ---------------------------------------------------------------------------

# Column names as they arrive from the raw VIC LGA shapefile CSV.
# abb_name is the abbreviated name used for deduplication, cleaned, then
# renamed to lga_name. dt_create is used to pick the latest record per region.
RAW_COLUMNS = ["lg_ply_pid", "abb_name", "dt_create", "geometry"]

# Expected output column names after the full pipeline.
# lga_name comes from renaming abb_name.
# lga_pid is joined in from df_population via add_lga_pid_from_lga_population_data.
# geometry passes through unmodified.
EXPECTED_OUTPUT_COLS = ["lga_name", "geometry", "lga_pid"]

SAMPLE_GEOMETRY = (
    "POLYGON ((144.9 -37.8, 145.0 -37.8, "
    "145.0 -37.9, 144.9 -37.9, 144.9 -37.8))"
)


def make_raw_df(**overrides) -> pd.DataFrame:
    """
    Minimal single-row DataFrame matching the raw VIC LGA shapefile CSV schema.

    Note: lga_pid is NOT present in the raw data — it is joined in from the
    population DataFrame. The lg_ply_pid column is renamed then dropped.
    """
    row = {
        "lg_ply_pid": "VIC_LGA_1234",
        "abb_name":   "Melbourne",
        "dt_create":  "2023-01-01",
        "geometry":   SAMPLE_GEOMETRY,
    }
    row.update(overrides)
    return pd.DataFrame([row])


def make_population_df(rows: list[dict] | None = None) -> pd.DataFrame:
    """
    Minimal population DataFrame for add_lga_pid_from_lga_population_data.
    Requires lga_pid and lga_name columns.
    """
    if rows is None:
        rows = [{"lga_pid": "LGA_PID_001", "lga_name": "Melbourne"}]
    return pd.DataFrame(rows)


def make_boundary_df(rows: list[dict] | None = None) -> pd.DataFrame:
    """Minimal DataFrame for take_latest_lga_boundaries unit tests."""
    if rows is None:
        rows = [{"abb_name": "Melbourne", "dt_create": "2023-01-01", "geometry": SAMPLE_GEOMETRY}]
    return pd.DataFrame(rows)


def make_lga_name_df(rows: list[dict] | None = None) -> pd.DataFrame:
    """Minimal DataFrame for clean_lga_names unit tests."""
    if rows is None:
        rows = [{"abb_name": "Melbourne"}]
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# take_latest_lga_boundaries
# ---------------------------------------------------------------------------

class TestTakeLatestLgaBoundaries:

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_boundary_df()
        result = take_latest_lga_boundaries(df)
        assert isinstance(result, pd.DataFrame)

    def test_single_row_passes_through(self):
        """Tests that a single-row DataFrame is returned with one row."""
        df = make_boundary_df()
        result = take_latest_lga_boundaries(df)
        assert len(result) == 1

    def test_keeps_latest_record_per_abb_name(self):
        """Tests that the most recent row is retained when duplicate abb_names exist."""
        df = make_boundary_df([
            {"abb_name": "Melbourne", "dt_create": "2021-01-01", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Melbourne", "dt_create": "2023-06-15", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Melbourne", "dt_create": "2019-12-31", "geometry": SAMPLE_GEOMETRY},
        ])
        result = take_latest_lga_boundaries(df)
        assert len(result) == 1
        assert pd.to_datetime(result["dt_create"].iloc[0]) == pd.Timestamp("2023-06-15")

    def test_keeps_all_unique_abb_names(self):
        """Tests that one row per unique abb_name is retained."""
        df = make_boundary_df([
            {"abb_name": "Melbourne", "dt_create": "2023-01-01", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Ballarat",  "dt_create": "2022-06-01", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Geelong",   "dt_create": "2021-03-15", "geometry": SAMPLE_GEOMETRY},
        ])
        result = take_latest_lga_boundaries(df)
        assert len(result) == 3
        assert set(result["abb_name"].tolist()) == {"Melbourne", "Ballarat", "Geelong"}

    def test_deduplicates_mixed_regions_keeping_latest_per_region(self):
        """Tests that each abb_name independently retains its own latest row."""
        df = make_boundary_df([
            {"abb_name": "Melbourne", "dt_create": "2020-01-01", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Melbourne", "dt_create": "2023-06-15", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Ballarat",  "dt_create": "2022-01-01", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Ballarat",  "dt_create": "2019-05-10", "geometry": SAMPLE_GEOMETRY},
        ])
        result = take_latest_lga_boundaries(df)
        assert len(result) == 2
        melb_row = result[result["abb_name"] == "Melbourne"]
        ball_row = result[result["abb_name"] == "Ballarat"]
        assert pd.to_datetime(melb_row["dt_create"].iloc[0]) == pd.Timestamp("2023-06-15")
        assert pd.to_datetime(ball_row["dt_create"].iloc[0]) == pd.Timestamp("2022-01-01")

    def test_dt_create_is_parsed_as_datetime(self):
        """Tests that dt_create is converted to datetime dtype for correct sorting."""
        df = make_boundary_df()
        result = take_latest_lga_boundaries(df)
        assert pd.api.types.is_datetime64_any_dtype(result["dt_create"])

    def test_string_dates_compared_correctly(self):
        """Tests that lexicographically-ambiguous string dates are compared as timestamps."""
        df = make_boundary_df([
            {"abb_name": "Melbourne", "dt_create": "2020-09-01", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Melbourne", "dt_create": "2020-10-01", "geometry": SAMPLE_GEOMETRY},
        ])
        result = take_latest_lga_boundaries(df)
        assert pd.to_datetime(result["dt_create"].iloc[0]) == pd.Timestamp("2020-10-01")

    def test_index_is_reset_after_deduplication(self):
        """Tests that the index is reset to a standard RangeIndex after dedup."""
        df = make_boundary_df([
            {"abb_name": "Melbourne", "dt_create": "2020-01-01", "geometry": SAMPLE_GEOMETRY},
            {"abb_name": "Melbourne", "dt_create": "2023-06-15", "geometry": SAMPLE_GEOMETRY},
        ])
        result = take_latest_lga_boundaries(df)
        assert list(result.index) == list(range(len(result)))
        assert result.index[0] == 0

    def test_other_columns_are_preserved(self):
        """Tests that columns other than abb_name and dt_create are intact."""
        df = make_boundary_df([
            {"abb_name": "Melbourne", "dt_create": "2023-01-01", "geometry": SAMPLE_GEOMETRY},
        ])
        result = take_latest_lga_boundaries(df)
        assert "geometry" in result.columns
        assert result["geometry"].iloc[0] == SAMPLE_GEOMETRY


# ---------------------------------------------------------------------------
# clean_lga_names
# ---------------------------------------------------------------------------

class TestCleanLgaNames:

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_lga_name_df()
        result = clean_lga_names(df)
        assert isinstance(result, pd.DataFrame)

    def test_removes_uninc_postfix(self):
        """Tests that the '(Uninc)' postfix is stripped from abb_name."""
        df = make_lga_name_df([{"abb_name": "Mildura (Uninc)"}])
        result = clean_lga_names(df)
        assert result["abb_name"].iloc[0] == "Mildura"

    def test_removes_any_parenthetical_postfix(self):
        """Tests that any text in parentheses at the end of abb_name is removed."""
        df = make_lga_name_df([{"abb_name": "Some LGA (Other)"}])
        result = clean_lga_names(df)
        assert result["abb_name"].iloc[0] == "Some LGA"

    def test_names_without_postfix_are_unchanged(self):
        """Tests that names with no parenthetical suffix pass through unmodified."""
        df = make_lga_name_df([{"abb_name": "Melbourne"}])
        result = clean_lga_names(df)
        assert result["abb_name"].iloc[0] == "Melbourne"

    def test_strips_trailing_whitespace_after_removal(self):
        """Tests that any whitespace left after removing the postfix is stripped."""
        df = make_lga_name_df([{"abb_name": "Mildura   (Uninc)"}])
        result = clean_lga_names(df)
        assert result["abb_name"].iloc[0] == "Mildura"

    def test_handles_multiple_rows(self):
        """Tests that cleaning is applied to every row."""
        df = make_lga_name_df([
            {"abb_name": "Mildura (Uninc)"},
            {"abb_name": "Melbourne"},
            {"abb_name": "Ballarat (Uninc)"},
        ])
        result = clean_lga_names(df)
        assert result["abb_name"].tolist() == ["Mildura", "Melbourne", "Ballarat"]

    def test_other_columns_are_not_affected(self):
        """Tests that columns other than abb_name are untouched."""
        df = pd.DataFrame([{
            "abb_name": "Mildura (Uninc)",
            "geometry": SAMPLE_GEOMETRY,
        }])
        result = clean_lga_names(df)
        assert result["geometry"].iloc[0] == SAMPLE_GEOMETRY


# ---------------------------------------------------------------------------
# wrangle_viclga_boundaries (single-function pipeline)
# ---------------------------------------------------------------------------

class TestWrangleViclgaBoundaries:
    """
    wrangle_viclga_boundaries(df, df_population) requires TWO arguments.

    Pipeline changes vs old version:
    - VICLGA_COLUMN_MAP now maps abb_name -> lga_name (and lga_name -> lga_name_full
      which is then dropped by select_columns).
    - VICLGA_INCLUED_COLS is ["lga_name", "geometry"] — lga_pid is NOT in the raw data.
    - add_lga_pid_from_lga_population_data joins lga_pid from df_population after select.
    - Rows with no matching lga_pid in the population DF are dropped.
    """

    # --- Return type ---------------------------------------------------------

    def test_returns_dataframe(self):
        """Tests that the pipeline returns a DataFrame."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert isinstance(result, pd.DataFrame)

    # --- Column renaming -----------------------------------------------------

    def test_renames_abb_name_to_lga_name(self):
        """Tests that 'abb_name' is renamed to 'lga_name'."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert "lga_name" in result.columns
        assert "abb_name" not in result.columns

    def test_geometry_column_is_preserved(self):
        """Tests that 'geometry' passes through without renaming."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert "geometry" in result.columns

    def test_lga_pid_present_after_population_join(self):
        """Tests that lga_pid is present in output, sourced from df_population join."""
        df = make_raw_df(abb_name="Melbourne")
        pop = make_population_df([{"lga_pid": "LGA_PID_001", "lga_name": "Melbourne"}])
        result = wrangle_viclga_boundaries(df, pop)
        assert "lga_pid" in result.columns
        assert result["lga_pid"].iloc[0] == "LGA_PID_001"

    def test_lg_ply_pid_not_in_output(self):
        """Tests that 'lg_ply_pid' is absent from the output."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert "lg_ply_pid" not in result.columns

    # --- Column selection ----------------------------------------------------

    def test_output_has_exactly_the_expected_columns(self):
        """Tests that the output contains exactly the three expected columns."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert sorted(result.columns.tolist()) == sorted(EXPECTED_OUTPUT_COLS)

    def test_extra_columns_are_dropped(self):
        """Tests that columns outside the inclusion list are removed."""
        df = make_raw_df()
        df["unexpected_col"] = "should be dropped"
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert "unexpected_col" not in result.columns

    def test_raises_on_missing_abb_name(self):
        """Tests that an error is raised when 'abb_name' is absent."""
        df = make_raw_df().drop(columns=["abb_name"])
        with pytest.raises(KeyError):
            wrangle_viclga_boundaries(df, make_population_df())

    def test_raises_on_missing_geometry(self):
        """Tests that a KeyError is raised when 'geometry' is absent."""
        df = make_raw_df().drop(columns=["geometry"])
        with pytest.raises(KeyError):
            wrangle_viclga_boundaries(df, make_population_df())

    def test_raises_on_missing_dt_create(self):
        """Tests that a KeyError is raised when 'dt_create' is absent."""
        df = make_raw_df().drop(columns=["dt_create"])
        with pytest.raises(KeyError):
            wrangle_viclga_boundaries(df, make_population_df())

    # --- Value correctness ---------------------------------------------------

    def test_lga_name_value_is_correct(self):
        """Tests that the renamed lga_name column carries the correct value."""
        df = make_raw_df(abb_name="Ballarat")
        pop = make_population_df([{"lga_pid": "LGA_PID_BAL", "lga_name": "Ballarat"}])
        result = wrangle_viclga_boundaries(df, pop)
        assert result["lga_name"].iloc[0] == "Ballarat"

    def test_geometry_value_is_preserved_exactly(self):
        """Tests that the geometry WKT string is passed through unmodified."""
        df = make_raw_df(geometry=SAMPLE_GEOMETRY)
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert result["geometry"].iloc[0] == SAMPLE_GEOMETRY

    # --- Population join (lga_pid) -------------------------------------------

    def test_rows_without_matching_population_entry_are_dropped(self):
        """Tests that rows with no lga_pid match in population DF are removed."""
        df = make_raw_df(abb_name="Unmatched Region")
        pop = make_population_df([{"lga_pid": "LGA_PID_001", "lga_name": "Melbourne"}])
        result = wrangle_viclga_boundaries(df, pop)
        assert len(result) == 0

    # --- Deduplication -------------------------------------------------------

    def test_deduplicates_to_one_row_per_abb_name(self):
        """Tests that duplicate abb_names are collapsed to the most recent row."""
        df = pd.DataFrame([
            {"lg_ply_pid": "PID_1", "abb_name": "Melbourne", "dt_create": "2020-01-01", "geometry": SAMPLE_GEOMETRY},
            {"lg_ply_pid": "PID_2", "abb_name": "Melbourne", "dt_create": "2023-06-15", "geometry": SAMPLE_GEOMETRY},
            {"lg_ply_pid": "PID_3", "abb_name": "Ballarat",  "dt_create": "2022-03-10", "geometry": SAMPLE_GEOMETRY},
        ])
        pop = make_population_df([
            {"lga_pid": "LGA_PID_MEL", "lga_name": "Melbourne"},
            {"lga_pid": "LGA_PID_BAL", "lga_name": "Ballarat"},
        ])
        result = wrangle_viclga_boundaries(df, pop)
        assert len(result) == 2

    # --- Name cleaning -------------------------------------------------------

    def test_uninc_postfix_is_stripped_from_lga_name(self):
        """Tests that the '(Uninc)' postfix is removed from abb_name end-to-end."""
        df = make_raw_df(abb_name="Mildura (Uninc)")
        pop = make_population_df([{"lga_pid": "LGA_PID_MIL", "lga_name": "Mildura"}])
        result = wrangle_viclga_boundaries(df, pop)
        assert result["lga_name"].iloc[0] == "Mildura"

    # --- Column standardisation ----------------------------------------------

    def test_handles_uppercase_raw_column_names(self):
        """Tests that uppercase raw column names are standardised before processing."""
        df = make_raw_df()
        df.columns = [c.upper() for c in df.columns]
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert "lga_name" in result.columns
        assert "geometry" in result.columns

    def test_strips_whitespace_from_string_values(self):
        """Tests that leading/trailing whitespace in cell values is stripped."""
        df = make_raw_df(abb_name="  Melbourne  ")
        pop = make_population_df([{"lga_pid": "LGA_PID_001", "lga_name": "Melbourne"}])
        result = wrangle_viclga_boundaries(df, pop)
        assert result["lga_name"].iloc[0] == "Melbourne"

    # --- Immutability --------------------------------------------------------

    def test_does_not_mutate_input_dataframe(self):
        """Tests that the original input DataFrame is not modified."""
        df = make_raw_df()
        original_columns = list(df.columns)
        original_name = df["abb_name"].iloc[0]
        wrangle_viclga_boundaries(df, make_population_df())
        assert list(df.columns) == original_columns
        assert df["abb_name"].iloc[0] == original_name

    # --- Multiple rows -------------------------------------------------------

    def test_handles_multiple_rows(self):
        """Tests that the pipeline processes all rows, not just the first."""
        df = pd.DataFrame([
            {"lg_ply_pid": "PID_1", "abb_name": "Melbourne", "dt_create": "2023-01-01", "geometry": SAMPLE_GEOMETRY},
            {"lg_ply_pid": "PID_2", "abb_name": "Ballarat",  "dt_create": "2022-06-01", "geometry": SAMPLE_GEOMETRY},
            {"lg_ply_pid": "PID_3", "abb_name": "Geelong",   "dt_create": "2021-03-15", "geometry": SAMPLE_GEOMETRY},
        ])
        pop = make_population_df([
            {"lga_pid": "LGA_PID_MEL", "lga_name": "Melbourne"},
            {"lga_pid": "LGA_PID_BAL", "lga_name": "Ballarat"},
            {"lga_pid": "LGA_PID_GEE", "lga_name": "Geelong"},
        ])
        result = wrangle_viclga_boundaries(df, pop)
        assert len(result) == 3
        assert set(result["lga_name"]) == {"Melbourne", "Ballarat", "Geelong"}

    def test_empty_dataframe_with_correct_columns_returns_empty(self):
        """Tests that an empty DataFrame with the right columns returns empty output."""
        df = pd.DataFrame(columns=RAW_COLUMNS)
        result = wrangle_viclga_boundaries(df, make_population_df())
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0