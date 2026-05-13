import pytest
import pandas as pd
import geopandas as gpd
from unittest.mock import patch, MagicMock, call

from src.scripts.download_dev_data import save_local_copy
from src.core.config import settings


# ---------------------------------------------------------------------------
# Shared sample data
# ---------------------------------------------------------------------------

SAMPLE_DF  = pd.DataFrame({"name": ["Alice", "Bob"], "city": ["Melbourne", "Sydney"]})
SAMPLE_GDF = gpd.GeoDataFrame({"name": ["Region A"], "geometry": [None]})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_path_mock(exists: bool = True):
    """Returns a configured mock for a pathlib.Path instance."""
    mock_path = MagicMock()
    mock_path.exists.return_value = exists
    return mock_path


def _base_patches(mock_path, extra_patches=()):
    """
    Common context-manager patches for a full save_local_copy() run.
    Download tasks (12 total):
      CSV       x8 : Melbourne, DataGov, LGA population, diet indicator,
                     health outcome, low cost diet, low cost diet health outcome,
                     recommended macronutrients intake
      Excel     x2 : food insecurity, food facts
      ZIP       x1 : VicLGA boundary
      Kaggle    x1 : grocery prices
    """
    return [
        patch("src.scripts.download_dev_data.Path",                   return_value=mock_path),
        patch("src.scripts.download_dev_data.fetch_csv_from_url",     return_value=SAMPLE_DF),
        patch("src.scripts.download_dev_data.fetch_excel_from_url",   return_value=SAMPLE_DF),
        patch("src.scripts.download_dev_data.fetch_zip_from_url",     return_value=SAMPLE_GDF),
        patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",  return_value=SAMPLE_DF),
        patch.object(pd.DataFrame, "to_csv"),
        patch.object(pd.DataFrame, "to_excel"),
    ] + list(extra_patches)


# ---------------------------------------------------------------------------
# Directory creation
# ---------------------------------------------------------------------------

class TestDirectoryHandling:
    def test_does_not_create_directory_if_exists(self):
        """Tests that mkdir is not called when the raw data directory already exists."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_path.mkdir.assert_not_called()

    def test_creates_directory_if_not_exists(self):
        """Tests that mkdir is called with parents=True, exist_ok=True when dir is absent."""
        mock_path = make_path_mock(exists=False)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_logs_when_creating_directory(self):
        """Tests that the correct log message is emitted when the directory is missing."""
        mock_path = make_path_mock(exists=False)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.logger")                as mock_logger, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_logger.info.assert_any_call(f"Creating directory: {mock_path}")

    def test_does_not_log_directory_creation_when_dir_exists(self):
        """Tests that the directory-creation log line is NOT emitted when the dir exists."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.logger")                as mock_logger, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        logged_messages = [str(c) for c in mock_logger.info.call_args_list]
        assert not any("Creating directory" in m for m in logged_messages)


# ---------------------------------------------------------------------------
# Fetcher calls — argument correctness
# ---------------------------------------------------------------------------

