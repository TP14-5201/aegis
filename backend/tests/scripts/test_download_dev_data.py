import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, call

from src.scripts.download_dev_data import save_local_copy


SAMPLE_DF = pd.DataFrame({
    "name": ["Alice", "Bob"],
    "city": ["Melbourne", "Sydney"]
})


class TestSaveLocalCopy:
    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.makedirs")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_does_not_create_directory_if_exists(self, mock_exists, mock_makedirs, mock_fetch):
        """Tests that the directory is not created if it already exists."""
        mock_fetch.return_value = SAMPLE_DF
        with patch.object(SAMPLE_DF, "to_csv"):
            save_local_copy()
        mock_makedirs.assert_not_called()

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.makedirs")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=False)
    def test_creates_directory_if_not_exists(self, mock_exists, mock_makedirs, mock_fetch):
        """Tests that the directory is created if it does not exist."""
        mock_fetch.return_value = SAMPLE_DF
        with patch.object(SAMPLE_DF, "to_csv"):
            save_local_copy()
        mock_makedirs.assert_called_once_with("src/data/raw")

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.makedirs")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=False)
    def test_logs_when_creating_directory(self, mock_exists, mock_makedirs, mock_fetch):
        """Tests that the function logs when creating the directory."""
        mock_fetch.return_value = SAMPLE_DF
        with patch("src.scripts.download_dev_data.logger") as mock_logger:
            with patch.object(SAMPLE_DF, "to_csv"):
                save_local_copy()
            mock_logger.info.assert_any_call(
                "Raw data directory does not exist. Creating raw data directory..."
            )

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_fetch_called_with_melbourne_settings(self, mock_exists, mock_fetch):
        """Tests that fetch_csv_from_url is called with Melbourne settings."""
        mock_fetch.return_value = SAMPLE_DF
        with patch.object(pd.DataFrame, "to_csv"):
            save_local_copy()
        from src.core.config import settings
        assert mock_fetch.call_args_list[0] == call(
            settings.MELBOURNE_API_URL, settings.MELBOURNE_SEP
        )

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_fetch_called_with_datagov_settings(self, mock_exists, mock_fetch):
        """Tests that fetch_csv_from_url is called with DataGov settings."""
        mock_fetch.return_value = SAMPLE_DF
        with patch.object(pd.DataFrame, "to_csv"):
            save_local_copy()
        from src.core.config import settings
        assert mock_fetch.call_args_list[1] == call(
            settings.OTHER_DATA_URL, settings.OTHER_SEP
        )

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_fetch_called_exactly_twice(self, mock_exists, mock_fetch):
        """Tests that fetch_csv_from_url is called exactly twice."""
        mock_fetch.return_value = SAMPLE_DF
        with patch.object(pd.DataFrame, "to_csv"):
            save_local_copy()
        assert mock_fetch.call_count == 2

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_melbourne_csv_saved_to_correct_path(self, mock_exists, mock_fetch):
        """Tests that the Melbourne CSV is saved to the correct path."""
        mock_fetch.return_value = SAMPLE_DF
        with patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
            save_local_copy()
        from src.core.config import settings
        assert mock_to_csv.call_args_list[0] == call(settings.MELBOURNE_RAW_PATH, index=False)

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_datagov_csv_saved_to_correct_path(self, mock_exists, mock_fetch):
        """Tests that the DataGov CSV is saved to the correct path."""
        mock_fetch.return_value = SAMPLE_DF
        with patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
            save_local_copy()
        from src.core.config import settings
        assert mock_to_csv.call_args_list[1] == call(settings.DATAGOV_RAW_PATH, index=False)

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_logs_melbourne_save_path(self, mock_exists, mock_fetch):
        """Tests that the function logs the Melbourne save path."""
        mock_fetch.return_value = SAMPLE_DF
        with patch("src.scripts.download_dev_data.logger") as mock_logger:
            with patch.object(pd.DataFrame, "to_csv"):
                save_local_copy()
        from src.core.config import settings
        mock_logger.info.assert_any_call(
            f"Local dev file saved to {settings.MELBOURNE_RAW_PATH}"
        )

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_logs_datagov_save_path(self, mock_exists, mock_fetch):
        """Tests that the function logs the DataGov save path."""
        mock_fetch.return_value = SAMPLE_DF
        with patch("src.scripts.download_dev_data.logger") as mock_logger:
            with patch.object(pd.DataFrame, "to_csv"):
                save_local_copy()
        from src.core.config import settings
        mock_logger.info.assert_any_call(
            f"Local dev file saved to {settings.DATAGOV_RAW_PATH}"
        )

    @patch("src.scripts.download_dev_data.fetch_csv_from_url")
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_returns_none(self, mock_exists, mock_fetch):
        """Tests that the function returns None."""
        mock_fetch.return_value = SAMPLE_DF
        with patch.object(pd.DataFrame, "to_csv"):
            result = save_local_copy()
        assert result is None

    @patch("src.scripts.download_dev_data.fetch_csv_from_url", side_effect=Exception("Network error"))
    @patch("src.scripts.download_dev_data.os.path.exists", return_value=True)
    def test_propagates_fetch_exception(self, mock_exists, mock_fetch):
        """Tests that the function propagates exceptions from fetch_csv_from_url."""
        with pytest.raises(Exception, match="Network error"):
            save_local_copy()