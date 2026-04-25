import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, call

from src.data.loaders.data_loader import (
    _load_and_wrangle,
    load_emergency_services_dataset,
    load_food_insecurity_dataset,
    load_vic_boundaries_dataset,
    load_viclga_boundaries_dataset,
)
from src.core.config import settings


# ---------------------------------------------------------------------------
# Shared sample data
# ---------------------------------------------------------------------------

def make_sample_df(name_values: list[str] | None = None) -> pd.DataFrame:
    """Returns a minimal DataFrame for use as wrangler output stubs."""
    names = name_values or ["Service A", "Service B"]
    return pd.DataFrame({
        "name": names,
        "suburb": ["Melbourne"] * len(names),
        "source": ["test"] * len(names),
    })


MELBOURNE_DF = make_sample_df(["Zed Service", "Alpha Service"])
DATAGOV_DF   = make_sample_df(["Middle Service"])
FOOD_DF      = pd.DataFrame({"indicator": ["food"], "estimate_pct": [10.0]})
VIC_DF       = pd.DataFrame({"vicgov_region": ["South East"], "geometry": ["POLYGON(...)"]})
LGA_DF       = pd.DataFrame({"lga_name": ["Melbourne"], "geometry": ["POLYGON(...)"]})


# ---------------------------------------------------------------------------
# _load_and_wrangle (private helper — unit tested directly)
# ---------------------------------------------------------------------------

class TestLoadAndWrangle:
    def test_reads_csv_by_default(self):
        """Tests that pd.read_csv is used when is_excel=False (the default)."""
        mock_df = make_sample_df()
        mock_wrangler = MagicMock(return_value=mock_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=mock_df) as mock_read_csv, \
             patch("src.data.loaders.data_loader.pd.read_excel") as mock_read_excel:
            _load_and_wrangle("some/path.csv", mock_wrangler, "test")

        mock_read_csv.assert_called_once_with("some/path.csv")
        mock_read_excel.assert_not_called()

    def test_reads_excel_when_is_excel_true(self):
        """Tests that pd.read_excel is used when is_excel=True."""
        mock_df = make_sample_df()
        mock_wrangler = MagicMock(return_value=mock_df)

        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=mock_df) as mock_read_excel, \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv:
            _load_and_wrangle("some/path.xlsx", mock_wrangler, "test", is_excel=True)

        mock_read_excel.assert_called_once_with("some/path.xlsx", sheet_name=0)
        mock_read_csv.assert_not_called()

    def test_excel_reads_first_sheet_by_default(self):
        """Tests that Excel files are read with sheet_name=0 (the first sheet)."""
        mock_df = make_sample_df()
        mock_wrangler = MagicMock(return_value=mock_df)

        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=mock_df) as mock_read_excel:
            _load_and_wrangle("path.xlsx", mock_wrangler, "test", is_excel=True)

        _, kwargs = mock_read_excel.call_args
        assert kwargs.get("sheet_name") == 0

    def test_passes_dataframe_to_wrangler(self):
        """Tests that the DataFrame returned by read_csv/read_excel is passed to the wrangler."""
        raw_df = make_sample_df()
        wrangled_df = make_sample_df(["Wrangled"])
        mock_wrangler = MagicMock(return_value=wrangled_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df):
            _load_and_wrangle("path.csv", mock_wrangler, "test")

        mock_wrangler.assert_called_once_with(raw_df)

    def test_returns_wrangler_output(self):
        """Tests that the return value is the wrangler's output, not the raw DataFrame."""
        raw_df = make_sample_df()
        wrangled_df = make_sample_df(["Wrangled Result"])
        mock_wrangler = MagicMock(return_value=wrangled_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df):
            result = _load_and_wrangle("path.csv", mock_wrangler, "test")

        assert result is wrangled_df

    def test_logs_error_on_read_failure(self):
        """Tests that a read failure is logged at ERROR level with the label and path."""
        error = FileNotFoundError("No such file")

        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=error), \
             patch("src.data.loaders.data_loader.logger") as mock_logger:
            with pytest.raises(FileNotFoundError):
                _load_and_wrangle("missing.csv", MagicMock(), "Melbourne")

        mock_logger.error.assert_called_once_with(
            f"Failed to read Melbourne raw data from 'missing.csv': {error}"
        )

    def test_reraises_exception_after_logging(self):
        """Tests that exceptions are re-raised after logging — NOT swallowed.

        This is the opposite behaviour from download_dev_data, which uses
        try/except without re-raise. Here, callers receive the exception.
        """
        error = FileNotFoundError("missing")

        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=error), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError, match="missing"):
                _load_and_wrangle("bad.csv", MagicMock(), "test")

    def test_logs_error_on_wrangler_failure(self):
        """Tests that a wrangler failure is also caught, logged, and re-raised."""
        raw_df = make_sample_df()
        error = ValueError("Wrangling failed")
        mock_wrangler = MagicMock(side_effect=error)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df), \
             patch("src.data.loaders.data_loader.logger") as mock_logger:
            with pytest.raises(ValueError):
                _load_and_wrangle("path.csv", mock_wrangler, "test label")

        mock_logger.error.assert_called_once_with(
            f"Failed to read test label raw data from 'path.csv': {error}"
        )

    def test_error_message_includes_path(self):
        """Tests that the logged error message contains the file path."""
        error = Exception("fail")

        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=error), \
             patch("src.data.loaders.data_loader.logger") as mock_logger:
            with pytest.raises(Exception):
                _load_and_wrangle("src/data/raw/specific.csv", MagicMock(), "label")

        logged_msg = mock_logger.error.call_args[0][0]
        assert "src/data/raw/specific.csv" in logged_msg

    def test_returns_dataframe(self):
        """Tests that the return value is a DataFrame."""
        raw_df = make_sample_df()
        mock_wrangler = MagicMock(return_value=raw_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df):
            result = _load_and_wrangle("path.csv", mock_wrangler, "test")

        assert isinstance(result, pd.DataFrame)