class TestFetcherCalls:
    """
    Verifies that each fetcher is called with the correct URL/dataset and kwargs.

    Download tasks in save_local_copy (order matters for call_args_list):
      fetch_csv_from_url[0] : MELBOURNE_API_URL,                    separator=MELBOURNE_SEP
      fetch_csv_from_url[1] : OTHER_DATA_URL,                       separator=OTHER_SEP
      fetch_excel_from_url[0]: FOOD_INSECURITY_URL,                 sheet_name=FOOD_INSECURITY_SHEET_NAME
      fetch_zip_from_url[0] : VICLGA_BOUNDARY_URL
      fetch_csv_from_url[2] : LGA_POPULATION_URL,                   separator=LGA_POPULATION_SEP
      fetch_csv_from_url[3] : DIET_INDICATOR_URL,                   separator=DIET_INDICATOR_SEP
      fetch_csv_from_url[4] : HEALTH_OUTCOME_URL,                   separator=HEALTH_OUTCOME_SEP
      fetch_csv_from_url[5] : LOW_COST_DIET_URL,                    separator=LOW_COST_DIET_SEP
      fetch_csv_from_url[6] : LOW_COST_DIET_HEALTH_OUTCOME_URL,     separator=LOW_COST_DIET_HEALTH_OUTCOME_SEP
      fetch_csv_from_url[7] : RECOMMENDED_MACRONUTRIENTS_INTAKE_URL,separator=RECOMMENDED_MACRONUTRIENTS_INTAKE_SEP
      fetch_csv_from_kaggle[0]: GROCERY_PRICES_DATASET,             filename=..., output_dir=..., usecols=..., separator=...
      fetch_excel_from_url[1]: FOOD_FACTS_DATASET_URL,              sheet_name=FOOD_FACTS_SHEET_NAME
    """

    def _run_with_all_mocked(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"), \
             patch.object(gpd.GeoDataFrame, "to_csv"):
            save_local_copy()

    # Decorators are applied bottom-to-top, so parameter order is:
    # mock_csv (innermost), mock_kaggle, mock_excel, mock_zip (outermost)
    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_fetch_csv_called_exactly_eight_times(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that fetch_csv_from_url is called 8 times (Melbourne, DataGov, LGA population,
        diet indicator, health outcome, low cost diet, low cost diet health outcome,
        recommended macronutrients intake)."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_count == 8

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_melbourne_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the Melbourne CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_args_list[0] == call(settings.MELBOURNE_API_URL, separator=settings.MELBOURNE_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_datagov_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the DataGov CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_args_list[1] == call(settings.OTHER_DATA_URL, separator=settings.OTHER_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_lga_population_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the LGA population CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_args_list[2] == call(settings.LGA_POPULATION_URL, separator=settings.LGA_POPULATION_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_diet_indicator_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the diet indicator CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_args_list[3] == call(settings.DIET_INDICATOR_URL, separator=settings.DIET_INDICATOR_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_health_outcome_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the health outcome CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_args_list[4] == call(settings.HEALTH_OUTCOME_URL, separator=settings.HEALTH_OUTCOME_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_low_cost_diet_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the low cost diet CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_args_list[5] == call(settings.LOW_COST_DIET_URL, separator=settings.LOW_COST_DIET_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_low_cost_diet_health_outcome_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the low cost diet health outcome CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_args_list[6] == call(
            settings.LOW_COST_DIET_HEALTH_OUTCOME_URL,
            separator=settings.LOW_COST_DIET_HEALTH_OUTCOME_SEP,
        )

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_recommended_macronutrients_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the recommended macronutrients intake CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_csv.call_args_list[7] == call(
            settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_URL,
            separator=settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_SEP,
        )

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_food_insecurity_fetched_with_correct_url_and_sheet(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the food insecurity Excel is fetched with the correct URL and sheet_name."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_excel.call_args_list[0] == call(
            settings.FOOD_INSECURITY_URL,
            sheet_name=settings.FOOD_INSECURITY_SHEET_NAME,
        )

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_food_facts_fetched_with_correct_url_and_sheet(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the food facts Excel is fetched with the correct URL and sheet_name."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_excel.call_args_list[1] == call(
            settings.FOOD_FACTS_DATASET_URL,
            sheet_name=settings.FOOD_FACTS_SHEET_NAME,
        )

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_viclga_boundary_fetched_with_correct_url(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the VicLGA ZIP boundary is fetched with the correct URL."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        mock_zip.assert_called_once_with(settings.VICLGA_BOUNDARY_URL)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_grocery_prices_fetched_from_kaggle_with_correct_args(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the grocery prices dataset is fetched via fetch_csv_from_kaggle
        with the correct dataset identifier and all required kwargs."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        mock_kaggle.assert_called_once_with(
            settings.GROCERY_PRICES_DATASET,
            filename=settings.GROCERY_PRICES_DATASET_FILENAME,
            output_dir=settings.RAW_DATA_DIR,
            usecols=settings.GROCERY_PRICES_COLS,
            separator=settings.GROCERY_PRICES_SEP,
        )

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_fetch_excel_called_exactly_twice(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that fetch_excel_from_url is called exactly twice (food insecurity + food facts)."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        assert mock_excel.call_count == 2

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_all_twelve_tasks_are_attempted(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that all 12 download tasks are attempted in a single save_local_copy() call."""
        self._run_with_all_mocked(mock_csv, mock_kaggle, mock_excel, mock_zip)
        total = mock_csv.call_count + mock_excel.call_count + mock_zip.call_count + mock_kaggle.call_count
        assert total == 12


# ---------------------------------------------------------------------------
# File saving — format routing
# ---------------------------------------------------------------------------

class TestFileSaving:
    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_excel_files_saved_with_to_excel(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that .xlsx files are saved via to_excel, not to_csv."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel") as mock_to_excel:
            save_local_copy()
        assert mock_to_excel.call_count == 2
        excel_paths = [c.args[0] for c in mock_to_excel.call_args_list]
        assert settings.FOOD_INSECURITY_RAW_PATH in excel_paths
        assert settings.FOOD_FACTS_RAW_PATH in excel_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_melbourne_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the Melbourne CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.MELBOURNE_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_datagov_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the DataGov CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.DATAGOV_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_lga_population_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the LGA population CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.LGA_POPULATION_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_diet_indicator_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the diet indicator CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.DIET_INDICATOR_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_health_outcome_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the health outcome CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.HEALTH_OUTCOME_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_low_cost_diet_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the low cost diet CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.LOW_COST_DIET_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_low_cost_diet_health_outcome_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the low cost diet health outcome CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.LOW_COST_DIET_HEALTH_OUTCOME_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_recommended_macronutrients_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the recommended macronutrients intake CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_grocery_prices_csv_saved_to_correct_path(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that the grocery prices CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.GROCERY_PRICES_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_all_csv_saves_use_index_false(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that all to_csv() calls are made with index=False."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        for c in mock_to_csv.call_args_list:
            assert c.kwargs.get("index") is False, f"to_csv called without index=False: {c}"

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",      return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url",    return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_kaggle",   return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",      return_value=SAMPLE_DF)
    def test_all_excel_saves_use_index_false(self, mock_csv, mock_kaggle, mock_excel, mock_zip):
        """Tests that all to_excel() calls are made with index=False."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel") as mock_to_excel:
            save_local_copy()
        for c in mock_to_excel.call_args_list:
            assert c.kwargs.get("index") is False, f"to_excel called without index=False: {c}"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    def test_does_not_propagate_exception_from_failed_download(self):
        """Tests that a download failure does NOT raise — it is caught and logged."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    side_effect=Exception("Network error")), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()

    def test_logs_error_when_download_fails(self):
        """Tests that a failed download is logged at ERROR level with the URL and exception."""
        mock_path = make_path_mock(exists=True)
        error = Exception("Timeout")
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    side_effect=error), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.logger")                as mock_logger, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_logger.error.assert_any_call(
            f"Failed to download {settings.MELBOURNE_API_URL}: {error}"
        )

    def test_remaining_tasks_run_after_one_failure(self):
        """Tests that a failure in one task does not stop subsequent downloads."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    side_effect=Exception("fail")), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF) as mock_excel, \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF) as mock_zip, \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF) as mock_kaggle, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        assert mock_excel.call_count == 2
        mock_zip.assert_called_once()
        mock_kaggle.assert_called_once()

    def test_logs_success_for_tasks_that_complete_despite_others_failing(self):
        """Tests that successful saves are still logged even when other tasks failed."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    side_effect=Exception("fail")), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.logger")                as mock_logger, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_logger.info.assert_any_call(
            f"Local dev file saved to {settings.FOOD_INSECURITY_RAW_PATH}"
        )


# ---------------------------------------------------------------------------
# Logging — success paths
# ---------------------------------------------------------------------------

class TestSuccessLogging:
    def _run_all_mocked(self):
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.logger")                as mock_logger, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
            return mock_logger

    def test_logs_melbourne_save_path(self):
        """Tests that the Melbourne save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.MELBOURNE_RAW_PATH}")

    def test_logs_datagov_save_path(self):
        """Tests that the DataGov save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.DATAGOV_RAW_PATH}")

    def test_logs_food_insecurity_save_path(self):
        """Tests that the food insecurity save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.FOOD_INSECURITY_RAW_PATH}")

    def test_logs_viclga_boundary_save_path(self):
        """Tests that the VicLGA boundary save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.VICLGA_BOUNDARY_RAW_PATH}")

    def test_logs_lga_population_save_path(self):
        """Tests that the LGA population save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.LGA_POPULATION_RAW_PATH}")

    def test_logs_diet_indicator_save_path(self):
        """Tests that the diet indicator save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.DIET_INDICATOR_RAW_PATH}")

    def test_logs_health_outcome_save_path(self):
        """Tests that the health outcome save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.HEALTH_OUTCOME_RAW_PATH}")

    def test_logs_low_cost_diet_save_path(self):
        """Tests that the low cost diet save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.LOW_COST_DIET_RAW_PATH}")

    def test_logs_low_cost_diet_health_outcome_save_path(self):
        """Tests that the low cost diet health outcome save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.LOW_COST_DIET_HEALTH_OUTCOME_RAW_PATH}")

    def test_logs_recommended_macronutrients_save_path(self):
        """Tests that the recommended macronutrients intake save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_RAW_PATH}")

    def test_logs_grocery_prices_save_path(self):
        """Tests that the grocery prices save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.GROCERY_PRICES_RAW_PATH}")

    def test_logs_food_facts_save_path(self):
        """Tests that the food facts save path is logged at INFO level."""
        mock_logger = self._run_all_mocked()
        mock_logger.info.assert_any_call(f"Local dev file saved to {settings.FOOD_FACTS_RAW_PATH}")


# ---------------------------------------------------------------------------
# Return value
# ---------------------------------------------------------------------------

class TestReturnValue:
    def test_returns_none(self):
        """Tests that save_local_copy() always returns None."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                  return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",    return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.fetch_csv_from_kaggle", return_value=SAMPLE_DF), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            result = save_local_copy()
        assert result is None