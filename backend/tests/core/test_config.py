import os

from src.core.config import Settings, settings


class TestMelbourneSettings:
    def test_settings_default_melbourne_api_url(self):
        """Tests the default Melbourne API URL."""
        s = Settings()
        assert s.MELBOURNE_API_URL == (
            "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/"
            "free-and-cheap-support-services-with-opening-hours-public-transport-and-parking-"
            "/exports/csv"
        )

    def test_settings_default_melbourne_sep(self):
        """Tests the default Melbourne separator is semicolon (;)."""
        s = Settings()
        assert s.MELBOURNE_SEP == ";"

    def test_settings_default_melbourne_raw_path(self):
        """Tests the default Melbourne raw local path."""
        s = Settings()
        assert s.MELBOURNE_RAW_PATH == os.path.join(s.RAW_DATA_DIR, "melbourne_raw.csv")


class TestOtherDataSettings:
    def test_settings_default_other_data_url(self):
        """Tests the default other data URL."""
        s = Settings()
        assert s.OTHER_DATA_URL == (
            "https://data.gov.au/data/dataset/d667403f-2016-463f-bb0a-3087ae67c57f/resource/"
            "0e32d958-3796-4dca-8312-489ef7a610f6/download/"
            "emergency-relief-provider-outlets-october-2016.csv"
        )

    def test_settings_default_other_sep(self):
        """Tests the default other data separator is comma (,)."""
        s = Settings()
        assert s.OTHER_SEP == ","

    def test_settings_default_datagov_raw_path(self):
        """Tests the default other data raw local path."""
        s = Settings()
        assert s.DATAGOV_RAW_PATH == os.path.join(s.RAW_DATA_DIR, "datagov_raw.csv")


class TestEmergencyServiceSettings:
    def test_settings_default_emergency_included_cols_is_list(self):
        """Tests that EMERGENCY_INCLUDED_COLS is a list."""
        s = Settings()
        assert isinstance(s.EMERGENCY_INCLUDED_COLS, list)

    def test_settings_default_emergency_included_cols_not_empty(self):
        """Tests that EMERGENCY_INCLUDED_COLS is non-empty."""
        s = Settings()
        assert len(s.EMERGENCY_INCLUDED_COLS) > 0

    def test_settings_default_emergency_included_cols_contains_required_fields(self):
        """Tests that EMERGENCY_INCLUDED_COLS contains all required fields."""
        s = Settings()
        required_fields = [
            "name", "description", "target_audience", "address", "suburb",
            "primary_phone", "phone_display", "email", "website", "social_media",
            "opening_hours", "cost", "tram_routes", "bus_routes",
            "nearest_train_station", "categories", "longitude", "latitude",
        ]
        for field in required_fields:
            assert field in s.EMERGENCY_INCLUDED_COLS, (
                f"Expected '{field}' in EMERGENCY_INCLUDED_COLS"
            )

    def test_settings_default_emergency_included_cols_has_correct_length(self):
        """Tests that EMERGENCY_INCLUDED_COLS has the expected number of columns."""
        s = Settings()
        assert len(s.EMERGENCY_INCLUDED_COLS) == 18

    def test_settings_default_emergency_included_cols_contain_coordinate_fields(self):
        """Tests that coordinate fields are included for geospatial use."""
        s = Settings()
        assert "latitude" in s.EMERGENCY_INCLUDED_COLS
        assert "longitude" in s.EMERGENCY_INCLUDED_COLS


