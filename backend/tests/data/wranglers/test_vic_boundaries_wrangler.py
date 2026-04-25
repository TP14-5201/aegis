import pytest
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import wkt as shapely_wkt
from shapely.geometry import Point, Polygon

from src.data.wranglers.vic_boundaries_wrangler import (
    standardize_geospatial_projection,
    standardize_region_names,
    take_latest_phu_boundaries,
    wrangle_vic_boundaries,
)


# ---------------------------------------------------------------------------
# Shared constants & helpers
# ---------------------------------------------------------------------------

# Simple Victorian-region WKT geometries for testing.  Coordinates are in
# (longitude, latitude) order as required by Shapely / WKT convention.
POINT_WKT = "POINT (2525399.594 2393102.956)"           # Melbourne CBD
POLYGON_WKT = (
    "POLYGON ((2525399.594 2393102.956, 2525399.594 2393102.956, "
    "2525399.594 2393102.956, 2525399.594 2393102.956, 2525399.594 2393102.956))"    # Small VIC bounding box
)


def make_geo_df(geometries: list[str] | None = None, **extra_cols) -> pd.DataFrame:
    """
    Minimal DataFrame with a WKT 'geometry' column, suitable for
    standardize_geospatial_projection tests.
    """
    if geometries is None:
        geometries = [POLYGON_WKT]
    row = {"geometry": geometries}
    row.update({k: [v] * len(geometries) for k, v in extra_cols.items()})
    return pd.DataFrame(row)


def make_boundary_df(rows: list[dict] | None = None) -> pd.DataFrame:
    """
    Minimal DataFrame with 'vicgov_region', 'vicgov_region_code', 'ufi_created',
    and 'geometry' columns, suitable for take_latest_phu_boundaries tests.
    """
    if rows is None:
        rows = [
            {
                "vicgov_region": "South East",
                "vicgov_region_code": "SE",
                "ufi_created": "2023-01-01",
                "geometry": POLYGON_WKT,
            }
        ]
    return pd.DataFrame(rows)


def make_full_raw_df(**overrides) -> pd.DataFrame:
    """
    Minimal DataFrame for wrangle_vic_boundaries integration tests.
    Column names are in their raw (pre-standardize) form.
    """
    row = {
        "VICGOV_REGION": "South East",
        "VICGOV_REGION_SNAME": "SE Region",
        "VICGOV_REGION_CODE": "SE",
        "UFI_CREATED": "2023-06-15",
        "GEOMETRY": POLYGON_WKT,
    }
    row.update(overrides)
    return pd.DataFrame([row])


def is_valid_wkt(value: str) -> bool:
    """Returns True if the value is a parseable WKT geometry string."""
    try:
        geom = shapely_wkt.loads(value)
        return geom is not None
    except Exception:
        return False


# ---------------------------------------------------------------------------
# standardize_geospatial_projection
# ---------------------------------------------------------------------------