# ---------------------------------------------------------------------------
# load_emergency_services_dataset
# ---------------------------------------------------------------------------

class TestLoadEmergencyServicesDataset:
    def _run(self, mel_df=None, gov_df=None):
        """Runs load_emergency_services_dataset with both wranglers mocked."""
        mel_df = mel_df if mel_df is not None else MELBOURNE_DF
        gov_df = gov_df if gov_df is not None else DATAGOV_DF

        with patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_melbourne", return_value=mel_df), \
             patch("src.data.loaders.data_loader.wrangle_datagov", return_value=gov_df):
            # read_csv is called twice; return different DFs for each call
            mock_read_csv.side_effect = [mel_df, gov_df]
            return load_emergency_services_dataset()

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        result = self._run()
        assert isinstance(result, pd.DataFrame)

    def test_reads_melbourne_from_correct_path(self):
        """Tests that the Melbourne raw CSV is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_melbourne", return_value=MELBOURNE_DF), \
             patch("src.data.loaders.data_loader.wrangle_datagov", return_value=DATAGOV_DF):
            mock_read_csv.side_effect = [MELBOURNE_DF, DATAGOV_DF]
            load_emergency_services_dataset()

        paths_called = [c.args[0] for c in mock_read_csv.call_args_list]
        assert settings.MELBOURNE_RAW_PATH in paths_called

    def test_reads_datagov_from_correct_path(self):
        """Tests that the DataGov raw CSV is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_melbourne", return_value=MELBOURNE_DF), \
             patch("src.data.loaders.data_loader.wrangle_datagov", return_value=DATAGOV_DF):
            mock_read_csv.side_effect = [MELBOURNE_DF, DATAGOV_DF]
            load_emergency_services_dataset()

        paths_called = [c.args[0] for c in mock_read_csv.call_args_list]
        assert settings.DATAGOV_RAW_PATH in paths_called

    def test_combines_both_datasets(self):
        """Tests that both Melbourne and DataGov rows appear in the output."""
        mel_df = make_sample_df(["Zed Service"])
        gov_df = make_sample_df(["Alpha Service"])
        result = self._run(mel_df=mel_df, gov_df=gov_df)
        assert "Zed Service" in result["name"].values
        assert "Alpha Service" in result["name"].values

    def test_combined_row_count_is_sum_of_both_sources(self):
        """Tests that the combined DataFrame has rows from both sources."""
        mel_df = make_sample_df(["A", "B"])
        gov_df = make_sample_df(["C", "D", "E"])
        result = self._run(mel_df=mel_df, gov_df=gov_df)
        assert len(result) == 5

    def test_output_is_sorted_by_name_ascending(self):
        """Tests that the combined result is sorted alphabetically by 'name'."""
        mel_df = make_sample_df(["Zed Service", "Middle Service"])
        gov_df = make_sample_df(["Alpha Service"])
        result = self._run(mel_df=mel_df, gov_df=gov_df)
        names = list(result["name"])
        assert names == sorted(names)

    def test_output_index_is_reset_after_concat(self):
        """Tests that the output has a clean 0..N integer index (ignore_index=True)."""
        mel_df = make_sample_df(["A", "B"])
        gov_df = make_sample_df(["C"])
        result = self._run(mel_df=mel_df, gov_df=gov_df)
        assert list(result.index) == list(range(len(result)))

    def test_propagates_exception_from_melbourne_load(self):
        """Tests that a failure loading the Melbourne dataset propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_emergency_services_dataset()

    def test_propagates_exception_from_datagov_load(self):
        """Tests that a failure loading the DataGov dataset propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_melbourne", return_value=MELBOURNE_DF), \
             patch("src.data.loaders.data_loader.logger"):
            mock_read_csv.side_effect = [MELBOURNE_DF, FileNotFoundError("missing")]
            with pytest.raises(FileNotFoundError):
                load_emergency_services_dataset()


