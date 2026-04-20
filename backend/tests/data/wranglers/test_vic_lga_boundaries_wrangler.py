import pytest
import numpy as np
import pandas as pd

from src.data.wranglers.vic_lga_boundaries_wrangler import wrangle_viclga_boundaries


# ---------------------------------------------------------------------------
# Shared constants & helpers
# ---------------------------------------------------------------------------

# Column names as they arrive from the raw VIC LGA shapefile CSV
# (pre-pipeline, i.e. before standardize_columns runs).
RAW_COLUMNS = ["lg_ply_pid", "lga_pid", "abb_name", "geometry"]

# Expected output column names after the full pipeline.
EXPECTED_OUTPUT_COLS = ["lga_ply_pid", "lga_pid", "lga_name", "geometry"]

# Sample WKT geometry — geometry values should pass through unmodified since
# this pipeline does NOT reproject or parse geometry (unlike vic_boundaries_wrangler).
SAMPLE_GEOMETRY = (
    "POLYGON ((144.9 -37.8, 145.0 -37.8, "
    "145.0 -37.9, 144.9 -37.9, 144.9 -37.8))"
)


def make_raw_df(**overrides) -> pd.DataFrame:
    """
    Minimal single-row DataFrame matching the raw VIC LGA shapefile CSV schema.
    All defaults produce a row that survives the full pipeline.
    """
    row = {
        "lg_ply_pid": "VIC_LGA_1234",
        "lga_pid":    "LGA_PID_001",
        "abb_name":   "Melbourne",
        "geometry":   SAMPLE_GEOMETRY,
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# wrangle_viclga_boundaries (single-function pipeline)
# ---------------------------------------------------------------------------

class TestWrangleViclgaBoundaries:

    # --- Return type ---------------------------------------------------------

    def test_returns_dataframe(self):
        """Tests that the pipeline returns a DataFrame."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df)
        assert isinstance(result, pd.DataFrame)

    # --- Column renaming -----------------------------------------------------

    def test_renames_lg_ply_pid_to_lga_ply_pid(self):
        """Tests that 'lg_ply_pid' is renamed to 'lga_ply_pid'."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df)
        assert "lga_ply_pid" in result.columns
        assert "lg_ply_pid" not in result.columns

    def test_renames_abb_name_to_lga_name(self):
        """Tests that 'abb_name' is renamed to 'lga_name'."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df)
        assert "lga_name" in result.columns
        assert "abb_name" not in result.columns

    def test_lga_pid_is_preserved_unchanged(self):
        """Tests that 'lga_pid' passes through without renaming.

        This column is NOT in the column map — it must already be named
        'lga_pid' in the raw data for the pipeline to succeed. This test
        documents that implicit contract.
        """
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df)
        assert "lga_pid" in result.columns

    def test_geometry_column_is_preserved_unchanged(self):
        """Tests that 'geometry' passes through without renaming or modification."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df)
        assert "geometry" in result.columns

    # --- Column selection ----------------------------------------------------

    def test_output_has_exactly_the_expected_columns(self):
        """Tests that the output contains exactly the four expected columns."""
        df = make_raw_df()
        result = wrangle_viclga_boundaries(df)
        assert sorted(result.columns.tolist()) == sorted(EXPECTED_OUTPUT_COLS)

    def test_extra_columns_are_dropped(self):
        """Tests that columns outside the inclusion list are removed."""
        df = make_raw_df()
        df["unexpected_col"] = "should be dropped"
        df["another_extra"] = 42
        result = wrangle_viclga_boundaries(df)
        assert "unexpected_col" not in result.columns
        assert "another_extra" not in result.columns

    def test_raises_on_missing_lg_ply_pid(self):
        """Tests that a KeyError is raised when 'lg_ply_pid' is absent.

        After rename, 'lga_ply_pid' would be missing from the included cols,
        causing select_columns to raise.
        """
        df = make_raw_df().drop(columns=["lg_ply_pid"])
        with pytest.raises(KeyError):
            wrangle_viclga_boundaries(df)

    def test_raises_on_missing_lga_pid(self):
        """Tests that a KeyError is raised when 'lga_pid' is absent from the raw data.

        'lga_pid' is not in the rename map — it must arrive under this exact
        name (or be standardisable to it) for select_columns to succeed.
        """
        df = make_raw_df().drop(columns=["lga_pid"])
        with pytest.raises(KeyError):
            wrangle_viclga_boundaries(df)

    def test_raises_on_missing_abb_name(self):
        """Tests that a KeyError is raised when 'abb_name' is absent.

        Without 'abb_name', the rename to 'lga_name' never happens and
        select_columns will fail to find 'lga_name'.
        """
        df = make_raw_df().drop(columns=["abb_name"])
        with pytest.raises(KeyError):
            wrangle_viclga_boundaries(df)

    def test_raises_on_missing_geometry(self):
        """Tests that a KeyError is raised when 'geometry' is absent."""
        df = make_raw_df().drop(columns=["geometry"])
        with pytest.raises(KeyError):
            wrangle_viclga_boundaries(df)

    # --- Value correctness ---------------------------------------------------

    def test_lga_ply_pid_value_is_correct(self):
        """Tests that the renamed lga_ply_pid column carries the correct value."""
        df = make_raw_df(lg_ply_pid="VIC_LGA_9999")
        result = wrangle_viclga_boundaries(df)
        assert result["lga_ply_pid"].iloc[0] == "VIC_LGA_9999"

    def test_lga_name_value_is_correct(self):
        """Tests that the renamed lga_name column carries the correct value."""
        df = make_raw_df(abb_name="Ballarat")
        result = wrangle_viclga_boundaries(df)
        assert result["lga_name"].iloc[0] == "Ballarat"

    def test_lga_pid_value_is_correct(self):
        """Tests that lga_pid retains its original value end-to-end."""
        df = make_raw_df(lga_pid="LGA_PID_XYZ")
        result = wrangle_viclga_boundaries(df)
        assert result["lga_pid"].iloc[0] == "LGA_PID_XYZ"

    def test_geometry_value_is_preserved_exactly(self):
        """Tests that the geometry WKT string is passed through unmodified.

        Unlike vic_boundaries_wrangler, this pipeline does NOT reproject or
        parse geometry — the raw string should be identical in the output.
        """
        df = make_raw_df(geometry=SAMPLE_GEOMETRY)
        result = wrangle_viclga_boundaries(df)
        assert result["geometry"].iloc[0] == SAMPLE_GEOMETRY

    # --- Column standardisation (initial_cleaning_pipeline) -----------------

    def test_handles_uppercase_raw_column_names(self):
        """Tests that uppercase raw column names are standardised before renaming.

        initial_cleaning_pipeline calls standardize_columns which lowercases
        all column names, so the rename map keys must match the post-lowercase names.
        """
        df = make_raw_df()
        # Simulate uppercase headers as they might appear in some CSV exports
        df.columns = [c.upper() for c in df.columns]
        result = wrangle_viclga_boundaries(df)
        assert "lga_ply_pid" in result.columns
        assert "lga_name" in result.columns

    def test_strips_whitespace_from_string_values(self):
        """Tests that leading/trailing whitespace in cell values is stripped."""
        df = make_raw_df(abb_name="  Melbourne  ", lga_pid="  LGA_001  ")
        result = wrangle_viclga_boundaries(df)
        assert result["lga_name"].iloc[0] == "Melbourne"
        assert result["lga_pid"].iloc[0] == "LGA_001"

    # --- Sentinel / NA handling ---------------------------------------------

    def test_sentinel_values_are_not_converted_to_nan(self):
        """Tests that sentinel strings (N/A, NULL etc.) are NOT converted to NaN.

        clean_na_values is intentionally absent from this pipeline — boundary
        data does not need sentinel cleanup. This test documents that contract
        and will catch an unintended addition of clean_na_values in future.
        """
        df = make_raw_df(abb_name="N/A", lga_pid="NULL")
        result = wrangle_viclga_boundaries(df)
        assert result["lga_name"].iloc[0] == "N/A"
        assert result["lga_pid"].iloc[0] == "NULL"

    # --- Immutability --------------------------------------------------------

    def test_does_not_mutate_input_dataframe(self):
        """Tests that the original input DataFrame is not modified.

        initial_cleaning_pipeline calls df.copy() internally, so the input
        should be fully isolated from pipeline mutations.
        """
        df = make_raw_df()
        original_columns = list(df.columns)
        original_name = df["abb_name"].iloc[0]
        wrangle_viclga_boundaries(df)
        assert list(df.columns) == original_columns
        assert df["abb_name"].iloc[0] == original_name

    # --- Multiple rows -------------------------------------------------------

    def test_handles_multiple_rows(self):
        """Tests that the pipeline processes all rows, not just the first."""
        df = pd.DataFrame([
            {"lg_ply_pid": "PID_1", "lga_pid": "LPID_1", "abb_name": "Melbourne", "geometry": SAMPLE_GEOMETRY},
            {"lg_ply_pid": "PID_2", "lga_pid": "LPID_2", "abb_name": "Ballarat",  "geometry": SAMPLE_GEOMETRY},
            {"lg_ply_pid": "PID_3", "lga_pid": "LPID_3", "abb_name": "Geelong",   "geometry": SAMPLE_GEOMETRY},
        ])
        result = wrangle_viclga_boundaries(df)
        assert len(result) == 3
        assert list(result["lga_name"]) == ["Melbourne", "Ballarat", "Geelong"]

    def test_empty_dataframe_with_correct_columns_returns_empty(self):
        """Tests that an empty DataFrame with the right columns returns empty output."""
        df = pd.DataFrame(columns=RAW_COLUMNS)
        result = wrangle_viclga_boundaries(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert sorted(result.columns.tolist()) == sorted(EXPECTED_OUTPUT_COLS)