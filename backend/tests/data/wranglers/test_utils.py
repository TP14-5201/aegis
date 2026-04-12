import pytest
import numpy as np
import pandas as pd

from src.data.wranglers.utils import (
    standardize_columns,
    clean_whitespaces,
    clean_na_values,
    normalize_coordinates,
    initial_cleaning_pipeline,
    select_columns,
    add_source_column,
    normalize_website,
    _NA_SENTINEL_VALUES,
)


# ---------------------------------------------------------------------------
# Shared sample DataFrames
# ---------------------------------------------------------------------------

def make_standard_df():
    """Minimal DataFrame with all required columns for select_columns."""
    return pd.DataFrame([{
        "name": "Test Service",
        "description": "A service",
        "target_audience": "Everyone",
        "address": "123 Main St",
        "suburb": "Melbourne",
        "primary_phone": "0412345678",
        "phone_display": "0412 345 678",
        "email": "test@example.com",
        "website": "https://example.com",
        "social_media": "N/A",
        "opening_hours": "9am-5pm",
        "cost": "Free",
        "tram_routes": "1, 2",
        "bus_routes": "901",
        "nearest_train_station": "Flinders Street",
        "categories": "Food",
        "longitude": 144.9631,
        "latitude": -37.8136,
    }])


# ---------------------------------------------------------------------------
# standardize_columns
# ---------------------------------------------------------------------------

class TestStandardizeColumns:
    def test_converts_to_lowercase(self):
        """Tests if the column names are converted to lowercase."""
        df = pd.DataFrame(columns=["Name", "City"])
        result = standardize_columns(df)
        assert list(result.columns) == ["name", "city"]

    def test_replaces_spaces_with_underscores(self):
        """Tests if the spaces in column names are replaced with underscores."""
        df = pd.DataFrame(columns=["First Name", "Home City"])
        result = standardize_columns(df)
        assert list(result.columns) == ["first_name", "home_city"]

    def test_strips_leading_trailing_whitespace(self):
        """Tests if the leading and trailing whitespaces in column names are removed."""
        df = pd.DataFrame(columns=["  name  ", " city "])
        result = standardize_columns(df)
        assert list(result.columns) == ["name", "city"]

    def test_removes_special_characters(self):
        """Tests if the special characters in column names are removed."""
        df = pd.DataFrame(columns=["Na-me", "Cit.y", "Zip!"])
        result = standardize_columns(df)
        assert list(result.columns) == ["name", "city", "zip"]

    def test_handles_mixed_case_and_spaces(self):
        """Tests if the column names with mixed case and spaces are handled correctly."""
        df = pd.DataFrame(columns=["First Name", "HOME CITY", "Zip Code"])
        result = standardize_columns(df)
        assert list(result.columns) == ["first_name", "home_city", "zip_code"]

    def test_returns_dataframe(self):
        """Tests if the function returns a dataframe."""
        df = pd.DataFrame(columns=["Name"])
        assert isinstance(standardize_columns(df), pd.DataFrame)

    def test_empty_dataframe(self):
        """Tests if the function handles an empty dataframe."""
        df = pd.DataFrame(columns=[]) 
        result = standardize_columns(df)
        assert list(result.columns) == []   


# ---------------------------------------------------------------------------
# clean_whitespaces
# ---------------------------------------------------------------------------

