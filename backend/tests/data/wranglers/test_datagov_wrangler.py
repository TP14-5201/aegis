import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch

from src.data.wranglers.datagov_wrangler import (
    filter_victoria_services,
    extract_organisation_url,
    rename_columns,
    create_placeholder_columns,
    wrangle_datagov,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

PLACEHOLDER_COLUMNS = [
    "description", "target_audience", "primary_phone", "phone_display",
    "email", "social_media", "opening_hours", "cost",
    "tram_routes", "bus_routes", "nearest_train_station", "categories",
]


def make_vic_row(**overrides):
    """Minimal valid Victorian row for filter_victoria_services."""
    row = {"address": "123 Main St VIC", "postcode": "3000"}
    row.update(overrides)
    return row


def make_full_datagov_df(**overrides):
    """
    Minimal DataFrame that survives the entire wrangle_datagov pipeline.
    Column names are pre-standardized (snake_case) to simplify pipeline tests.
    """
    row = {
        "outlet_name": "Test Service",
        "organistaion_website": "https://example.com",
        "outlet_address": "123 Main St VIC",
        "town_or_suburb": "Melbourne",
        "postcode": "3000",
        "latitude": "-37.8136",
        "longitude": "144.9631",
    }
    row.update(overrides)
    return pd.DataFrame([row])


@pytest.fixture
def lga_boundaries():
    """
    Empty placeholder DataFrame standing in for real LGA boundary geometry.

    determine_emergency_service_lga is patched to a no-op in all integration
    tests, so the actual content of this fixture does not matter; it exists
    only to satisfy the wrangle_datagov signature.
    """
    return pd.DataFrame()


# Patch target for determine_emergency_service_lga used across integration tests.
_PATCH_LGA = "src.data.wranglers.datagov_wrangler.determine_emergency_service_lga"


# ---------------------------------------------------------------------------
# filter_victoria_services
# ---------------------------------------------------------------------------

class TestFilterVictoriaServices:
    def test_keeps_vic_address_with_vic_postcode(self):
        df = pd.DataFrame([make_vic_row()])
        result = filter_victoria_services(df)
        assert len(result) == 1

    def test_removes_non_vic_address(self):
        df = pd.DataFrame([make_vic_row(address="123 Main St NSW", postcode="2000")])
        result = filter_victoria_services(df)
        assert len(result) == 0

    def test_removes_vic_address_with_non_vic_postcode(self):
        df = pd.DataFrame([make_vic_row(postcode="2000")])
        result = filter_victoria_services(df)
        assert len(result) == 0

    def test_removes_vic_postcode_with_non_vic_address(self):
        df = pd.DataFrame([make_vic_row(address="123 Main St NSW")])
        result = filter_victoria_services(df)
        assert len(result) == 0

    def test_accepts_postcode_starting_with_8(self):
        df = pd.DataFrame([make_vic_row(postcode="8000")])
        result = filter_victoria_services(df)
        assert len(result) == 1

    def test_case_insensitive_vic_match(self):
        df = pd.DataFrame([make_vic_row(address="123 Main St vic")])
        result = filter_victoria_services(df)
        assert len(result) == 1

    def test_does_not_match_vic_as_substring(self):
        # "VICTOR" should not match \bVIC\b
        df = pd.DataFrame([make_vic_row(address="123 Victor St NSW", postcode="2000")])
        result = filter_victoria_services(df)
        assert len(result) == 0

    def test_filters_mixed_rows(self):
        df = pd.DataFrame([
            make_vic_row(address="123 Main St VIC", postcode="3000"),
            make_vic_row(address="456 Other St NSW", postcode="2000"),
            make_vic_row(address="789 Another St VIC", postcode="3001"),
        ])
        result = filter_victoria_services(df)
        assert len(result) == 2

    def test_na_address_is_excluded(self):
        df = pd.DataFrame([make_vic_row(address=np.nan)])
        result = filter_victoria_services(df)
        assert len(result) == 0

    def test_returns_dataframe(self):
        df = pd.DataFrame([make_vic_row()])
        assert isinstance(filter_victoria_services(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# extract_organisation_url
# ---------------------------------------------------------------------------

class TestExtractOrganisationUrl:
    def test_extracts_url_from_single_quote_href(self):
        df = pd.DataFrame({"website": ["<a href='https://example.com'>Link</a>"]})
        result = extract_organisation_url(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_extracts_url_from_double_quote_href(self):
        df = pd.DataFrame({"website": ['<a href="https://example.com">Link</a>']})
        result = extract_organisation_url(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_returns_raw_value_if_no_href(self):
        df = pd.DataFrame({"website": ["https://example.com"]})
        result = extract_organisation_url(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_nan_becomes_none(self):
        df = pd.DataFrame({"website": [np.nan]})
        result = extract_organisation_url(df)
        assert result["website"].iloc[0] is None

    def test_empty_string_becomes_none(self):
        df = pd.DataFrame({"website": [""]})
        result = extract_organisation_url(df)
        assert result["website"].iloc[0] is None

    def test_whitespace_only_becomes_none(self):
        df = pd.DataFrame({"website": ["   "]})
        result = extract_organisation_url(df)
        assert result["website"].iloc[0] is None

    def test_handles_multiple_rows(self):
        df = pd.DataFrame({"website": [
            "<a href='https://a.com'>A</a>",
            "<a href='https://b.com'>B</a>",
            np.nan,
        ]})
        result = extract_organisation_url(df)
        assert result["website"].iloc[0] == "https://a.com"
        assert result["website"].iloc[1] == "https://b.com"
        assert pd.isna(result["website"].iloc[2])

    def test_returns_dataframe(self):
        df = pd.DataFrame({"website": ["https://example.com"]})
        assert isinstance(extract_organisation_url(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# rename_columns
# ---------------------------------------------------------------------------

class TestRenameColumns:
    def test_renames_outlet_name_to_name(self):
        df = pd.DataFrame(columns=["outlet_name"])
        result = rename_columns(df, cols_rename_map={"outlet_name": "name"})
        assert "name" in result.columns
        assert "outlet_name" not in result.columns

    def test_renames_organistaion_website_to_website(self):
        df = pd.DataFrame(columns=["organistaion_website"])
        result = rename_columns(df, cols_rename_map={"organistaion_website": "website"})
        assert "website" in result.columns
        assert "organistaion_website" not in result.columns

    def test_renames_outlet_address_to_address(self):
        df = pd.DataFrame(columns=["outlet_address"])
        result = rename_columns(df, cols_rename_map={"outlet_address": "address"})
        assert "address" in result.columns
        assert "outlet_address" not in result.columns

    def test_renames_town_or_suburb_to_suburb(self):
        df = pd.DataFrame(columns=["town_or_suburb"])
        result = rename_columns(df, cols_rename_map={"town_or_suburb": "suburb"})
        assert "suburb" in result.columns
        assert "town_or_suburb" not in result.columns

    def test_unrelated_columns_are_unchanged(self):
        df = pd.DataFrame(columns=["outlet_name", "postcode", "latitude"])
        result = rename_columns(df, cols_rename_map={"outlet_name": "name"})
        assert "postcode" in result.columns
        assert "latitude" in result.columns

    def test_returns_dataframe(self):
        df = pd.DataFrame(columns=["outlet_name"])
        assert isinstance(rename_columns(df, cols_rename_map={"outlet_name": "name"}), pd.DataFrame)


# ---------------------------------------------------------------------------
# create_placeholder_columns
# ---------------------------------------------------------------------------

class TestCreatePlaceholderColumns:
    def test_all_placeholder_columns_created(self):
        df = pd.DataFrame({"name": ["Test"]})
        result = create_placeholder_columns(df)
        for col in PLACEHOLDER_COLUMNS:
            assert col in result.columns, f"Missing placeholder column: {col}"

    def test_all_placeholder_columns_are_empty_strings(self):
        df = pd.DataFrame({"name": ["Test"]})
        result = create_placeholder_columns(df)
        for col in PLACEHOLDER_COLUMNS:
            assert result[col].iloc[0] == "", f"Column {col} should be empty string"

    def test_existing_columns_are_preserved(self):
        df = pd.DataFrame({"name": ["Test Service"], "postcode": ["3000"]})
        result = create_placeholder_columns(df)
        assert result["name"].iloc[0] == "Test Service"
        assert result["postcode"].iloc[0] == "3000"

    def test_returns_dataframe(self):
        df = pd.DataFrame({"name": ["Test"]})
        assert isinstance(create_placeholder_columns(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# wrangle_datagov (integration)
# ---------------------------------------------------------------------------

class TestWrangleDatagov:
    """
    Integration tests for wrangle_datagov.

    determine_emergency_service_lga requires real LGA boundary geometry and is
    tested separately.  It is patched here to a no-op (returns df unchanged)
    so these tests remain focused on the wrangling logic alone.
    """

    def test_returns_dataframe(self, lga_boundaries):
        df = make_full_datagov_df()
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            result = wrangle_datagov(df, lga_boundaries)
        assert isinstance(result, pd.DataFrame)

    def test_output_has_source_column_set_to_datagov(self, lga_boundaries):
        df = make_full_datagov_df()
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            result = wrangle_datagov(df, lga_boundaries)
        assert "source" in result.columns
        assert all(result["source"] == "DataGov")

    def test_output_columns_match_expected_schema(self, lga_boundaries):
        df = make_full_datagov_df()
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            result = wrangle_datagov(df, lga_boundaries)
        expected_cols = [
            "name", "description", "target_audience", "address", "suburb",
            "primary_phone", "phone_display", "email", "website", "social_media",
            "opening_hours", "cost", "tram_routes", "bus_routes",
            "nearest_train_station", "categories", "longitude", "latitude", "source"
        ]
        for col in expected_cols:
            assert col in result.columns, f"Missing column: {col}"

    def test_filters_out_non_vic_rows(self, lga_boundaries):
        df = pd.DataFrame([
            {
                "outlet_name": "VIC Service",
                "organistaion_website": "https://vic.com",
                "outlet_address": "123 Main St VIC",
                "town_or_suburb": "Melbourne",
                "postcode": "3000",
                "latitude": "-37.8136",
                "longitude": "144.9631",
            },
            {
                "outlet_name": "NSW Service",
                "organistaion_website": "https://nsw.com",
                "outlet_address": "456 Other St NSW",
                "town_or_suburb": "Sydney",
                "postcode": "2000",
                "latitude": "-33.8688",
                "longitude": "151.2093",
            },
        ])
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            result = wrangle_datagov(df, lga_boundaries)
        assert len(result) == 1
        assert result["name"].iloc[0] == "VIC Service"

    def test_placeholder_columns_become_nan_after_pipeline(self, lga_boundaries):
        df = make_full_datagov_df()
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            result = wrangle_datagov(df, lga_boundaries)
        for col in PLACEHOLDER_COLUMNS:
            assert pd.isna(result[col].iloc[0]), f"Column {col} should be NaN after pipeline"

    def test_coordinates_are_numeric(self, lga_boundaries):
        df = make_full_datagov_df()
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            result = wrangle_datagov(df, lga_boundaries)
        assert result["latitude"].dtype in [float, np.float64]
        assert result["longitude"].dtype in [float, np.float64]

    def test_website_is_normalised(self, lga_boundaries):
        df = make_full_datagov_df(organistaion_website="http://example.com")
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            result = wrangle_datagov(df, lga_boundaries)
        assert result["website"].iloc[0] == "https://example.com"

    def test_empty_dataframe_returns_empty_dataframe(self, lga_boundaries):
        df = make_full_datagov_df()
        # Make all rows non-VIC so filter removes everything
        df["outlet_address"] = "123 Main St NSW"
        df["postcode"] = "2000"
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            result = wrangle_datagov(df, lga_boundaries)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_does_not_mutate_input_dataframe(self, lga_boundaries):
        df = make_full_datagov_df()
        original_columns = list(df.columns)
        original_values = df["outlet_name"].iloc[0]
        with patch(_PATCH_LGA, side_effect=lambda df, _: df):
            wrangle_datagov(df, lga_boundaries)
        assert list(df.columns) == original_columns
        assert df["outlet_name"].iloc[0] == original_values

    def test_lga_function_is_called_with_boundaries(self, lga_boundaries):
        """determine_emergency_service_lga must receive the df_lga_boundaries argument."""
        df = make_full_datagov_df()
        with patch(_PATCH_LGA, side_effect=lambda df, _: df) as mock_lga:
            wrangle_datagov(df, lga_boundaries)
        mock_lga.assert_called_once()
        _, called_boundaries = mock_lga.call_args.args
        assert called_boundaries is lga_boundaries