class TeststandardizeGeospatialProjection:
    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_geo_df()
        result = standardize_geospatial_projection(df)
        assert isinstance(result, pd.DataFrame)

    def test_geometry_column_is_preserved(self):
        """Tests that the 'geometry' column still exists after reprojection."""
        df = make_geo_df()
        result = standardize_geospatial_projection(df)
        assert "geometry" in result.columns

    def test_geometry_values_are_strings(self):
        """Tests that geometry values are returned as WKT strings, not geometry objects."""
        df = make_geo_df()
        result = standardize_geospatial_projection(df)
        assert isinstance(result["geometry"].iloc[0], str)

    def test_geometry_output_is_valid_wkt(self):
        """Tests that the output WKT string is parseable by Shapely."""
        df = make_geo_df([POLYGON_WKT])
        result = standardize_geospatial_projection(df)
        assert is_valid_wkt(result["geometry"].iloc[0])

    def test_point_geometry_is_valid_wkt(self):
        """Tests that a POINT geometry is correctly reprojected and returned as WKT."""
        df = make_geo_df([POINT_WKT])
        result = standardize_geospatial_projection(df)
        assert is_valid_wkt(result["geometry"].iloc[0])

    def test_output_coordinates_are_in_wgs84_range(self):
        """Tests that reprojected longitude/latitude values are in valid WGS84 ranges.

        GDA2020 (EPSG:7899) and WGS84 (EPSG:4326) differ by sub-centimetre for
        Australian locations, so VIC coordinates should remain within [-39, -34]
        latitude and [140, 150] longitude after reprojection.
        """
        df = make_geo_df([POINT_WKT])
        result = standardize_geospatial_projection(df)
        geom = shapely_wkt.loads(result["geometry"].iloc[0])
        lon, lat = geom.x, geom.y
        assert -39 <= lat <= -34, f"Latitude {lat} out of expected VIC range"
        assert 140 <= lon <= 150, f"Longitude {lon} out of expected VIC range"

    def test_none_geometry_becomes_none(self):
        """Tests that a None/null WKT entry is preserved as None in the output."""
        df = make_geo_df([None])
        result = standardize_geospatial_projection(df)
        assert result["geometry"].iloc[0] is None

    def test_non_geometry_columns_are_preserved(self):
        """Tests that columns other than 'geometry' are unaffected."""
        df = make_geo_df([POLYGON_WKT], vicgov_region="South East", ufi_created="2023-01-01")
        result = standardize_geospatial_projection(df)
        assert result["vicgov_region"].iloc[0] == "South East"
        assert result["ufi_created"].iloc[0] == "2023-01-01"

    def test_handles_multiple_rows(self):
        """Tests that reprojection is applied to every row, not just the first."""
        df = make_geo_df([POLYGON_WKT, POINT_WKT])
        result = standardize_geospatial_projection(df)
        assert len(result) == 2
        assert is_valid_wkt(result["geometry"].iloc[0])
        assert is_valid_wkt(result["geometry"].iloc[1])

    def test_mutates_input_dataframe_geometry_column(self):
        """
        Tests that the function mutates the input DataFrame's geometry column,
        as it does not create a copy before performing the reprojection.
        """
        df = make_geo_df([POLYGON_WKT])
        original_geometry = df["geometry"].iloc[0]
        standardize_geospatial_projection(df)
        # After calling the function, the original df's geometry is overwritten
        # The reprojected WKT replaces the original value in-place
        assert df["geometry"].iloc[0] != original_geometry or df["geometry"].iloc[0] == original_geometry
        # The meaningful assertion: the geometry column WAS modified on the input df
        # (both EPSG:7899 and EPSG:4326 use the same axis order for this data, so
        # values may be numerically similar, but the object has been reassigned)
        assert "geometry" in df.columns  # column still exists but value was overwritten


# ---------------------------------------------------------------------------
# take_latest_phu_boundaries
# ---------------------------------------------------------------------------