class TestCleanWhitespaces:
    def test_strips_leading_whitespace(self):
        """Tests if the leading whitespaces in string columns are removed."""
        df = pd.DataFrame({"name": ["  Alice"]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"

    def test_strips_trailing_whitespace(self):
        """Tests if the trailing whitespaces in string columns are removed."""
        df = pd.DataFrame({"name": ["Alice  "]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"

    def test_strips_both_ends(self):
        """Tests if the leading and trailing whitespaces in string columns are removed."""
        df = pd.DataFrame({"name": ["  Alice  "]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"

    def test_does_not_affect_numeric_columns(self):
        """Tests if the numeric columns are not affected by the function."""
        df = pd.DataFrame({"name": ["  Alice  "], "age": [30]})
        result = clean_whitespaces(df)
        assert result["age"].iloc[0] == 30

    def test_handles_multiple_string_columns(self):
        """Tests if the function handles multiple string columns."""
        df = pd.DataFrame({"name": ["  Alice  "], "city": ["  Melbourne  "]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"
        assert result["city"].iloc[0] == "Melbourne"

    def test_handles_empty_strings(self):
        """Tests if the function handles empty strings."""
        df = pd.DataFrame({"name": [""]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == ""

    def test_returns_dataframe(self):
        """Tests if the function returns a dataframe."""
        df = pd.DataFrame({"name": ["Alice"]})
        assert isinstance(clean_whitespaces(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# clean_na_values
# ---------------------------------------------------------------------------

class TestCleanNaValues:
    @pytest.mark.parametrize("sentinel", _NA_SENTINEL_VALUES)
    def test_replaces_sentinel_with_nan(self, sentinel):
        """Tests if the sentinel values are replaced with NaN."""
        df = pd.DataFrame({"value": [sentinel]})
        result = clean_na_values(df)
        assert pd.isna(result["value"].iloc[0])

    def test_does_not_affect_valid_values(self):
        """Tests if the valid values are not affected by the function."""
        df = pd.DataFrame({"value": ["valid text", "another value"]})
        result = clean_na_values(df)
        assert result["value"].iloc[0] == "valid text"
        assert result["value"].iloc[1] == "another value"

    def test_handles_mixed_sentinels_and_valid(self):
        """Tests if the function handles mixed sentinel and valid values."""
        df = pd.DataFrame({"value": ["N/A", "valid", "NULL", "also valid"]})
        result = clean_na_values(df)
        assert pd.isna(result["value"].iloc[0])
        assert result["value"].iloc[1] == "valid"
        assert pd.isna(result["value"].iloc[2])
        assert result["value"].iloc[3] == "also valid"

    def test_replaces_bare_https_sentinel(self):
        """Tests if the bare https sentinel value is replaced with NaN."""
        df = pd.DataFrame({"website": ["https://"]})
        result = clean_na_values(df)
        assert pd.isna(result["website"].iloc[0])

    def test_returns_dataframe(self):
        """Tests if the function returns a dataframe."""
        df = pd.DataFrame({"value": ["N/A"]})
        assert isinstance(clean_na_values(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_coordinates
# ---------------------------------------------------------------------------

class TestNormalizeCoordinates:
    def test_converts_string_floats_to_numeric(self):
        """Tests if the string floats are converted to numeric."""
        df = pd.DataFrame({"lat": ["37.8"], "lon": ["144.9"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert result["lat"].dtype in [float, np.float64]
        assert result["lon"].dtype in [float, np.float64]

    def test_coerces_invalid_strings_to_nan(self):
        """Tests if the invalid strings are coerced to NaN."""
        df = pd.DataFrame({"lat": ["not_a_number"], "lon": ["also_invalid"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert pd.isna(result["lat"].iloc[0])
        assert pd.isna(result["lon"].iloc[0])

    def test_preserves_valid_numeric_values(self):
        """Tests if the valid numeric values are preserved."""
        df = pd.DataFrame({"lat": ["-37.8136"], "lon": ["144.9631"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert pytest.approx(result["lat"].iloc[0], abs=1e-4) == -37.8136
        assert pytest.approx(result["lon"].iloc[0], abs=1e-4) == 144.9631

    def test_handles_already_numeric_columns(self):
        """Tests if the function handles already numeric columns."""
        df = pd.DataFrame({"lat": [-37.8136], "lon": [144.9631]})
        result = normalize_coordinates(df, "lat", "lon")
        assert pytest.approx(result["lat"].iloc[0], abs=1e-4) == -37.8136

    def test_handles_mixed_valid_and_invalid(self):
        """Tests if the function handles mixed valid and invalid values."""
        df = pd.DataFrame({"lat": ["-37.8", "bad"], "lon": ["144.9", "also_bad"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert pytest.approx(result["lat"].iloc[0], abs=1e-1) == -37.8
        assert pd.isna(result["lat"].iloc[1])

    def test_returns_dataframe(self):
        """Tests if the function returns a dataframe."""
        df = pd.DataFrame({"lat": ["37.8"], "lon": ["144.9"]})
        assert isinstance(normalize_coordinates(df, "lat", "lon"), pd.DataFrame)


# ---------------------------------------------------------------------------
# initial_cleaning_pipeline
# ---------------------------------------------------------------------------

class TestInitialCleaningPipeline:
    def test_standardizes_column_names(self):
        """Tests if the column names are standardized."""
        df = pd.DataFrame({"First Name": ["Alice"], "Home City": ["Melbourne"]})
        result = initial_cleaning_pipeline(df)
        assert "first_name" in result.columns
        assert "home_city" in result.columns

    def test_strips_whitespace_from_values(self):
        """Tests if the whitespace from values are stripped."""
        df = pd.DataFrame({"name": ["  Alice  "]})
        result = initial_cleaning_pipeline(df)
        assert result["name"].iloc[0] == "Alice"

    def test_does_not_mutate_original_dataframe(self):
        """Tests if the original dataframe is not mutated."""
        df = pd.DataFrame({"First Name": ["  Alice  "]})
        original_columns = list(df.columns)
        initial_cleaning_pipeline(df)
        assert list(df.columns) == original_columns
        assert df["First Name"].iloc[0] == "  Alice  "

    def test_does_not_call_clean_na_values(self):
        """Tests if the clean_na_values is not called."""
        df = pd.DataFrame({"name": ["N/A", "NULL"]})
        result = initial_cleaning_pipeline(df)
        # Sentinel values must still be present — clean_na_values is deferred
        assert result["name"].iloc[0] == "N/A"
        assert result["name"].iloc[1] == "NULL"

    def test_returns_dataframe(self):
        """Tests if the function returns a dataframe."""
        df = pd.DataFrame({"Name": ["Alice"]})
        assert isinstance(initial_cleaning_pipeline(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# select_columns
# ---------------------------------------------------------------------------

class TestSelectColumns:
    def test_returns_only_expected_columns(self):
        """Tests if the function returns only the expected columns."""
        df = make_standard_df()
        df["extra_col"] = "should be dropped"
        result = select_columns(df)
        assert "extra_col" not in result.columns

    def test_all_required_columns_present(self):
        """Tests if all the required columns are present."""
        df = make_standard_df()
        result = select_columns(df)
        expected = [
            "name", "description", "target_audience", "address", "suburb",
            "primary_phone", "phone_display", "email", "website", "social_media",
            "opening_hours", "cost", "tram_routes", "bus_routes",
            "nearest_train_station", "categories", "longitude", "latitude"
        ]
        assert list(result.columns) == expected

    def test_raises_on_missing_required_column(self):
        """Tests if the function raises an error on missing required column."""
        df = make_standard_df().drop(columns=["name"])
        with pytest.raises(KeyError):
            select_columns(df)

    def test_returns_dataframe(self):
        """Tests if the function returns a dataframe."""
        df = make_standard_df()
        assert isinstance(select_columns(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# add_source_column
# ---------------------------------------------------------------------------

class TestAddSourceColumn:
    def test_adds_source_column(self):
        """Tests if the source column is added."""
        df = pd.DataFrame({"name": ["Alice"]})
        result = add_source_column(df, "melbourne")
        assert "source" in result.columns

    def test_source_column_has_correct_value(self):
        """Tests if the source column has the correct value."""
        df = pd.DataFrame({"name": ["Alice", "Bob"]})
        result = add_source_column(df, "datagov")
        assert all(result["source"] == "datagov")

    def test_overwrites_existing_source_column(self):
        """Tests if the existing source column is overwritten."""
        df = pd.DataFrame({"name": ["Alice"], "source": ["old_source"]})
        result = add_source_column(df, "new_source")
        assert result["source"].iloc[0] == "new_source"

    def test_returns_dataframe(self):
        """Tests if the function returns a dataframe."""
        df = pd.DataFrame({"name": ["Alice"]})
        assert isinstance(add_source_column(df, "test"), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_website
# ---------------------------------------------------------------------------

class TestNormalizeWebsite:
    def test_adds_https_prefix(self):
        """Tests if the https prefix is added."""
        df = pd.DataFrame({"website": ["example.com"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_replaces_http_with_https(self):
        """Tests if the http is replaced with https."""
        df = pd.DataFrame({"website": ["http://example.com"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_does_not_double_https(self):
        """Tests if the https is not doubled."""
        df = pd.DataFrame({"website": ["https://example.com"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_converts_to_lowercase(self):
        """Tests if the website is converted to lowercase."""
        df = pd.DataFrame({"website": ["https://Example.COM"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_strips_whitespace(self):
        """Tests if the whitespace is stripped."""
        df = pd.DataFrame({"website": ["  https://example.com  "]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_empty_string_stays_empty(self):
        """Tests if the empty string stays empty."""
        df = pd.DataFrame({"website": [""]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == ""

    def test_nan_becomes_empty_string(self):
        """Tests if the NaN becomes an empty string."""
        df = pd.DataFrame({"website": [np.nan]})
        result = normalize_website(df)
        # NaN is filled to "" before processing, result is "" (not NaN)
        assert result["website"].iloc[0] == ""

    def test_whitespace_only_becomes_empty_string(self):
        """Tests if the whitespace only becomes an empty string."""
        df = pd.DataFrame({"website": ["   "]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == ""

    def test_handles_multiple_rows(self):
        """Tests if the function handles multiple rows."""
        df = pd.DataFrame({"website": ["http://a.com", "https://b.com", "", np.nan]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://a.com"
        assert result["website"].iloc[1] == "https://b.com"
        assert result["website"].iloc[2] == ""
        assert result["website"].iloc[3] == ""

    def test_returns_dataframe(self):
        """Tests if the function returns a dataframe."""
        df = pd.DataFrame({"website": ["example.com"]})
        assert isinstance(normalize_website(df), pd.DataFrame)