# ---------------------------------------------------------------------------
# load_food_insecurity_dataset
#
# This function has a bespoke try/except rather than delegating to
# _load_and_wrangle for the food insecurity file itself. It calls
# _load_and_wrangle for the two boundary datasets (CSV), then calls
# wrangle_food_insecurity(df_raw, df_vic, df_lga) with all three DataFrames.
# ---------------------------------------------------------------------------

class TestLoadFoodInsecurityDataset:

    def _run(self, food_df=None, vic_df=None, lga_df=None, wrangled_df=None):
        """
        Runs load_food_insecurity_dataset with all three reads and wranglers mocked.

        pd.read_excel is called once (food insecurity raw file).
        pd.read_csv is called twice via _load_and_wrangle (vic then lga boundaries).
        """
        food_df    = food_df    if food_df    is not None else FOOD_DF
        vic_df     = vic_df     if vic_df     is not None else VIC_DF
        lga_df     = lga_df     if lga_df     is not None else LGA_DF
        wrangled_df = wrangled_df if wrangled_df is not None else FOOD_DF

        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=food_df), \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=vic_df), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=lga_df), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=wrangled_df):
            mock_read_csv.side_effect = [vic_df, lga_df]
            return load_food_insecurity_dataset()

    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        result = self._run()
        assert isinstance(result, pd.DataFrame)

    def test_reads_food_insecurity_raw_file_from_correct_path(self):
        """Tests that the food insecurity Excel is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_DF) as mock_read_excel, \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_DF):
            mock_read_csv.side_effect = [VIC_DF, LGA_DF]
            load_food_insecurity_dataset()

        mock_read_excel.assert_called_once_with(settings.FOOD_INSECURITY_RAW_PATH, sheet_name=0)

    def test_food_insecurity_raw_file_is_read_with_excel(self):
        """Tests that pd.read_excel is used for the food insecurity raw file (is_excel=True)."""
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_DF) as mock_excel, \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_DF):
            mock_read_csv.side_effect = [VIC_DF, LGA_DF]
            load_food_insecurity_dataset()

        mock_excel.assert_called_once()

    def test_boundary_files_are_read_with_csv(self):
        """Tests that pd.read_csv is used for the two boundary datasets.

        Unlike the food insecurity file (Excel), both vic_boundaries and
        viclga_boundaries are CSVs loaded via _load_and_wrangle (is_excel=False).
        """
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_DF):
            mock_read_csv.side_effect = [VIC_DF, LGA_DF]
            load_food_insecurity_dataset()

        assert mock_read_csv.call_count == 2

    def test_reads_vic_boundaries_from_correct_path(self):
        """Tests that vic_boundaries are read from VICGOV_BOUNDARY_RAW_PATH."""
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_DF):
            mock_read_csv.side_effect = [VIC_DF, LGA_DF]
            load_food_insecurity_dataset()

        paths_called = [c.args[0] for c in mock_read_csv.call_args_list]
        assert settings.VICGOV_BOUNDARY_RAW_PATH in paths_called

    def test_reads_viclga_boundaries_from_correct_path(self):
        """Tests that viclga_boundaries are read from VICLGA_BOUNDARY_RAW_PATH."""
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", return_value=FOOD_DF):
            mock_read_csv.side_effect = [VIC_DF, LGA_DF]
            load_food_insecurity_dataset()

        paths_called = [c.args[0] for c in mock_read_csv.call_args_list]
        assert settings.VICLGA_BOUNDARY_RAW_PATH in paths_called

    def test_calls_wrangle_food_insecurity_with_all_three_dataframes(self):
        """Tests that wrangle_food_insecurity is called with (df_raw, df_vic, df_lga).

        The wrangler requires all three DataFrames to resolve ufi and lga_pid
        via joins — passing only the raw food insecurity DataFrame would be wrong.
        """
        raw_df     = FOOD_DF.copy()
        vic_df     = VIC_DF.copy()
        lga_df     = LGA_DF.copy()
        wrangled   = pd.DataFrame({"result": [1]})
        mock_food_wrangler = MagicMock(return_value=wrangled)

        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=raw_df), \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=vic_df), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=lga_df), \
             patch("src.data.loaders.data_loader.wrangle_food_insecurity", mock_food_wrangler):
            mock_read_csv.side_effect = [vic_df, lga_df]
            result = load_food_insecurity_dataset()

        mock_food_wrangler.assert_called_once_with(raw_df, vic_df, lga_df)
        assert result is wrangled

    def test_logs_error_with_correct_message_on_failure(self):
        """Tests that a failure is logged with the food-insecurity-specific message.

        Unlike _load_and_wrangle (which logs 'Failed to read {label} raw data from ...'),
        this function logs 'Failed to load food insecurity dataset: {e}'.
        """
        error = FileNotFoundError("missing file")

        with patch("src.data.loaders.data_loader.pd.read_excel", side_effect=error), \
             patch("src.data.loaders.data_loader.logger") as mock_logger:
            with pytest.raises(FileNotFoundError):
                load_food_insecurity_dataset()

        mock_logger.error.assert_called_once_with(
            f"Failed to load food insecurity dataset: {error}"
        )

    def test_propagates_exception_on_missing_food_insecurity_file(self):
        """Tests that a FileNotFoundError from the Excel read propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_excel", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_food_insecurity_dataset()

    def test_propagates_exception_from_vic_boundaries_load(self):
        """Tests that a failure loading vic_boundaries propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv", side_effect=FileNotFoundError("vic missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_food_insecurity_dataset()

    def test_propagates_exception_from_viclga_boundaries_load(self):
        """Tests that a failure loading viclga_boundaries propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_excel", return_value=FOOD_DF), \
             patch("src.data.loaders.data_loader.pd.read_csv") as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.logger"):
            mock_read_csv.side_effect = [VIC_DF, FileNotFoundError("lga missing")]
            with pytest.raises(FileNotFoundError):
                load_food_insecurity_dataset()