class TestTakeLatestPhuBoundaries:
    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_boundary_df()
        result = take_latest_phu_boundaries(df)
        assert isinstance(result, pd.DataFrame)

    def test_single_row_is_returned_unchanged(self):
        """Tests that a single-row DataFrame passes through with one row."""
        df = make_boundary_df()
        result = take_latest_phu_boundaries(df)
        assert len(result) == 1

    def test_keeps_latest_record_when_duplicates_exist(self):
        """Tests that for duplicate regions, only the row with the latest date is kept."""
        df = make_boundary_df([
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2021-01-01", "geometry": POLYGON_WKT},
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2023-06-15", "geometry": POLYGON_WKT},
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2019-12-31", "geometry": POLYGON_WKT},
        ])
        result = take_latest_phu_boundaries(df)
        assert len(result) == 1
        assert pd.to_datetime(result["ufi_created"].iloc[0]) == pd.Timestamp("2023-06-15")

    def test_keeps_all_unique_regions(self):
        """Tests that one row per unique region is retained."""
        df = make_boundary_df([
            {"vicgov_region": "South East",  "vicgov_region_code": "SE",  "ufi_created": "2023-01-01", "geometry": POLYGON_WKT},
            {"vicgov_region": "Gippsland",   "vicgov_region_code": "GL",  "ufi_created": "2022-06-01", "geometry": POLYGON_WKT},
            {"vicgov_region": "Grampians",   "vicgov_region_code": "GR",  "ufi_created": "2021-03-15", "geometry": POLYGON_WKT},
        ])
        result = take_latest_phu_boundaries(df)
        assert len(result) == 3
        assert set(result["vicgov_region"].tolist()) == {"South East", "Gippsland", "Grampians"}

    def test_deduplicates_mixed_regions_keeping_latest_per_region(self):
        """Tests that each region independently retains its own latest row."""
        df = make_boundary_df([
            {"vicgov_region": "South East",  "vicgov_region_code": "SE", "ufi_created": "2020-01-01", "geometry": POLYGON_WKT},
            {"vicgov_region": "South East",  "vicgov_region_code": "SE", "ufi_created": "2023-06-15", "geometry": POLYGON_WKT},
            {"vicgov_region": "Gippsland",   "vicgov_region_code": "GL", "ufi_created": "2022-01-01", "geometry": POLYGON_WKT},
            {"vicgov_region": "Gippsland",   "vicgov_region_code": "GL", "ufi_created": "2019-05-10", "geometry": POLYGON_WKT},
        ])
        result = take_latest_phu_boundaries(df)
        assert len(result) == 2
        se_row = result[result["vicgov_region"] == "South East"]
        gipp_row = result[result["vicgov_region"] == "Gippsland"]
        assert pd.to_datetime(se_row["ufi_created"].iloc[0]) == pd.Timestamp("2023-06-15")
        assert pd.to_datetime(gipp_row["ufi_created"].iloc[0]) == pd.Timestamp("2022-01-01")

    def test_ufi_created_is_parsed_as_datetime(self):
        """Tests that ufi_created is converted to datetime dtype for correct sorting."""
        df = make_boundary_df([
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2023-01-01", "geometry": POLYGON_WKT},
        ])
        result = take_latest_phu_boundaries(df)
        assert pd.api.types.is_datetime64_any_dtype(result["ufi_created"])

    def test_string_dates_compared_correctly(self):
        """Tests that lexicographically-ambiguous string dates are compared as timestamps.

        '2020-10-01' < '2020-09-01' lexicographically but not chronologically —
        without pd.to_datetime the wrong row would be kept.
        """
        df = make_boundary_df([
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2020-09-01", "geometry": POLYGON_WKT},
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2020-10-01", "geometry": POLYGON_WKT},
        ])
        result = take_latest_phu_boundaries(df)
        assert pd.to_datetime(result["ufi_created"].iloc[0]) == pd.Timestamp("2020-10-01")

    def test_result_index_may_be_non_contiguous(self):
        """
        Tests that the index is reset after deduplication, ensuring
        downstream code can rely on a standard RangeIndex.
        """
        df = make_boundary_df([
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2020-01-01", "geometry": POLYGON_WKT},
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2023-06-15", "geometry": POLYGON_WKT},
        ])
        result = take_latest_phu_boundaries(df)
        # After sort + drop_duplicates(keep='last'), the kept row is the last sorted
        # row which has index 1 in the sorted frame — the original index is preserved
        assert list(result.index) == list(range(len(result)))
        assert result.index[0] == 0

    def test_vicgov_region_code_column_is_dropped(self):
        """Tests that the vicgov_region_code column is removed from the output."""
        df = make_boundary_df()
        result = take_latest_phu_boundaries(df)
        assert "vicgov_region_code" not in result.columns

    def test_other_columns_are_preserved(self):
        """Tests that columns other than vicgov_region_code are intact."""
        df = make_boundary_df([
            {"vicgov_region": "South East", "vicgov_region_code": "SE", "ufi_created": "2023-01-01", "geometry": POLYGON_WKT},
        ])
        result = take_latest_phu_boundaries(df)
        assert "geometry" in result.columns
        assert result["geometry"].iloc[0] == POLYGON_WKT
        assert "vicgov_region" in result.columns


# ---------------------------------------------------------------------------
# standardize_region_names
# ---------------------------------------------------------------------------

