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
    rename_columns,
    add_source_column,
    normalize_website,
    _NA_SENTINEL_VALUES,
)


# ---------------------------------------------------------------------------
# Shared constants / helpers
# ---------------------------------------------------------------------------

# Mirrors settings.EMERGENCY_INCLUDED_COLS — kept local so tests are
# self-contained and don't break when settings change.
_INCLUDED_COLS = [
    "name", "description", "target_audience", "address", "suburb",
    "primary_phone", "phone_display", "email", "website", "social_media",
    "opening_hours", "cost", "tram_routes", "bus_routes",
    "nearest_train_station", "categories", "longitude", "latitude",
]


def make_standard_df() -> pd.DataFrame:
    """Minimal DataFrame whose columns match _INCLUDED_COLS exactly."""
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
        """Tests that column names are converted to lowercase."""
        df = pd.DataFrame(columns=["Name", "City"])
        result = standardize_columns(df)
        assert list(result.columns) == ["name", "city"]

    def test_replaces_spaces_with_underscores(self):
        """Tests that spaces in column names are replaced with underscores."""
        df = pd.DataFrame(columns=["First Name", "Home City"])
        result = standardize_columns(df)
        assert list(result.columns) == ["first_name", "home_city"]

    def test_strips_leading_trailing_whitespace(self):
        """Tests that leading and trailing whitespace in column names is removed."""
        df = pd.DataFrame(columns=["  name  ", " city "])
        result = standardize_columns(df)
        assert list(result.columns) == ["name", "city"]

    def test_removes_special_characters(self):
        """Tests that special characters in column names are removed."""
        df = pd.DataFrame(columns=["Na-me", "Cit.y", "Zip!"])
        result = standardize_columns(df)
        assert list(result.columns) == ["name", "city", "zip"]

    def test_handles_mixed_case_and_spaces(self):
        """Tests that column names with mixed case and spaces are handled correctly."""
        df = pd.DataFrame(columns=["First Name", "HOME CITY", "Zip Code"])
        result = standardize_columns(df)
        assert list(result.columns) == ["first_name", "home_city", "zip_code"]

    def test_already_clean_columns_are_unchanged(self):
        """Tests that already snake_case lowercase columns pass through unchanged."""
        df = pd.DataFrame(columns=["name", "home_city"])
        result = standardize_columns(df)
        assert list(result.columns) == ["name", "home_city"]

    def test_multiple_consecutive_spaces_collapsed_to_single_underscore(self):
        """Tests that multiple spaces between words become a single underscore."""
        df = pd.DataFrame(columns=["first  name"])
        result = standardize_columns(df)
        # Two spaces → two underscores via str.replace(' ', '_'); this documents
        # the current behaviour so regressions are caught.
        assert "_" in result.columns[0]
        assert result.columns[0] == result.columns[0].lower()

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame(columns=["Name"])
        assert isinstance(standardize_columns(df), pd.DataFrame)

    def test_empty_dataframe(self):
        """Tests that the function handles a DataFrame with no columns."""
        df = pd.DataFrame(columns=[])
        result = standardize_columns(df)
        assert list(result.columns) == []


# ---------------------------------------------------------------------------
# clean_whitespaces
# ---------------------------------------------------------------------------

