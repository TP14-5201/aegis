import pytest
import numpy as np
import pandas as pd

from src.data.wranglers.melbourne_wrangler import (
    remove_missing_service_names,
    normalize_address,
    normalize_phone,
    normalize_social_media,
    format_time_string,
    clean_opening_hours_text,
    transform_opening_hours,
    transform_categories,
    rename_columns,
    wrangle_melbourne,
)


# ---------------------------------------------------------------------------
# Shared constants & helpers
# ---------------------------------------------------------------------------

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday",
        "saturday", "sunday", "public_holidays"]

CAT_COLS = [f"category_{i}" for i in range(1, 7)]

# Mirrors the MEL_COLUMN_MAP defined inside wrangle_melbourne — kept here so
# rename_columns tests exercise the exact mapping used in production.
MEL_COLUMN_MAP = {
    "what": "description",
    "who": "target_audience",
}


def make_full_melbourne_df(**overrides):
    """
    Minimal single-row DataFrame that survives the entire wrangle_melbourne
    pipeline. All required columns are present with safe default values.
    """
    row = {
        # Core identity
        "name": "Test Service",
        "what": "A helpful service",
        "who": "Everyone",
        # Address
        "address_1": "123 Main St",
        "address_2": "Level 2",
        # Phone
        "phone": "0312345678",
        "phone_2": "",
        "free_call": "",
        # Email
        "email": "test@test.com",
        # Website / social
        "website": "https://example.com",
        "social_media": "https://facebook.com/test",
        # Coordinates
        "latitude": "-37.8136",
        "longitude": "144.9631",
        # Opening hours
        **{day: "9am - 5pm" for day in DAYS},
        # Categories
        **{col: "" for col in CAT_COLS},
        # Suburb
        "suburb": "Melbourne",
        # Costs / transport (required by select_columns)
        "cost": "Free",
        "tram_routes": "1, 2",
        "bus_routes": "901",
        "nearest_train_station": "Flinders Street",
    }
    row.update(overrides)
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# remove_missing_service_names
# ---------------------------------------------------------------------------

