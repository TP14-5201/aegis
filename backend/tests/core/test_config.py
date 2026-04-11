from src.core.config import Settings, settings


class TestSettings:
    def test_settings_default_melbourne_api_url(self):
        s = Settings()
        assert s.MELBOURNE_API_URL == (
            "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/"
            "free-and-cheap-support-services-with-opening-hours-public-transport-and-parking-"
            "/exports/csv"
        )

    def test_settings_default_melbourne_sep(self):
        s = Settings()
        assert s.MELBOURNE_SEP == ";"

    def test_settings_default_other_data_url(self):
        s = Settings()
        assert s.OTHER_DATA_URL == (
            "https://data.gov.au/data/dataset/d667403f-2016-463f-bb0a-3087ae67c57f/resource/"
            "0e32d958-3796-4dca-8312-489ef7a610f6/download/"
            "emergency-relief-provider-outlets-october-2016.csv"
        )

    def test_settings_default_other_sep(self):
        s = Settings()
        assert s.OTHER_SEP == ","

    def test_settings_default_melbourne_raw_path(self):
        s = Settings()
        assert s.MELBOURNE_RAW_PATH == "src/data/raw/melbourne_raw.csv"

    def test_settings_default_datagov_raw_path(self):
        s = Settings()
        assert s.DATAGOV_RAW_PATH == "src/data/raw/datagov_raw.csv"

    def test_settings_can_be_overridden_with_env_vars(self, monkeypatch):
        monkeypatch.setenv("MELBOURNE_SEP", ",")
        monkeypatch.setenv("OTHER_SEP", ";")
        s = Settings()
        assert s.MELBOURNE_SEP == ","
        assert s.OTHER_SEP == ";"

    def test_settings_override_url(self, monkeypatch):
        custom_url = "https://custom.api.example.com/data.csv"
        monkeypatch.setenv("MELBOURNE_API_URL", custom_url)
        s = Settings()
        assert s.MELBOURNE_API_URL == custom_url

    def test_settings_override_file_paths(self, monkeypatch):
        monkeypatch.setenv("MELBOURNE_RAW_PATH", "custom/path/melbourne.csv")
        monkeypatch.setenv("DATAGOV_RAW_PATH", "custom/path/datagov.csv")
        s = Settings()
        assert s.MELBOURNE_RAW_PATH == "custom/path/melbourne.csv"
        assert s.DATAGOV_RAW_PATH == "custom/path/datagov.csv"

    def test_global_settings_instance_is_settings_type(self):
        assert isinstance(settings, Settings)

    def test_global_settings_instance_has_correct_defaults(self):
        assert settings.MELBOURNE_SEP == ";"
        assert settings.OTHER_SEP == ","