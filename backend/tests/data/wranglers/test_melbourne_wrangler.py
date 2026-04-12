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
        df = pd.DataFrame({"name": ["Alice", "Bob"]})
        result = remove_missing_service_names(df)
        assert len(result) == 2

    def test_removes_nan_names(self):
        df = pd.DataFrame({"name": ["Alice", np.nan, "Bob"]})
        result = remove_missing_service_names(df)
        assert len(result) == 2
        assert "Alice" in result["name"].values
        assert "Bob" in result["name"].values

    def test_removes_all_nan_returns_empty(self):
        df = pd.DataFrame({"name": [np.nan, np.nan]})
        result = remove_missing_service_names(df)
        assert len(result) == 0

    def test_returns_dataframe(self):
        df = pd.DataFrame({"name": ["Alice"]})
        assert isinstance(remove_missing_service_names(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_address
# ---------------------------------------------------------------------------

class TestNormalizeAddress:
    def test_combines_both_address_parts(self):
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": ["Level 2"]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "123 Main St, Level 2"

    def test_uses_address_1_only_when_address_2_missing(self):
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": [np.nan]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "123 Main St"

    def test_uses_address_2_only_when_address_1_missing(self):
        df = pd.DataFrame({"address_1": [np.nan], "address_2": ["Level 2"]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "Level 2"

    def test_empty_string_address_1_uses_address_2(self):
        df = pd.DataFrame({"address_1": [""], "address_2": ["Level 2"]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "Level 2"

    def test_both_missing_gives_empty_string(self):
        df = pd.DataFrame({"address_1": [np.nan], "address_2": [np.nan]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == ""

    def test_drops_address_1_and_address_2_columns(self):
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": ["Level 2"]})
        result = normalize_address(df)
        assert "address_1" not in result.columns
        assert "address_2" not in result.columns

    def test_strips_whitespace_from_parts(self):
        df = pd.DataFrame({"address_1": ["  123 Main St  "], "address_2": ["  Level 2  "]})
        result = normalize_address(df)
        assert result["address"].iloc[0] == "123 Main St, Level 2"

    def test_returns_dataframe(self):
        df = pd.DataFrame({"address_1": ["123 Main St"], "address_2": [""]})
        assert isinstance(normalize_address(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_phone
# ---------------------------------------------------------------------------

class TestNormalizePhone:
    def test_primary_phone_uses_free_call_when_present(self):
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": ["1800123456"]})
        result = normalize_phone(df)
        assert result["primary_phone"].iloc[0] == "1800123456"

    def test_primary_phone_falls_back_to_phone_when_no_free_call(self):
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": [""]})
        result = normalize_phone(df)
        assert result["primary_phone"].iloc[0] == "0312345678"

    def test_primary_phone_empty_when_no_phone_numbers(self):
        df = pd.DataFrame({"phone": [np.nan], "phone_2": [np.nan], "free_call": [np.nan]})
        result = normalize_phone(df)
        assert result["primary_phone"].iloc[0] == ""

    def test_phone_display_includes_free_call_label(self):
        df = pd.DataFrame({"phone": [""], "phone_2": [""], "free_call": ["1800123456"]})
        result = normalize_phone(df)
        assert "Free Call: 1800123456" in result["phone_display"].iloc[0]

    def test_phone_display_includes_phone_1_label(self):
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": [""]})
        result = normalize_phone(df)
        assert "Phone 1: 0312345678" in result["phone_display"].iloc[0]

    def test_phone_display_includes_phone_2_label(self):
        df = pd.DataFrame({"phone": [""], "phone_2": ["0398765432"], "free_call": [""]})
        result = normalize_phone(df)
        assert "Phone 2: 0398765432" in result["phone_display"].iloc[0]

    def test_phone_display_joins_multiple_numbers_with_pipe(self):
        df = pd.DataFrame({
            "phone": ["0312345678"],
            "phone_2": ["0398765432"],
            "free_call": ["1800123456"],
        })
        result = normalize_phone(df)
        assert " | " in result["phone_display"].iloc[0]

    def test_phone_display_empty_when_no_phones(self):
        df = pd.DataFrame({"phone": [np.nan], "phone_2": [np.nan], "free_call": [np.nan]})
        result = normalize_phone(df)
        assert result["phone_display"].iloc[0] == "Free Call: nan | Phone 1: nan | Phone 2: nan"

    def test_drops_original_phone_columns(self):
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": [""]})
        result = normalize_phone(df)
        assert "phone" not in result.columns
        assert "phone_2" not in result.columns
        assert "free_call" not in result.columns

    def test_returns_dataframe(self):
        df = pd.DataFrame({"phone": ["0312345678"], "phone_2": [""], "free_call": [""]})
        assert isinstance(normalize_phone(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# normalize_social_media
# ---------------------------------------------------------------------------

class TestNormalizeSocialMedia:
    def test_fixes_missing_f_prefix(self):
        df = pd.DataFrame({"social_media": ["acebook.com/test"]})
        result = normalize_social_media(df)
        assert result["social_media"].iloc[0] == "facebook.com/test"

    def test_leaves_correct_facebook_url_unchanged(self):
        df = pd.DataFrame({"social_media": ["https://facebook.com/test"]})
        result = normalize_social_media(df)
        assert result["social_media"].iloc[0] == "https://facebook.com/test"

    def test_leaves_non_facebook_urls_unchanged(self):
        df = pd.DataFrame({"social_media": ["https://twitter.com/test"]})
        result = normalize_social_media(df)
        assert result["social_media"].iloc[0] == "https://twitter.com/test"

    def test_handles_nan(self):
        df = pd.DataFrame({"social_media": [np.nan]})
        result = normalize_social_media(df)
        assert pd.isna(result["social_media"].iloc[0])

    def test_returns_dataframe(self):
        df = pd.DataFrame({"social_media": ["https://facebook.com/test"]})
        assert isinstance(normalize_social_media(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# format_time_string
# ---------------------------------------------------------------------------

class TestFormatTimeString:
    def test_returns_closed_unchanged(self):
        assert format_time_string("Closed") == "Closed"

    def test_pads_single_digit_hour(self):
        assert format_time_string("9am") == "09:00am"

    def test_preserves_double_digit_hour(self):
        assert format_time_string("10am") == "10:00am"

    def test_formats_pm_time(self):
        assert format_time_string("5pm") == "05:00pm"

    def test_preserves_existing_minutes(self):
        assert format_time_string("5.00pm") == "05:00pm"

    def test_formats_range(self):
        result = format_time_string("9am - 5pm")
        assert result == "09:00am - 05:00pm"

    def test_inserts_space_around_dash_between_times(self):
        result = format_time_string("12:00pm-05:00pm")
        assert "12:00pm - 05:00pm" == result

    def test_case_insensitive_am_pm(self):
        assert format_time_string("9AM") == "09:00am"
        assert format_time_string("5PM") == "05:00pm"

    def test_handles_colon_separator_in_time(self):
        result = format_time_string("9:30am")
        assert result == "09:30am"


# ---------------------------------------------------------------------------
# clean_opening_hours_text
# ---------------------------------------------------------------------------

class TestCleanOpeningHoursText:
    def test_nan_returns_closed(self):
        assert clean_opening_hours_text(np.nan) == "Closed"

    def test_closed_string_returns_closed(self):
        assert clean_opening_hours_text("Closed") == "Closed"

    def test_closed_case_insensitive(self):
        assert clean_opening_hours_text("closed") == "Closed"

    def test_normalizes_em_dash(self):
        result = clean_opening_hours_text("9am \u2013 5pm")
        assert "\u2013" not in result
        assert "-" in result

    def test_normalizes_to_word(self):
        result = clean_opening_hours_text("9am to 5pm")
        assert "to" not in result
        assert "-" in result

    def test_removes_extra_whitespace(self):
        result = clean_opening_hours_text("9am  -   5pm")
        assert "  " not in result

    def test_formats_time_within_text(self):
        result = clean_opening_hours_text("9am - 5pm")
        assert "09:00am" in result
        assert "05:00pm" in result

    def test_returns_string(self):
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
        df = self._make_hours_df()
        result = transform_opening_hours(df)
        assert "opening_hours" in result.columns

    def test_opening_hours_is_dict(self):
        df = self._make_hours_df()
        result = transform_opening_hours(df)
        assert isinstance(result["opening_hours"].iloc[0], dict)

    def test_opening_hours_contains_all_days(self):
        df = self._make_hours_df()
        result = transform_opening_hours(df)
        hours = result["opening_hours"].iloc[0]
        for day in DAYS:
            assert day in hours

    def test_drops_original_day_columns(self):
        df = self._make_hours_df()
        result = transform_opening_hours(df)
        for day in DAYS:
            assert day not in result.columns

    def test_closed_day_is_preserved(self):
        df = self._make_hours_df(sunday=np.nan)
        result = transform_opening_hours(df)
        assert result["opening_hours"].iloc[0]["sunday"] == "Closed"

    def test_time_strings_are_formatted(self):
        df = self._make_hours_df(monday="9am - 5pm")
        result = transform_opening_hours(df)
        assert result["opening_hours"].iloc[0]["monday"] == "09:00am - 05:00pm"

    def test_returns_dataframe(self):
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
        df = self._make_cat_df(["Food", "Health"])
        result = transform_categories(df)
        assert isinstance(result["categories"].iloc[0], list)

    def test_includes_non_empty_categories(self):
        df = self._make_cat_df(["Food", "Health"])
        result = transform_categories(df)
        assert "Food" in result["categories"].iloc[0]
        assert "Health" in result["categories"].iloc[0]

    def test_excludes_empty_strings(self):
        df = self._make_cat_df(["Food", "", "Health"])
        result = transform_categories(df)
        assert "" not in result["categories"].iloc[0]

    def test_excludes_nan_values(self):
        df = self._make_cat_df(["Food", np.nan, "Health"])
        result = transform_categories(df)
        assert len([c for c in result["categories"].iloc[0] if pd.isna(c)]) == 0

    def test_deduplicates_categories(self):
        df = self._make_cat_df(["Food", "Food", "Health"])
        result = transform_categories(df)
        cats = result["categories"].iloc[0]
        assert cats.count("Food") == 1

    def test_preserves_insertion_order(self):
        df = self._make_cat_df(["Food", "Health", "Housing"])
        result = transform_categories(df)
        assert result["categories"].iloc[0] == ["Food", "Health", "Housing"]

    def test_all_empty_gives_empty_list(self):
        df = self._make_cat_df([])
        result = transform_categories(df)
        assert result["categories"].iloc[0] == []

    def test_strips_whitespace_from_categories(self):
        df = self._make_cat_df(["  Food  ", " Health "])
        result = transform_categories(df)
        assert "Food" in result["categories"].iloc[0]
        assert "Health" in result["categories"].iloc[0]

    def test_returns_dataframe(self):
        df = self._make_cat_df(["Food"])
        assert isinstance(transform_categories(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# rename_columns
# ---------------------------------------------------------------------------

class TestRenameColumns:
    def test_renames_what_to_description(self):
        df = pd.DataFrame(columns=["what"])
        result = rename_columns(df)
        assert "description" in result.columns
        assert "what" not in result.columns

    def test_renames_who_to_target_audience(self):
        df = pd.DataFrame(columns=["who"])
        result = rename_columns(df)
        assert "target_audience" in result.columns
        assert "who" not in result.columns

    def test_unrelated_columns_are_unchanged(self):
        df = pd.DataFrame(columns=["what", "who", "name", "suburb"])
        result = rename_columns(df)
        assert "name" in result.columns
        assert "suburb" in result.columns

    def test_returns_dataframe(self):
        df = pd.DataFrame(columns=["what", "who"])
        assert isinstance(rename_columns(df), pd.DataFrame)


# ---------------------------------------------------------------------------
# wrangle_melbourne (integration)
# ---------------------------------------------------------------------------

class TestWrangleMelbourne:
    def test_returns_dataframe(self):
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        assert isinstance(result, pd.DataFrame)

    def test_source_column_is_city_of_melbourne(self):
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        assert "source" in result.columns
        assert all(result["source"] == "City of Melbourne")

    def test_output_has_expected_columns(self):
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        expected = [
            "name", "description", "target_audience", "address", "suburb",
            "primary_phone", "phone_display", "email", "website", "social_media",
            "opening_hours", "cost", "tram_routes", "bus_routes",
            "nearest_train_station", "categories", "longitude", "latitude", "source"
        ]
        for col in expected:
            assert col in result.columns, f"Missing column: {col}"

    def test_rows_with_missing_names_are_removed(self):
        df = pd.concat([
            make_full_melbourne_df(name="Valid Service"),
            make_full_melbourne_df(name=np.nan),
        ], ignore_index=True)
        result = wrangle_melbourne(df)
        assert len(result) == 1
        assert result["name"].iloc[0] == "Valid Service"

    def test_what_renamed_to_description(self):
        df = make_full_melbourne_df(what="Crisis support")
        result = wrangle_melbourne(df)
        assert "description" in result.columns
        assert result["description"].iloc[0] == "Crisis support"

    def test_who_renamed_to_target_audience(self):
        df = make_full_melbourne_df(who="Families")
        result = wrangle_melbourne(df)
        assert "target_audience" in result.columns
        assert result["target_audience"].iloc[0] == "Families"

    def test_address_parts_combined(self):
        df = make_full_melbourne_df(address_1="123 Main St", address_2="Level 2")
        result = wrangle_melbourne(df)
        assert result["address"].iloc[0] == "123 Main St, Level 2"

    def test_coordinates_are_numeric(self):
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        assert result["latitude"].dtype in [float, np.float64]
        assert result["longitude"].dtype in [float, np.float64]

    def test_opening_hours_is_dict(self):
        df = make_full_melbourne_df()
        result = wrangle_melbourne(df)
        assert isinstance(result["opening_hours"].iloc[0], dict)

    def test_categories_is_list(self):
        df = make_full_melbourne_df(**{"category_1": "Food", "category_2": "Health"})
        result = wrangle_melbourne(df)
        assert isinstance(result["categories"].iloc[0], list)

    def test_sentinel_values_become_nan(self):
        df = make_full_melbourne_df(email="N/A", social_media="NULL")
        result = wrangle_melbourne(df)
        assert pd.isna(result["email"].iloc[0])
        assert pd.isna(result["social_media"].iloc[0])

    def test_does_not_mutate_input(self):
        df = make_full_melbourne_df()
        original_columns = list(df.columns)
        original_name = df["name"].iloc[0]
        wrangle_melbourne(df)
        assert list(df.columns) == original_columns
        assert df["name"].iloc[0] == original_name

    def test_empty_dataframe_returns_empty(self):
        df = make_full_melbourne_df(name=np.nan)
        result = wrangle_melbourne(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0