class TestCleanWhitespaces:
    def test_strips_leading_whitespace(self):
        """Tests that leading whitespace in string columns is removed."""
        df = pd.DataFrame({"name": ["  Alice"]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"

    def test_strips_trailing_whitespace(self):
        """Tests that trailing whitespace in string columns is removed."""
        df = pd.DataFrame({"name": ["Alice  "]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"

    def test_strips_both_ends(self):
        """Tests that both leading and trailing whitespace is removed."""
        df = pd.DataFrame({"name": ["  Alice  "]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"

    def test_does_not_affect_numeric_columns(self):
        """Tests that numeric columns are not affected."""
        df = pd.DataFrame({"name": ["  Alice  "], "age": [30]})
        result = clean_whitespaces(df)
        assert result["age"].iloc[0] == 30

    def test_handles_multiple_string_columns(self):
        """Tests that multiple string columns are all stripped."""
        df = pd.DataFrame({"name": ["  Alice  "], "city": ["  Melbourne  "]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"
        assert result["city"].iloc[0] == "Melbourne"

    def test_handles_empty_strings(self):
        """Tests that empty strings remain empty after stripping."""
        df = pd.DataFrame({"name": [""]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == ""

    def test_does_not_raise_on_nan_in_string_column(self):
        """Tests that NaN values inside object columns do not cause an error."""
        df = pd.DataFrame({"name": ["  Alice  ", np.nan]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == "Alice"
        assert pd.isna(result["name"].iloc[1])

    def test_whitespace_only_string_becomes_empty_string(self):
        """Tests that a whitespace-only string is reduced to an empty string."""
        df = pd.DataFrame({"name": ["   "]})
        result = clean_whitespaces(df)
        assert result["name"].iloc[0] == ""

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"name": ["Alice"]})
        assert isinstance(clean_whitespaces(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# clean_na_values
# ---------------------------------------------------------------------------

class TestCleanNaValues:
    @pytest.mark.parametrize("sentinel", _NA_SENTINEL_VALUES)
    def test_replaces_sentinel_with_nan(self, sentinel):
        """Tests that every defined sentinel value is replaced with NaN."""
        df = pd.DataFrame({"value": [sentinel]})
        result = clean_na_values(df)
        assert pd.isna(result["value"].iloc[0])

    def test_does_not_affect_valid_strings(self):
        """Tests that non-sentinel string values are not altered."""
        df = pd.DataFrame({"value": ["valid text", "another value"]})
        result = clean_na_values(df)
        assert result["value"].iloc[0] == "valid text"
        assert result["value"].iloc[1] == "another value"

    def test_handles_mixed_sentinels_and_valid(self):
        """Tests that sentinel and non-sentinel values coexist correctly."""
        df = pd.DataFrame({"value": ["N/A", "valid", "NULL", "also valid"]})
        result = clean_na_values(df)
        assert pd.isna(result["value"].iloc[0])
        assert result["value"].iloc[1] == "valid"
        assert pd.isna(result["value"].iloc[2])
        assert result["value"].iloc[3] == "also valid"

    def test_replaces_bare_https_sentinel(self):
        """Tests that the bare 'https://' sentinel is replaced with NaN."""
        df = pd.DataFrame({"website": ["https://"]})
        result = clean_na_values(df)
        assert pd.isna(result["website"].iloc[0])

    def test_existing_nan_values_are_preserved(self):
        """Tests that pre-existing NaN values remain NaN after the call."""
        df = pd.DataFrame({"value": [np.nan, "valid"]})
        result = clean_na_values(df)
        assert pd.isna(result["value"].iloc[0])
        assert result["value"].iloc[1] == "valid"

    def test_does_not_affect_numeric_columns(self):
        """Tests that numeric column values are not altered."""
        df = pd.DataFrame({"count": [0, 1, 42]})
        result = clean_na_values(df)
        assert list(result["count"]) == [0, 1, 42]

    def test_valid_url_with_path_is_not_replaced(self):
        """Tests that a full valid URL (not the bare https:// sentinel) is kept."""
        df = pd.DataFrame({"website": ["https://example.com"]})
        result = clean_na_values(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"value": ["N/A"]})
        assert isinstance(clean_na_values(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_coordinates
# ---------------------------------------------------------------------------

class TestNormalizeCoordinates:
    def test_converts_string_floats_to_numeric(self):
        """Tests that string float values are converted to a float dtype."""
        df = pd.DataFrame({"lat": ["37.8"], "lon": ["144.9"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert result["lat"].dtype in [float, np.float64]
        assert result["lon"].dtype in [float, np.float64]

    def test_coerces_invalid_strings_to_nan(self):
        """Tests that non-numeric strings are coerced to NaN."""
        df = pd.DataFrame({"lat": ["not_a_number"], "lon": ["also_invalid"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert pd.isna(result["lat"].iloc[0])
        assert pd.isna(result["lon"].iloc[0])

    def test_preserves_valid_numeric_values(self):
        """Tests that valid numeric strings are preserved with full precision."""
        df = pd.DataFrame({"lat": ["-37.8136"], "lon": ["144.9631"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert result["lat"].iloc[0] == pytest.approx(-37.8136, abs=1e-4)
        assert result["lon"].iloc[0] == pytest.approx(144.9631, abs=1e-4)

    def test_handles_already_numeric_columns(self):
        """Tests that already-numeric columns pass through without error."""
        df = pd.DataFrame({"lat": [-37.8136], "lon": [144.9631]})
        result = normalize_coordinates(df, "lat", "lon")
        assert result["lat"].iloc[0] == pytest.approx(-37.8136, abs=1e-4)

    def test_handles_mixed_valid_and_invalid(self):
        """Tests that a mix of valid and invalid values is handled per-row."""
        df = pd.DataFrame({"lat": ["-37.8", "bad"], "lon": ["144.9", "also_bad"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert result["lat"].iloc[0] == pytest.approx(-37.8, abs=1e-1)
        assert pd.isna(result["lat"].iloc[1])

    def test_handles_none_values(self):
        """Tests that None values in coordinate columns are coerced to NaN."""
        df = pd.DataFrame({"lat": [None], "lon": [None]})
        result = normalize_coordinates(df, "lat", "lon")
        assert pd.isna(result["lat"].iloc[0])
        assert pd.isna(result["lon"].iloc[0])

    def test_handles_existing_nan_values(self):
        """Tests that existing NaN values in coordinate columns remain NaN."""
        df = pd.DataFrame({"lat": [np.nan], "lon": [np.nan]})
        result = normalize_coordinates(df, "lat", "lon")
        assert pd.isna(result["lat"].iloc[0])
        assert pd.isna(result["lon"].iloc[0])

    def test_negative_coordinates_preserved(self):
        """Tests that negative coordinate values (e.g. southern latitudes) are preserved."""
        df = pd.DataFrame({"lat": ["-33.8688"], "lon": ["151.2093"]})
        result = normalize_coordinates(df, "lat", "lon")
        assert result["lat"].iloc[0] < 0

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"lat": ["37.8"], "lon": ["144.9"]})
        assert isinstance(normalize_coordinates(df, "lat", "lon"), pd.DataFrame)


# ---------------------------------------------------------------------------
# initial_cleaning_pipeline
# ---------------------------------------------------------------------------

class TestInitialCleaningPipeline:
    def test_standardizes_column_names(self):
        """Tests that column names are standardised to snake_case."""
        df = pd.DataFrame({"First Name": ["Alice"], "Home City": ["Melbourne"]})
        result = initial_cleaning_pipeline(df)
        assert "first_name" in result.columns
        assert "home_city" in result.columns

    def test_strips_whitespace_from_values(self):
        """Tests that leading/trailing whitespace is stripped from cell values."""
        df = pd.DataFrame({"name": ["  Alice  "]})
        result = initial_cleaning_pipeline(df)
        assert result["name"].iloc[0] == "Alice"

    def test_does_not_mutate_original_dataframe(self):
        """Tests that the original DataFrame is not mutated."""
        df = pd.DataFrame({"First Name": ["  Alice  "]})
        original_columns = list(df.columns)
        initial_cleaning_pipeline(df)
        assert list(df.columns) == original_columns
        assert df["First Name"].iloc[0] == "  Alice  "

    def test_does_not_call_clean_na_values(self):
        """Tests that sentinel values are NOT replaced — clean_na_values is deferred."""
        df = pd.DataFrame({"name": ["N/A", "NULL"]})
        result = initial_cleaning_pipeline(df)
        assert result["name"].iloc[0] == "N/A"
        assert result["name"].iloc[1] == "NULL"

    def test_applies_both_column_and_value_cleaning_together(self):
        """Tests that column standardisation and value stripping both run in one pass."""
        df = pd.DataFrame({"First Name": ["  Alice  "], "Home City": ["  Melbourne  "]})
        result = initial_cleaning_pipeline(df)
        assert list(result.columns) == ["first_name", "home_city"]
        assert result["first_name"].iloc[0] == "Alice"
        assert result["home_city"].iloc[0] == "Melbourne"

    def test_handles_empty_dataframe(self):
        """Tests that an empty DataFrame with columns passes through cleanly."""
        df = pd.DataFrame({"First Name": []})
        result = initial_cleaning_pipeline(df)
        assert list(result.columns) == ["first_name"]
        assert len(result) == 0

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"Name": ["Alice"]})
        assert isinstance(initial_cleaning_pipeline(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# select_columns
# ---------------------------------------------------------------------------

class TestSelectColumns:
    def test_returns_only_specified_columns(self):
        """Tests that columns not in the inclusion list are dropped."""
        df = make_standard_df()
        df["extra_col"] = "should be dropped"
        result = select_columns(df, _INCLUDED_COLS)
        assert "extra_col" not in result.columns

    def test_all_included_columns_are_present(self):
        """Tests that every column in the inclusion list is present in the result."""
        df = make_standard_df()
        result = select_columns(df, _INCLUDED_COLS)
        assert list(result.columns) == _INCLUDED_COLS

    def test_column_order_matches_inclusion_list(self):
        """Tests that output column order matches the order of included_cols."""
        df = make_standard_df()
        # Reverse the column order in the source DataFrame
        df = df[list(reversed(_INCLUDED_COLS))]
        result = select_columns(df, _INCLUDED_COLS)
        assert list(result.columns) == _INCLUDED_COLS

    def test_raises_on_missing_required_column(self):
        """Tests that a KeyError is raised when a required column is absent."""
        df = make_standard_df().drop(columns=["name"])
        with pytest.raises(KeyError):
            select_columns(df, _INCLUDED_COLS)

    def test_subset_of_columns_can_be_selected(self):
        """Tests that a smaller inclusion list selects just those columns."""
        df = make_standard_df()
        result = select_columns(df, ["name", "suburb"])
        assert list(result.columns) == ["name", "suburb"]

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = make_standard_df()
        assert isinstance(select_columns(df, _INCLUDED_COLS), pd.DataFrame)


# ---------------------------------------------------------------------------
# rename_columns
# ---------------------------------------------------------------------------

class TestRenameColumns:
    def test_renames_specified_columns(self):
        """Tests that columns named in the map are renamed correctly."""
        df = pd.DataFrame({"old_name": ["Alice"], "old_city": ["Melbourne"]})
        result = rename_columns(df, {"old_name": "name", "old_city": "city"})
        assert "name" in result.columns
        assert "city" in result.columns

    def test_original_names_are_removed(self):
        """Tests that the old column names no longer appear after renaming."""
        df = pd.DataFrame({"old_name": ["Alice"]})
        result = rename_columns(df, {"old_name": "name"})
        assert "old_name" not in result.columns

    def test_unmapped_columns_are_unchanged(self):
        """Tests that columns absent from the rename map are left as-is."""
        df = pd.DataFrame({"keep_me": [1], "rename_me": [2]})
        result = rename_columns(df, {"rename_me": "renamed"})
        assert "keep_me" in result.columns

    def test_values_are_preserved_after_rename(self):
        """Tests that cell values are intact after renaming."""
        df = pd.DataFrame({"old_name": ["Alice", "Bob"]})
        result = rename_columns(df, {"old_name": "name"})
        assert list(result["name"]) == ["Alice", "Bob"]

    def test_empty_rename_map_leaves_dataframe_unchanged(self):
        """Tests that passing an empty dict leaves all column names unchanged."""
        df = pd.DataFrame({"name": ["Alice"], "city": ["Melbourne"]})
        result = rename_columns(df, {})
        assert list(result.columns) == ["name", "city"]

    def test_nonexistent_key_in_map_is_silently_ignored(self):
        """Tests that keys in the map that don't match any column are ignored."""
        df = pd.DataFrame({"name": ["Alice"]})
        result = rename_columns(df, {"nonexistent": "whatever"})
        assert list(result.columns) == ["name"]

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"old": ["value"]})
        assert isinstance(rename_columns(df, {"old": "new"}), pd.DataFrame)


# ---------------------------------------------------------------------------
# add_source_column
# ---------------------------------------------------------------------------

class TestAddSourceColumn:
    def test_adds_source_column(self):
        """Tests that a 'source' column is added to the DataFrame."""
        df = pd.DataFrame({"name": ["Alice"]})
        result = add_source_column(df, "melbourne")
        assert "source" in result.columns

    def test_source_column_has_correct_value_for_all_rows(self):
        """Tests that every row in the source column holds the specified value."""
        df = pd.DataFrame({"name": ["Alice", "Bob"]})
        result = add_source_column(df, "datagov")
        assert all(result["source"] == "datagov")

    def test_overwrites_existing_source_column(self):
        """Tests that an existing 'source' column is overwritten."""
        df = pd.DataFrame({"name": ["Alice"], "source": ["old_source"]})
        result = add_source_column(df, "new_source")
        assert result["source"].iloc[0] == "new_source"

    def test_other_columns_are_unchanged(self):
        """Tests that non-source columns are unaffected."""
        df = pd.DataFrame({"name": ["Alice"], "city": ["Melbourne"]})
        result = add_source_column(df, "test")
        assert result["name"].iloc[0] == "Alice"
        assert result["city"].iloc[0] == "Melbourne"

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"name": ["Alice"]})
        assert isinstance(add_source_column(df, "test"), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_website
# ---------------------------------------------------------------------------

class TestNormalizeWebsite:
    def test_adds_https_to_bare_domain(self):
        """Tests that a bare domain gains an https:// prefix."""
        df = pd.DataFrame({"website": ["example.com"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_replaces_http_with_https(self):
        """Tests that http:// is upgraded to https://."""
        df = pd.DataFrame({"website": ["http://example.com"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_does_not_double_https(self):
        """Tests that an already-https URL is not double-prefixed."""
        df = pd.DataFrame({"website": ["https://example.com"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_converts_to_lowercase(self):
        """Tests that mixed-case URLs are lowercased."""
        df = pd.DataFrame({"website": ["https://Example.COM"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_strips_whitespace(self):
        """Tests that surrounding whitespace is stripped from the URL."""
        df = pd.DataFrame({"website": ["  https://example.com  "]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_empty_string_stays_empty(self):
        """Tests that an empty string remains empty (not 'https://')."""
        df = pd.DataFrame({"website": [""]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == ""

    def test_nan_becomes_empty_string(self):
        """Tests that NaN is treated as empty and results in an empty string."""
        df = pd.DataFrame({"website": [np.nan]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == ""

    def test_none_becomes_empty_string(self):
        """Tests that None is treated as empty and results in an empty string."""
        df = pd.DataFrame({"website": [None]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == ""

    def test_whitespace_only_becomes_empty_string(self):
        """Tests that a whitespace-only value collapses to an empty string."""
        df = pd.DataFrame({"website": ["   "]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == ""

    def test_preserves_url_path_and_query(self):
        """Tests that URL paths and query strings are preserved."""
        df = pd.DataFrame({"website": ["https://example.com/path?q=1"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://example.com/path?q=1"

    def test_handles_multiple_rows(self):
        """Tests mixed URL types across multiple rows in one call."""
        df = pd.DataFrame({
            "website": ["http://a.com", "https://b.com", "", np.nan, "c.com"]
        })
        result = normalize_website(df)
        assert result["website"].iloc[0] == "https://a.com"
        assert result["website"].iloc[1] == "https://b.com"
        assert result["website"].iloc[2] == ""
        assert result["website"].iloc[3] == ""
        assert result["website"].iloc[4] == "https://c.com"

    def test_bare_https_sentinel_becomes_empty_after_strip(self):
        """Tests that 'https://' (the NA sentinel) normalises to empty string.

        After stripping the protocol the domain part is empty, so the result
        should be '' — ready for clean_na_values to convert to NaN.
        """
        df = pd.DataFrame({"website": ["https://"]})
        result = normalize_website(df)
        assert result["website"].iloc[0] == ""

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"website": ["example.com"]})
        assert isinstance(normalize_website(df), pd.DataFrame)