# ---------------------------------------------------------------------------
# load_vic_boundaries_dataset
# ---------------------------------------------------------------------------

class TestLoadVicBoundariesDataset:
    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF):
            result = load_vic_boundaries_dataset()
        assert isinstance(result, pd.DataFrame)

    def test_reads_from_correct_path(self):
        """Tests that the VIC boundaries CSV is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=VIC_DF) as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF):
            load_vic_boundaries_dataset()

        mock_read_csv.assert_called_once_with(settings.VICGOV_BOUNDARY_RAW_PATH)

    def test_uses_csv_reader_not_excel(self):
        """Tests that pd.read_csv is used (is_excel defaults to False)."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=VIC_DF), \
             patch("src.data.loaders.data_loader.pd.read_excel") as mock_excel, \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", return_value=VIC_DF):
            load_vic_boundaries_dataset()

        mock_excel.assert_not_called()

    def test_passes_result_through_vic_boundaries_wrangler(self):
        """Tests that the raw DataFrame is passed to wrangle_vic_boundaries."""
        raw_df = VIC_DF.copy()
        wrangled_df = VIC_DF.copy()
        mock_wrangler = MagicMock(return_value=wrangled_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df), \
             patch("src.data.loaders.data_loader.wrangle_vic_boundaries", mock_wrangler):
            result = load_vic_boundaries_dataset()

        mock_wrangler.assert_called_once_with(raw_df)
        assert result is wrangled_df

    def test_propagates_exception_on_missing_file(self):
        """Tests that a FileNotFoundError propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_vic_boundaries_dataset()


# ---------------------------------------------------------------------------
# load_viclga_boundaries_dataset
# ---------------------------------------------------------------------------

class TestLoadViclgaBoundariesDataset:
    def test_returns_dataframe(self):
        """Tests that the function returns a DataFrame."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF):
            result = load_viclga_boundaries_dataset()
        assert isinstance(result, pd.DataFrame)

    def test_reads_from_correct_path(self):
        """Tests that the VIC LGA boundaries CSV is read from the configured path."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=LGA_DF) as mock_read_csv, \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF):
            load_viclga_boundaries_dataset()

        mock_read_csv.assert_called_once_with(settings.VICLGA_BOUNDARY_RAW_PATH)

    def test_uses_csv_reader_not_excel(self):
        """Tests that pd.read_csv is used (is_excel defaults to False)."""
        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=LGA_DF), \
             patch("src.data.loaders.data_loader.pd.read_excel") as mock_excel, \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", return_value=LGA_DF):
            load_viclga_boundaries_dataset()

        mock_excel.assert_not_called()

    def test_passes_result_through_viclga_boundaries_wrangler(self):
        """Tests that the raw DataFrame is passed to wrangle_viclga_boundaries."""
        raw_df = LGA_DF.copy()
        wrangled_df = LGA_DF.copy()
        mock_wrangler = MagicMock(return_value=wrangled_df)

        with patch("src.data.loaders.data_loader.pd.read_csv", return_value=raw_df), \
             patch("src.data.loaders.data_loader.wrangle_viclga_boundaries", mock_wrangler):
            result = load_viclga_boundaries_dataset()

        mock_wrangler.assert_called_once_with(raw_df)
        assert result is wrangled_df

    def test_propagates_exception_on_missing_file(self):
        """Tests that a FileNotFoundError propagates to the caller."""
        with patch("src.data.loaders.data_loader.pd.read_csv", side_effect=FileNotFoundError("missing")), \
             patch("src.data.loaders.data_loader.logger"):
            with pytest.raises(FileNotFoundError):
                load_viclga_boundaries_dataset()

    def test_viclga_path_differs_from_vic_path(self):
        """Documents that VICLGA_BOUNDARY_RAW_PATH and VICGOV_BOUNDARY_RAW_PATH are
        distinct settings — the two boundary loaders must NOT share the same path."""
        assert settings.VICLGA_BOUNDARY_RAW_PATH != settings.VICGOV_BOUNDARY_RAW_PATH