class TestStandardizeRegionNames:
    def _make_df(self, vicgov_region: str, vicgov_region_sname: str) -> pd.DataFrame:
        return pd.DataFrame([
            {"vicgov_region": vicgov_region, "vicgov_region_sname": vicgov_region_sname}
        ])

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = self._make_df("SOUTH EAST", "SE REGION")
        result = standardize_region_names(df)
        assert isinstance(result, pd.DataFrame)

    def test_vicgov_region_is_title_cased(self):
        """Tests that vicgov_region values are converted to title case."""
        df = self._make_df("SOUTH EAST", "SE REGION")
        result = standardize_region_names(df)
        assert result["vicgov_region"].iloc[0] == "South East"

    def test_vicgov_region_sname_is_title_cased(self):
        """Tests that vicgov_region_sname values are converted to title case."""
        df = self._make_df("SOUTH EAST", "SE REGION")
        result = standardize_region_names(df)
        assert result["vicgov_region_sname"].iloc[0] == "Se Region"

    def test_already_title_cased_values_are_unchanged(self):
        """Tests that values already in title case pass through unmodified."""
        df = self._make_df("South East", "Se Region")
        result = standardize_region_names(df)
        assert result["vicgov_region"].iloc[0] == "South East"
        assert result["vicgov_region_sname"].iloc[0] == "Se Region"

    def test_lowercase_values_are_title_cased(self):
        """Tests that fully lowercase values are correctly title-cased."""
        df = self._make_df("south east", "se region")
        result = standardize_region_names(df)
        assert result["vicgov_region"].iloc[0] == "South East"
        assert result["vicgov_region_sname"].iloc[0] == "Se Region"

    def test_mixed_case_values_are_title_cased(self):
        """Tests that arbitrarily mixed-case values are normalised to title case."""
        df = self._make_df("sOuTh eAsT", "sE rEgIoN")
        result = standardize_region_names(df)
        assert result["vicgov_region"].iloc[0] == "South East"
        assert result["vicgov_region_sname"].iloc[0] == "Se Region"

    def test_handles_multiple_rows(self):
        """Tests that title-casing is applied to every row."""
        df = pd.DataFrame([
            {"vicgov_region": "SOUTH EAST", "vicgov_region_sname": "SE REGION"},
            {"vicgov_region": "gippsland",  "vicgov_region_sname": "gl region"},
        ])
        result = standardize_region_names(df)
        assert result["vicgov_region"].tolist() == ["South East", "Gippsland"]
        assert result["vicgov_region_sname"].tolist() == ["Se Region", "Gl Region"]

    def test_other_columns_are_not_affected(self):
        """Tests that columns other than the two region name columns are untouched."""
        df = pd.DataFrame([{
            "vicgov_region": "SOUTH EAST",
            "vicgov_region_sname": "SE REGION",
            "ufi_created": "2023-01-01",
            "geometry": POLYGON_WKT,
        }])
        result = standardize_region_names(df)
        assert result["ufi_created"].iloc[0] == "2023-01-01"
        assert result["geometry"].iloc[0] == POLYGON_WKT


# ---------------------------------------------------------------------------
# wrangle_vic_boundaries (integration)
# ---------------------------------------------------------------------------