class TestFoodInsecuritySettings:
    def test_settings_default_food_insecurity_url(self):
        """Tests the default food insecurity data URL."""
        s = Settings()
        assert s.FOOD_INSECURITY_URL == (
            "https://www.dropbox.com/scl/fi/8dj6f9knai1pvc2kuxbq8/"
            "food_insecurity_data.xlsx"
            "?rlkey=jxyaf0viyy84fnev3t3m0atod&st=7vc78ayw&dl=1"
        )

    def test_settings_default_food_insecurity_sheet_name(self):
        """Tests the default food insecurity sheet name defaults to index 0."""
        s = Settings()
        assert s.FOOD_INSECURITY_SHEET_NAME == 0

    def test_settings_default_food_insecurity_raw_path(self):
        """Tests the default food insecurity raw local path."""
        s = Settings()
        assert s.FOOD_INSECURITY_RAW_PATH == os.path.join(s.RAW_DATA_DIR, "food_insecurity_raw.xlsx")

    def test_settings_default_selected_regions_is_list(self):
        """Tests that SELECTED_REGIONS is a list."""
        s = Settings()
        assert isinstance(s.SELECTED_REGIONS, list)

    def test_settings_default_selected_regions_not_empty(self):
        """Tests that SELECTED_REGIONS is non-empty."""
        s = Settings()
        assert len(s.SELECTED_REGIONS) > 0

    def test_settings_default_selected_regions_contains_expected_regions(self):
        """Tests that SELECTED_REGIONS contains all expected Victorian PHU regions."""
        s = Settings()
        expected_regions = [
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
        for region in expected_regions:
            assert region in s.SELECTED_REGIONS, (
                f"Expected region '{region}' in SELECTED_REGIONS"
            )

    def test_settings_default_selected_regions_has_correct_length(self):
        """Tests that SELECTED_REGIONS has the expected number of regions."""
        s = Settings()
        assert len(s.SELECTED_REGIONS) == 9


class TestBoundarySettings:
    def test_settings_default_vicgov_boundary_url(self):
        """Tests the default VicGov boundary URL."""
        s = Settings()
        assert s.VICGOV_BOUNDARY_URL == (
            "https://www.dropbox.com/scl/fo/qr05jgmxcdbdn0boev1w7/"
            "ANUNe4e7aGOSzulbbzNLqX4"
            "?rlkey=8sna6zqjt5xrw52pf2jv37r0c&st=c3sn5k9r&dl=1"
        )

    def test_settings_default_viclga_boundary_url(self):
        """Tests the default VicLGA boundary URL."""
        s = Settings()
        assert s.VICLGA_BOUNDARY_URL == (
            "https://data.gov.au/data/dataset/bdf92691-c6fe-42b9-a0e2-a4cd716fa811/resource/"
            "95079e79-37d0-43c7-9f80-10eda1b0d05f/download/vic_lga_gda2020.zip"
        )

    def test_settings_default_vicgov_boundary_raw_path(self):
        """Tests the default VicGov boundary raw local path."""
        s = Settings()
        assert s.VICGOV_BOUNDARY_RAW_PATH == os.path.join(s.RAW_DATA_DIR, "vicgov_boundary_raw.csv")

    def test_settings_default_viclga_boundary_raw_zip_path(self):
        """Tests the default VicLGA boundary raw zip local path."""
        s = Settings()
        assert s.VICLGA_BOUNDARY_RAW_ZIP_PATH == os.path.join(s.RAW_DATA_DIR, "viclga_boundary_raw.zip")

    def test_settings_default_viclga_boundary_raw_unzip_path(self):
        """Tests the default VicLGA boundary raw unzip directory path."""
        s = Settings()
        assert s.VICLGA_BOUNDARY_RAW_UNZIP_PATH == os.path.join(s.RAW_DATA_DIR, "viclga_boundary_raw")

    def test_settings_default_viclga_boundary_raw_path(self):
        """Tests the default VicLGA boundary raw CSV path is nested under the unzip dir."""
        s = Settings()
        assert s.VICLGA_BOUNDARY_RAW_PATH == os.path.join(s.VICLGA_BOUNDARY_RAW_UNZIP_PATH, "vic_lga.csv")

    def test_settings_viclga_boundary_raw_path_is_nested_under_unzip_path(self):
        """Tests that VICLGA_BOUNDARY_RAW_PATH is a child of VICLGA_BOUNDARY_RAW_UNZIP_PATH."""
        s = Settings()
        assert s.VICLGA_BOUNDARY_RAW_PATH.startswith(s.VICLGA_BOUNDARY_RAW_UNZIP_PATH)


class TestRawDataDirSettings:
    def test_settings_default_raw_data_dir(self):
        """Tests the default raw data directory."""
        s = Settings()
        assert s.RAW_DATA_DIR == "src/data/raw"

    def test_settings_all_raw_paths_are_under_raw_data_dir(self):
        """Tests that all raw file paths are rooted under RAW_DATA_DIR."""
        s = Settings()
        raw_paths = [
            s.MELBOURNE_RAW_PATH,
            s.DATAGOV_RAW_PATH,
            s.FOOD_INSECURITY_RAW_PATH,
            s.VICGOV_BOUNDARY_RAW_PATH,
            s.VICLGA_BOUNDARY_RAW_ZIP_PATH,
            s.VICLGA_BOUNDARY_RAW_UNZIP_PATH,
            s.VICLGA_BOUNDARY_RAW_PATH,
        ]
        for path in raw_paths:
            assert path.startswith(s.RAW_DATA_DIR), (
                f"Expected '{path}' to start with RAW_DATA_DIR ('{s.RAW_DATA_DIR}')"
            )


class TestSettingsEnvOverrides:
    def test_settings_can_be_overridden_with_env_vars(self, monkeypatch):
        """Tests that separator settings can be overridden with environment variables."""
        monkeypatch.setenv("MELBOURNE_SEP", ",")
        monkeypatch.setenv("OTHER_SEP", ";")
        s = Settings()
        assert s.MELBOURNE_SEP == ","
        assert s.OTHER_SEP == ";"

    def test_settings_override_url(self, monkeypatch):
        """Tests that Melbourne API URL can be overridden with an environment variable."""
        custom_url = "https://custom.api.example.com/data.csv"
        monkeypatch.setenv("MELBOURNE_API_URL", custom_url)
        s = Settings()
        assert s.MELBOURNE_API_URL == custom_url

    def test_settings_override_file_paths(self, monkeypatch):
        """Tests that raw file paths can be overridden with environment variables."""
        monkeypatch.setenv("MELBOURNE_RAW_PATH", os.path.join("src/data/raw", "melbourne.csv"))
        monkeypatch.setenv("DATAGOV_RAW_PATH", os.path.join("src/data/raw", "datagov.csv"))
        s = Settings()
        assert s.MELBOURNE_RAW_PATH == os.path.join(s.RAW_DATA_DIR, "melbourne.csv")
        assert s.DATAGOV_RAW_PATH == os.path.join(s.RAW_DATA_DIR, "datagov.csv")

    def test_settings_override_food_insecurity_sheet_name(self, monkeypatch):
        """Tests that FOOD_INSECURITY_SHEET_NAME can be overridden."""
        monkeypatch.setenv("FOOD_INSECURITY_SHEET_NAME", "Sheet1")
        s = Settings()
        assert s.FOOD_INSECURITY_SHEET_NAME == "Sheet1"

    def test_settings_override_raw_data_dir_does_not_affect_already_computed_paths(
        self, monkeypatch
    ):
        """Tests that overriding RAW_DATA_DIR alone does not retroactively change
        computed paths like MELBOURNE_RAW_PATH, since those are set at class definition time."""
        monkeypatch.setenv("RAW_DATA_DIR", "src/data/raw")
        s = Settings()
        assert s.RAW_DATA_DIR == "src/data/raw"
        assert s.MELBOURNE_RAW_PATH == os.path.join(s.RAW_DATA_DIR, "melbourne_raw.csv")


class TestGlobalSettingsInstance:
    def test_global_settings_instance_is_settings_type(self):
        """Tests the global settings instance is of type Settings."""
        assert isinstance(settings, Settings)

    def test_global_settings_instance_has_correct_separator_defaults(self):
        """Tests the global settings instance has the correct separator defaults."""
        assert settings.MELBOURNE_SEP == ";"
        assert settings.OTHER_SEP == ","

    def test_global_settings_instance_has_correct_raw_data_dir(self):
        """Tests the global settings instance has the correct default raw data dir."""
        assert settings.RAW_DATA_DIR == "src/data/raw"

    def test_global_settings_instance_has_correct_selected_regions_count(self):
        """Tests the global settings instance has 9 selected PHU regions."""
        assert len(settings.SELECTED_REGIONS) == 9

    def test_global_settings_instance_has_correct_emergency_cols_count(self):
        """Tests the global settings instance has 18 emergency included columns."""
        assert len(settings.EMERGENCY_INCLUDED_COLS) == 18