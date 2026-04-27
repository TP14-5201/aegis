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
    Download tasks (5 total):
      CSV  x3 : Melbourne, DataGov, LGA population
      Excel x1 : food insecurity
      ZIP  x1 : VicLGA boundary
    """
    return [
        patch("src.scripts.download_dev_data.Path",                  return_value=mock_path),
        patch("src.scripts.download_dev_data.fetch_csv_from_url",    return_value=SAMPLE_DF),
        patch("src.scripts.download_dev_data.fetch_excel_from_url",  return_value=SAMPLE_DF),
        patch("src.scripts.download_dev_data.fetch_zip_from_url",    return_value=SAMPLE_GDF),
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
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_path.mkdir.assert_not_called()

    def test_creates_directory_if_not_exists(self):
        """Tests that mkdir is called with parents=True, exist_ok=True when dir is absent."""
        mock_path = make_path_mock(exists=False)
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_path.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_logs_when_creating_directory(self):
        """Tests that the correct log message is emitted when the directory is missing."""
        mock_path = make_path_mock(exists=False)
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.logger")               as mock_logger, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_logger.info.assert_any_call(f"Creating directory: {mock_path}")

    def test_does_not_log_directory_creation_when_dir_exists(self):
        """Tests that the directory-creation log line is NOT emitted when the dir exists."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.logger")               as mock_logger, \
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
    Verifies that each fetcher is called with the correct URL and kwargs.

    Download tasks in save_local_copy (order matters for call_args_list):
      0: fetch_csv_from_url(MELBOURNE_API_URL, separator=MELBOURNE_SEP)
      1: fetch_csv_from_url(OTHER_DATA_URL,    separator=OTHER_SEP)
      2: fetch_excel_from_url(FOOD_INSECURITY_URL, sheet_name=FOOD_INSECURITY_SHEET_NAME)
      3: fetch_zip_from_url(VICLGA_BOUNDARY_URL)
      4: fetch_csv_from_url(LGA_POPULATION_URL,  separator=LGA_POPULATION_SEP)
    """

    def _run_with_all_mocked(self, mock_csv, mock_excel, mock_zip):
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"), \
             patch.object(gpd.GeoDataFrame, "to_csv"):
            save_local_copy()

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_fetch_csv_called_exactly_three_times(self, mock_csv, mock_excel, mock_zip):
        """Tests that fetch_csv_from_url is called 3 times (Melbourne + DataGov + LGA population)."""
        self._run_with_all_mocked(mock_csv, mock_excel, mock_zip)
        assert mock_csv.call_count == 3

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_melbourne_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_excel, mock_zip):
        """Tests that the Melbourne CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_excel, mock_zip)
        first_call = mock_csv.call_args_list[0]
        assert first_call == call(settings.MELBOURNE_API_URL, separator=settings.MELBOURNE_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_datagov_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_excel, mock_zip):
        """Tests that the DataGov CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_excel, mock_zip)
        second_call = mock_csv.call_args_list[1]
        assert second_call == call(settings.OTHER_DATA_URL, separator=settings.OTHER_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_lga_population_csv_fetched_with_correct_url_and_sep(self, mock_csv, mock_excel, mock_zip):
        """Tests that the LGA population CSV is fetched with the correct URL and sep kwarg."""
        self._run_with_all_mocked(mock_csv, mock_excel, mock_zip)
        third_call = mock_csv.call_args_list[2]
        assert third_call == call(settings.LGA_POPULATION_URL, separator=settings.LGA_POPULATION_SEP)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_food_insecurity_fetched_with_correct_url_and_sheet(self, mock_csv, mock_excel, mock_zip):
        """Tests that the food insecurity Excel is fetched with the correct URL and sheet_name."""
        self._run_with_all_mocked(mock_csv, mock_excel, mock_zip)
        mock_excel.assert_called_once_with(
            settings.FOOD_INSECURITY_URL,
            sheet_name=settings.FOOD_INSECURITY_SHEET_NAME,
        )

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_viclga_boundary_fetched_with_correct_url(self, mock_csv, mock_excel, mock_zip):
        """Tests that the VicLGA ZIP boundary is fetched with the correct URL."""
        self._run_with_all_mocked(mock_csv, mock_excel, mock_zip)
        mock_zip.assert_called_once_with(settings.VICLGA_BOUNDARY_URL)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_fetch_excel_called_exactly_once(self, mock_csv, mock_excel, mock_zip):
        """Tests that fetch_excel_from_url is called exactly once (food insecurity only)."""
        self._run_with_all_mocked(mock_csv, mock_excel, mock_zip)
        assert mock_excel.call_count == 1

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_all_five_tasks_are_attempted(self, mock_csv, mock_excel, mock_zip):
        """Tests that all 5 download tasks are attempted in a single save_local_copy() call."""
        self._run_with_all_mocked(mock_csv, mock_excel, mock_zip)
        total = mock_csv.call_count + mock_excel.call_count + mock_zip.call_count
        assert total == 5


# ---------------------------------------------------------------------------
# File saving — format routing
# ---------------------------------------------------------------------------

class TestFileSaving:
    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_excel_file_saved_with_to_excel(self, mock_csv, mock_excel, mock_zip):
        """Tests that .xlsx files are saved via to_excel, not to_csv."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel") as mock_to_excel:
            save_local_copy()
        assert mock_to_excel.call_count == 1
        mock_to_excel.assert_called_once_with(settings.FOOD_INSECURITY_RAW_PATH, index=False)

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_melbourne_csv_saved_to_correct_path(self, mock_csv, mock_excel, mock_zip):
        """Tests that the Melbourne CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.MELBOURNE_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_datagov_csv_saved_to_correct_path(self, mock_csv, mock_excel, mock_zip):
        """Tests that the DataGov CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.DATAGOV_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_lga_population_csv_saved_to_correct_path(self, mock_csv, mock_excel, mock_zip):
        """Tests that the LGA population CSV result is saved to the configured path."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        saved_paths = [c.args[0] for c in mock_to_csv.call_args_list]
        assert settings.LGA_POPULATION_RAW_PATH in saved_paths

    @patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF)
    @patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF)
    @patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF)
    def test_all_csv_saves_use_index_false(self, mock_csv, mock_excel, mock_zip):
        """Tests that all to_csv() calls are made with index=False."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path", return_value=mock_path), \
             patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        for c in mock_to_csv.call_args_list:
            assert c.kwargs.get("index") is False, f"to_csv called without index=False: {c}"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    def test_does_not_propagate_exception_from_failed_download(self):
        """Tests that a download failure does NOT raise — it is caught and logged."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   side_effect=Exception("Network error")), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()

    def test_logs_error_when_download_fails(self):
        """Tests that a failed download is logged at ERROR level with the URL and exception."""
        mock_path = make_path_mock(exists=True)
        error = Exception("Timeout")
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   side_effect=error), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.logger")               as mock_logger, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_logger.error.assert_any_call(
            f"Failed to download {settings.MELBOURNE_API_URL}: {error}"
        )

    def test_remaining_tasks_run_after_one_failure(self):
        """Tests that a failure in one task does not stop subsequent downloads."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   side_effect=Exception("fail")), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF) as mock_excel, \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF) as mock_zip, \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            save_local_copy()
        mock_excel.assert_called_once()
        mock_zip.assert_called_once()

    def test_logs_success_for_tasks_that_complete_despite_others_failing(self):
        """Tests that successful saves are still logged even when other tasks failed."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   side_effect=Exception("fail")), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.logger")               as mock_logger, \
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
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch("src.scripts.download_dev_data.logger")               as mock_logger, \
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


# ---------------------------------------------------------------------------
# Return value
# ---------------------------------------------------------------------------

class TestReturnValue:
    def test_returns_none(self):
        """Tests that save_local_copy() always returns None."""
        mock_path = make_path_mock(exists=True)
        with patch("src.scripts.download_dev_data.Path",                 return_value=mock_path), \
             patch("src.scripts.download_dev_data.fetch_csv_from_url",   return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_excel_from_url", return_value=SAMPLE_DF), \
             patch("src.scripts.download_dev_data.fetch_zip_from_url",   return_value=SAMPLE_GDF), \
             patch.object(pd.DataFrame, "to_csv"), \
             patch.object(pd.DataFrame, "to_excel"):
            result = save_local_copy()
        assert result is None