class TestRemoveMissingServiceNames:
    def test_keeps_rows_with_names(self):
        """Tests that rows with valid names are retained."""
        df = pd.DataFrame({"name": ["Alice", "Bob"]})
        result = remove_missing_service_names(df)
        assert len(result) == 2

    def test_removes_nan_names(self):
        """Tests that rows with NaN names are removed."""
        df = pd.DataFrame({"name": ["Alice", np.nan, "Bob"]})
        result = remove_missing_service_names(df)
        assert len(result) == 2
        assert "Alice" in result["name"].values
        assert "Bob" in result["name"].values

    def test_removes_all_nan_returns_empty(self):
        """Tests that a DataFrame of only NaN names returns an empty DataFrame."""
        df = pd.DataFrame({"name": [np.nan, np.nan]})
        result = remove_missing_service_names(df)
        assert len(result) == 0

    def test_none_name_is_removed(self):
        """Tests that None is treated as missing and the row is removed."""
        df = pd.DataFrame({"name": ["Valid", None]})
        result = remove_missing_service_names(df)
        assert len(result) == 1
        assert result["name"].iloc[0] == "Valid"

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"name": ["Alice"]})
        assert isinstance(remove_missing_service_names(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_address
# ---------------------------------------------------------------------------

class TestNormalizeAddress:
    def test_combines_both_address_parts_with_separator(self):
        """Tests that two address parts are joined with ', '."""
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": ["Level 2"]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "123 Main St, Level 2"

    def test_uses_address_1_only_when_address_2_is_nan(self):
        """Tests that only address_1 is used when address_2 is NaN."""
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": [np.nan]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "123 Main St"

    def test_uses_address_1_only_when_address_2_is_empty_string(self):
        """Tests that only address_1 is used when address_2 is an empty string."""
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": [""]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "123 Main St"

    def test_uses_address_2_only_when_address_1_is_nan(self):
        """Tests that only address_2 is used when address_1 is NaN."""
        df = pd.DataFrame({"address_1": [np.nan], "address_2": ["Level 2"]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "Level 2"

    def test_uses_address_2_only_when_address_1_is_empty_string(self):
        """Tests that only address_2 is used when address_1 is an empty string."""
        df = pd.DataFrame({"address_1": [""], "address_2": ["Level 2"]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "Level 2"

    def test_both_missing_gives_empty_string(self):
        """Tests that two NaN address parts produce an empty combined address."""
        df = pd.DataFrame({"address_1": [np.nan], "address_2": [np.nan]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == ""

    def test_drops_address_1_and_address_2_columns(self):
        """Tests that the source address_1 and address_2 columns are removed."""
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": ["Level 2"]})
        result = normalize_address(df)
        assert "address_1" not in result.columns
        assert "address_2" not in result.columns

    def test_strips_whitespace_from_parts_before_combining(self):
        """Tests that leading/trailing whitespace is stripped from each part."""
        df = pd.DataFrame({"address_1": ["  123 Main St  "], "address_2": ["  Level 2  "]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "123 Main St, Level 2"

    def test_no_leading_separator_when_address_1_is_empty(self):
        """Tests that the combined address does not start with ', ' when address_1 is empty."""
        df = pd.DataFrame({"address_1": [""], "address_2": ["Suite 5"]})
        result = normalize_address(df)
        assert not result["address"].iloc[0].startswith(", ")

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": [""]})
        assert isinstance(normalize_address(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_phone
# ---------------------------------------------------------------------------

class TestNormalizePhone:
    def test_primary_phone_uses_free_call_when_present(self):
        """Tests that free_call takes priority over phone for primary_phone."""
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": ["1800123456"]})
        result = normalize_phone(df)
        assert result["primary_phone"].iloc[0] == "1800123456"

    def test_primary_phone_falls_back_to_phone_when_no_free_call(self):
        """Tests that phone is used as primary_phone when free_call is empty."""
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": [""]})
        result = normalize_phone(df)
        assert result["primary_phone"].iloc[0] == "0312345678"

    def test_primary_phone_empty_when_all_phone_fields_empty(self):
        """Tests that primary_phone is empty string when all phone fields are empty strings."""
        df = pd.DataFrame({"phone": [""], "phone_2": [""], "free_call": [""]})
        result = normalize_phone(df)
        assert result["primary_phone"].iloc[0] == ""

    def test_phone_display_includes_free_call_label(self):
        """Tests that the free_call number appears with a 'Free Call:' label."""
        df = pd.DataFrame({"phone": [""], "phone_2": [""], "free_call": ["1800123456"]})
        result = normalize_phone(df)
        assert "Free Call: 1800123456" in result["phone_display"].iloc[0]

    def test_phone_display_includes_phone_1_label(self):
        """Tests that the phone number appears with a 'Phone 1:' label."""
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": [""]})
        result = normalize_phone(df)
        assert "Phone 1: 0312345678" in result["phone_display"].iloc[0]

    def test_phone_display_includes_phone_2_label(self):
        """Tests that phone_2 appears with a 'Phone 2:' label."""
        df = pd.DataFrame({"phone": [""], "phone_2": ["0398765432"], "free_call": [""]})
        result = normalize_phone(df)
        assert "Phone 2: 0398765432" in result["phone_display"].iloc[0]

    def test_phone_display_joins_multiple_numbers_with_pipe(self):
        """Tests that multiple numbers in phone_display are separated by ' | '."""
        df = pd.DataFrame({
            "phone": ["0312345678"],
            "phone_2": ["0398765432"],
            "free_call": ["1800123456"],
        })
        result = normalize_phone(df)
        assert " | " in result["phone_display"].iloc[0]

    def test_phone_display_order_is_free_call_then_phone_then_phone_2(self):
        """Tests that phone_display lists numbers in the correct priority order."""
        df = pd.DataFrame({
            "phone": ["0312345678"],
            "phone_2": ["0398765432"],
            "free_call": ["1800123456"],
        })
        result = normalize_phone(df)
        display = result["phone_display"].iloc[0]
        free_call_pos = display.index("Free Call:")
        phone1_pos = display.index("Phone 1:")
        phone2_pos = display.index("Phone 2:")
        assert free_call_pos < phone1_pos < phone2_pos

    def test_phone_display_empty_when_all_fields_are_empty_strings(self):
        """Tests that phone_display is empty string when all phone fields are empty."""
        df = pd.DataFrame({"phone": [""], "phone_2": [""], "free_call": [""]})
        result = normalize_phone(df)
        assert result["phone_display"].iloc[0] == ""

    def test_nan_phone_inputs_produce_nan_strings_in_display(self):
        """Documents current behaviour: bool(np.nan) is True in Python, so NaN values
        are treated as truthy by the if-guards in _build_phone_list and end up included
        as the string 'nan' in phone_display.

        NOTE: This is a known implementation quirk. Callers should ensure phone
        columns are filled (e.g. with '') before calling normalize_phone, or the
        implementation should guard against NaN explicitly.
        """
        df = pd.DataFrame({"phone": [np.nan], "phone_2": [np.nan], "free_call": [np.nan]})
        result = normalize_phone(df)
        # All three NaN fields pass the truthiness check and are included as "nan"
        assert "Free Call: nan" in result["phone_display"].iloc[0]
        assert "Phone 1: nan" in result["phone_display"].iloc[0]
        assert "Phone 2: nan" in result["phone_display"].iloc[0]

    def test_drops_original_phone_columns(self):
        """Tests that phone, phone_2, and free_call are removed from the result."""
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": [""]})
        result = normalize_phone(df)
        assert "phone" not in result.columns
        assert "phone_2" not in result.columns
        assert "free_call" not in result.columns

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": [""]})
        assert isinstance(normalize_phone(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_social_media
# ---------------------------------------------------------------------------

class TestNormalizeSocialMedia:
    def test_fixes_missing_f_prefix(self):
        """Tests that 'acebook.com/...' is corrected to 'facebook.com/...'."""
        df = pd.DataFrame({"social_media": ["acebook.com/test"]})
        result = normalize_social_media(df)
        assert result["social_media"].iloc[0] == "facebook.com/test"

    def test_leaves_correct_facebook_url_unchanged(self):
        """Tests that a correctly-prefixed facebook.com URL is left unchanged."""
        df = pd.DataFrame({"social_media": ["https://facebook.com/test"]})
        result = normalize_social_media(df)
        assert result["social_media"].iloc[0] == "https://facebook.com/test"

    def test_leaves_non_facebook_urls_unchanged(self):
        """Tests that non-Facebook social media URLs (e.g. Twitter) are unaffected."""
        df = pd.DataFrame({"social_media": ["https://twitter.com/test"]})
        result = normalize_social_media(df)
        assert result["social_media"].iloc[0] == "https://twitter.com/test"

    def test_preserves_facebook_url_with_path(self):
        """Tests that a Facebook URL with a path is preserved exactly."""
        df = pd.DataFrame({"social_media": ["https://facebook.com/pages/test/123"]})
        result = normalize_social_media(df)
        assert result["social_media"].iloc[0] == "https://facebook.com/pages/test/123"

    def test_nan_values(self):
        """
        Verifies that NaN values are preserved as true nulls using 
        the pandas 'string' extension type, ensuring they are correctly
        handled by downstream clean_na_values functions.
        """
        df = pd.DataFrame({"social_media": [np.nan]})
        result = normalize_social_media(df)
        assert pd.isna(result["social_media"].iloc[0])

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame({"social_media": ["https://facebook.com/test"]})
        assert isinstance(normalize_social_media(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# format_time_string
# ---------------------------------------------------------------------------

class TestFormatTimeString:
    def test_returns_closed_unchanged(self):
        """Tests that the string 'Closed' is returned as-is."""
        assert format_time_string("Closed") == "Closed"

    def test_pads_single_digit_hour(self):
        """Tests that a single-digit hour is zero-padded."""
        assert format_time_string("9am") == "09:00am"

    def test_preserves_double_digit_hour(self):
        """Tests that a double-digit hour is left unchanged."""
        assert format_time_string("10am") == "10:00am"

    def test_formats_pm_time(self):
        """Tests that a PM time is zero-padded correctly."""
        assert format_time_string("5pm") == "05:00pm"

    def test_preserves_existing_dot_separated_minutes(self):
        """Tests that minutes given with a dot separator (5.00pm) are preserved."""
        assert format_time_string("5.00pm") == "05:00pm"

    def test_preserves_existing_colon_separated_minutes(self):
        """Tests that minutes given with a colon separator (9:30am) are preserved."""
        assert format_time_string("9:30am") == "09:30am"

    def test_preserves_non_round_minutes(self):
        """Tests that non-zero minutes (e.g. :30) are kept intact."""
        assert format_time_string("5.30pm") == "05:30pm"

    def test_formats_time_range(self):
        """Tests that a full time range is formatted correctly."""
        assert format_time_string("9am - 5pm") == "09:00am - 05:00pm"

    def test_inserts_space_around_dash_between_times(self):
        """Tests that a dash between two times gets spaces inserted."""
        assert format_time_string("12:00pm-05:00pm") == "12:00pm - 05:00pm"

    def test_case_insensitive_am(self):
        """Tests that uppercase AM is normalised to lowercase am."""
        assert format_time_string("9AM") == "09:00am"

    def test_case_insensitive_pm(self):
        """Tests that uppercase PM is normalised to lowercase pm."""
        assert format_time_string("5PM") == "05:00pm"


# ---------------------------------------------------------------------------
# clean_opening_hours_text
# ---------------------------------------------------------------------------

class TestCleanOpeningHoursText:
    def test_nan_returns_closed(self):
        """Tests that NaN is treated as no hours available and returns 'Closed'."""
        assert clean_opening_hours_text(np.nan) == "Closed"

    def test_closed_string_returns_closed(self):
        """Tests that the string 'Closed' is returned as 'Closed'."""
        assert clean_opening_hours_text("Closed") == "Closed"

    def test_closed_lowercase_returns_closed(self):
        """Tests that 'closed' (lowercase) is normalised to 'Closed'."""
        assert clean_opening_hours_text("closed") == "Closed"

    def test_closed_uppercase_returns_closed(self):
        """Tests that 'CLOSED' (uppercase) is normalised to 'Closed'."""
        assert clean_opening_hours_text("CLOSED") == "Closed"

    def test_normalizes_en_dash(self):
        """Tests that an en dash (U+2013) is replaced with a hyphen."""
        result = clean_opening_hours_text("9am \u2013 5pm")
        assert "\u2013" not in result
        assert "-" in result

    def test_normalizes_em_dash(self):
        """Tests that an em dash (U+2014) is replaced with a hyphen."""
        result = clean_opening_hours_text("9am \u2014 5pm")
        assert "\u2014" not in result
        assert "-" in result

    def test_normalizes_to_word(self):
        """Tests that ' to ' between times is replaced with ' - '."""
        result = clean_opening_hours_text("9am to 5pm")
        assert " to " not in result
        assert "-" in result

    def test_removes_extra_whitespace(self):
        """Tests that multiple consecutive spaces are collapsed to one."""
        result = clean_opening_hours_text("9am  -   5pm")
        assert "  " not in result

    def test_formats_time_within_text(self):
        """Tests that raw time values are formatted to hh:mm am/pm."""
        result = clean_opening_hours_text("9am - 5pm")
        assert "09:00am" in result
        assert "05:00pm" in result

    def test_returns_string(self):
        """Tests that the function always returns a string."""
        assert isinstance(clean_opening_hours_text("9am - 5pm"), str)


# ---------------------------------------------------------------------------
# transform_opening_hours
# ---------------------------------------------------------------------------

class TestTransformOpeningHours:
    def _make_hours_df(self, **overrides):
        row = {day: "9am - 5pm" for day in DAYS}
        row.update(overrides)
        return pd.DataFrame([row])

    def test_creates_opening_hours_column(self):
        """Tests that an 'opening_hours' column is created."""
        df = self._make_hours_df()
        result = transform_opening_hours(df)
        assert "opening_hours" in result.columns

    def test_opening_hours_is_dict(self):
        """Tests that the opening_hours value is a dict."""
        df = self._make_hours_df()
        result = transform_opening_hours(df)
        assert isinstance(result["opening_hours"].iloc[0], dict)

    def test_opening_hours_contains_all_days(self):
        """Tests that the dict contains an entry for every day including public_holidays."""
        df = self._make_hours_df()
        result = transform_opening_hours(df)
        hours = result["opening_hours"].iloc[0]
        for day in DAYS:
            assert day in hours

    def test_public_holidays_included_in_dict(self):
        """Tests that public_holidays is explicitly included in the output dict."""
        df = self._make_hours_df(public_holidays="10am - 2pm")
        result = transform_opening_hours(df)
        assert "public_holidays" in result["opening_hours"].iloc[0]

    def test_drops_original_day_columns(self):
        """Tests that the individual day columns are removed after collapsing."""
        df = self._make_hours_df()
        result = transform_opening_hours(df)
        for day in DAYS:
            assert day not in result.columns

    def test_nan_day_is_converted_to_closed(self):
        """Tests that a NaN value for a day is normalised to 'Closed'."""
        df = self._make_hours_df(sunday=np.nan)
        result = transform_opening_hours(df)
        assert result["opening_hours"].iloc[0]["sunday"] == "Closed"

    def test_time_strings_are_formatted(self):
        """Tests that raw time strings are formatted to hh:mm am/pm in the dict."""
        df = self._make_hours_df(monday="9am - 5pm")
        result = transform_opening_hours(df)
        assert result["opening_hours"].iloc[0]["monday"] == "09:00am - 05:00pm"

    def test_missing_day_column_is_not_included_in_dict(self):
        """Tests that days absent from the DataFrame are not included in the output dict."""
        # Only provide weekday columns, omit saturday/sunday/public_holidays
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        df = pd.DataFrame([{day: "9am - 5pm" for day in weekdays}])
        result = transform_opening_hours(df)
        hours = result["opening_hours"].iloc[0]
        assert "saturday" not in hours
        assert "sunday" not in hours
        assert "public_holidays" not in hours

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = self._make_hours_df()
        assert isinstance(transform_opening_hours(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# transform_categories
# ---------------------------------------------------------------------------

class TestTransformCategories:
    def _make_cat_df(self, cats):
        """cats: list of up to 6 values, padded with empty strings."""
        padded = (cats + [""] * 6)[:6]
        row = {f"category_{i+1}": v for i, v in enumerate(padded)}
        return pd.DataFrame([row])

    def test_collapses_categories_into_list(self):
        """Tests that the result is a list, not a string or other type."""
        df = self._make_cat_df(["Food", "Health"])
        result = transform_categories(df)
        assert isinstance(result["categories"].iloc[0], list)

    def test_includes_non_empty_categories(self):
        """Tests that valid category values are present in the list."""
        df = self._make_cat_df(["Food", "Health"])
        result = transform_categories(df)
        assert "Food" in result["categories"].iloc[0]
        assert "Health" in result["categories"].iloc[0]

    def test_excludes_empty_strings(self):
        """Tests that empty string values are not included in the category list."""
        df = self._make_cat_df(["Food", "", "Health"])
        result = transform_categories(df)
        assert "" not in result["categories"].iloc[0]

    def test_excludes_nan_values(self):
        """Tests that NaN values are not included in the category list."""
        df = self._make_cat_df(["Food", np.nan, "Health"])
        result = transform_categories(df)
        assert len([c for c in result["categories"].iloc[0] if pd.isna(c)]) == 0

    def test_excludes_none_values(self):
        """Tests that None values are not included in the category list."""
        df = self._make_cat_df(["Food", None, "Health"])
        result = transform_categories(df)
        assert None not in result["categories"].iloc[0]

    def test_excludes_whitespace_only_strings(self):
        """Tests that whitespace-only strings are stripped then excluded."""
        df = self._make_cat_df(["Food", "   ", "Health"])
        result = transform_categories(df)
        cats = result["categories"].iloc[0]
        assert not any(c.strip() == "" for c in cats)

    def test_deduplicates_categories(self):
        """Tests that duplicate category values appear only once."""
        df = self._make_cat_df(["Food", "Food", "Health"])
        result = transform_categories(df)
        cats = result["categories"].iloc[0]
        assert cats.count("Food") == 1

    def test_preserves_insertion_order(self):
        """Tests that the deduplication preserves original insertion order."""
        df = self._make_cat_df(["Food", "Health", "Housing"])
        result = transform_categories(df)
        assert result["categories"].iloc[0] == ["Food", "Health", "Housing"]

    def test_all_empty_gives_empty_list(self):
        """Tests that a row with all empty category columns returns an empty list."""
        df = self._make_cat_df([])
        result = transform_categories(df)
        assert result["categories"].iloc[0] == []

    def test_strips_whitespace_from_category_values(self):
        """Tests that leading/trailing whitespace is stripped from each category."""
        df = self._make_cat_df(["  Food  ", " Health "])
        result = transform_categories(df)
        assert "Food" in result["categories"].iloc[0]
        assert "Health" in result["categories"].iloc[0]

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = self._make_cat_df(["Food"])
        assert isinstance(transform_categories(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# rename_columns (melbourne-specific mapping)
# ---------------------------------------------------------------------------

class TestRenameColumns:
    def test_renames_what_to_description(self):
        """Tests that 'what' is renamed to 'description'."""
        df = pd.DataFrame(columns=["what"])
        result = rename_columns(df, MEL_COLUMN_MAP)
        assert "description" in result.columns
        assert "what" not in result.columns

    def test_renames_who_to_target_audience(self):
        """Tests that 'who' is renamed to 'target_audience'."""
        df = pd.DataFrame(columns=["who"])
        result = rename_columns(df, MEL_COLUMN_MAP)
        assert "target_audience" in result.columns
        assert "who" not in result.columns

    def test_both_mel_columns_renamed_in_one_call(self):
        """Tests that both 'what' and 'who' are renamed atomically."""
        df = pd.DataFrame(columns=["what", "who"])
        result = rename_columns(df, MEL_COLUMN_MAP)
        assert "description" in result.columns
        assert "target_audience" in result.columns
        assert "what" not in result.columns
        assert "who" not in result.columns

    def test_unrelated_columns_are_unchanged(self):
        """Tests that columns outside the map are left as-is."""
        df = pd.DataFrame(columns=["what", "who", "name", "suburb"])
        result = rename_columns(df, MEL_COLUMN_MAP)
        assert "name" in result.columns
        assert "suburb" in result.columns

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        df = pd.DataFrame(columns=["what", "who"])
        assert isinstance(rename_columns(df, MEL_COLUMN_MAP), pd.DataFrame)


# ---------------------------------------------------------------------------
# wrangle_melbourne (integration)
# ---------------------------------------------------------------------------

class TestWrangleMelbourne:
    def test_returns_dataframe(self):
        """Tests that the pipeline returns a DataFrame."""
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        assert isinstance(result, pd.DataFrame)

    def test_source_column_is_city_of_melbourne(self):
        """Tests that the 'source' column is set to 'City of Melbourne' for every row."""
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        assert "source" in result.columns
        assert all(result["source"] == "City of Melbourne")

    def test_output_has_expected_columns(self):
        """Tests that all required schema columns are present in the output."""
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        expected = [
            "name", "description", "target_audience", "address", "suburb",
            "primary_phone", "phone_display", "email", "website", "social_media",
            "opening_hours", "cost", "tram_routes", "bus_routes",
            "nearest_train_station", "categories", "longitude", "latitude", "source",
        ]
        for col in expected:
            assert col in result.columns, f"Missing column: {col}"

    def test_rows_with_missing_names_are_removed(self):
        """Tests that rows with NaN names are dropped end-to-end."""
        df = pd.concat([
            make_full_melbourne_df(name="Valid Service"),
            make_full_melbourne_df(name=np.nan),
        ], ignore_index=True)
        result = wrangle_melbourne(df)
        assert len(result) == 1
        assert result["name"].iloc[0] == "Valid Service"

    def test_what_renamed_to_description(self):
        """Tests that the 'what' column value is accessible as 'description'."""
        df = make_full_melbourne_df(what="Crisis support")
        result = wrangle_melbourne(df)
        assert "description" in result.columns
        assert result["description"].iloc[0] == "Crisis support"

    def test_who_renamed_to_target_audience(self):
        """Tests that the 'who' column value is accessible as 'target_audience'."""
        df = make_full_melbourne_df(who="Families")
        result = wrangle_melbourne(df)
        assert "target_audience" in result.columns
        assert result["target_audience"].iloc[0] == "Families"

    def test_address_parts_combined(self):
        """Tests that address_1 and address_2 are combined with ', ' end-to-end."""
        df = make_full_melbourne_df(address_1="123 Main St", address_2="Level 2")
        result = wrangle_melbourne(df)
        assert result["address"].iloc[0] == "123 Main St, Level 2"

    def test_coordinates_are_numeric(self):
        """Tests that latitude and longitude are cast to float dtype."""
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        assert result["latitude"].dtype in [float, np.float64]
        assert result["longitude"].dtype in [float, np.float64]

    def test_invalid_coordinates_become_nan(self):
        """Tests that non-numeric coordinate strings are coerced to NaN."""
        df = make_full_melbourne_df(latitude="invalid", longitude="bad")
        result = wrangle_melbourne(df)
        assert pd.isna(result["latitude"].iloc[0])
        assert pd.isna(result["longitude"].iloc[0])

    def test_http_website_upgraded_to_https(self):
        """Tests that an http:// website URL is normalised to https://."""
        df = make_full_melbourne_df(website="http://example.com")
        result = wrangle_melbourne(df)
        assert result["website"].iloc[0] == "https://example.com"

    def test_opening_hours_is_dict(self):
        """Tests that opening_hours is a dict after the full pipeline."""
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        assert isinstance(result["opening_hours"].iloc[0], dict)

    def test_opening_hours_dict_contains_all_days(self):
        """Tests that the opening_hours dict contains all 8 expected keys."""
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        hours = result["opening_hours"].iloc[0]
        for day in DAYS:
            assert day in hours, f"Missing day in opening_hours: {day}"

    def test_categories_is_list(self):
        """Tests that categories is a list after the full pipeline."""
        df = make_full_melbourne_df(**{"category_1": "Food", "category_2": "Health"})
        result = wrangle_melbourne(df)
        assert isinstance(result["categories"].iloc[0], list)

    def test_categories_values_are_correct(self):
        """Tests that non-empty category values are preserved end-to-end."""
        df = make_full_melbourne_df(**{"category_1": "Food", "category_2": "Health"})
        result = wrangle_melbourne(df)
        cats = result["categories"].iloc[0]
        assert "Food" in cats
        assert "Health" in cats

    def test_sentinel_values_become_nan(self):
        """Tests that common sentinel strings (N/A, NULL) are converted to NaN."""
        df = make_full_melbourne_df(email="N/A", social_media="NULL")
        result = wrangle_melbourne(df)
        assert pd.isna(result["email"].iloc[0])
        assert pd.isna(result["social_media"].iloc[0])

    def test_does_not_mutate_input(self):
        """Tests that the original input DataFrame is not modified by the pipeline."""
        df = make_full_melbourne_df()
        original_columns = list(df.columns)
        original_name = df["name"].iloc[0]
        wrangle_melbourne(df)
        assert list(df.columns) == original_columns
        assert df["name"].iloc[0] == original_name

    def test_empty_dataframe_after_name_filter_returns_empty(self):
        """Tests that filtering all rows returns an empty DataFrame (not an error)."""
        df = make_full_melbourne_df(name=np.nan)
        result = wrangle_melbourne(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0