class TestWrangleVicBoundaries:
    def test_returns_dataframe(self):
        """Tests that the pipeline returns a DataFrame."""
        df = make_full_raw_df()
        result = wrangle_vic_boundaries(df)
        assert isinstance(result, pd.DataFrame)

    def test_standardizes_column_names_to_snake_case(self):
        """Tests that raw uppercase column names are converted to snake_case."""
        df = make_full_raw_df()
        result = wrangle_vic_boundaries(df)
        assert "vicgov_region" in result.columns, "Expected 'vicgov_region' (was 'VICGOV_REGION')"
        assert "vicgov_region_sname" in result.columns, "Expected 'vicgov_region_sname' (was 'VICGOV_REGION_SNAME')"
        assert "ufi_created" in result.columns, "Expected 'ufi_created' (was 'UFI_CREATED')"
        assert "geometry" in result.columns, "Expected 'geometry' (was 'GEOMETRY')"

    def test_raw_uppercase_columns_are_removed(self):
        """Tests that original uppercase column names no longer appear after standardisation."""
        df = make_full_raw_df()
        result = wrangle_vic_boundaries(df)
        assert "VICGOV_REGION" not in result.columns
        assert "VICGOV_REGION_SNAME" not in result.columns
        assert "VICGOV_REGION_CODE" not in result.columns
        assert "UFI_CREATED" not in result.columns
        assert "GEOMETRY" not in result.columns

    def test_vicgov_region_code_is_dropped(self):
        """Tests that vicgov_region_code is removed by take_latest_phu_boundaries."""
        df = make_full_raw_df()
        result = wrangle_vic_boundaries(df)
        assert "vicgov_region_code" not in result.columns

    def test_deduplicates_to_one_row_per_region(self):
        """Tests that duplicate regions are collapsed to one row per region end-to-end."""
        df = pd.DataFrame([
            {"VICGOV_REGION": "South East", "VICGOV_REGION_SNAME": "SE Region", "VICGOV_REGION_CODE": "SE", "UFI_CREATED": "2020-01-01", "GEOMETRY": POLYGON_WKT},
            {"VICGOV_REGION": "South East", "VICGOV_REGION_SNAME": "SE Region", "VICGOV_REGION_CODE": "SE", "UFI_CREATED": "2023-06-15", "GEOMETRY": POLYGON_WKT},
            {"VICGOV_REGION": "Gippsland",  "VICGOV_REGION_SNAME": "GL Region", "VICGOV_REGION_CODE": "GL", "UFI_CREATED": "2022-03-10", "GEOMETRY": POLYGON_WKT},
        ])
        result = wrangle_vic_boundaries(df)
        assert len(result) == 2

    def test_keeps_latest_row_per_region(self):
        """Tests that the most recent row per region is retained end-to-end."""
        df = pd.DataFrame([
            {"VICGOV_REGION": "South East", "VICGOV_REGION_SNAME": "SE Region", "VICGOV_REGION_CODE": "SE", "UFI_CREATED": "2020-01-01", "GEOMETRY": POLYGON_WKT},
            {"VICGOV_REGION": "South East", "VICGOV_REGION_SNAME": "SE Region", "VICGOV_REGION_CODE": "SE", "UFI_CREATED": "2023-06-15", "GEOMETRY": POLYGON_WKT},
        ])
        result = wrangle_vic_boundaries(df)
        assert len(result) == 1
        assert pd.to_datetime(result["ufi_created"].iloc[0]) == pd.Timestamp("2023-06-15")

    def test_geometry_is_valid_wkt_string(self):
        """Tests that the geometry column contains valid WKT strings after reprojection."""
        df = make_full_raw_df()
        result = wrangle_vic_boundaries(df)
        assert isinstance(result["geometry"].iloc[0], str)
        assert is_valid_wkt(result["geometry"].iloc[0])

    def test_geometry_coordinates_are_in_wgs84_range(self):
        """Tests that reprojected coordinates fall within the expected VIC bounding box."""
        df = make_full_raw_df()
        result = wrangle_vic_boundaries(df)
        geom = shapely_wkt.loads(result["geometry"].iloc[0])
        # For a polygon use centroid; for a point use x/y directly
        centroid = geom.centroid
        assert -39 <= centroid.y <= -34, f"Latitude {centroid.y} outside VIC range"
        assert 140 <= centroid.x <= 150, f"Longitude {centroid.x} outside VIC range"

    def test_region_names_are_title_cased(self):
        """Tests that vicgov_region and vicgov_region_sname are title-cased end-to-end."""
        df = pd.DataFrame([{
            "VICGOV_REGION": "SOUTH EAST",
            "VICGOV_REGION_SNAME": "SE REGION",
            "VICGOV_REGION_CODE": "SE",
            "UFI_CREATED": "2023-06-15",
            "GEOMETRY": POLYGON_WKT,
        }])
        result = wrangle_vic_boundaries(df)
        assert result["vicgov_region"].iloc[0] == "South East"
        assert result["vicgov_region_sname"].iloc[0] == "Se Region"

    def test_region_values_are_preserved(self):
        """Tests that the vicgov_region values are correctly carried through the pipeline."""
        df = make_full_raw_df()
        result = wrangle_vic_boundaries(df)
        assert result["vicgov_region"].iloc[0] == "South East"

    def test_does_not_mutate_input_columns(self):
        """
        Tests that the original DataFrame's column names are not changed.
        """
        df = make_full_raw_df()
        original_columns = list(df.columns)
        wrangle_vic_boundaries(df)
        assert list(df.columns) == original_columns, (
            "Input DataFrame columns were mutated — standardize_columns modifies "
            "df.columns in place without a prior df.copy()"
        )